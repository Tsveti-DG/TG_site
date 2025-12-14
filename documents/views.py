# documents/views.py
from django.shortcuts import render, get_object_or_404

from .models import SuperCategory, DocumentCategory, Document


def documents_overview(request):
    """ Основна страница 'Документи' — изброява всички суперкатегории """
    supercategories = SuperCategory.objects.all()
    return render(request, 'documents/documents_overview.html', {
        'supercategories': supercategories
    })


def documents_by_supercategory(request, supercategory_slug):
    supercategory = get_object_or_404(SuperCategory, slug=supercategory_slug)
    categories = DocumentCategory.objects.filter(
        supercategory=supercategory
    ).order_by('order', 'name')

    # ако това е Архив — показваме само архивираните
    if supercategory.name.lower() == "архив":
        for cat in categories:
            cat.documents = Document.objects.filter(
                category=cat, is_archived=True
            )
    else:
        for cat in categories:
            cat.documents = Document.objects.filter(
                category=cat, is_archived=False
            )

    return render(request, 'documents/documents_by_supercategory.html', {
        'supercategory': supercategory,
        'categories': categories,
    })
