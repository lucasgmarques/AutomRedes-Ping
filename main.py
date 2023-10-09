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

# Formato da data e hora do nome do log
DATA_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H-%M-%S"
# Formato da data e hora da tabela
TABLE_DATA_FORMAT = "%d/%m/%Y"
TABLE_TIME_FORMAT = "%H:%M:%S"
# Define o nome do arquivo de log temporário
LOG_TEMP_FILE = "log_temp.txt"

def execute_ping(url, count_number=2, timeout=None): # Trocar para 4
    '''Executa a ferramenta ping. '''
    try:
        system = platform.system()
        if system == 'Windows':
            count_flag = 'n'
        else:
            count_flag = 'c'

        ping_command = f"ping -{count_flag} {count_number} -W {timeout} {url} > {LOG_TEMP_FILE}"
        os.system(ping_command)
    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def check_status(result):
    '''Verifica se o host está online.

    Returns:
        Online(str): != 100% de packet loss
        Offline(str): == 100% de packet loss
        N/A: Valor padrão

    '''
    try:
        for line in result.splitlines():
            if "packets transmitted" in line:
                if "100% packet loss" in line:
                    return "Offline"
                return "Online"
        return "N/A"
    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def extract_packet_loss(result):
    '''Extrai o packet loss do output'''
    try:
        for line in result.splitlines():
            if "packet loss" in line:
                match = re.search(r'(\d+)%', line)
                if match:
                    return match.group(1)
        return "N/A"
    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def extract_ttl(result):
    '''Extrai o TTL do output'''
    try:
        for line in result.splitlines():
            if "ttl=" in line:
                match = re.search(r'ttl=(\d+)', line)
                if match:
                    return match.group(1)
        return "N/A"
    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def read_ping_result(log_file):
    '''Lê o arquivo de log temporário'''
    try:
        with open(log_file, "r", encoding='utf-8') as file:
            result = file.read()
        return result
    except OSError:
        return "Arquivo não encontrado."


def extract_ip(result):
    '''Extrai o endereço IP do output'''
    try:
        ip_address = ""
        for line in result.splitlines():
            if "PING" in line:
                match = re.search(r'\((.*?)\)', line)
                if match:
                    ip_address = match.group(1)
                    break
        return ip_address
    except Exception as error:
        print(f"Ocorreu um erro: {error}")
        

def extract_avg_time(result):
    '''Extrai o Tempo Médio(avg) do output'''
    try:
        for line in result.splitlines():
            if "rtt min/avg/max/mdev" in line:
                match = re.search(r'\/(\d+\.\d{3})\/', line)
                if match:
                    return match.group(1)
        return "N/A"
    except Exception as error:
        print(f"Ocorreu um erro: {error}")

def create_table(url, ip_address, status, ttl, time_avg, packet_loss):
    '''Cria a tabela do log'''
    try:
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
        table.add_row([current_time.strftime(TABLE_DATA_FORMAT),
                       current_time.strftime(TABLE_TIME_FORMAT),
                       url,
                       ip_address,
                       status,
                       ttl,
                       time_avg,
                       packet_loss + "%"])
        return table
    except Exception as error:
        print(f"Ocorreu um erro: {error}")


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

    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def ping_url(url):
    '''Executa as principais funções do ping e cria uma tabela com os resultados.'''
    try:
        # Modificar o timeout se preciso
        execute_ping(url, timeout=1)

        # Lê o resultado do ping
        result = read_ping_result(LOG_TEMP_FILE)
        print(result)

        # Extrai as informações necessárias
        ip_address = extract_ip(result)
        avg = extract_avg_time(result)
        status = check_status(result)
        ttl = extract_ttl(result)
        packet_loss = extract_packet_loss(result)

        if ip_address:
            table = create_table(url, ip_address, status, ttl, avg, packet_loss)
            return table
        return None
    except Exception as error:
        print(f"Ocorreu um erro: {error}")
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
            #print("Saindo ...")
            print('#################### FIM DE PROGRAMA ####################')
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
