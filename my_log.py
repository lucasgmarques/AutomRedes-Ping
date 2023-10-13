#!/usr/bin/env python3

import datetime
from prettytable import PrettyTable

# Formato da data e hora do nome do log
DATA_FORMAT = "%d-%m-%Y"
TIME_FORMAT = "%H-%M-%S"
# Formato da data e hora da tabela
TABLE_DATA_FORMAT = "%d/%m/%Y"
TABLE_TIME_FORMAT = "%H:%M:%S"

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
