# Central de Atendimento Multithread

Este projeto é uma simulação de uma central de atendimento onde **técnicos (threads)** atendem chamados de forma concorrente, utilizando **Python** e **fila sincronizada (`queue.Queue`)** para controle de tarefas.

---

## 💡 Objetivo

Demonstrar o uso de **multithreading** em Python em um ambiente simulado de atendimento técnico, com:

- Processamento simultâneo de chamados
- Fila segura entre threads
- Geração de logs individuais para cada técnico
- Organização de arquivos por técnico e por data

---

## 📁 Estrutura do Projeto

```
├── central_atendimento.py     # Arquivo principal do projeto
└── logs/                      # Subpasta gerada automaticamente com os logs
    ├── tecnico_1/
    │   └── log_DD-MM-YYYY.txt
    ├── tecnico_2/
    │   └── log_DD-MM-YYYY.txt
    └── tecnico_3/
        └── log_DD-MM-YYYY.txt
```

Cada técnico possui uma pasta própria dentro da pasta `logs/`, e nela são criados os arquivos de log do atendimento com base na **data atual**.

---

## ▶️ Como Executar

1. Certifique-se de ter o **Python 3 instalado**.
2. Salve o código no arquivo `central_atendimento.py`.
3. Execute o script:
   ```bash
   python central_atendimento.py
   ```

Os logs dos atendimentos serão salvos automaticamente na subpasta `logs/`.

---

## 📌 Tecnologias utilizadas

- Python 3
- Módulo `threading`
- Módulo `queue`
- Manipulação de arquivos e diretórios com `os`
- `datetime` para data e hora dos logs

---

## ✍️ Autores
- João Pedro Labussiere
- Leonardo Vasconcellos
- Marcell Dactes Andrade
- Pedro Vinícius Mota

Desenvolvido como parte da disciplina **Programação em plataformas de alto desempenho**.

---
