from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Course, Chapter, Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'subtitle', 'description', 'slug', 'img_link', 
            'instructor', 'duration_hours', 'level', 'price', 
            'is_published', 'certificate_available'
        ]
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'img_link': forms.TextInput(attrs={'class': 'form-control'}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'certificate_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': '課程標題',
            'subtitle': '副標題',
            'description': '課程介紹',
            'slug': '網址代稱 (Slug)',
            'img_link': '圖片連結',
            'instructor': '講師名稱',
            'duration_hours': '課程時數 (小時)',
            'level': '難易度',
            'price': '價格',
            'is_published': '是否發布',
            'certificate_available': '提供證書',
        }

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '章節標題',
            'order': '排序',
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'video_url', 'order', 'is_preview']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_preview': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': '單元標題',
            'video_url': '影片連結',
            'order': '排序',
            'is_preview': '設為試看',
        }
