from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),

    # За нас
    #     path("about/", views.about, name="about"),
    path("about/base/", views.about_base, name="about_base"),
    path("about/history/", views.about_history, name="about_history"),
    path("about/mission/", views.about_mission, name="about_mission"),
    path("about/team/", views.about_team, name="about_team"),
    path("about/council/", views.about_council, name="about_council"),
    path("about/profile/", views.about_profile, name="about_profile"),

    # Документи
    path("documents/", views.documents_overview, name="documents_overview"),
    path('documents/<slug:supercategory_slug>/',
         views.documents_by_supercategory, name='documents_by_super'),

    # Други
    path("admission/", views.admission, name="admission"),
    path("education/", views.education, name="education"),

    # За учениците
    path("students", views.students, name="students"),
    path("students/schedule/", views.students_schedule, name="students_schedule"),
    path("students/graphics/", views.students_graphics, name="students_graphics"),
    path("students/nvo/", views.students_nvo, name="students_nvo"),
    path("students/dzi/", views.students_dzi, name="students_dzi"),
    path("students/scholarships/", views.students_scholarships,
         name="students_scholarships"),
    path("students/diary/", views.students_diary, name="students_diary"),

    # Проекти и програми
    path("projects/", views.projects, name="projects"),

    # Новини
    #     path("news/", views.news, name="news"),
    path('news/', views.news_list, name='news_list'),

    path('news/newspaper/', views.newspaper, name='newspaper'),
    path('news/creativity/', views.creativity, name='creativity'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),

    # Галерия
    #     path("gallery/", views.gallery, name="gallery"),
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/<slug:slug>/', views.gallery_detail, name='gallery_detail'),

    # Контакти
    path("contacts/", views.contacts, name="contacts"),
]
