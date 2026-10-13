from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import OrdenInputSerializer
from tienda_app.services import CompraService
from tienda_app.infra.factories import PaymentFactory
from tienda_app.models import Libro

class CompraAPIView(APIView):
    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        datos = serializer.validated_data
        try:
            # Obtenemos el libro y el usuario real
            libro = Libro.objects.get(id=datos['libro_id'])
            usuario_obj, _ = User.objects.get_or_create(username="tomas_vera")

            gateway = PaymentFactory.get_processor()
            servicio = CompraService(gateway)
            
            # Reutilizamos la logica del Taller 2
            resultado = servicio.ejecutar_proceso_compra(
                usuario=usuario_obj, 
                lista_productos=[libro], 
                direccion=datos['direccion_envio']
            )
            
            return Response({
                "estado": "exito",
                "mensaje": resultado
            }, status=status.HTTP_201_CREATED)
            
        except Libro.DoesNotExist:
            return Response({"error": "Libro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"error": "Error interno: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)