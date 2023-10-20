
import sys
import my_ping
import my_log

def menu():
    while True:
        print("-------------------------- Bem Vindo ----------------------")
        url = input("Digite uma URL (ou 'q' para sair): ")
        if url.lower() == 'q':
            print("Saindo ...")
            break
        print("-------------------------- PINGANDO -----------------------")
        output = my_ping.ping_url(url)
        if output is None:
            print("Não foi possível encontrar o IP.")
        else:
            print(output)
            my_log.create_log(output)

        option = input("Deseja continuar? [S]im [N]ao: ").upper()

        if option == 'N':
            print('#################### FIM DE PROGRAMA ####################')
            break

        if option == 'S':
            continue
        print("Opção inválida. Encerrando o programa.")
        sys.exit()

