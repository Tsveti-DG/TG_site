from django.db import models
from django.utils import timezone
from core.utils.text import unique_code


class GalleryAlbum(models.Model):
    title = models.CharField("Заглавие", max_length=255)
    description = models.TextField("Описание", blank=True)
    cover_image = models.ImageField(
        "Корица",
        upload_to="gallery_covers/",
        blank=True,
        null=True
    )
    code = models.SlugField(
        "Код (URL)",
        max_length=50,
        unique=True,
        # blank=True,
        help_text="Автоматично генериран от заглавието"
    )
    order = models.PositiveIntegerField("Ред", default=0)
    related_news = models.ForeignKey(
        "news.News",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Свързана новина",
        help_text="По желание можеш да свържеш албума с новина.",
    )
    created_at = models.DateTimeField(
        "Създаден на",
        default=timezone.now,
        editable=False,
    )

    class Meta:
        ordering = ["order", "-created_at", "title"]
        verbose_name = "Фото албум"
        verbose_name_plural = "Фото албуми"

    def save(self, *args, **kwargs):
        # 1️⃣ code – винаги от заглавието
        self.code = unique_code(GalleryAlbum, self.title, self.pk)

        # 2️⃣ Основен save – гарантира PK
        super().save(*args, **kwargs)

        # 3️⃣ Ако ИМА cover_image → уверяваме се, че е в албума
        if self.cover_image:
            if not self.images.filter(image=self.cover_image).exists():
                GalleryImage.objects.create(
                    album=self,
                    image=self.cover_image,
                    caption="",
                )

        # 4️⃣ Ако НЯМА cover_image, но има снимки → първата става корица
        elif self.images.exists():
            first_image = self.images.order_by("order", "id").first()
            if first_image and first_image.image:
                self.cover_image = first_image.image
                super().save(update_fields=["cover_image"])

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    album = models.ForeignKey(
        GalleryAlbum,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Албум"
    )
    image = models.ImageField("Снимка", upload_to="gallery/")
    caption = models.CharField("Описание", max_length=255, blank=True)
    order = models.PositiveIntegerField("Ред", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Снимка"
        verbose_name_plural = "Снимки"

    def __str__(self):
        return f"{self.album.title} – снимка"


# class GalleryVideo(models.Model):
#     album = models.ForeignKey(
#         GalleryAlbum,
#         on_delete=models.CASCADE,
#         related_name="videos",
#         verbose_name="Албум"
#     )

#     video_url = models.URLField(
#         "Видео (YouTube / Vimeo)",
#         help_text="Постави линк към YouTube или Vimeo видео"
#     )

#     title = models.CharField(
#         "Заглавие",
#         max_length=255,
#         blank=True
#     )

#     order = models.PositiveIntegerField("Ред", default=0)

#     class Meta:
#         ordering = ["order", "id"]
#         verbose_name = "Видео"
#         verbose_name_plural = "Видеа"

#     def __str__(self):
#         return self.title or self.video_url
