#!/usr/bin/env python
'''
Nome: Lucas Garcia Marques
Disciplina: Automação e Programabilidade em Redes
Professor(a): Eduarda Rodrigues Monteiro

Programa que verifica se um determinado site está operacional usando a ferramenta Ping,
imprimindo os resultados na tela do usuário e salvando em um arquivo de log. 
O programa está funcionando, atualmente, somente em ambiente Linux, 
porém deverá ser executado em Windows futuramente.

'''
import datetime
import os
import re
import platform
from prettytable import PrettyTable

# Formato da data e hora
DATA_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H-%M-%S"

# Define o nome do arquivo de log temporário
LOG_TEMP_FILE = "log_temp.txt"

def execute_ping(url, count_number=2): # Trocar para 4
    '''Executa o ping'''
    system = platform.system()
    if system == 'Windows':
        count_flag = 'n'
    else:
        count_flag = 'c'

    ping_command = f"ping -{count_flag} {count_number} {url} > {LOG_TEMP_FILE}"
    os.system(ping_command)

def read_ping_result(log_file):
    '''Lê o arquivo de log temporário'''
    try:
        with open(log_file, "r", encoding='utf-8') as file:
            result = file.read()
        return result
    except OSError:
        return "Arquivo não encontrado."

def extract_ip(result):
    '''Extrai o endereço IP'''
    ip_address = ""
    for line in result.splitlines():
        if "PING" in line:
            match = re.search(r'\((.*?)\)', line)
            if match:
                ip_address = match.group(1)
                break
    return ip_address

def extract_avg_time(result):
    '''Extrai o Tempo Médio(avg)'''
    for line in result.splitlines():
        if "rtt min/avg/max/mdev" in line:
            match = re.search(r'\/(\d+\.\d{3})\/', line)
            if match:
                return match.group(1)
    return "N/A"

def create_table(url, ip_address, time_avg):
    '''Cria a tabela do log'''
    current_time = datetime.datetime.now()
    table = PrettyTable()
    table.field_names = [
                         "Data", 
                         "Horário", 
                         "URL", 
                         "IP", 
                         "Status", 
                         "TTL", 
                         "Time (média)", 
                         "Pacotes Perdidos",
                         ]
    table.add_row([current_time.strftime(DATA_FORMAT),
                   current_time.strftime(TIME_FORMAT),
                   url,
                   ip_address,
                   "Online", 
                   "N/A", 
                   time_avg,
                   "N/A"])

    return table

def create_log(table):
    '''Cria o arquivo de log com a tabela'''
    try:
        current_time = datetime.datetime.now()

        formatted_date = current_time.strftime(DATA_FORMAT)
        formatted_time = current_time.strftime(TIME_FORMAT)

        log_file_name = f"log_{formatted_date}_{formatted_time}.txt"
        print(f'Salvando em {log_file_name}...')
        with open(log_file_name, 'w', encoding='utf-8') as file:
            file.write(str(table))
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def ping_url(url):
    '''Executa as principais funções'''
    try:
        execute_ping(url)

        # Lê o resultado do ping
        result = read_ping_result(LOG_TEMP_FILE)
        print(result)

        # Extrai o endereço IP e o Tempo Médio (avg time)
        ip_address = extract_ip(result)
        avg = extract_avg_time(result)

        if ip_address:
            table = create_table(url, ip_address, avg)
            return table
        return None

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        # Remove o arquivo temporário
        if os.path.exists(LOG_TEMP_FILE):
            os.remove(LOG_TEMP_FILE)

def main():
    '''Função Principal'''
    while True:
        print("-------------------------- Bem Vindo ----------------------")
        url = input("Digite uma URL (ou 'q' para sair): ")
        if url.lower() == 'q':
            print("Saindo ...")
            break
        print("-------------------------- PINGANDO -----------------------")
        output = ping_url(url)
        if output is None:
            print("Não foi possível encontrar o IP na saída do ping.")
        else:
            print(output)
            create_log(output)

        while True:
            option = input("Deseja continuar? [S]im [N]ao: ")

            if option.upper() == 'S':
                break
            if option.upper() == 'N':
                print('#################### FIM DE PROGRAMA ####################')
                return
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVocê interrompeu usando o teclado!")
