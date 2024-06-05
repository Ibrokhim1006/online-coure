from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from django.utils.encoding import smart_bytes
from utils.renderers import UserRenderers
from utils.utils import Util
from utils.permissions import IsLogin
from utils.expected_fields import check_required_key
from utils.response import (
    bad_request_response,
    success_created_response,
    success_response,
    user_not_found_response
)

from django.contrib.auth.models import Group
from authen.models import CustomUser, GroupUser
from authen.serializers import (
    UserGroupSerializer,
    GroupClass,
    UserSignUpSerializer,
    UserSignInSerializer,
    UserInformationSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    PasswordResetCompleteSerializer,
)



def login(request):
    return render(request, 'login.html')


def register(request):
    context = {}
    context['user_group'] = GroupUser.objects.all().order_by('id')
    context['groups'] = Group.objects.all()
    return render(request, 'register.html', context)










def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserGroupsView(APIView):
    render_classes = [UserRenderers]

    @swagger_auto_schema(tags=['User Roll'], responses={200: UserGroupSerializer(many=True)})
    def get(self, request):
        instance = Group.objects.all()
        serializer = UserGroupSerializer(instance, many=True, context={"request": request})
        return success_response(serializer.data)


class StudentGroupView(APIView):
    render_classes = [UserRenderers]

    @swagger_auto_schema(tags=['Student Group'], responses={200: GroupClass(many=True)})
    def get(self, request):
        instance = GroupUser.objects.all()
        serializer = GroupClass(instance, many=True, context={"request": request})
        return success_response(serializer.data)
    

class UserSignUp(APIView):
    render_classes = [UserRenderers]

    @swagger_auto_schema(
            tags=['Auth'],
            request_body=UserSignUpSerializer,
            operation_description="groups: User role, id_group: student or teacher gorup class name"   
    )
    def post(self, request):
        valid_fields = {"email", "first_name", "last_name", "groups", "id_group", "username", "password", "confirm_password",}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instanse = serializer.save()
            tokens = get_token_for_user(instanse)
            return success_created_response(tokens)
        return bad_request_response(serializer.errors)        


class UserSignIn(APIView):
    render_classes = [UserRenderers]

    @swagger_auto_schema(tags=['Auth'], request_body=UserSignInSerializer)
    def post(self, request):
        valid_fields = {"username", "password"}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializer = UserSignInSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            username = request.data["username"]
            password = request.data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                tokens = get_token_for_user(user)
                return success_created_response(tokens)
            else:
                return user_not_found_response("This user is not available to the system")
        return success_created_response(serializer.errors)


class UserProfile(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=['Auth'], responses={200: UserInformationSerializer(many=True)})
    def get(self, request):
        serializer = UserInformationSerializer(request.user, context={"request": request})
        return success_response(serializer.data)
    

    @swagger_auto_schema(tags=['Auth'], request_body=UserUpdateSerializer)
    def put(self, request, *args, **kwarg):
        valid_fields = {"email", "first_name", "last_name", "group", "id_group", "username",}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        queryset = get_object_or_404(CustomUser, id=request.user.id)
        serializer = UserUpdateSerializer(context={"request": request}, instance=queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    @swagger_auto_schema(tags=['Auth'], responses={204:  'No Content'})
    def delete(self, request):
        user_delete = CustomUser.objects.get(id=request.user.id)
        user_delete.delete()
        return success_response("delete success")


@api_view(["POST"])
@swagger_auto_schema(tags=['Auth'], request_body=ChangePasswordSerializer)
@permission_classes([IsAuthenticated])
@permission_classes([IsLogin])
def change_password(request):
    if request.method == "POST":
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get("old_password")):
                user.set_password(serializer.data.get("new_password"))
                user.save()
                update_session_auth_hash(request, user)
                return success_response("Password changed successfully.")
            return bad_request_response("Incorrect old password.")
        return bad_request_response(serializer.errors)


class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(tags=['Forget Password'], request_body=ResetPasswordSerializer)
    @action(methods=['post'], detail=False)
    def post(self, request):
        email = request.data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            absurl = f"http://localhost:5173/reset-password/{uidb64}/{token}"
            email_body = f"Hi \n Use link below to reset password \n link: {absurl}"
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Reset your password",
            }

            Util.send(data)

            return success_response("We have sent you to rest your password")
        return user_not_found_response("This email is not found.")



class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetCompleteSerializer

    @swagger_auto_schema(tags=['Forget Password'], request_body=PasswordResetCompleteSerializer)
    @action(methods=['patch'], detail=False)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response("success.")