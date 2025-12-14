from django.db import models
from django.utils import timezone
# Start
from django.urls import reverse


class Newspaper(models.Model):
    issue_number = models.PositiveIntegerField(
        help_text="Номер на броя: 1, 2, 3..."
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Опционално заглавие на броя"
    )
    pdf = models.FileField(
        upload_to='newspaper/',
        help_text="PDF файл на броя"
    )
    cover_image = models.ImageField(
        upload_to='newspaper_covers/',
        blank=True,
        null=True,
        help_text="Качи снимка за превю"
    )
    published_at = models.DateTimeField(
        default=timezone.now,
        help_text="Дата и час на публикуване"
    )

    class Meta:
        ordering = ['-published_at', '-issue_number']
        verbose_name = "Брой на училищния вестник"
        verbose_name_plural = "Училищен вестник"

    def __str__(self):
        return f"Брой {self.issue_number} / {self.published_at.date()}"

    def get_absolute_url(self):
        return reverse("newspaper:newspaper_list")

    def get_cover(self):
        """
        Връща корицата, ако има. Ако няма – дефолтна.
        """
        if self.cover_image:
            return self.cover_image.url
        return '/static/assets/images/default_newspaper_cover.png'
