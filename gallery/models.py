from django.db import models
from django.utils.text import slugify


class GalleryAlbum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(
        upload_to="gallery_covers/", blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    related_news = models.ForeignKey(
        "news.News",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="По желание можеш да свържеш албума с новина.",
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Албум"
        verbose_name_plural = "Фото албуми"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_cover = None

        if not is_new:
            old_cover = (
                GalleryAlbum.objects.filter(pk=self.pk)
                .values_list("cover_image", flat=True)
                .first()
            )

        # 1) Автоматично order
        if self.order == 0:
            last = (
                GalleryAlbum.objects.aggregate(
                    models.Max("order"))["order__max"]
                or 0
            )
            self.order = last + 1

        # 2) Slug
        if not self.slug:
            self.slug = slugify(self.title)

        # Първо стандартен save
        super().save(*args, **kwargs)

        # --- A) cover_image → GalleryImage (както досега) ---
        if self.cover_image:
            if is_new or self.cover_image.name != old_cover:
                exists = self.images.filter(image=self.cover_image).exists()
                if not exists:
                    last_order = (
                        self.images.aggregate(models.Max("order"))[
                            "order__max"]
                        or 0
                    )
                    GalleryImage.objects.create(
                        album=self,
                        image=self.cover_image,
                        caption="",
                        order=last_order + 1,
                    )

        # --- B) GalleryImage → cover_image (НОВОТО ПОВЕДЕНИЕ) ---
        if not self.cover_image and self.images.exists():
            first_image = self.images.order_by("order", "id").first()
            if first_image and first_image.image:
                self.cover_image = first_image.image
                # втори лек save само за cover_image – няма да влезе в безкраен цикъл
                super().save(update_fields=["cover_image"])


class GalleryImage(models.Model):
    album = models.ForeignKey(
        GalleryAlbum, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Снимка"
        verbose_name_plural = "Снимки"

    def save(self, *args, **kwargs):
        if self.order == 0:
            last = GalleryImage.objects.filter(album=self.album).aggregate(
                models.Max("order")
            )["order__max"] or 0
            self.order = last + 1
        super().save(*args, **kwargs)
