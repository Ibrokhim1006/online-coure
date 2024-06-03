from rest_framework import serializers
from quiz.models import Quiz, QuizChoice


class QuizChoicesSerializser(serializers.ModelSerializer):
    class Meta:
        model = QuizChoice
        fields = ['id', 'question', 'text', 'is_correct']


class QuizsSerializer(serializers.ModelSerializer):
    choice = QuizChoicesSerializser(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields  = ['id', 'question', 'image', 'answer', 'choice', 'group', 'course', 'owner']


class QuizSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    choice = QuizChoicesSerializser(many=True)
    
    class Meta:
        model = Quiz
        fields  = ['id', 'question', 'image', 'answer', 'choice', 'group', 'course', 'owner']
    
    def create(self, validated_data):
        choice = validated_data.pop('choice')
        owner = self.context.get('owner')
        quiz = Quiz.objects.create(**validated_data)
        quiz.owner = owner
        quiz.save()
        for choice_data in choice:
            QuizChoice.objects.create(question=quiz, **choice_data)
        return quiz
    
    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choice', None)
        instance.question = validated_data.get("question", instance.question)
        instance.answer = validated_data.get("answer", instance.answer)
        if instance.image == None:
            instance.image = self.context.get("image")
        else:
            instance.image = validated_data.get("image", instance.image)
        instance.save()
        if choices_data:
            instance.choice.all().delete()  # Clear existing choices
            for choice_data in choices_data:
                QuizChoice.objects.create(question=instance, **choice_data)
        return instance