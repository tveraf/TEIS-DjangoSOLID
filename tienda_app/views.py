from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User  # IMPORTANTE: Importamos el modelo User
from .models import Libro
from .services import CompraService
from tienda_app.infra.factories import PaymentFactory

class CompraView(View):
    def setup_service(self):
        # AHORA: Delegacion total a la Fabrica
        gateway = PaymentFactory.get_processor()
        return CompraService(gateway)

    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        return render(request, 'tienda_app/compra_rapida.html', {'libro': libro, 'total': float(libro.precio) * 1.19})

    def post(self, request, libro_id):
        try:
            libro = get_object_or_404(Libro, id=libro_id)
            servicio = self.setup_service()
            
            # Buscamos o creamos un usuario real de Django en la base de datos
            usuario_obj, creado = User.objects.get_or_create(username="tomas_vera")
            
            # Inyectamos el objeto usuario real al Builder
            mensaje = servicio.ejecutar_proceso_compra(usuario_obj, [libro], "Universidad EAFIT")
            
            return HttpResponse(mensaje)
        except Exception as e:
            return HttpResponse(str(e), status=400)