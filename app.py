import time
import random
from tarea import procesar_ticket, celery_app
from flask import Flask, request, jsonify
app = Flask(__name__)



@app.route("/comprar-ticket", methods=["POST"])
def comprar_ticket():
    try:
        #Esto bloquea a Gunicorn y tumba la API bajo carga
        datos = request.get_json()
        compra_id = datos.get("compra_id", "000")
        tarea =  procesar_ticket.delay(compra_id)

        return jsonify({"status": "Exito", "mensaje": "Solicitud recibida", "tarea_id": tarea.id}), 202
    except Exception as e:
        return jsonify({"status": "Fallo", "error": str(e)}), 500
@app.route("/estado-compra/<task_id>", methods=["GET"])
def estado_compra(task_id):
    tarea = celery_app.AsyncResult(task_id)
    if tarea.state == 'PENDING':
        return jsonify({"status": "Pendiente", "mensaje": "La compra está en cola"}), 202
    elif tarea.state == 'SUCCESS':
        return jsonify({"status": "Exito", "mensaje": tarea.result}), 200
    elif tarea.state == 'FAILURE':
        return jsonify({"status": "Fallo", "mensaje": "El banco rechazo la tarjeta tras los tres reintentos", "error": str(tarea.result)}), 500