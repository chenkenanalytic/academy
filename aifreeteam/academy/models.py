from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField('課程主題名稱', max_length=256)
    slug = models.CharField('主題網址', max_length=256, db_index=True, unique=True)
    intro = models.TextField('主題簡介', default='')
    display = models.BooleanField('主題顯示', default=False)

    def __str__(self):
        return self.name

class Course(models.Model):
    cate = models.ManyToManyField(Category, verbose_name='歸屬主題')
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    slug = models.CharField('課程網址', max_length=256, db_index=True, unique=True)
    img_link = models.CharField('課程圖片連結', max_length=2560, default="/static/academy/img/hero.png")
    instructor = models.CharField(max_length=50)
    duration_hours = models.FloatField()
    level = models.CharField(max_length=20, choices=[
        ('beginner', '初學者'),
        ('intermediate', '中階'),
        ('advanced', '進階')
    ])
    certificate_available = models.BooleanField(default=True)
    # student_limit = models.PositiveIntegerField(default=100)
    price = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'order'], name='unique_chapter_order_per_course')
        ]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    is_preview = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'order'], name='unique_lesson_order_per_course')
        ]

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"

    @property
    def video_embed_url(self):
        if not self.video_url:
            return ""
        if "youtube.com" in self.video_url or "youtu.be" in self.video_url:
            # Handle standard YouTube URLs
            import re
            # Regex to extract video ID from various YouTube URL formats
            regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
            match = re.search(regex, self.video_url)
            if match:
                video_id = match.group(1)
                return f"https://www.youtube.com/embed/{video_id}"
        return self.video_url # Return original if not matched or other source

# ✅ 學員是否購買此課程
class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    has_paid = models.BooleanField(default=True)  # 未來可加付款記錄
    progress = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} in {self.course.title}"

# ✅ 學員觀看單元進度
class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    watched = models.BooleanField(default=False)
    watched_seconds = models.PositiveIntegerField(default=1)  # 可選紀錄秒數
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} [{ '✓' if self.watched else '×' }]"
