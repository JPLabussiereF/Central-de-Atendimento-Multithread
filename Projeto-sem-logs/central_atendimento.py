import threading
import queue
import time
import random
import logging

# Configurar o log
logging.basicConfig(
    filename='log_central.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

# Fila de chamados
fila_chamados = queue.Queue()

# Definição do chamado
class Chamado:
    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao

# Função do técnico
def tecnico(id_tecnico):
    while True:
        chamado = fila_chamados.get()
        if chamado is None:
            logging.info(f"Técnico {id_tecnico} encerrando.")
            print(f"Técnico {id_tecnico} encerrando.")
            break

        log_inicio = f"Técnico {id_tecnico} atendendo chamado {chamado.id}: {chamado.descricao}"
        print(log_inicio)
        logging.info(log_inicio)

        tempo = random.randint(1, 3)
        time.sleep(tempo)  # Simula o atendimento

        log_fim = f"Técnico {id_tecnico} finalizou chamado {chamado.id} em {tempo}s"
        print(log_fim)
        logging.info(log_fim)

        fila_chamados.task_done()

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
    print(f"Chamado {chamado.id} criado.")
    logging.info(f"Chamado {chamado.id} criado.")
    time.sleep(random.uniform(0.1, 0.5))

# Esperar os chamados acabarem
fila_chamados.join()

# Enviar sinal de encerramento
for _ in range(NUM_TECNICOS):
    fila_chamados.put(None)

# Esperar técnicos finalizarem
for t in tecnicos:
    t.join()

print("Central encerrada.")
logging.info("Central encerrada.")
