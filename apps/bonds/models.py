from decimal import Decimal

from apps.bonds.enums import InterestFrequencyChoices
from apps.bonds.validators import validate_isin, validate_maturity_date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Bond(models.Model):
    issuer = models.CharField(max_length=400, verbose_name=_("Issuer"))
    isin = models.CharField(max_length=12, unique=True, validators=[validate_isin], verbose_name=_("ISIN"))
    face_value = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=_("Face Value"))
    interest_rate = models.DecimalField(max_digits=7, decimal_places=4, verbose_name=_("Bond Rate"))
    date_added = models.DateField(verbose_name=_("Date Added"))
    maturity_date = models.DateField(verbose_name=_("Maturity Date"))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="bonds",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    interest_frequency = models.CharField(
        max_length=11,
        choices=InterestFrequencyChoices.choices,
        default=InterestFrequencyChoices.ANNUAL,
        verbose_name=_("Interest Frequency"),
    )

    class Meta:
        verbose_name = _("Bond")
        verbose_name_plural = _("Bonds")

    def __str__(self):
        return f"{self.isin} - {self.issuer}"

    def clean(self):
        super().clean()
        validate_maturity_date(self)

    """
    For compounding interest:
    return self.face_value * (1 + self.interest_rate / 100) ** years_to_maturity
    Which we don't want here probably, since we are dealing with bonds.
    """

    def calculate_future_bond_value(self):
        delta = relativedelta(self.maturity_date, self.date_added)
        years_to_maturity = Decimal(delta.years + delta.months / 12 + delta.days / 365)
        return self.face_value * (1 + self.interest_rate / 100 * years_to_maturity)
