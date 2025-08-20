import multiprocessing
import os
import time
import random
import logging
from os import path

# Configuração do logger para registrar as saídas em um arquivo.
# Isso simula o consumidor processando e armazenando os dados recebidos.
log_file = path.join(path.dirname(path.realpath(__file__)),"consumer_log.txt")
logging.basicConfig(
    filename='IPC_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='w'  # 'w' para sobrescrever o arquivo a cada execução
)
 
# Número de mensagens que o produtor irá gerar.
NUM_MESSAGES = 10

def producer(pipe_connection):
    
    # Processo Produtor.
    # Gera dados dinâmicos e os envia através do pipe para o consumidor.
    
    # Obtém o ID do processo para identificação clara nas mensagens.
    pid = os.getpid()
    print(f"[Produtor PID: {pid}] Iniciado. Enviando {NUM_MESSAGES} mensagens.")

    for i in range(NUM_MESSAGES):
        try:
            # Gera um dado variável (não repetitivo).
            random_number = random.randint(1, 1000)
            message = f"Mensagem {i+1} de {pid}: {random_number}"
            
            # Envia a mensagem pelo pipe.
            # Esta é a chamada "send" do modelo de troca de mensagens[cite: 329, 350].
            # Pode bloquear se o buffer do pipe estiver cheio[cite: 561].
            pipe_connection.send(message)
            print(f"[Produtor PID: {pid}] Enviou: '{message}'")
            logging.info(f"[Produtor PID: {pid}] Enviou: '{message}'")
            
            # Pausa por um tempo aleatório para simular um trabalho real.
            time.sleep(random.uniform(0.1, 0.5))

        except BrokenPipeError:
            # Trata o erro caso o consumidor encerre sua execução inesperadamente.
            print(f"[Produtor PID: {pid}] Erro: O canal (pipe) foi quebrado. O consumidor pode ter sido encerrado.")
            break

    # Após enviar todas as mensagens, envia um sinal de "FIM" (sentinela).
    # Isso informa ao consumidor que não há mais dados a serem lidos.
    pipe_connection.send("FIM")
    print(f"[Produtor PID: {pid}] Todas as mensagens enviadas. Encerrando.")
    pipe_connection.close()

def consumer(pipe_connection):
    """
    Processo Consumidor.
    Aguarda por dados do pipe, processa-os e registra a saída em um log.
    """
    pid = os.getpid()
    print(f"[Consumidor PID: {pid}] Iniciado. Aguardando mensagens...")

    
    while True:
        try:
            
            # O processo ficará no estado "Waiting"  até que um dado chegue.
            message = pipe_connection.recv()

            # Verifica se recebeu o sinal de finalização do produtor.
            if message == "FIM":
                print(f"[Consumidor PID: {pid}] Sinal de 'FIM' recebido. Encerrando.")
                logging.info("Sinal de 'FIM' recebido. Encerrando o consumidor.")
                break
            
            print(f"[Consumidor PID: {pid}] Recebeu: '{message}'")
            logging.info(f"[Consumidor PID: {pid}] Recebeu: '{message}'")
           
            # Extrai o número da mensagem para processá-lo.
            try:
                number_part = int(message.split(":")[-1].strip())
                result = "PAR" if number_part % 2 == 0 else "ÍMPAR"
                processed_message = f"Dado processado de '{message}' -> O número {number_part} é {result}."
            except (ValueError, IndexError):
                processed_message = f"Dado processado de '{message}' -> Não foi possível extrair um número."

            # Registra o resultado processado no arquivo de log.
            logging.info(processed_message)
            print(f"[Consumidor PID: {pid}] Processou e registrou a mensagem.")

        except EOFError:
            # Este erro ocorre se o produtor fechar a conexão sem enviar "FIM".
            # Garante que o consumidor não fique em um loop infinito.
            print(f"[Consumidor PID: {pid}] Erro: Fim do arquivo. O produtor encerrou a conexão inesperadamente.")
            logging.error("O produtor encerrou a conexão inesperadamente.")
            break

    pipe_connection.close()

if __name__ == "__main__":
    print("Iniciando o sistema Produtor-Consumidor com Pipes...")

    
    producer_pipe, consumer_pipe = multiprocessing.Pipe()

    # Cria os processos independentes, passando a respectiva ponta do pipe para cada um.
    process_producer = multiprocessing.Process(target=producer, args=(producer_pipe,))
    process_consumer = multiprocessing.Process(target=consumer, args=(consumer_pipe,))
    
    # Inicia a execução dos processos.
    # A partir daqui, o Sistema Operacional os escalona para usar a CPU.
    process_consumer.start()
    process_producer.start()

    # Aguarda o término de ambos os processos antes de continuar o script principal.
    process_producer.join()
    process_consumer.join()

    print("\nExecução concluída. Verifique o arquivo 'IPC_log.txt' para ver os resultados processados.")