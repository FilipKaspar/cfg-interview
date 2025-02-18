from apps.bonds.models import Bond
from apps.bonds.serializers import BondSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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
        bonds = Bond.objects.filter(user=request.user)

        average_interest_rate = sum(bond.interest_rate for bond in bonds) / len(bonds) if bonds else 0
        nearest_maturity_date = min(bond.maturity_date for bond in bonds) if bonds else None
        total_portfolio_value = sum(bond.face_value for bond in bonds)
        total_future_portfolio_value = sum(bond.calculate_future_bond_value() for bond in bonds)

        response_data = {
            "average_interest_rate": average_interest_rate,
            "nearest_maturity": nearest_maturity_date,
            "total_portfolio_value": total_portfolio_value,
            "total_future_portfolio_value": total_future_portfolio_value,
        }

        return Response(response_data)
