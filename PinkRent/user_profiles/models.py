from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    picture = models.ImageField(_("picture"), upload_to='user_pictures/', blank=True, null=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse("user_detail_current", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.picture:
            image = Image.open(self.picture.path)
            if image.size[0] > 400 or image.size[1] > 300:
                image.resize((400, 300))
                image.save(self.picture.path)

class FavoriteUser(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_("favorited_by"), on_delete=models.CASCADE, related_name='favorited_by')
    favorite_user = models.ForeignKey(get_user_model(), verbose_name=_("favorite user"), on_delete=models.CASCADE, related_name='favorite_user')

    class Meta:
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("favorite_detail", kwargs={"pk": self.pk})
