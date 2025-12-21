# documents/views.py

from django.shortcuts import render, get_object_or_404
from .models import Category, SubCategory, Document


def documents_overview(request):
    categories = Category.objects.all().order_by("order", "name")
    return render(request, "documents/documents_overview.html", {
        "categories": categories,
    })


def documents_by_category(request, category_code):
    category = get_object_or_404(Category, code=category_code)

    subcategories = SubCategory.objects.filter(
        category=category
    ).order_by("order", "name")

    return render(request, "documents/documents_by_category.html", {
        "category": category,
        "subcategories": subcategories,
    })


def documents_archive(request):
    archived_docs = Document.objects.filter(is_archived=True)

    if not archived_docs.exists():
        # ако някой ръчно напише URL-а
        return render(request, "documents/documents_archive.html", {
            "archive_tree": []
        })

    categories = Category.objects.all().order_by("order", "name")

    archive_tree = []

    for category in categories:
        subcats_data = []

        for sub in category.subcategories.all():
            docs = archived_docs.filter(subcategory=sub)

            if docs.exists():
                subcats_data.append({
                    "subcategory": sub,
                    "documents": docs,
                })

        if subcats_data:
            archive_tree.append({
                "category": category,
                "subcategories": subcats_data,
            })

    return render(request, "documents/documents_archive.html", {
        "archive_tree": archive_tree
    })


# def documents_archive(request):
#     documents = Document.objects.filter(is_archived=True).order_by(
#         "subcategory__category__order",
#         "subcategory__order",
#         "order",
#         "-uploaded_at",
#     )

#     return render(request, "documents/documents_archive.html", {
#         "documents": documents,
#     })
