from django.shortcuts import render, get_object_or_404
# from .models import News, DocumentCategory, GalleryImage, ContactInfo

# Create your views here.

from .models import SuperCategory, DocumentCategory, Document


def documents_overview(request):
    """ Основна страница 'Документи' — изброява всички суперкатегории """
    supercategories = SuperCategory.objects.all()
    return render(request, 'core/documents_overview.html',
                  {'supercategories': supercategories})


# def documents_by_supercategory(request, super_slug):
#     supercategory = get_object_or_404(SuperCategory, slug=super_slug)
#     categories = DocumentCategory.objects.filter(
#         supercategory=supercategory
#     ).order_by('order', 'name')
#     return render(request, 'core/documents_by_supercategory.html', {
#         'supercategory': supercategory,
#         'categories': categories,
#     })


def documents_by_supercategory(request, supercategory_slug):
    supercategory = get_object_or_404(SuperCategory, slug=supercategory_slug)
    categories = DocumentCategory.objects.filter(
        supercategory=supercategory).order_by('order', 'name')

    # ако това е Архив — показваме само архивираните
    if supercategory.name.lower() == "архив":
        for cat in categories:
            cat.documents = Document.objects.filter(
                category=cat, is_archived=True)
    else:
        for cat in categories:
            cat.documents = Document.objects.filter(
                category=cat, is_archived=False)

    return render(request, 'core/documents_by_supercategory.html', {
        'supercategory': supercategory,
        'categories': categories,
    })


# def documents_by_supercategory(request, super_slug):
#     """ Динамична страница за всяка суперкатегория """
#     supercategory = get_object_or_404(SuperCategory.objects.prefetch_related(
#         'documentcategory_set__document_set'
#     ), slug=super_slug)

#     categories = supercategory.documentcategory_set.all().order_by('name')

#     return render(request, 'core/documents_by_supercategory.html', {
#         'supercategory': supercategory,
#         'categories': categories
#     })


# Основна страница
def home(request):
    return render(request, "core/home.html")

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

# Документи


def documents(request):
    return render(request, "core/documents.html")


def documents_strategy(request):
    return render(request, "core/documents_strategy.html")


def documents_rules(request):
    return render(request, "core/documents_rules.html")


def documents_programs(request):
    return render(request, "core/documents_programs.html")


def documents_services(request):
    return render(request, "core/documents_services.html")


def documents_bdp(request):
    return render(request, "core/documents_bdp.html")


def documents_charter(request):
    return render(request, "core/documents_charter.html")

# Други


def admission(request):
    return render(request, "core/admission.html")


def education(request):
    return render(request, "core/education.html")

# За учениците


def students(request):
    return render(request, "core/students.html")


def students_schedule(request):
    return render(request, "core/students_schedule.html")


def students_graphics(request):
    return render(request, "core/students_graphics.html")


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

# Новини


def news(request):
    return render(request, "core/news.html")

# Галерия


def gallery(request):
    return render(request, "core/gallery.html")

# Контакти


def contacts(request):
    return render(request, "core/contacts.html")


# def home(request):
#     news = News.objects.order_by('-date')[:6]
#     doc_cats = DocumentCategory.objects.order_by('order')
#     gallery = GalleryImage.objects.order_by('order')[:8]
#     contact = ContactInfo.objects.first()
#     return render(request, 'core/home.html', {
#         'news': news,
#         'doc_cats': doc_cats,
#         'gallery': gallery,
#         'contact': contact
#     })


# def news_detail(request, slug):
#     post = get_object_or_404(News, slug=slug)
#     return render(request, 'core/news_detail.html', {'post': post})
