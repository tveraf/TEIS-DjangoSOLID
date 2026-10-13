from django.urls import path
from .views import CompraView
from .api.views import CompraAPIView

urlpatterns = [
    path('compra/<int:libro_id>/', CompraView.as_view(), name='compra'),
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]