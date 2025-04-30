import threading
import queue
import time
import random
import os
from datetime import datetime

# Escolha o modo de execução
MODO_SEQUENCIAL = True  # Defina como True para executar versão sequencial

# Fila de chamados
fila_chamados = queue.Queue()

# Definição do chamado
class Chamado:
    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao

# Utilitário para hora formatada
def hora():
    return datetime.now().strftime("%H:%M:%S")

# Função do técnico (thread)
def tecnico(id_tecnico):
    data_hoje = datetime.now().strftime("%d-%m-%Y")
    pasta_base = os.getcwd()
    pasta_logs = os.path.join(pasta_base, "logs")
    pasta_tecnico = os.path.join(pasta_logs, f"tecnico_{id_tecnico}")
    os.makedirs(pasta_tecnico, exist_ok=True)
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

# Função do cliente (thread)
def cliente(id_cliente):
    chamado = Chamado(id_cliente, f"Problema {id_cliente}")
    print(f"{hora()} - Cliente {id_cliente} criou um chamado.")
    fila_chamados.put(chamado)
    time.sleep(random.uniform(0.1, 0.5))

# Versão sequencial
def atendimento_sequencial(chamados):
    print("\n--- INÍCIO DO ATENDIMENTO SEQUENCIAL ---\n")
    for chamado in chamados:
        print(f"{hora()} - Técnico único atendendo chamado {chamado.id}: {chamado.descricao}")
        tempo = random.randint(1, 3)
        time.sleep(tempo)
        print(f"{hora()} - Chamado {chamado.id} finalizado em {tempo}s")
    print("\n--- FIM DO ATENDIMENTO SEQUENCIAL ---\n")

# Execução principal
if __name__ == "__main__":
    start_time = time.time()

    if MODO_SEQUENCIAL:
        chamados_seq = [Chamado(i+1, f"Problema {i+1}") for i in range(10)]
        atendimento_sequencial(chamados_seq)
    else:
        # Criar técnicos
        NUM_TECNICOS = 3
        tecnicos = []
        for i in range(NUM_TECNICOS):
            t = threading.Thread(target=tecnico, args=(i+1,))
            t.start()
            tecnicos.append(t)

        # Criar clientes (threads)
        NUM_CLIENTES = 10
        clientes = []
        for i in range(NUM_CLIENTES):
            c = threading.Thread(target=cliente, args=(i+1,))
            c.start()
            clientes.append(c)

        for c in clientes:
            c.join()

        # Esperar fila ser esvaziada
        fila_chamados.join()

        # Sinalizar término aos técnicos
        for _ in range(NUM_TECNICOS):
            fila_chamados.put(None)

        # Esperar técnicos terminarem
        for t in tecnicos:
            t.join()

        print("Central encerrada.")

    end_time = time.time()
    tempo_total = end_time - start_time
    print(f"\nTempo total de execução: {tempo_total:.2f}s")
