import datetime
from tienda_app.domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    def pagar(self, monto: float) -> bool:
        archivo_log = "pagos_locales_TOMAS_VERA_FRANCO.log"
        with open(archivo_log, "a") as f:
            f.write(f"[{datetime.datetime.now()}] Transaccion exitosa por: ${monto}\n")
        return True