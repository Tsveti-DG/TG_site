from django.contrib import admin
from .models import SuperCategory, DocumentCategory, Document


# ---------------------------
#  SuperCategory Admin
# ---------------------------

@admin.register(SuperCategory)
class SuperCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "slug")
    list_editable = ("order",)
    ordering = ("order", "name")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


# ---------------------------
#  Document Inline
# ---------------------------

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1
    fields = ("title", "file", "uploaded_at", "order", "is_archived")
    show_change_link = True


# ---------------------------
#  DocumentCategory Admin
# ---------------------------

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "supercategory", "order")
    list_editable = ("order",)
    list_filter = ("supercategory",)
    search_fields = ("name",)
    ordering = ("supercategory__order", "order", "name")
    inlines = [DocumentInline]


# ---------------------------
#  Document Admin
# ---------------------------

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "uploaded_at", "is_archived",
                    "order", "file")
    list_editable = ("order", "is_archived")
    list_filter = ("category__supercategory", "category", "is_archived")
    search_fields = ("title", "description")
    ordering = (
        "category__supercategory__order",
        "category__order",
        "order",
        "-uploaded_at",
    )

    actions = ["archive_documents", "restore_documents"]

    # -------------------------
    # Archive action
    # -------------------------
    @admin.action(description="Архивирай избраните документи")
    def archive_documents(self, request, queryset):
        archive_supercat = SuperCategory.objects.filter(
            name__iexact="Архив").first()
        if not archive_supercat:
            self.message_user(
                request,
                "❌ Няма създадена суперкатегория 'Архив'!",
                level="error"
            )
            return

        for doc in queryset:
            original_cat = doc.category
            original_super = original_cat.supercategory

            # Записваме оригиналната суперкатегория, ако още не е записана
            if not doc.original_supercategory:
                doc.original_supercategory = original_super

            # Намираме същата категория, но под Архив
            archive_cat, created = DocumentCategory.objects.get_or_create(
                name=original_cat.name,
                supercategory=archive_supercat,
            )

            doc.category = archive_cat
            doc.is_archived = True
            doc.save()

        self.message_user(
            request,
            f"✔ Успешно архивирани {queryset.count()} документа."
        )

    # -------------------------
    # Restore action
    # -------------------------
    @admin.action(description="Възстанови от архива избраните документи")
    def restore_documents(self, request, queryset):
        for doc in queryset:
            if not doc.original_supercategory:
                # няма как да знаем откъде е дошъл
                continue

            original_super = doc.original_supercategory

            # Търсим или създаваме категория със същото име под оригиналната суперкатегория
            restored_category, created = DocumentCategory.objects.get_or_create(
                name=doc.category.name,
                supercategory=original_super
            )

            doc.category = restored_category
            doc.is_archived = False
            doc.original_supercategory = None
            doc.save()

        self.message_user(
            request,
            f"✔ Успешно възстановени {queryset.count()} документа от архива."
        )


# from django.contrib import admin
# from .models import SuperCategory, DocumentCategory, Document


# @admin.register(SuperCategory)
# class SuperCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'order')
#     ordering = ('order',)


# @admin.register(DocumentCategory)
# class DocumentCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'supercategory', 'order')
#     ordering = ('supercategory__order', 'order')


# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'uploaded_at', 'is_archived')
#     list_filter = ('category', 'category__supercategory', 'is_archived')
#     search_fields = ('title', 'description')
