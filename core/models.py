from django.db import models
from django.utils import timezone
from slugify import slugify  # python-slugify
# from django.utils.text import slugify


# core/models.py


class SuperCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Суперкатегория'
        verbose_name_plural = 'Суперкатегории'

    def save(self, *args, **kwargs):
        if self.order == 0:
            last = SuperCategory.objects.aggregate(models.Max('order'))[
                'order__max'] or 0
            self.order = last + 1

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DocumentCategory(models.Model):
    supercategory = models.ForeignKey(SuperCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    # original_supercategory = models.ForeignKey(
    #     SuperCategory,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='original_categories',
    #     help_text="Оригиналната суперкатегория, от която е архивирана тази категория."
    # )

    class Meta:
        unique_together = ('supercategory', 'name')
        ordering = ['supercategory__order', 'order']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    # def save(self, *args, **kwargs):
    #     if self.order == 0:
    #         last = DocumentCategory.objects.filter(supercategory=self.supercategory)\
    #             .aggregate(models.Max('order'))['order__max'] or 0
    #         self.order = last + 1

    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.supercategory.name})"


class Document(models.Model):
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateField(default=timezone.localdate)
    # uploaded_at = models.DateField(default=timezone.now)
    order = models.PositiveIntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    original_supercategory = models.ForeignKey(
        SuperCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='original_documents'
    )

    class Meta:
        # ordering = ['category', 'order', '-uploaded_at', 'title']
        ordering = ['category__supercategory__order',
                    'category__order', 'order', '-uploaded_at']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'

    def save(self, *args, **kwargs):
        if not self.uploaded_at:
            self.uploaded_at = timezone.now().date()

        # if self.order == 0:
        #     last = Document.objects.filter(category=self.category)\
        #         .aggregate(models.Max('order'))['order__max'] or 0
        #     self.order = last + 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# class SuperCategory(models.Model):
#     """Най-горно ниво – например 'Правилници', 'Бюджет', 'Харта на клиента'."""
#     name = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(unique=True, blank=True)

#     class Meta:
#         ordering = ['name']
#         verbose_name = 'Суперкатегория'
#         verbose_name_plural = 'Суперкатегории'

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name


# class DocumentCategory(models.Model):
#     """Категория в рамките на дадена суперкатегория (напр. 'Вътрешни правила')."""
#     supercategory = models.ForeignKey(SuperCategory, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True, blank=True)

#     class Meta:
#         unique_together = ('supercategory', 'name')
#         ordering = ['name']
#         verbose_name = 'Категория'
#         verbose_name_plural = 'Категории'

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name} ({self.supercategory.name})"


# class Document(models.Model):
#     """Всеки отделен документ, свързан с категория."""
#     category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     file = models.FileField(upload_to='documents/')
#     uploaded_at = models.DateField(default=timezone.now)
#     slug = models.SlugField(unique=True, blank=True)

#     class Meta:
#         ordering = ['-uploaded_at']  # новите документи най-отгоре
#         verbose_name = 'Документ'
#         verbose_name_plural = 'Документи'

#     def save(self, *args, **kwargs):
#         # Автоматично генериране на slug, ако липсва
#         if not self.slug:
#             base_slug = slugify(self.title)
#             slug = base_slug
#             counter = 1
#             while Document.objects.filter(slug=slug).exists():
#                 slug = f"{base_slug}-{counter}"
#                 counter += 1
#             self.slug = slug

#         # Ако няма дата, задаваме днешната
#         if not self.uploaded_at:
#             self.uploaded_at = timezone.now().date()

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title


# from django.db import models
# from django.utils.text import slugify
# from django.utils import timezone


# class SuperCategory(models.Model):
#     """
#     Супер-категория (Menu top-level). Пример: 'Стратегия на училището',
#     'Правилници' и т.н.
#     Тези ще са предварително зададени и ще се ползват в менюто "Документи".
#     """
#     name = models.CharField(max_length=200, unique=True)
#     slug = models.SlugField(max_length=200, unique=True, blank=True)

#     class Meta:
#         verbose_name = "Супер категория"
#         verbose_name_plural = "Супер категории"
#         ordering = ["name"]

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             # автоматично прави slug от името
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name


# class DocumentCategory(models.Model):
#     """
#     Категорията е под суперкатегорията.
#     Пример: за SuperCategory = 'Правилници' -> categories:
#     'Вътрешни правилници', 'Правилник за дейността' и т.н.
#     """
#     supercategory = models.ForeignKey(
#         SuperCategory, on_delete=models.CASCADE, related_name="categories")
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, blank=True)
#     order = models.PositiveIntegerField(default=0)

#     class Meta:
#         verbose_name = "Категория документи"
#         verbose_name_plural = "Категории документи"
#         ordering = ["order", "name"]
#         unique_together = ("supercategory", "name")

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name}"


# class Document(models.Model):
#     category = models.ForeignKey(
#         DocumentCategory, on_delete=models.CASCADE, related_name="documents")
#     title = models.CharField(max_length=255)
#     # файлове в MEDIA_ROOT/documents/YYYY/MM
#     file = models.FileField(upload_to="documents/%Y/%m/")
#     description = models.TextField(blank=True)
#     uploaded_at = models.DateTimeField(default=timezone.now, blank=True)
#     published = models.DateField(null=True, blank=True)
#     order = models.PositiveIntegerField(default=0)

#     class Meta:
#         verbose_name = "Документ"
#         verbose_name_plural = "Документи"
#         ordering = ["order", "-uploaded_at"]

#     def __str__(self):
#         return self.title


# from django.db import models

# # Create your models here.


# class News(models.Model):
#     title = models.CharField(max_length=255)
#     excerpt = models.TextField(blank=True)
#     content = models.TextField(blank=True)
#     date = models.DateField()
#     slug = models.SlugField(unique=True)

#     def __str__(self):
#         return self.title


# class DocumentCategory(models.Model):
#     name = models.CharField(max_length=150)
#     order = models.IntegerField(default=0)
#     def __str__(self): return self.name


# class Document(models.Model):
#     category = models.ForeignKey(
#         DocumentCategory, on_delete=models.CASCADE, related_name='docs')
#     title = models.CharField(max_length=255)
#     file = models.FileField(upload_to='documents/')
#     published = models.DateField(null=True, blank=True)
#     def __str__(self): return self.title


# class GalleryImage(models.Model):
#     title = models.CharField(max_length=200, blank=True)
#     image = models.ImageField(upload_to='gallery/')
#     order = models.IntegerField(default=0)
#     def __str__(self): return self.title or str(self.pk)


# class ContactInfo(models.Model):
#     phone = models.CharField(max_length=50, blank=True)
#     email = models.EmailField(blank=True)
#     address = models.CharField(max_length=255, blank=True)
#     map_embed = models.TextField(blank=True)
#     def __str__(self): return 'Contacts'
