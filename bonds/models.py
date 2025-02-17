from django.contrib.auth.models import User
from django.db import models

from bonds.enums import InterestFrequencyChoices
from bonds.validators import validate_isin


class Bond(models.Model):
    issuer = models.CharField(max_length=400)
    isin = models.CharField(max_length=12, unique=True, validators=[validate_isin])
    face_value = models.DecimalField(max_digits=14, decimal_places=4)
    bond_rate = models.DecimalField(max_digits=7, decimal_places=4)
    date_bought = models.DateField()
    maturity_date = models.DateField()
    user = models.ForeignKey(
        User, related_name="bonds", on_delete=models.CASCADE, null=True
    )
    interest_frequency = models.CharField(
        max_length=11,
        choices=InterestFrequencyChoices.choices,
        default=InterestFrequencyChoices.ANNUAL,
    )

    def __str__(self):
        return f"{self.isin} - {self.issuer}"
