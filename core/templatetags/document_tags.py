from django import template
from core.models import Document

register = template.Library()


@register.inclusion_tag('core/includes/documents_list.html')
def show_documents(category):
    if not category:
        return {'documents': []}

    # Проверяваме дали суперкатегорията е "Архив"
    is_archive = category.supercategory.name.lower() == "архив"

    # Ако сме в "Архив", взимаме само архивирани документи
    # иначе — само неархивирани
    documents = Document.objects.filter(
        category=category,
        is_archived=is_archive
    ).order_by('order', '-uploaded_at', 'title')

    return {'documents': documents}
# @register.inclusion_tag('core/includes/documents_list.html')
# def show_documents(category):
#     if category:
#         documents = Document.objects.filter(
#             category=category).order_by('order', '-uploaded_at', 'title')
#         return {'documents': documents}
