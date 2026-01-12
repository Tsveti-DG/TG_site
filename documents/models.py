from django.db import models
from django.utils import timezone
from core.utils.text import unique_code


class Category(models.Model):
    name = models.CharField("Име", max_length=200, unique=True)
    code = models.SlugField(
        "Код (URL)",
        max_length=50,
        unique=True,
        help_text="Автоматично генериран от името",
    )
    order = models.PositiveIntegerField("Ред", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self, *args, **kwargs):
        self.code = unique_code(Category, self.name, self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория"
    )
    name = models.CharField("Име", max_length=200)
    order = models.PositiveIntegerField("Ред", default=0)

    class Meta:
        unique_together = ("category", "name")
        ordering = ["category__order", "order", "name"]
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Document(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="Подкатегория"
    )

    title = models.CharField("Заглавие", max_length=255)
    description = models.TextField("Описание", blank=True)
    file = models.FileField("Файл", upload_to="documents/")
    uploaded_at = models.DateField(
        "Дата на качване",
        default=timezone.localdate
    )
    is_archived = models.BooleanField("Архивиран", default=False)

    class Meta:
        ordering = [
            "subcategory__category__order",
            "subcategory__category__name",
            "subcategory__order",
            "subcategory__name",
            "-uploaded_at",
            "title",
        ]
        verbose_name = "Документ"
        verbose_name_plural = "Документи"

    def __str__(self):
        return self.title
