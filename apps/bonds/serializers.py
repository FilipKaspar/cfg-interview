from apps.bonds.models import Bond
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = "__all__"
        read_only_fields = ("user",)

    """
    Only security measure in case user field would somehow get passed to serializer.
    """

    def validate_user(self, value):
        if self.instance and value != self.instance.user:
            raise serializers.ValidationError(_("Nelze změnit vlastníka dluhopisu."))
        return value
