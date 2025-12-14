from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    youtube_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Новина"
        verbose_name_plural = "Новини"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'slug': self.slug})


class NewsImage(models.Model):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='news_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.news.title}"
