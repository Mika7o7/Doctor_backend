from modeltranslation.translator import TranslationOptions, register

from .models import FAQ, Doctor, Opinion, Professions


@register(Professions)
class ProfessionsTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(Doctor)
class DoctorTranslationOptions(TranslationOptions):
    fields = ("description",)


@register(Opinion)
class OpinionTranslationOptions(TranslationOptions):
    fields = ("text", "name")


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ("answer", "question")
