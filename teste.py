
import os
from csvArq import *

# Funções
# ==================================================================================================================================


def switch(menu, handler, exit):
    #implementação de menu com iteração caso usuário faça escolhas erradas.
    while menu != 0:
        if menu == 1:
            print("Listagem de artigos de um autor.\n")
            exit.write("Listagem de artigos de um autor.\n")

            candidato(handler, input("Nome procurado: "), exit)
            break
        elif menu == 2:
            print("Listagem de artigos de um conjunto de candidatos.\n")
            exit.write("Listagem de artigos de um conjunto de candidatos.\n")

          
            break
        elif menu == 3:
            print("Listagem de artigos com palavra consultada no título.\n")
            exit.write(
                "Listagem de artigos com palavra consultada no título.\n")

            title(handler, input("Palavra: "), exit)
            break
        elif menu == 4:
            print(
                "Listagem ordenado por autor, do número de artigos do autor nessa área.\n")
            exit.write(
                "Listagem ordenado por autor, do número de artigos do autor nessa área.\n")

            area(handler, input("Area: "), exit)
            break
        elif menu == 5:
            print("Listagem por ano.\n")
            exit.write("Listagem por ano.\n")

            year(handler, input("Ano: "), exit)
            break
        else:
            print("Valor inválido, tente novamente.")
            return 0
    if menu == 0:
        print("TCHAU!\n")
        exit.write("Arquivo Fechado.\n")
        exit.close()

    return 0

def candidato(name_archive, word_author, exit):
    #função lê o arquivo e retorna os dados do autor
    #Função printa dados do autor.
    list_art = []

    f = open(name_archive + "data_candidato_index.bin", 'rb')

    tree = pickle.load(f)

    word_author = word_author.lower()

    list_art = list_candidato(word_author, tree, name_archive)

    print_list(list_art)

    if list_art != None:
        for i in list_art:
            r = i.__repr__()
            exit.write(r + "\n")

    f.close()

def verify_entry(nomedaentrada):
    try:
        entrada = open(nomedaentrada+"data_candidato_index.bin", "wb")
        print("\nArquivo já processado anteriormente\n")
        entrada.close()
        return True
    except:
        print("\nArquivo novo.\nVamos processar o arquivo pela primeira vez.\nAguarde\n")
        return False


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
    print("[2] Listagem de cargos disputados.\n")
    print("[3] Listagem de candidatos por partido.\n")
    print("[4] Listagem de candidatos por ocupação.\n")
    menu = int(input())
    switch(menu, handler, saida)
    input()
