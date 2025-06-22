from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class MediaContent(models.Model):
    CONTENT_TYPES = (
        ('article', 'Maqola'),
        ('image', 'Rasm'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    )

    category = models.CharField("Kategoriya", max_length=100, blank=True)
    title = models.CharField("Sarlavha", max_length=200)
    description = models.TextField("Tavsif", blank=True)
    file = models.FileField("Fayl", upload_to='media/', blank=True, null=True)
    content_type = models.CharField("Kontent turi", max_length=20, choices=CONTENT_TYPES)
    created_at = models.DateTimeField("Yaratilgan vaqt", auto_now_add=True)

    is_active = models.BooleanField("Faol (saytda ko‘rinsinmi?)", default=True)
    publish_time = models.DateTimeField("Chop etish vaqti", default=timezone.now)
    views_count = models.PositiveIntegerField("Ko‘rishlar soni", default=0)  # Har xil IPlar uchun oshiriladi

    def __str__(self):
        return f"{self.title} ({self.content_type})"

    def clean(self):
        # Agar maqola emas bo‘lsa va fayl bo‘lmasa, xatolik ber
        if self.content_type != 'article' and not self.file:
            raise ValidationError({'file': f"'{self.content_type}' turi uchun fayl yuklash majburiy!"})

    class Meta:
        verbose_name = "Media kontent"
        verbose_name_plural = "Barcha kontentlar"
        ordering = ['-publish_time']


class Comment(models.Model):
    content = models.ForeignKey(
        MediaContent,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Tegishli kontent"
    )
    name = models.CharField('Ismingiz', max_length=100)
    text = models.TextField('Fikr matni')
    created_at = models.DateTimeField('Yozilgan vaqti', auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.content.title[:20]}"

    class Meta:
        verbose_name = "Fikr"
        verbose_name_plural = "Fikrlar"
        ordering = ['-created_at']


class ViewLog(models.Model):
    content = models.ForeignKey(MediaContent, on_delete=models.CASCADE, related_name='view_logs')
    ip_address = models.GenericIPAddressField("Foydalanuvchi IP manzili")
    viewed_at = models.DateTimeField("Ko‘rilgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "Ko‘rish logi"
        verbose_name_plural = "Ko‘rishlar logi"
        unique_together = ('content', 'ip_address')  # Har bir IP uchun faqat bitta kirish
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.ip_address} → {self.content.title}"
