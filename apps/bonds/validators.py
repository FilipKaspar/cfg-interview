import requests
from django.core.exceptions import ValidationError


def validate_isin(isin):
    response = requests.get(f"https://www.cdcp.cz/isbpublicjson/api/VydaneISINy?isin={isin}", timeout=5)
    if response.status_code != 200 or not response.json().get("vydaneisiny"):
        raise ValidationError("ISIN is not valid or is not in the list!")


def validate_maturity_date(instance):
    if instance.date_added and instance.maturity_date <= instance.date_added:
        raise ValidationError("Maturity Date must be after Date Added!")
