from rest_framework import serializers
from course.serializers.course_serializers import CoursesSerializer
from course.models import CourseModul


class CoursModulesSerializer(serializers.ModelSerializer):
    course = CoursesSerializer(read_only=True)

    class Meta:
        model = CourseModul
        fields = ['id', 'name', 'content', 'files', 'course', 'owner']


class CoursModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseModul
        fields = ['id', 'name', 'content', 'files', 'course', 'owner']

    def create(self, validated_data):
        owner = self.context.get('owner')
        course = CourseModul.objects.create(**validated_data)
        course.owner = owner
        course.save()
        return course
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.content = validated_data.get("content", instance.content)
        instance.course = validated_data.get("course", instance.course)
        instance.save()
        return instance
    