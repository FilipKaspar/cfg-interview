from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BondsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bonds"
    verbose_name = _("Bonds")
