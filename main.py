#!/usr/bin/env python

import os
import datetime
import re
import sys
from prettytable import PrettyTable

# Formato da data e hora
FORMATO_DATA = "%d-%m-%Y"
FORMATO_HORA = "%H:%M:%S"
LOG_TEMP_FILE = "log_temp.txt"

count_flag = "c"
if sys.platform == 'win32':
    count_flag = "n"


def execute_ping(url, count_number=2):
    ping_command = f"ping -{count_flag} {count_number} {url} > {LOG_TEMP_FILE}"
    os.system(ping_command)

def read_ping_result(log_file):
    with open(log_file, "r", encoding='utf8') as file:
        result = file.read()
    return result

def extract_ip(result):
    ip_address = ""
    for line in result.splitlines():
        if "PING" in line:
            match = re.search(r'\((.*?)\)', line)
            if match:
                ip_address = match.group(1)
                break
    return ip_address

def extract_avg_time(result):
    for line in result.splitlines():
        if "rtt min/avg/max/mdev" in line:
            stats_data = re.search(r'\/(\d+\.\d{3})\/', line)
            if stats_data:
                return stats_data.group(1)
    return "N/A"

def create_table(url, ip_address, time_avg):
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
    table.add_row([current_time.strftime(FORMATO_DATA),
                   current_time.strftime(FORMATO_HORA),
                   url,
                   ip_address,
                   "Online", 
                   "N/A", 
                   time_avg,
                   "N/A"])

    return table

def create_log(table):
    try:
        current_time = datetime.datetime.now()

        formatted_date = current_time.strftime(FORMATO_DATA)
        formatted_time = current_time.strftime(FORMATO_HORA)

        log_file_name = f"log_{formatted_date}_{formatted_time}.txt"
        print(f'Salvando em {log_file_name}...')
        with open(log_file_name, 'w', encoding='utf-8') as file:
            file.write(str(table))
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def ping_url(url):
    try:
        execute_ping(url)

        # Lê o resultado do ping
        result = read_ping_result(LOG_TEMP_FILE)
        print(result)

        # Extrai o IP e o avg time
        ip_address = extract_ip(result)
        avg = extract_avg_time(result)

        if ip_address:
            table = create_table(url, ip_address, avg)
            return table
        print("Não foi possível encontrar o IP na saída do ping.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if os.path.exists(LOG_TEMP_FILE):
            os.remove(LOG_TEMP_FILE)

def main():
    while True:
        print("-------------------------- Bem Vindo ----------------------")
        url = input("Digite uma URL (ou 'q' para sair): ")
        if url.lower() == 'q':
            print("Saindo ...")
            break
        print("-------------------------- PINGANDO -----------------------")
        output = ping_url(url)
        print(output)

        # Cria o log file
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
