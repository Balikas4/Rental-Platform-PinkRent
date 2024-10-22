from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _ , get_language
from PIL import Image
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    slug = models.SlugField(_("slug"), max_length=255, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)


    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")

    def __str__(self):
        return self.name

class Listing(models.Model):
    QUALITY_CHOICES = {
        'en': {
            'newwithtags': 'New with tags',
            'newwithouttags': 'New without tags',
            'great': 'Great',
            'good': 'Good',
            'worn': 'Worn',
        },
        'lt': {
            'newwithtags': 'Nauja su etiketėmis',
            'newwithouttags': 'Nauja be etikečių',
            'great': 'Puiki',
            'good': 'Gera',
            'worn': 'Vidutinė',
        },
    }

    COLOR_CHOICES = {
        'en': {
            'black': 'Black',
            'white': 'White',
            'gray': 'Grey',
            'silver': 'Silver',
            'gold': 'Golden',
            'beige': 'Beige',
            'brown': 'Brown',
            'dark_blue': 'Dark Blue',
            'blue': 'Blue',
            'light_blue': 'Light Blue',
            'cyan': 'Blue',
            'green': 'Green',
            'khaki': 'Khaki',
            'yellow': 'Yellow',
            'mustard': 'Mustard',
            'orange': 'Orange',
            'coral': 'Coral',
            'red': 'Red',
            'burgundy': 'Burgundy',
            'light_pink': 'Light Pink',
            'pink': 'Pink',
            'bright_pink': 'Bright Pink',
            'purple': 'Purple',
            'lavender': 'Lavender',
            'mint': 'Mint',
            'turquoise': 'Turquoise',
            'maroon': 'Burgundy',
            'peach': 'Peach',
            'ivory': 'Ivory',
            'champagne': 'Champagne',
            'rose_gold': 'Rose Gold',
            'bronze': 'Bronze',
            'blush': 'Pink',
            'cobalt_blue': 'Cobalt Blue',
            'emerald': 'Emerald',
            'magenta': 'Purple',
            'fuchsia': 'Fuchsia',
        },
        'lt': {
            'black': 'Juoda',
            'white': 'Balta',
            'gray': 'Pilka',
            'silver': 'Sidabrinė',
            'gold': 'Auksinė',
            'beige': 'Smėlio',
            'brown': 'Ruda',
            'dark_blue': 'Tamsiai mėlyna',
            'blue': 'Mėlyna',
            'light_blue': 'Šviesiai mėlyna',
            'cyan': 'Žydra',
            'green': 'Žalia',
            'khaki': 'Chaki',
            'yellow': 'Geltona',
            'mustard': 'Garstyčių',
            'orange': 'Oranžinė',
            'coral': 'Koralinė',
            'red': 'Raudona',
            'burgundy': 'Bordo',
            'light_pink': 'Šviesiai rožinė',
            'pink': 'Rožinė',
            'bright_pink': 'Ryškiai rožinė',
            'purple': 'Violetinė',
            'lavender': 'Levandų',
            'mint': 'Mėtų',
            'turquoise': 'Turkio',
            'maroon': 'Bordo',
            'peach': 'Persikinė',
            'ivory': 'Dramblio kaulo',
            'champagne': 'Šampaninė',
            'rose_gold': 'Rožinis auksas',
            'bronze': 'Bronzinė',
            'blush': 'Rožinė',
            'cobalt_blue': 'Kobalto mėlyna',
            'emerald': 'Smaragdinė',
            'magenta': 'Purpurinė',
            'fuchsia': 'Fuksija',
        },
    }
    
    SIZE_CHOICES = [
        ('XXXS / 30 / 2', 'XXXS / 30 / 2'), ('XXS / 32 / 4', 'XXS / 32 / 4'), ('XS / 34 / 6', 'XS / 34 / 6'),
        ('S / 36 / 8', 'S / 36 / 8'), ('M / 38 / 10', 'M / 38 / 10'), ('L / 40 / 12', 'L / 40 / 12'),
        ('XL / 42 / 14', 'XL / 42 / 14'), ('XXL / 44 / 16', 'XXL / 44 / 16'), ('XXXL / 46 / 18', 'XXXL / 46 / 18'),
        ('4XL / 48 / 20', '4XL / 48 / 20'), ('5XL / 50 / 22', '5XL / 50 / 22'), ('6XL / 52 / 24', '6XL / 52 / 24'),
        ('7XL / 54 / 26', '7XL / 54 / 26'), ('8XL / 56 / 28', '8XL / 56 / 28'), ('35', '35'), 
        ('35.5', '35.5'), ('36', '36'), ('36.5', '36.5'), ('37', '37'), ('37.5', '37.5'), 
        ('38', '38'), ('38.5', '38.5'), ('39', '39'), ('39.5', '39.5'), ('40', '40'), 
        ('40.5', '40.5'), ('41', '41'), ('41.5', '41.5'), ('42', '42'), ('42.5', '42.5'), 
        ('43', '43'), ('43.5', '43.5'), ('44', '44'), ('44.5', '44.5'), ('45', '45'), 
        ('45.5', '45.5'), ('46', '46'), ('46.5', '46.5'), ('47', '47'), ('47.5', '47.5'), 
        ('48', '48'), ('48.5', '48.5'), ('One Size', 'One Size'), ('Other', 'Other')
    ]

    name = models.CharField(_("name"), max_length=100, db_index = True)
    description = models.TextField(_("description"), blank=True, max_length = 100000)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(_("sell_price"), default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index = True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index = True)
    is_available = models.BooleanField(_("is available"), db_index = True, default = False)
    is_for_sale = models.BooleanField(_("is for sale"), db_index = True, default = False)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings')
    picture = models.ImageField(upload_to='listing_pictures/', blank=True, null=True)
    picture_1 = models.ImageField(upload_to='listing_pictures/', blank=True, null=True)
    picture_2 = models.ImageField(upload_to='listing_pictures/', blank=True, null=True)
    picture_3 = models.ImageField(upload_to='listing_pictures/', blank=True, null=True)
    size = models.CharField(_("size"), max_length=20, choices=SIZE_CHOICES, db_index = True)
    quality = models.CharField(max_length=20, choices=[(key, key) for key in QUALITY_CHOICES['en'].keys()], default='good')
    color = models.CharField(_("color"), max_length=20, choices=COLOR_CHOICES, default=None, db_index = True)
    value = models.DecimalField(_("value"), max_digits=10, decimal_places=2)
    owner = models.ForeignKey(
        get_user_model(), 
        verbose_name=_("owner"), 
        on_delete=models.CASCADE,
        related_name = 'listings',
        )
    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='listing',
    )
    tags = models.ManyToManyField(Tag, related_name='listings', blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        max_size = (800, 1200)
        if self.picture:
            self._resize_image(self.picture, max_size)
        if self.picture_1:
            self._resize_image(self.picture_1, max_size)
        if self.picture_2:
            self._resize_image(self.picture_2, max_size)
        if self.picture_3:
            self._resize_image(self.picture_3, max_size)

    def _resize_image(self, image_field, max_size):
        image = Image.open(image_field.path)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size)
            image.save(image_field.path)

    class Meta:
        verbose_name = _("listing")
        verbose_name_plural = _("listings")
        ordering = ['is_available', 'created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("listing_detail", kwargs={"pk": self.pk})

    def get_color_choices(self):
        language = get_language()  # Get the current language code
        return [(key, value) for key, value in self.COLOR_CHOICES.get(language, self.COLOR_CHOICES['en']).items()]
    
    def get_color_display(self):
        language = get_language()  # Get the current language code
        # Fetch the correct color display based on the current language
        color_choices = self.COLOR_CHOICES.get(language, self.COLOR_CHOICES['en'])
        return color_choices.get(self.color, self.color)  # Fallback to the key itself if not found

    def get_quality_choices(self):
        language = get_language()  # Get the current language code
        return [(key, value) for key, value in self.QUALITY_CHOICES.get(language, self.QUALITY_CHOICES['en']).items()]

    def get_quality_display(self):
        language = get_language()  # Get the current language code
        # Fetch the correct quality display based on the current language
        quality_choices = self.QUALITY_CHOICES.get(language, self.QUALITY_CHOICES['en'])
        return quality_choices.get(self.quality, self.quality)  # Fallback to the key itself if not found


class FavoriteListing(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_("favorited_by"), on_delete=models.CASCADE, related_name='favorite_listings')
    favorite_listing = models.ForeignKey(Listing, verbose_name=_("favorite listing"), on_delete=models.CASCADE, related_name='favorite_listings')
    

    class Meta:
        verbose_name = _("favorite listing")
        verbose_name_plural = _("favorite listings")

    def __str__(self):
        return f"{self.user.username} favorited {self.favorite_listing.name}"

    def get_absolute_url(self):
        return reverse("favorite_listing_detail", kwargs={"pk": self.pk})

class ListingReview(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_("review_by"), on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, verbose_name=_("reviewed_listing"), on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("listing_review")
        verbose_name_plural = _("listing_reviews")

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("listing_review_detail", kwargs={"pk": self.pk})

class Feedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.rating}"

class WaitlistEntry(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email