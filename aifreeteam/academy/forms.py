from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Course, Chapter, Lesson, Category

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'cate', 'title', 'subtitle', 'description', 'slug', 'img_link', 
            'instructor', 'duration_hours', 'level', 'price', 
            'is_published', 'certificate_available'
        ]
        widgets = {
            'cate': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'img_link': forms.TextInput(attrs={'class': 'form-control'}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'certificate_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'cate': '歸屬主題',
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

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'intro', 'display']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'intro': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'display': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': '主題名稱',
            'slug': '網址代稱 (Slug)',
            'intro': '主題簡介',
            'display': '是否顯示',
        }
