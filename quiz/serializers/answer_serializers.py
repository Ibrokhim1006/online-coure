from rest_framework import serializers
from quiz.models import QuizAnswers


class AnswersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuizAnswers
        fields  = ['id', 'answer', 'image', 'video', 'course', 'owner']


class AnswerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    
    class Meta:
        model = QuizAnswers
        fields  = ['id', 'answer', 'image', 'video', 'course', 'owner']
    
    def create(self, validated_data):
        owner = self.context.get('owner')
        answer = QuizAnswers.objects.create(**validated_data)
        answer.owner = owner
        answer.save()
        return answer
    
    def update(self, instance, validated_data):
        instance.answer = validated_data.get("answer", instance.answer)
        instance.video = validated_data.get("video", instance.video)
        if instance.image == None:
            instance.image = self.context.get("image")
        else:
            instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance