from django.db import models
from django.urls import reverse


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
        "Основна снимка", upload_to='news_images/', blank=True, null=True)

    youtube_id = models.CharField(
        "YouTube идентификатор",
        max_length=50,
        blank=True,
        null=True,
        help_text="Символите от url адреса след https://www.youtube.com/watch?v=",
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Новина"
        verbose_name_plural = "Новини"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'code': self.code})


class NewsImage(models.Model):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField("Снимка", upload_to='news_images/')
    caption = models.CharField("Надпис", max_length=255, blank=True)

    def __str__(self):
        return f"Снимка за {self.news.title}"
