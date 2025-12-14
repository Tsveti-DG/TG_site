# core/urls.py
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),

    # За нас
    path("about/", views.about, name="about"),
    path("about/base/", views.about_base, name="about_base"),
    path("about/history/", views.about_history, name="about_history"),
    path("about/mission/", views.about_mission, name="about_mission"),
    path("about/team/", views.about_team, name="about_team"),
    path("about/council/", views.about_council, name="about_council"),
    path("about/profile/", views.about_profile, name="about_profile"),

    # Кандидатстване / образование
    path("admission/", views.admission, name="admission"),
    path("education/", views.education, name="education"),

    # За учениците
    path("students/", views.students, name="students"),
    path("students/schedule/", views.students_schedule, name="students_schedule"),
    path("students/graphics/", views.students_graphics, name="students_graphics"),
    path("students/nvo/", views.students_nvo, name="students_nvo"),
    path("students/dzi/", views.students_dzi, name="students_dzi"),
    path("students/scholarships/", views.students_scholarships,
         name="students_scholarships"),
    path("students/diary/", views.students_diary, name="students_diary"),

    # Проекти и програми
    path("projects/", views.projects, name="projects"),

    # Контакти
    path("contacts/", views.contacts, name="contacts"),
]
