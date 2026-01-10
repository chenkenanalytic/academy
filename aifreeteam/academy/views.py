from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from academy.models import Course, CourseEnrollment, Lesson
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .forms import CourseForm, ChapterForm, LessonForm

# Create your views here.

def academy_main(request):
    top_courses = Course.objects.annotate(enroll_count=Count('enrollments')).order_by('-enroll_count')[:3]
    return render(request, 'academy/main.html', locals())

def academy_course_search(request):
    return render(request, 'academy/course_search.html', locals())

def academy_course(request, slug):
    course = Course.objects.annotate(enroll_count=Count('enrollments')).get(slug=slug)
    # 檢查是否已登入 & 是否有報名
    has_enrolled = False
    if request.user.is_authenticated:
        has_enrolled = CourseEnrollment.objects.filter(user=request.user, course=course).exists()
    return render(request, 'academy/course.html', locals())

def academy_course_class(request, slug):
    course = Course.objects.get(slug=slug)
    if request.user.is_authenticated:
        try:
            enrollment = CourseEnrollment.objects.get(user=request.user, course=course)
            num_progress = len(Lesson.objects.filter(chapter__course=course))
            progress = enrollment.progress
            progress = num_progress if progress > num_progress else progress
            return redirect(f'/academy/course/{course.slug}/{progress}/')
        except CourseEnrollment.DoesNotExist:
            enrollment = None
            return redirect(f'/academy/course/{course.slug}')
    # return render(request, 'academy/lesson.html', locals())

@login_required
def academy_course_register(request, slug):
    course = get_object_or_404(Course, slug=slug)

    # 檢查是否已報名
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'has_paid': True, 'progress': 1}
    )

    if not created:
        messages.info(request, "你已經報名過這門課程。")
    else:
        messages.success(request, f"成功報名：{course.title}")

    return redirect(f'/academy/course/{course.slug}')

@login_required
def academy_course_lesson(request, slug, progress, status=None):
    course = Course.objects.get(slug=slug)
    lesson = Lesson.objects.filter(
        chapter__course=course,  # 指定課程
        order=progress           # 指定單元順序
    ).first()

    if status == 'complete':
        user_enrollment = CourseEnrollment.objects.get(user=request.user, course=course)
        user_enrollment.progress = progress
        user_enrollment.save()
    if status == 'complete_all':
        user_enrollment = CourseEnrollment.objects.get(user=request.user, course=course)
        user_enrollment.progress = progress+1
        user_enrollment.save()
        messages.info(request,f"恭喜您，完成【{course.title}】！")
    
    user_progress = CourseEnrollment.objects.get(user=request.user, course=course).progress
    num_progress = len(Lesson.objects.filter(chapter__course=course))

    return render(request, 'academy/lesson.html', locals())

def academy_login(request):
    if request.user.is_authenticated:
        return redirect('/academy/main/')  # 換成你想導向的 URL name
    else:
        return render(request, 'academy/login.html', locals())

@login_required
def academy_logout(request):
    logout(request)
    messages.success(request, "你已成功登出。")
    return redirect('/academy/main/')  # 換成你想導向的 URL name


def academy_login_post(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        # user = authenticate(request, username=username, password=password)
        # print(login(request, user))
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '登入成功！')
            return redirect('/academy/main/')  # 要導向的頁面
        else:
            messages.error(request, '帳號或密碼錯誤')

    return render(request, 'academy/login.html', locals())

def academy_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, '兩次密碼輸入不一致')
            return render(request, 'academy/register.html', locals())

        if User.objects.filter(username=username).exists():
            messages.error(request, '此使用者名稱已被使用')
            return render(request, 'academy/register.html', locals())
        
        if User.objects.filter(email=email).exists():
            messages.error(request, '此電子信箱已被註冊')
            return render(request, 'academy/register.html', locals())

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        # Login immediately
        login(request, user)
        messages.success(request, '註冊成功！歡迎加入自由學院')
        return redirect('/academy/main/')

    return render(request, 'academy/register.html', locals())

@login_required
def academy_account(request):
    return render(request, 'academy/profile.html', locals())

@login_required
def academy_my_course(request):
    enrollments = CourseEnrollment.objects.select_related('course').filter(user=request.user)

    course_progress_data = []
    for enroll in enrollments:
        course = enroll.course
        # 計算總 lessons 數（跨所有章節）
        total_lessons = sum(chapter.lessons.count() for chapter in course.chapters.all())
        progress_count = enroll.progress - 1
        progress_percent = round((progress_count / total_lessons) * 100) if total_lessons > 0 else 0
        # print(progress_percent)

        course_progress_data.append({
            'course': course,
            'progress': progress_percent,
            'enroll': enroll,
        })
    return render(request, 'academy/my_course.html', locals())


### 測試前端用
# from copy import deepcopy
# template = Course.objects.first()
# fake_courses = [deepcopy(template) for _ in range(100)]

def api_course_list(request):
    page = int(request.GET.get('page', 1))
    per_page = 9  # 每次載入 6 筆

    courses = Course.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(courses, per_page)
    page_obj = paginator.get_page(page)

    data = []
    for course in page_obj:
        data.append({
            'title': course.title,
            'subtitle': course.subtitle,
            'category': ','.join([c.slug for c in course.cate.all()]),
            'img': course.img_link,
            'slug': course.slug,
            'price': course.price,
            'instructor': course.instructor,
            'students': course.enrollments.count()
        })

    return JsonResponse({'courses': data, 'has_next': page_obj.has_next()})

# --- Dashboard Views ---

@staff_member_required
def dashboard_home(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'academy/dashboard/home.html', locals())

@staff_member_required
def dashboard_course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"課程 {course.title} 建立成功")
            return redirect('dashboard_course_manage', slug=course.slug)
    else:
        form = CourseForm()
    return render(request, 'academy/dashboard/course_form.html', locals())

@staff_member_required
def dashboard_course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "課程資訊更新成功")
            return redirect('dashboard_course_manage', slug=course.slug)
    else:
        form = CourseForm(instance=course)
    return render(request, 'academy/dashboard/course_form.html', locals())

@staff_member_required
def dashboard_course_manage(request, slug):
    course = get_object_or_404(Course, slug=slug)
    chapters = course.chapters.all().order_by('order')
    return render(request, 'academy/dashboard/course_manage.html', locals())

@staff_member_required
def dashboard_chapter_create(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.course = course
            chapter.save()
            messages.success(request, "章節新增成功")
            return redirect('dashboard_course_manage', slug=course.slug)
    else:
        form = ChapterForm()
    return render(request, 'academy/dashboard/chapter_form.html', locals())

@staff_member_required
def dashboard_lesson_create(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    course = chapter.course
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.chapter = chapter
            lesson.save()
            messages.success(request, "單元新增成功")
            return redirect('dashboard_course_manage', slug=course.slug)
    else:
        form = LessonForm()
    return render(request, 'academy/dashboard/lesson_form.html', locals())