from django.contrib import admin
from .models import SuperCategory, DocumentCategory, Document, News, NewsImage, GalleryAlbum, GalleryImage, Newspaper


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ('issue_number', 'title', 'published_at')
    list_filter = ('published_at',)
    ordering = ('-issue_number', '-published_at')


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "related_news")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [GalleryImageInline]


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3  # броят празни полета по подразбиране


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    inlines = [NewsImageInline]
    fields = ('title', 'slug', 'content', 'image', 'youtube_id')


@admin.register(SuperCategory)
class SuperCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'slug')
    list_editable = ('order',)
    ordering = ('order', 'name')


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'supercategory', 'order')
    list_editable = ('order',)
    list_filter = ('supercategory',)
    ordering = ('supercategory', 'order', 'name')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at', 'is_archived',
                    'order', 'file')
    list_editable = ('order',)
    list_filter = ('category', 'is_archived')
    ordering = ('category__supercategory__order',
                'category__order', 'order', '-uploaded_at')
    # ordering = ('category', 'order', '-uploaded_at')
    actions = ['archive_documents', 'restore_documents']

    @admin.action(description="Архивирай избраните документи")
    def archive_documents(self, request, queryset):
        archive_supercat = SuperCategory.objects.filter(
            name__iexact="Архив").first()
        if not archive_supercat:
            self.message_user(
                request, "Няма създадена суперкатегория 'Архив'!", level="error")
            return

        for doc in queryset:
            # Преместваме категорията му към Архив (ако не е вече там)
            category = doc.category
            if category.supercategory != archive_supercat:
                # Записваме оригиналната суперкатегория, ако още не е запомнена
                if not doc.original_supercategory:
                    doc.original_supercategory = category.supercategory

                # Проверяваме дали вече има такава категория под Архив
                archived_category, created = DocumentCategory.objects.get_or_create(
                    name=category.name,
                    supercategory=archive_supercat,
                )
                doc.category = archived_category

            doc.is_archived = True
            doc.save()

        self.message_user(
            request, f"Успешно архивирани {queryset.count()} документа.")

    @admin.action(description="Възстанови от архива избраните документи")
    def restore_documents(self, request, queryset):
        for doc in queryset:
            if not doc.original_supercategory:
                continue  # Ако няма записана оригинална суперкатегория, пропускаме

            original_supercat = doc.original_supercategory
            archived_cat = doc.category

            # Търсим дали има категория със същото име под оригиналната суперкатегория
            original_category, created = DocumentCategory.objects.get_or_create(
                name=archived_cat.name,
                supercategory=original_supercat
            )

            doc.category = original_category
            doc.is_archived = False
            doc.original_supercategory = None  # изчистваме, след като е върнат
            doc.save()

        self.message_user(
            request, f"Успешно възстановени {queryset.count()} документа.")

    # @admin.action(description="Възстанови избраните документи от архива")
    # def restore_documents(self, request, queryset):
    #     for doc in queryset:
    #         category = doc.category
    #         # Проверяваме дали категорията има оригинална суперкатегория
    #         if category.supercategory.name.lower() == "архив" and category.original_supercategory:
    #             # Търсим същата категория под оригиналната суперкатегория
    #             restored_category, created = DocumentCategory.objects.get_or_create(
    #                 name=category.name,
    #                 supercategory=category.original_supercategory
    #             )
    #             doc.category = restored_category
    #             doc.is_archived = False
    #             doc.save()

    #     self.message_user(
    #         request, f"Успешно възстановени {queryset.count()} документа.")


# @admin.register(SuperCategory)
# class SuperCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)


# @admin.register(DocumentCategory)
# class DocumentCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'supercategory')
#     list_filter = ('supercategory',)
#     search_fields = ('name',)
#     ordering = ('supercategory', 'name')


# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'uploaded_at')
#     list_filter = ('category',)
#     search_fields = ('title', 'description')
#     ordering = ('category', 'title')

#     # Позволява да избереш категория, но визуално групира по суперкатегория
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "category":
#             kwargs["queryset"] = DocumentCategory.objects.select_related(
#                 "supercategory").order_by("supercategory__name", "name")
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


# from django.contrib import admin
# from .models import SuperCategory, DocumentCategory, Document


# @admin.register(SuperCategory)
# class SuperCategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "slug")
#     prepopulated_fields = {"slug": ("name",)}
#     ordering = ("name",)


# class DocumentInline(admin.TabularInline):
#     model = Document
#     extra = 1
#     fields = ("title", "file", "published", "order")
#     readonly_fields = ()
#     show_change_link = True


# @admin.register(DocumentCategory)
# class DocumentCategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "supercategory", "order")
#     list_filter = ("supercategory",)
#     search_fields = ("name",)
#     prepopulated_fields = {"slug": ("name",)}
#     inlines = [DocumentInline]


# @admin.register(Document)
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ("title", "category", "uploaded_at", "published")
#     list_filter = ("category__supercategory", "category")
#     search_fields = ("title", "description")
#     raw_id_fields = ("category",)


# from .models import News, DocumentCategory, Document, GalleryImage,
# ContactInfo

# # Register your models here.


# @admin.register(News)
# class NewsAdmin(admin.ModelAdmin):
#     list_display = ('title', 'date')
#     prepopulated_fields = {'slug': ('title',)}


# admin.site.register(DocumentCategory)
# admin.site.register(Document)
# admin.site.register(GalleryImage)
# admin.site.register(ContactInfo)
