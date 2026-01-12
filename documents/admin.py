from django.contrib import admin
from .models import Category, SubCategory, Document


# =========================
# Document inline (само preview)
# =========================

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1
    fields = ("title", "file", "uploaded_at", "is_archived")
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at", "title")
    show_change_link = True


# =========================
# SubCategory inline (в Category)
# =========================

# class SubCategoryInline(admin.StackedInline):
#     model = SubCategory
#     extra = 0
#     fields = ("name", "order")
#     show_change_link = True


# =========================
# Category admin (главният екран)
# =========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "order")
    list_editable = ("order",)
    readonly_fields = ("code",)
    ordering = ("order", "name")
    search_fields = ("name", "code")
    # inlines = [SubCategoryInline]


# =========================
# SubCategory admin
# =========================

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_editable = ("order",)
    list_filter = ("category",)
    search_fields = ("name",)
    ordering = ("category__order", "order", "name")
    inlines = [DocumentInline]


# =========================
# Document admin
# =========================

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subcategory",
        "category_name",
        "is_archived",
        "uploaded_at",
        "file",
    )

    list_editable = ("is_archived",)

    list_filter = (
        "is_archived",
        "subcategory__category",
        "subcategory",
    )

    search_fields = ("title", "description")

    ordering = (
        "subcategory__category__order",
        "subcategory__category__name",
        "subcategory__order",
        "subcategory__name",
        "-uploaded_at",
        "title",
    )

    date_hierarchy = "uploaded_at"

    # ---------- custom columns ----------

    @admin.display(
        description="Категория",
        ordering="subcategory__category__order",
    )
    def category_name(self, obj):
        return obj.subcategory.category.name
