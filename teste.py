
import os
from csvArq import *

# Funções
# ==================================================================================================================================


def switch(menu, handler, saida):
    #implementação de menu com iteração caso usuário faça escolhas erradas.
    while menu != 0:
        if menu == 1:
            print("Listagem de candidatos por nome.\n")
            saida.write("Listagem de candidatos nome.\n")

            candidato(handler, input("Nome procurado: "), saida)
            break
        elif menu == 2:
            print("Lista Candidatos por profissão.\n")
            ocupacao(handler, input("Profissão: "), saida)
           
            break
        elif menu == 3:
            print("Listagem de candidatos por cargo Disputado.\n")
            saida.write(
                "Listagem de candidatos por cargo Disputado.\n")

            cargo(handler, input("Cargo procurado: "), saida)
            break
    if menu == 0:
        print("TCHAU!\n")
        saida.write("Arquivo Fechado.\n")
        saida.close()

    return 0

def candidato(name_archive, nomeCandidato, exit):
    #função lê o arquivo e retorna os dados do autor
    #Função printa dados do autor.
    list_art = []

    f = open(name_archive + "data_candidato_index.bin", 'rb')

    tree = pickle.load(f)
    nomeCandidato = nomeCandidato.lower()
    list_art = list_candidato(nomeCandidato, tree, name_archive)

    print_list(list_art,exit)

    if list_art != None:
        for i in list_art:
            r = i.__repr__()
            exit.write(r + "\n")
    f.close()


def ocupacao(name_archive, ocupacaoCandidato, exit):
    list_art = []

    f = open(name_archive + "data_ocupacao_index.bin", 'rb')

    tree = pickle.load(f)

    ocupacaoCandidato = ocupacaoCandidato.lower()

    list_art = list_candidato_ocupacao(ocupacaoCandidato, tree, name_archive)

    print_list(list_art, exit)

    if list_art != None:
        for i in list_art:
            r = i.__repr__()
            exit.write(r + "\n")
    f.close()


def cargo(name_archive, cargoCandidato, exit):

    list_art = []

    f = open(name_archive + "data_cargo_index.bin", 'rb')

    tree = pickle.load(f)
    cargoCandidato = cargoCandidato.lower()
    list_art = list_candidato_cargo(cargoCandidato, tree, name_archive)

    print_list(list_art, exit)

    if list_art != None:
        for i in list_art:
            r = i.__repr__()
            exit.write(r + "\n")
    f.close()

def test():
    try:
        handler = input("File name:")
        f = open(handler + ".csv", 'r', errors='ignore', encoding="UTF-8")

        return [f, handler]

    except:
        print("\nEste arquivo não existe, tente de novo\n")
        return test()


Registers = []
files = []

k = test()

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
                i = 16
                for element in line[16::1]:
                    i += 1
                    if element == "":
                        del line[i-1::]
                newElement = Register(offset, line)
                Registers.append(newElement)
                pickle.dump(newElement, handler_data, pickle.HIGHEST_PROTOCOL)

                #offset += newElement.nbytes  #Em teste
                offset += 1

    f.close()
    make_index_files(Registers, handler)

print("\nArquivo " + handler + " aberto e processado com sucesso\n")

arquivodesaida = input(
    "\nPara melhor visualizar os dados, tudo será impresso em um arquivo de saida. \nPor favor, escolha um nome para este arquivo.\n")
arquivodesaida = arquivodesaida + ".txt"
print(arquivodesaida + " criado\n")
saida = open(arquivodesaida, "w")

menu = 1
while menu != 0:
    print("Escolha uma das opções abaixo:\n\n")
    print("[1] Buscar Candidato.\n")
    print("[2] Listagem de candidatos por ocupação.\n")
    print("[3] Listagem de cargos disputados..\n")
    menu = int(input())
    switch(menu, handler, saida)
    input()
