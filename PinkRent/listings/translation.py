from modeltranslation.translator import translator, TranslationOptions
from .models import Tag

class TagTranslationOptions(TranslationOptions):
    fields = ('name',)  # Specify the fields you want to translate

# Register the model for translation
translator.register(Tag, TagTranslationOptions)
