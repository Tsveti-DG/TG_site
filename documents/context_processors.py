# from .models import Category


# def categories_processor(request):
#     categories = Category.objects.all().order_by("order", "name")

#     return {
#         "menu_categories": categories,
#         "menu_archive_url": "/documents/archive/",
#     }


from .models import Category, Document


def categories_processor(request):
    categories = Category.objects.all().order_by("order", "name")

    archived_count = Document.objects.filter(is_archived=True).count()

    return {
        "menu_categories": categories,
        "show_archive": archived_count > 0,
        "archived_count": archived_count,
    }
