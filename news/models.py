from django.db import models
from django.urls import reverse
from core.utils.text import unique_code


class News(models.Model):
    title = models.CharField("Заглавие", max_length=255)
    content = models.TextField("Съдържание")
    created_at = models.DateTimeField("Публикувана на", auto_now_add=True)
    code = models.SlugField(
        "Код (URL)",
        max_length=80,
        unique=True,
        help_text="Автоматично генерирано от заглавието",
    )
    image = models.ImageField(
        "Водеща снимка",
        upload_to='news_images/',
        blank=True,
        null=True,
        help_text="Снимка, която се показва в списъка с новини и в началото на статията"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Новина"
        verbose_name_plural = "Новини"

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'code': self.code})

    def save(self, *args, **kwargs):
        self.code = unique_code(News, self.title, self.pk)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
