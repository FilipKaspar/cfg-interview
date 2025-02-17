import requests
from django.core.exceptions import ValidationError


def validate_isin(isin):
    response = requests.get(
        f"https://www.cdcp.cz/isbpublicjson/api/VydaneISINy?isin={isin}", timeout=5
    )
    if response.status_code != 200 or not response.json().get("vydaneisiny"):
        raise ValidationError("ISIN není platný nebo není v seznamu cenných papírů!")
