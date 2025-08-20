# Entrega 1
Esse projeto teve como objetivo a implementaçao de um sistema Produtor-Consumidor, utilizando a linguagem Python, foi usado Pipes como o mecanismo de IPC (Comunicação entre Processos)

Esse Projeto faz parte da primeira entrega da matéria

Foram utilizadas:
- O Python 3 como a linguagem de programação
- O multiprocessing - para a criação de processos independentes
- Logging - Registro de eventos dentro de um arquivo log

# Estrutura do Código
# O producer(piper_connection):
- Vai gerar 10 mensagens aleatórias - Sendo definidas no código, podendo aumentar ou diminuir
- Envia as mensagens através do Pipe
- E no fim, registra no log cada mensagem enviada
# O consumer(piper_connection):
- Recebe as mensagens do Pipe
- Processa os dados, verificando se os números recebidos são PAR OU ÍMPAR
- Registra o resultado no arquivo de log
- Encerra quando recebe a mensagem especial "FIM"
# Main(if name == "Main"):
- Cria os dois processos independentes (Produtor e Consumidor)
- Inicia ambos e aguarda sua finalização
# Como Executar
1. Primeiro Clone o repositório
git clone https://github.com/Andrei-SantAnna/Sistemas-Distribuidos.git
2. Execute o código:
Python Entrega-1.py
Se estiver utilizando o Python3
Python3 Entrega-1.py
4. Verifique a saída no arquivo de log
cat IPC_log.txt
# Fluxo de Comunicação
A[Produtor] -- ENVIA MENSAGENS --> B[Pipe]

B -- REPASSA AS MENSAGENS -->C[Consumidor]

C -- Processa --> D[Log (IPC_log.txt)]

