from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.expected_fields import check_required_key
from utils.response import success_response, success_created_response, bad_request_response

from quiz.models import Quiz
from quiz.serializers.quiz_serializers import QuizsSerializer, QuizSerializer


class QuizsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(tags=['Quiz'], request_body=QuizSerializer)
    def post(self, request):
        valid_fields = { 'question', 'image', 'answer', 'choice', 'group', 'course', 'owner',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = QuizSerializer(data=request.data, context={'request': request, 'owner': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class QuizView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(tags=['Quiz'], responses={200: QuizsSerializer(many=True)})
    def get(self, request, pk):
        objects_list = get_object_or_404(Quiz, id=pk)
        serializers = QuizsSerializer(objects_list)
        return success_response(serializers.data)

    @swagger_auto_schema(tags=['Quiz'], request_body=QuizSerializer)
    def put(self, request, pk):
        valid_fields = { 'question', 'image', 'answer', 'choice', 'group', 'course', 'owner',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = QuizSerializer(instance=Quiz.objects.filter(id=pk)[0], context={"request": request}, data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    @swagger_auto_schema(tags=['Quiz'], responses={204:  'No Content'})
    def delete(self, request, pk):
        quiz = Quiz.objects.get(id=pk)
        quiz.delete()
        return success_response({"message": "Deleted successfully."})


class GroupQuestionView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(tags=['Quiz'], responses={200: QuizsSerializer(many=True)})
    def get(self, request, pk, course_pk):
        queryset = Quiz.objects.filter(group=pk, course=course_pk).order_by('-create_at')
        serializer = QuizsSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)