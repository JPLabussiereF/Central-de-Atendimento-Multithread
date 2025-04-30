import threading
import queue
import time
import random
import os
from datetime import datetime
import matplotlib.pyplot as plt

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

# Medir tempo sequencial
def medir_tempo_sequencial():
    chamados_seq = [Chamado(i+1, f"Problema {i+1}") for i in range(10)]
    start = time.time()
    atendimento_sequencial(chamados_seq)
    return time.time() - start

# Medir tempo concorrente
def medir_tempo_concorrente():
    start = time.time()

    NUM_TECNICOS = 3
    tecnicos = []
    for i in range(NUM_TECNICOS):
        t = threading.Thread(target=tecnico, args=(i+1,))
        t.start()
        tecnicos.append(t)

    NUM_CLIENTES = 10
    clientes = []
    for i in range(NUM_CLIENTES):
        c = threading.Thread(target=cliente, args=(i+1,))
        c.start()
        clientes.append(c)

    for c in clientes:
        c.join()

    fila_chamados.join()

    for _ in range(NUM_TECNICOS):
        fila_chamados.put(None)

    for t in tecnicos:
        t.join()

    return time.time() - start

# Execução principal
if __name__ == "__main__":
    print("\nExecutando comparações de desempenho...\n")

    tempo_seq = medir_tempo_sequencial()
    print(f"Tempo sequencial: {tempo_seq:.2f}s\n")

    # Resetar fila
    fila_chamados = queue.Queue()

    tempo_conc = medir_tempo_concorrente()
    print(f"Tempo concorrente: {tempo_conc:.2f}s\n")

    # Gráfico comparativo
    modos = ['Sequencial', 'Concorrente']
    tempos = [tempo_seq, tempo_conc]

    plt.figure(figsize=(8, 5))
    plt.bar(modos, tempos, color=['gray', 'green'])
    plt.title('Comparação de Tempos de Execução')
    plt.ylabel('Tempo (s)')
    plt.savefig("grafico_comparativo.png")
    plt.show()

    print("Gráfico gerado: grafico_comparativo.png")
    