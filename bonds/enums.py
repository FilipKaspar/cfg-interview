from django.db import models


class InterestFrequencyChoices(models.TextChoices):
    ANNUAL = "Annual"
    SEMI_ANNUAL = "Semi-annual"
    QUARTERLY = "Quarterly"
    MONTHLY = "Monthly"
