# from django.db import models
# from django.utils import timezone
# from django.utils.text import slugify
# from django.urls import reverse
# from slugify import slugify  # python-slugify
# from django.utils.text import slugify

# core/models.py


# class Newspaper(models.Model):
#     issue_number = models.PositiveIntegerField(
#         help_text="Номер на броя: 1, 2, 3..."
#     )
#     title = models.CharField(
#         max_length=255,
#         blank=True,
#         help_text="Опционално заглавие на броя"
#     )
#     pdf = models.FileField(
#         upload_to='newspaper/',
#         help_text="PDF файл на броя"
#     )
#     cover_image = models.ImageField(
#         upload_to='newspaper_covers/',
#         blank=True,
#         null=True,
#         help_text="Качи снимка за превю (ако няма — ще се използва стандартна)"
#     )
#     published_at = models.DateField(
#         default=timezone.now,
#         help_text="Дата на публикуване"
#     )

#     class Meta:
#         ordering = ['-published_at', '-issue_number']
#         verbose_name = "Брой на училищния вестник"
#         verbose_name_plural = "Училищен вестник"

#     def __str__(self):
#         return f"Брой {self.issue_number} / {self.published_at}"

#     def get_cover(self):
#         """Връща качената корица или стандартна по подразбиране."""
#         if self.cover_image:
#             return self.cover_image.url
#         return '/static/core/images/default_newspaper_cover.png'


# class GalleryAlbum(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     cover_image = models.ImageField(
#         upload_to="gallery_covers/", blank=True, null=True)
#     slug = models.SlugField(unique=True, blank=True)
#     order = models.PositiveIntegerField(default=0)
#     related_news = models.ForeignKey(
#         'News',
#         on_delete=models.SET_NULL,
#         blank=True,
#         null=True,
#         help_text="По желание можеш да свържеш албума с новина."
#     )

#     class Meta:
#         ordering = ['order', 'title']
#         verbose_name = "Албум"
#         verbose_name_plural = "Фото албуми"

#     def save(self, *args, **kwargs):
#         is_new = self.pk is None
#         old_cover = None

#         # За съществуващи албуми – вземаме предишната корица
#         if not is_new:
#             old_cover = GalleryAlbum.objects.filter(pk=self.pk).values_list(
#                 "cover_image", flat=True
#             ).first()

#         # Автоматично задаване на order
#         if self.order == 0:
#             last = GalleryAlbum.objects.aggregate(models.Max("order"))[
#                 "order__max"] or 0
#             self.order = last + 1

#         # Автоматично генериране на slug
#         if not self.slug:
#             self.slug = slugify(self.title)

#         # Първо записваме албума
#         super().save(*args, **kwargs)

#         # Ако няма корица, спираме
#         if not self.cover_image:
#             return

#         # Ако корицата е нова или е променена
#         if is_new or self.cover_image.name != old_cover:

#             # Проверяваме дали вече има снимка със същото изображение
#             exists = self.images.filter(image=self.cover_image).exists()

#             # Ако я няма → добавяме я като снимка
#             if not exists:
#                 last_order = self.images.aggregate(models.Max("order"))[
#                     "order__max"] or 0

#                 GalleryImage.objects.create(
#                     album=self,
#                     image=self.cover_image,
#                     caption="",
#                     order=last_order + 1
#                 )

#     def __str__(self):
#         return self.title


# class GalleryImage(models.Model):
#     album = models.ForeignKey(
#         GalleryAlbum, on_delete=models.CASCADE, related_name="images")
#     image = models.ImageField(upload_to="gallery/")
#     caption = models.CharField(max_length=255, blank=True)
#     order = models.PositiveIntegerField(default=0)

#     class Meta:
#         ordering = ['order']
#         verbose_name = "Снимка"
#         verbose_name_plural = "Снимки"

#     def save(self, *args, **kwargs):
#         if self.order == 0:
#             last = GalleryImage.objects.filter(album=self.album).aggregate(
#                 models.Max("order"))["order__max"] or 0
#             self.order = last + 1
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Снимка от {self.album.title}"


# class News(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField(unique=True, max_length=255)
#     image = models.ImageField(upload_to='news_images/', blank=True, null=True)
#     youtube_id = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = "Новина"
#         verbose_name_plural = "Новини"

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('core:news_detail', kwargs={'slug': self.slug})


# class NewsImage(models.Model):
#     news = models.ForeignKey(
#         News, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='news_images/')
#     caption = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return f"Image for {self.news.title}"
