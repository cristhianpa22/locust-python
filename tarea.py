import time
import os
import requests
import random
from celery.exceptions import SoftTimeLimitExceeded
from celery import Celery

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
celery_app = Celery('tareas', broker=broker_url, backend=broker_url)

def llamar_pasarela_bancaria():
    """Simula el comportamiento de un banco real muy inestable"""
    time.sleep(random.uniform(1, 4)) # Tarda entre 1 y 4 segundos
    if random.random() < 0.3: # 30% de probabilidad de fallar
        raise Exception("Error 504: El banco no responde")
    return "Pago Aprobado"

@celery_app.task(bind=True, soft_time_limit=5, time_limit=10)
def procesar_ticket(self, compra_id):
    try:
        llamar_pasarela_bancaria()
        return f"La compra {compra_id} ha sido procesada"
    except SoftTimeLimitExceeded:
        return {"status": "Fallo", "error": "Tiempo de espera excedido"}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2, max_retries=3)