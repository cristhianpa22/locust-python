from locust import HttpUser, task, between
import random

class UserAsincrono(HttpUser):
    wait_time = between(1, 3)
    @task(3)
    def comprar_ticket(self):
        payload = {"compra_id": str(random.randint(1000, 9999))}
        with self.client.post("/comprar-ticket", json=payload, catch_response=True) as response:
            if response.status_code == 202:
                response.success()
            else:
                response.failure(f"Error al comprar ticket: {response.text}")
    @task(1)
    def estado_compra(self):
        payload = {"compra_id": str(random.randint(1000, 9999))}
        response = self.client.post("/comprar-ticket", json=payload)
        if response.status_code == 202:
            datos = response.json()
            task_id = datos.get("task_id")
            if task_id:
                self.client.get(f"/estado-compra/{task_id}", name="/estado_compra/[id]")