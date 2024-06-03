from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissions import IsTeacher
from utils.expected_fields import check_required_key
from utils.response import success_response, success_created_response, bad_request_response

from course.models import CourseModul
from course.serializers.module_serializers import CoursModulesSerializer, CoursModuleSerializer


class CoursModulesView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTeacher]

    @swagger_auto_schema(tags=['Course Module'], responses={200: CoursModulesSerializer(many=True)})
    def get(self, request):
        objects_list = CourseModul.objects.filter(owner=request.user)
        serializers = CoursModulesSerializer(objects_list, many=True)
        return success_response(serializers.data)

    @swagger_auto_schema(tags=['Course Module'], request_body=CoursModuleSerializer)
    def post(self, request):
        serializers = CoursModuleSerializer(data=request.data, context={'owner': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)
    


class CoursModuleView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsTeacher]

    @swagger_auto_schema(tags=['Course Module'], responses={200: CoursModulesSerializer(many=True)})
    def get(self, request, pk):
        objects_list = get_object_or_404(CourseModul, id=pk)
        serializers = CoursModulesSerializer(objects_list)
        return success_response(serializers.data)

    @swagger_auto_schema(tags=['Course Module'], request_body=CoursModuleSerializer)
    def put(self, request, pk):
        serializers = CoursModuleSerializer(instance=CourseModul.objects.filter(id=pk)[0], data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    @swagger_auto_schema(tags=['Course Module'], responses={204:  'No Content'})
    def delete(self, request, pk):
        course = CourseModul.objects.get(id=pk)
        course.delete()
        return success_response({"message": "Deleted successfully."})