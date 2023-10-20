#!/usr/bin/env python3

import os
import re
import my_log

# Define o nome do arquivo de log temporário
LOG_TEMP_FILE = "log_temp.txt"

def execute_ping(url, count_number=4, timeout=None):
    '''Executa a ferramenta ping. '''
    try:
        ping_command = f"ping -c {count_number} -W {timeout} {url} > {LOG_TEMP_FILE}"
        os.system(ping_command)
    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def check_status(result):
    '''Verifica se o host está online. '''
    try:
        for line in result.splitlines():
            if "packets transmitted" in line:
                if "100% packet loss" in line:
                    return "Offline"
                return "Online"
        return "N/A"
    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def get_info(result, pattern):
    '''Extrair as informações baseado nas expressões regulares'''
    try:
        for line in result.splitlines():
            match = re.search(pattern, line)
            if match:
                return match.group(1)
        return "N/A"
    except Exception as error:
        print(f"Ocorreu um erro: {error}")


def get_packet_loss(result):
    '''Extrai o packet loss do resultado'''
    return get_info(result, r'(\d+)%')


def get_ttl(result):
    '''Extrai o TTL do output'''
    return get_info(result, r'ttl=(\d+)')


def get_ip(result):
    '''Extrai o endereço IP do resultado'''
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

        
def get_avg_time(result):
    '''Extrai o Tempo Médio(avg) do resultado'''
    try:
        for line in result.splitlines():
            if "rtt min/avg/max/mdev" in line:
                match = re.search(r'\/(\d+\.\d{3})\/', line)
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


def ping_url(url):
    '''Executa as principais funções do ping e cria uma tabela com os resultados.'''
    try:
        # Modificar o timeout se preciso
        execute_ping(url, timeout=1)

        # Lê o resultado do ping
        result = read_ping_result(LOG_TEMP_FILE)
        print(result)

        # Extrai as informações necessárias
        ip_address = get_ip(result)
        avg = get_avg_time(result)
        status = check_status(result)
        ttl = get_ttl(result)
        packet_loss = get_packet_loss(result)

        if ip_address:
            table = my_log.create_table(url, ip_address, status, ttl, avg, packet_loss)
            return table
        return None
    except Exception as error:
        print(f"Ocorreu um erro: {error}")
    finally:
        if os.path.exists(LOG_TEMP_FILE):
            os.remove(LOG_TEMP_FILE)
