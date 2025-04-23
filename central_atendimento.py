import threading
import queue
import time
import random
import os
from datetime import datetime

# Fila de chamados
fila_chamados = queue.Queue()

# Definição do chamado
class Chamado:
    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao

# Função do técnico com logs organizados em logs/tecnico_X/
def tecnico(id_tecnico):
    data_hoje = datetime.now().strftime("%d-%m-%Y")

    # Caminho da pasta base (onde está o script)
    pasta_base = os.getcwd()
    pasta_logs = os.path.join(pasta_base, "logs")
    pasta_tecnico = os.path.join(pasta_logs, f"tecnico_{id_tecnico}")

    os.makedirs(pasta_tecnico, exist_ok=True)  # Cria todas as pastas se não existirem

    caminho_log = os.path.join(pasta_tecnico, f"log_{data_hoje}.txt")

    with open(caminho_log, "a") as log_file:
        while True:
            chamado = fila_chamados.get()
            if chamado is None:
                mensagem = f"{hora()} - Técnico {id_tecnico} encerrando.\n"
                print(mensagem.strip())
                log_file.write(mensagem)
                break

            msg_inicio = f"{hora()} - Técnico {id_tecnico} atendendo chamado {chamado.id}: {chamado.descricao}\n"
            print(msg_inicio.strip())
            log_file.write(msg_inicio)

            tempo = random.randint(1, 3)
            time.sleep(tempo)

            msg_fim = f"{hora()} - Técnico {id_tecnico} finalizou chamado {chamado.id} em {tempo}s\n"
            print(msg_fim.strip())
            log_file.write(msg_fim)

            fila_chamados.task_done()

# Utilitário para hora formatada
def hora():
    return datetime.now().strftime("%H:%M:%S")

# Criar técnicos
NUM_TECNICOS = 3
tecnicos = []
for i in range(NUM_TECNICOS):
    t = threading.Thread(target=tecnico, args=(i+1,))
    t.start()
    tecnicos.append(t)

# Criar chamados
for i in range(10):
    chamado = Chamado(i+1, f"Problema {i+1}")
    fila_chamados.put(chamado)
    print(f"{hora()} - Chamado {chamado.id} criado.")
    time.sleep(random.uniform(0.1, 0.5))

# Aguardar fila
fila_chamados.join()

# Enviar sinal de parada
for _ in range(NUM_TECNICOS):
    fila_chamados.put(None)

# Esperar todos finalizarem
for t in tecnicos:
    t.join()

print("Central encerrada.")