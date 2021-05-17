
import os
from csvArq import *
import time
#--coding: ANSI - -

# Funções
# ==================================================================================================================================

def switch(menu, handler):
    #implementação de menu com iteração caso usuário faça escolhas erradas.
    while menu != 0:
        if menu == 1:
            
            inicio = time.time()
            candidato(handler, input("Nome procurado: "), menu)
            fim = time.time()
            print(fim - inicio)
            break
        elif menu == 2:
            ocupacao(handler, input("Profissão: "),menu)
            break
        elif menu == 3:
            cargo(handler, input("Cargo procurado: "),menu)
            break
        else:
            print('[%s] É COMANDO INVALIDO, TENTE NOVAMENTE\n' %  menu)
            break
    if menu == 0:
        print("###### PROGRAMA FINALIZADO! ######\n")
           
    return 0

def printMenu(menu):
    if menu == 3:
        print("\n\nORDENAR POR:")
        print("IDADE\n")
        print("\t[1]  Decrescente\n")
        print("\t[2]  Crescente.\n")
        print("GRAU DE INSTRUÇÃO.\n")
        print("\t[5]  Decrescente\n")
        print("\t[6]  Crescente.\n")
        print("\n[0] BUSCAR OUTRO CANDIDATO")
    else:
        print("\n\nORDENAR POR:")
        print("IDADE\n")
        print("\t[1]  Decrescente\n")
        print("\t[2]  Crescente.\n")
        print("CARGO DISPUTADO.\n")
        print("\t[3]  Decrescente\n")
        print("\t[4]  Crescente.\n")
        print("GRAU DE INSTRUÇÃO.\n")
        print("\t[5]  Decrescente\n")
        print("\t[6]  Crescente.\n")
        print("\n[0] FAZER OUTRA BUSCA")


def menuOrdem(menuPrint, list_cand, nomeCandidato):
    menu = 1
    while menu != 0:
        printMenu(menuPrint)

        menu = int(input())
        if menu == 0:
            return
        #função lê o arquivo e retorna os dados do candidato
        print_list(list_cand, int(input("Qual o máximo de candidatos deseja listar?: ")), menu,
                   menuPrint, nomeCandidato)

def candidato(name_archive, nomeCandidato,menuPrint):
    
    list_cand = []

    f = open(name_archive + "data_candidato_index.bin", 'rb')
    tree = pickle.load(f)
    nomeCandidato = nomeCandidato.lower()

    list_cand = list_candidato(nomeCandidato, tree, name_archive)
    f.close()
    menuOrdem(menuPrint, list_cand, nomeCandidato)


def ocupacao(name_archive, ocupacaoCandidato,menuPrint):

    list_cand = []

    f = open(name_archive + "data_ocupacao_index.bin", 'rb')
    tree = pickle.load(f)
    ocupacaoCandidato = ocupacaoCandidato.lower()

    list_cand = list_candidato(ocupacaoCandidato, tree, name_archive)
    f.close()
    menuOrdem(menuPrint, list_cand, ocupacaoCandidato)



def cargo(name_archive, cargoCandidato,menuPrint):

    list_cand = []

    f = open(name_archive + "data_cargo_index.bin", 'rb')
    tree = pickle.load(f)
    cargoCandidato = cargoCandidato.lower()

    list_cand = list_candidato(cargoCandidato, tree, name_archive)
    f.close()
    menuOrdem(menuPrint, list_cand, cargoCandidato)

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
    print("\n___________________________________\n")
    print("| ESCOLHA UMA DAS OPÇÕES ABAIXO   |")
    print("___________________________________\n")
    print("[1] Buscar Candidato.\n")
    print("[2] Listagem de candidatos por ocupação.\n")
    print("[3] Listagem de cargos disputados.\n")
    print("[0] Finalizar programa.\n")
    menu = int(input())
    switch(menu, handler)

