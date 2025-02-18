from django.db import models
from django.utils.translation import gettext_lazy as _


class InterestFrequencyChoices(models.TextChoices):
    ANNUAL = "Annual", _("Annual")
    SEMI_ANNUAL = "Semi-annual", _("Semi-annual")
    QUARTERLY = "Quarterly", _("Quarterly")
    MONTHLY = "Monthly", _("Monthly")
