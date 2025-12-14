from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# ------------------------
#  SuperCategory
# ------------------------


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


# ------------------------
#  DocumentCategory
# ------------------------

class DocumentCategory(models.Model):
    supercategory = models.ForeignKey(SuperCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('supercategory', 'name')
        ordering = ['supercategory__order', 'order']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f"{self.name} ({self.supercategory.name})"


# ------------------------
#  Document
# ------------------------

class Document(models.Model):
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateField(default=timezone.localdate)
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
        ordering = [
            'category__supercategory__order',
            'category__order',
            'order',
            '-uploaded_at'
        ]
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'

    def save(self, *args, **kwargs):
        # if not self.uploaded_at:
        #     self.uploaded_at = timezone.now().date()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
