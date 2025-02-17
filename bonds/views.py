from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Bond
from .serializers import BondSerializer


class BondViewSet(viewsets.ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bond.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PortfolioAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO
        pass
