from django.contrib import admin
from .models import (
    Category, Course, Chapter, Lesson,
    CourseEnrollment, LessonProgress
)

# --- Inline Config ---

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ('title', 'video_url', 'order', 'is_preview')

class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0

# --- Main Admin Classes ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display')
    list_editable = ('display',)
    search_fields = ('name', 'intro')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'level', 'price', 'is_published')
    list_filter = ('level', 'is_published', 'cate')
    search_fields = ('title', 'subtitle', 'instructor')
    filter_horizontal = ('cate',)
    inlines = [ChapterInline]
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order', 'is_preview')
    list_filter = ('chapter', 'is_preview')
    search_fields = ('title', 'video_url')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'has_paid', 'progress', 'enrolled_at')
    list_filter = ('has_paid', 'course')
    search_fields = ('user__username', 'course__title')

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'watched', 'watched_seconds', 'updated_at')
    list_filter = ('watched', 'lesson')
    search_fields = ('user__username', 'lesson__title')
