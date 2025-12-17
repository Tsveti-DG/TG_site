# core/views.py
from django.shortcuts import render
from news.models import News


# Основна страница
def home(request):
    latest_news = News.objects.order_by('-created_at')[:3]
    return render(request, 'core/home.html', {
        'latest_news': latest_news,
    })


# За нас
def about(request):
    return render(request, "core/about.html")


def about_base(request):
    return render(request, "core/about_base.html")


def about_history(request):
    return render(request, "core/about_history.html")


def about_mission(request):
    return render(request, "core/about_mission.html")


def about_team(request):
    return render(request, "core/about_team.html")


def about_council(request):
    return render(request, "core/about_council.html")


def about_profile(request):
    return render(request, "core/about_profile.html")


# Други
def admission(request):
    return render(request, "core/admission.html")


def education(request):
    return render(request, "core/education.html")


# За учениците
def students(request):
    return render(request, "core/students.html")


def students_daily_regime(request):
    return render(request, "core/students_daily_regime.html")


def students_schedules(request):
    return render(request, "core/students_schedules.html")


def students_nvo(request):
    return render(request, "core/students_nvo.html")


def students_dzi(request):
    return render(request, "core/students_dzi.html")


def students_scholarships(request):
    return render(request, "core/students_scholarships.html")


def students_diary(request):
    return render(request, "core/students_diary.html")


# Проекти и програми
def projects(request):
    return render(request, "core/projects.html")


# Контакти
def contacts(request):
    return render(request, "core/contacts.html")
