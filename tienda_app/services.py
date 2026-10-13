from .models import Libro, Inventario
from .domain.builders import OrdenBuilder

class CompraRapidaService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago

    def procesar(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        inv = Inventario.objects.get(libro=libro)
        
        if inv.cantidad <= 0:
            raise ValueError("No hay existencias.")
            
        total = float(libro.precio) * 1.19
        
        if self.procesador_pago.pagar(total):
            inv.cantidad -= 1
            inv.save()
            return total
        return None

class CompraService:
    def __init__(self, procesador_pago):
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        # Uso del Builder: Semantica clara y validacion interna
        orden = (self.builder
                 .con_usuario(usuario)
                 .con_productos(lista_productos)
                 .para_envio(direccion)
                 .build())
                 
        # Uso del Factory (inyectado): Cambio de comportamiento sin cambio de codigo
        if self.procesador.pagar(orden.total):
            # Requisito Taller 3: Descontar inventario
            for libro in lista_productos:
                inv = Inventario.objects.get(libro=libro)
                inv.cantidad -= 1
                inv.save()
            return f"Orden {orden.id} procesada exitosamente."
            
        orden.delete()
        raise Exception("Error en la pasarela de pagos.")