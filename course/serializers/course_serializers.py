from rest_framework import serializers
from course.models import Languages, Course


class LanguageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Languages
        fields = ['id', 'name']


class CoursesSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'content', 'language', 'owner']


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'content', 'language', 'owner']

    def create(self, validated_data):
        owner = self.context.get('owner')
        course = Course.objects.create(**validated_data)
        course.owner = owner
        course.save()
        return course
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.content = validated_data.get("content", instance.content)
        instance.language = validated_data.get("language", instance.language)
        instance.save()
        return instance
    