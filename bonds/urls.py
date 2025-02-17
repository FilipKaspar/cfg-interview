from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BondViewSet, PortfolioAnalysisView

router = DefaultRouter()
router.register(r"bonds", BondViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("portfolio-analysis/", PortfolioAnalysisView.as_view()),
]
