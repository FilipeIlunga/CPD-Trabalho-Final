
import os
from csvArq import *

# Funções
# ==================================================================================================================================

def switch(menu, handler):
    #implementação de menu com iteração caso usuário faça escolhas erradas.
    while menu != 0:
        if menu == 1:
            candidato(handler, input("Nome procurado: "), int(input("Qual o máximo de candidatos deseja listar?: ")))
            break
        elif menu == 2:
            ocupacao(handler, input("Profissão: "), int(input("Qual o máximo de candidatos deseja listar?: ")))
            break
        elif menu == 3:
            cargo(handler, input("Cargo procurado: "), int(input("Qual o máximo de candidatos deseja listar?: ")))
            break
    if menu == 0:
        print("###### PROGRAMA FINALIZADO! ######\n")

    return 0


def candidato(name_archive, nomeCandidato, numMaxCandidatos):
    print("\n\nORDENACAO:")
    print("[1] Ordenar por cargo, maior para o menor.\n")
    print("[2] Ordenar por cargo, menor para o maior.\n")
    print("[3] Ordenar por idade, maior para o menor.\n")
    print("[4] Ordenar por idade, menor para o maior.\n")
    print("[3] Ordenar por grau de instrucao, maior para o menor.\n")
    print("[4] Ordenar por grau de instrucao, menor para o maior.\n")
    
    menu = int(input())

    #função lê o arquivo e retorna os dados do candidato
    list_cand = []

    f = open(name_archive + "data_candidato_index.bin", 'rb')

    tree = pickle.load(f)
    nomeCandidato = nomeCandidato.lower()
    list_cand = list_candidato(nomeCandidato, tree, name_archive)

    print_list(list_cand, numMaxCandidatos,menu)

    f.close()


def ocupacao(name_archive, ocupacaoCandidato, numMaxCandidatos):
    #função lê o arquivo e retorna os dados do candidato da ocupação informada
    list_cand = []

    f = open(name_archive + "data_ocupacao_index.bin", 'rb')

    tree = pickle.load(f)

    ocupacaoCandidato = ocupacaoCandidato.lower()

    list_cand = list_candidato(ocupacaoCandidato, tree, name_archive)

    print_list(list_cand, numMaxCandidatos)

    f.close()


def cargo(name_archive, cargoCandidato, numMaxCandidatos):
    #função lê o arquivo e retorna os dados do candidato que disputou o cargo informado

    list_cand = []

    f = open(name_archive + "data_cargo_index.bin", 'rb')

    tree = pickle.load(f)
    cargoCandidato = cargoCandidato.lower()
    list_cand = list_candidato(cargoCandidato, tree, name_archive)

    print_list(list_cand, numMaxCandidatos)

    f.close()

def abrirArq():
    try:
        handler = input("Nome do arquivo base:")
        f = open(handler + ".csv", 'r', errors='ignore', encoding="UTF-8")

        return [f, handler]

    except:
        print("\nEste arquivo não existe, tente de novo\n")
        return abrirArq()


Registers = []
files = []

k = abrirArq()

f = k[0]

handler = k[1]

del k
# parte de processamento do arquivo.
offset = 0

if os.path.isfile(handler + 'Data.bin') == False:
    with open(handler + 'Data.bin', "wb") as handler_data:
        for line in csv.reader(f, dialect='excel', delimiter=';'):
            if line[0] == "NM_UE":  # se for a primeira linha, ignora
                del line
            else:
                i = 19
                for element in line[19::1]:
                    i += 1
                    if element == "":
                        del line[i-1::]
                newElement = Register(offset, line)
                Registers.append(newElement)
                pickle.dump(newElement, handler_data, pickle.HIGHEST_PROTOCOL)

                offset += 1

    f.close()
    make_index_files(Registers, handler)

print("\nArquivo " + handler + " aberto e processado com sucesso\n")

menu = 1
while menu != 0:
    print("Escolha uma das opções abaixo:\n\n")
    print("[1] Buscar Candidato.\n")
    print("[2] Listagem de candidatos por ocupação.\n")
    print("[3] Listagem de cargos disputados.\n")
    print("[0] Finalizar programa.\n")
    menu = int(input())
    switch(menu, handler)
    input()
