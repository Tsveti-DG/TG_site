from django import template
from documents.models import Document

# documents/templatetags/document_tags.py

register = template.Library()


@register.inclusion_tag("documents/includes/documents_list.html")
def show_documents(subcategory):
    documents = Document.objects.filter(
        subcategory=subcategory,
        is_archived=False
    ).order_by("-uploaded_at", "title")

    return {"documents": documents}
