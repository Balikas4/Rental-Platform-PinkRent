from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    profile_picture = models.ImageField(_("profile_picture"), upload_to='profile_pictures/', blank=True, null=True)
    first_name = models.TextField(_("First Name"))
    last_name =  models.TextField(_("Last name"))

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse("user_detail_current", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.profile_picture:
            image = Image.open(self.profile_picture.path)
            if image.size[0] > 400 or image.size[1] > 300:
                image.resize((400, 300))
                image.save(self.profile_picture.path)