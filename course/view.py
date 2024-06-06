from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from course.models import *


@login_required
def home(request):
    context = {}
    context['language'] = Languages.objects.all()
    return render(request, 'home.html', context)


@login_required
def teacher_course(request):
    context = {}
    context['objects_list'] = Course.objects.filter(owner=request.user)
    return render(request, 'teacher/teacher_course.html',context)


@login_required
def add_course(request):
    context = {}
    context['language'] = Languages.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        language_id  = request.POST.get('language')
        if name and content and language_id:
            language = Languages.objects.get(id=language_id)
            Course.objects.create(name=name, content=content, language=language, owner=request.user)
            return redirect('teacher_course')
    return render(request, 'teacher/add_course.html', context)


@login_required
def modul_teacher(request):
    context = {}
    context['objects_list'] = CourseModul.objects.filter(owner=request.user)
    return render(request, 'teacher/module.html', context)

@login_required
def module_test(request, pk):
    context = {}
    context['objects_list'] = CourseModul.objects.get(id=pk)
    context['test'] = Quiz.objects.filter(module=context['objects_list'])
    return render(request, 'teacher/test.html', context)

@login_required
def add_test(request, pk):
    context = {}
    context['objects_list'] = CourseModul.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        module = CourseModul.objects.get(id=pk)
        
        quiz = Quiz.objects.create(name=name, module=module, owner=request.user)
        
        for i in range(1, 4):
            text = request.POST.get(f'text{i}')
            is_correct = request.POST.get(f'is_correct{i}') == 'on'
            QuizChoice.objects.create(question=quiz, text=text, is_correct=is_correct)
        
        return redirect('module_teacher') 
    return render(request, 'teacher/add_test.html', context)


@login_required
def add_module(request):
    context = {}
    context['course'] = Course.objects.filter(owner=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        course_id  = request.POST.get('course')
        if name and content and course_id:
            course = Course.objects.get(id=course_id)
            CourseModul.objects.create(name=name, content=content, course=course, owner=request.user)
            return redirect('module_teacher')
    return render(request, 'teacher/add_module.html', context)


@login_required
def lesson_teacher(request):
    context = {}
    context['objects_list'] = Lesson.objects.filter(owner=request.user)
    return render(request, 'teacher/lessons.html', context)


@login_required
def add_lesson(request):
    context = {}
    context['modul'] = CourseModul.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        module_id = request.POST.get('model')
        
        files = request.FILES.get('files')
        videos = request.FILES.get('videos')
        print(videos)
        if name and module_id and (files or videos):
            module = CourseModul.objects.get(id=module_id, owner=request.user)
            lesson = Lesson.objects.create(
                name=name,
                model=module,
                files=files,
                videos=videos,
                owner=request.user
            )
            return redirect('lesson_teacher')
    return render(request, 'teacher/add_lesson.html', context)


@login_required
def deteile_course(request, pk):
    context = {}
    context['course'] = Course.objects.filter(id=pk)
    context['has_joined'] = request.user.coursestudent_set.filter(course_id=pk).exists()

    return render(request, 'student/deteile_course.html', context)


@login_required
def course_student(request):
    context = {}
    context['course'] = CourseStudent.objects.filter(student=request.user)
    return render(request, 'student/student_course.html', context)


@login_required
def add_student_course(request, pk):
    course = get_object_or_404(Course, pk=pk)  # Retrieve the Course instance
    CourseStudent.objects.create(student=request.user, course=course)
    return redirect('course_student')


@login_required
def my_course(request, pk):
    context = {}
    context['module'] = CourseStudent.objects.filter(course=pk)
    return render(request, 'student/my_corse.html', context)


@login_required
def test_student(request, pk):
    context = {}
    module = get_object_or_404(CourseModul, id=pk)
    context['module'] = module
    context['tests'] = Quiz.objects.filter(module=module)

    if request.method == 'POST':
        total_score = 0
        user_id = request.user.id

        for quiz in context['tests']:
            selected_options = request.POST.getlist(f'question_{quiz.id}_choices')
            correct_options = list(quiz.choice.filter(is_correct=True).values_list('id', flat=True))
            score = sum([5 for option in selected_options if int(option) in correct_options])
            total_score += score

            # Get or create UserTest for the current user and quiz
            user_tests = UserTest.objects.filter(user_id=user_id, quiz=quiz)
            if user_tests.exists():
                user_test = user_tests.first()  # Use the first instance if multiple exist
                user_test.selected_options.clear()  # Clear previous selections
            else:
                user_test = UserTest.objects.create(user_id=user_id, quiz=quiz)

            user_test.selected_options.add(*selected_options)
        
        print(f'Total score: {total_score}')  # Debugging statement
        # Update user's total score in the profile
        user_profile = CustomUser.objects.filter(id=user_id).first()
        if user_profile:
            user_profile.ball = total_score
            user_profile.save()

        context['total_score'] = total_score
        messages.success(request, f'Your total score: {total_score}')
        return render(request, 'student/result.html', context)

    return render(request, 'student/tests.html', context)