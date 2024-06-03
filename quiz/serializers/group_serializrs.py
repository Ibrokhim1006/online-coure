from rest_framework import serializers
from quiz.models import QuizGroup


class QuizGroupsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizGroup
        fields  = ['id', 'name', 'course']


class QuizGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizGroup
        fields  = ['id', 'name', 'course', 'owner']
    
    def create(self, validated_data):
        owner = self.context.get('owner')
        answer = QuizGroup.objects.create(**validated_data)
        answer.owner = owner
        answer.save()
        return answer
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.course = validated_data.get("course", instance.course)
        instance.save()
        return instance