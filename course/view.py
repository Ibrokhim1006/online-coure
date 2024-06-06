from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from course.models import Course, Languages, CourseModul, Lesson


@login_required
def home(request):
    return render(request, 'home.html')


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