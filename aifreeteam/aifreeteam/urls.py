"""
URL configuration for aifreeteam project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from academy.views import academy_main, academy_course_search, academy_course, academy_course_lesson, academy_login, academy_course_class, academy_register
from academy.views import academy_login_post, academy_account, academy_my_course, academy_logout, api_course_list, academy_course_register, academy_course_checkout, academy_course_payment_confirm
from academy.views import (
    dashboard_home, dashboard_course_create, dashboard_course_edit, 
    dashboard_course_manage, dashboard_chapter_create, dashboard_lesson_create,
    dashboard_course_export, dashboard_lesson_delete,
    dashboard_chapter_edit, dashboard_chapter_delete, dashboard_lesson_edit,
    dashboard_category_list, dashboard_category_create, dashboard_category_edit, dashboard_category_delete,
    api_category_create
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path('summernote/', include('django_summernote.urls')),

    path("", academy_main, name='academy_main'),
    path("academy/main/", academy_main),
    path("academy/search/", academy_course_search, name='academy_course_search'),
    path("academy/course/<str:slug>/", academy_course, name='academy_course'),
    path("academy/course/<str:slug>/class/", academy_course_class, name='academy_course_class'),
    path("academy/course/<str:slug>/register/", academy_course_register, name='academy_course_register'),
    path("academy/course/<str:slug>/checkout/", academy_course_checkout, name='academy_course_checkout'),
    path("academy/course/<str:slug>/payment/confirm/", academy_course_payment_confirm, name='academy_course_payment_confirm'),
    path("academy/course/<str:slug>/<int:progress>/", academy_course_lesson, name='academy_course_lesson'),
    path("academy/course/<str:slug>/<int:progress>/<str:status>/", academy_course_lesson),
    path("academy/login/", academy_login, name='academy_login'),
    path("academy/register/", academy_register, name='academy_register'),
    path("academy/login/post", academy_login_post, name='academy_login_post'),
    path("academy/logout/", academy_logout, name='academy_logout'),
    path("academy/account/", academy_account),
    path("academy/my_course/", academy_my_course),
    path('academy/api/courses/', api_course_list, name='api_course_list'),
    path('academy/api/category/create/', api_category_create, name='api_category_create'),

    # Dashboard URLs
    path('academy/dashboard/', dashboard_home, name='dashboard_home'),
    path('academy/dashboard/course/create/', dashboard_course_create, name='dashboard_course_create'),
    path('academy/dashboard/course/<str:slug>/edit/', dashboard_course_edit, name='dashboard_course_edit'),
    path('academy/dashboard/course/<str:slug>/manage/', dashboard_course_manage, name='dashboard_course_manage'),
    path('academy/dashboard/course/<str:slug>/chapter/create/', dashboard_chapter_create, name='dashboard_chapter_create'),
    path('academy/dashboard/chapter/<int:chapter_id>/lesson/create/', dashboard_lesson_create, name='dashboard_lesson_create'),
    path('academy/dashboard/export/courses/', dashboard_course_export, name='dashboard_course_export'),
    path('academy/dashboard/lesson/<int:lesson_id>/delete/', dashboard_lesson_delete, name='dashboard_lesson_delete'),
    path('academy/dashboard/chapter/<int:chapter_id>/edit/', dashboard_chapter_edit, name='dashboard_chapter_edit'),
    path('academy/dashboard/chapter/<int:chapter_id>/delete/', dashboard_chapter_delete, name='dashboard_chapter_delete'),
    path('academy/dashboard/lesson/<int:lesson_id>/edit/', dashboard_lesson_edit, name='dashboard_lesson_edit'),

    # Category Management
    path('academy/dashboard/category/', dashboard_category_list, name='dashboard_category_list'),
    path('academy/dashboard/category/create/', dashboard_category_create, name='dashboard_category_create'),
    path('academy/dashboard/category/<int:category_id>/edit/', dashboard_category_edit, name='dashboard_category_edit'),
    path('academy/dashboard/category/<int:category_id>/delete/', dashboard_category_delete, name='dashboard_category_delete'),
]
