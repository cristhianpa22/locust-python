from locust import HttpUser, task, between


class UserNavegador(HttpUser):
    wait_time = between(1, 2)
    @task(1)
    def navegarCarrito(self):
        self.client.get("/carrito")

class UserComprador(HttpUser):
    wait_time = between(1, 2)
    @task(1)
    def comprar(self):
        self.client.post("/comprar")