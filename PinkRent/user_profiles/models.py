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
    user = models.ForeignKey(get_user_model(), verbose_name=_("favorited by"), on_delete=models.CASCADE, related_name='favorited_users')
    favorite_user = models.ForeignKey(get_user_model(), verbose_name=_("favorite user"), on_delete=models.CASCADE, related_name='favorited_by_users')


    class Meta:
        verbose_name = _("favorite user")
        verbose_name_plural = _("favorite users")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("favorite_detail", kwargs={"pk": self.pk})

class UserProfileReview(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_("review_by"), on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, verbose_name=_("reviewed_profile"), on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("profile_review")
        verbose_name_plural = _("profile_reviews")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("profile_review_detail", kwargs={"pk": self.pk})
    