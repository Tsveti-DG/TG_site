from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from core.utils.text import unique_code

from django.utils.html import strip_tags
import html
import re


class CreativeWork(models.Model):
    title = models.CharField("Заглавие", max_length=255)

    author = models.CharField(
        "Автор",
        max_length=255,
        blank=True,
        help_text="По желание (ученик, клас, псевдоним)"
    )

    published_at = models.DateTimeField(
        "Дата на публикуване",
        default=timezone.now,
        help_text="Ако не избереш дата, ще се използва днешната"
    )

    content = CKEditor5Field("Съдържание")

    image = models.ImageField(
        "Водеща снимка",
        upload_to="creativity_images/",
        blank=True,
        null=True
    )

    code = models.SlugField(
        "Код (URL)",
        max_length=80,
        unique=True,
        help_text="Автоматично генериран от заглавието"
    )

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Творба"
        verbose_name_plural = "Творчество"

    def save(self, *args, **kwargs):
        self.code = unique_code(CreativeWork, self.title, self.pk)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("creativity:detail", kwargs={"code": self.code})

    def __str__(self):
        return self.title

    def excerpt(self, words=25):
        text = self.content

        # 1️⃣ HTML редове → \n
        text = re.sub(r'<\s*br\s*/?>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p\s*>', '\n', text, flags=re.IGNORECASE)

        # 2️⃣ махаме HTML
        text = strip_tags(text)

        # 3️⃣ декодираме entities (&nbsp; и др.)
        text = html.unescape(text)

        # 4️⃣ нормализираме редовете
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\n{2,}', '\n', text)

        # 5️⃣ режем по думи, БЕЗ да губим новите редове
        result = []
        word_count = 0

        for token in re.split(r'(\s+)', text):
            if token.strip():
                word_count += 1
            result.append(token)
            if word_count >= words:
                break

        final_text = "".join(result).strip()
        return final_text + "…"
