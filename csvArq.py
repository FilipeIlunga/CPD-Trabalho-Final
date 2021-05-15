import csv
from csvArq import *
import numpy as np
# Para ler o arquivo fonte, aonde se extráira os dados        {.reader()}
import csv
# Para manipular strings obtidas no arquivo                      {.sub(), .split()}
import re
# Para usar função hash                                          {.md5(), .hexdigest()}
import hashlib
# Para utilizar protocolos binários para serializar objetos      {.dump(), .load()}
import pickle


class Register(object):
    def __init__(self, offset=0, info=[]):
        self.offset = offset
     
        self.unidadeEleitoral = info[0]
        self.CODcargo = int(info[1],10)
        self.cargo = info[2]
        self.numero = info[3]
        self.nome = info[4]
        self.cpf = info[5]
        self.numeroPartido = info[6]
        self.siglaPartido = info[7]
        self.nomePartido = info[8]
        self.municipioNascimento = info[9]
        self.dataNascimento = info[10]
        if info[11] == '':
            self.Idade = info[11]
        else:
            self.Idade = int(info[11])
        self.CODgenero = int(info[12],10)
        self.genero = info[13]
        self.CODgrauInstrucao = int(info[14],10)
        self.grauInstrucao = info[15]
        self.cor = info[16]
        self.ocupacao = info[17]
        self.CODsituacaoPosEleicao = int(info[18],10)
        self.situacaoPosEleicao = info[19]
########

    def __repr__(self):
        return "%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%d\t%d\t%s\t%d\t%s\t%s\t%s\t%d\t%s" % (str(self.unidadeEleitoral), str(self.CODcargo), str(self.cargo), str(self.numero), str(self.nome), str(self.cpf), str(self.numeroPartido), str(self.siglaPartido), str(self.nomePartido), str(self.municipioNascimento), str(self.dataNascimento), str(self.Idade), str(self.CODgenero), str(self.genero), str(self.CODgrauInstrucao), str(self.grauInstrucao), str(self.cor), str(self.ocupacao), str(self.CODsituacaoPosEleicao), str(self.situacaoPosEleicao))

class NodeTrie(object):
    def __init__(self, value, children_right=None, children_left=None, offsets=[], rest_word=[]):
        self.value = value            # parte do código que o nodo representa
        self.children_right = children_right   # filho direito do nodo
        self.children_left = children_left    # filho esquerdo do nodo
        self.offsets = offsets          # offset em outro arquivo
        # resto da palavra/código (se houver) na folha
        self.rest_word = rest_word
########

    def search(self, code_bin):                 # procura um código binário na árvore - Trie

        if code_bin[0] == '0':
            if self.children_left != None:
                if len(code_bin[1:]) > 0:
                    return self.children_left.search(code_bin[1:])
                else:
                    return [True, self.children_left]
            else:
                return [False, None]
        elif code_bin[0] == '1':
            if self.children_right != None:
                if len(code_bin[1:]) > 0:
                    return self.children_right.search(code_bin[1:])
                else:
                    return [True, self.children_right]
            else:
                return [False, None]
        return [None, "Código inválido"]

    # o código já foi procurado previamente, então ele não existe na árvore (todos códigos tem o mesmo tamanho, já que vem da mesma função hash)
    def AddCodeBin(self, code, word, offset):
        if code[0] == '0':
            if self.children_left != None:
                if len(code[1:]) > 0:
                    return self.children_left.AddCodeBin(code[1:], word, offset)
            elif len(code[1:]) > 0:
                self.children_left = NodeTrie(code[0], offsets=[])
                self.children_left.AddCodeBin(code[1:], word, offset)
            else:
                self.children_left = NodeTrie(code[0], offsets=[])
                self.children_left.offsets.append(offset)
                self.children_left.rest_word = word
        elif code[0] == '1':
            if self.children_right != None:
                if len(code[1:]) > 0:
                    return self.children_right.AddCodeBin(code[1:], word, offset)
            elif len(code[1:]) > 0:
                self.children_right = NodeTrie(code[0], offsets=[])
                self.children_right.AddCodeBin(code[1:], word, offset)
            else:
                self.children_right = NodeTrie(code[0], offsets=[])
                self.children_right.offsets.append(offset)
                self.children_right.rest_word = word

    def AddNodeWord(self, word, offset):

        # coloca string na função hash, (Unicode-objects must be encoded before hashing)
        hash_w = hashlib.md5(word.encode())
        # Devolve o código em hexadecimal, transforma em inteiro e então em bits (string)
        hash_w_bin = bin(int(hash_w.hexdigest(), 16))
        hash_w_bin = hash_w_bin[2:]

        node = self.search(hash_w_bin)  # Procura código na árvore
        if node[0]:
            # Se já existe e offset não está na lista de offsets,
            if offset not in node[1].offsets:
                # coloca novo offset na lista de offsets
                node[1].offsets.append(offset)
        else:
            self.AddCodeBin(hash_w_bin, word, offset)


def normalize(word):
    aux_word = word.lower()  # normaliza a palavra, todas letras em minusculo

    word_list = re.sub("[\W]", " ", aux_word).split()

    return word_list


# monta arquivos invertidos, que armazenam os indices em árvores Trie.
def make_index_files(lista_registros, handler):
    trie_candidato = NodeTrie(None, offsets=[])
    trie_partido = NodeTrie(None, offsets=[])
    trie_ocupacao = NodeTrie(None, offsets=[])
    trie_cargo = NodeTrie(None, offsets=[])

    f_candidato = open(handler + "data_candidato_index.bin", 'wb')
    f_partido = open(handler + "data_partido_index.bin", 'wb')
    f_ocupacao = open(handler + "data_ocupacao_index.bin", 'wb')
    f_cargo = open(handler + "data_cargo_index.bin", 'wb')

    for registro in lista_registros:  # para cada registro, insere suas palavras na Trie

        nomeCandidato = registro.nome  
        candidatoN = normalize(nomeCandidato)
        # para cada palavra, insere-a na Trie ou (se já existe) dá um novo offset
        for word in candidatoN:
            trie_candidato.AddNodeWord(word, registro.offset)

        nomePartido = registro.nomePartido
        nomePartido = [x.lower() for x in nomePartido]
        for partido in nomePartido:
            trie_partido.AddNodeWord(partido, registro.offset)

        ocupacaoCandidato = registro.ocupacao  
        ocupacaoN = normalize(ocupacaoCandidato) 
        for word in ocupacaoN:
            trie_ocupacao.AddNodeWord(word, registro.offset)

        cargoCandidato = registro.cargo 
        cargoN = normalize(cargoCandidato)
        for word in cargoN:
            trie_cargo.AddNodeWord(word, registro.offset)

    pickle.dump(trie_candidato, f_candidato, pickle.HIGHEST_PROTOCOL)
    pickle.dump(trie_partido, f_partido, pickle.HIGHEST_PROTOCOL)
    pickle.dump(trie_ocupacao, f_ocupacao, pickle.HIGHEST_PROTOCOL)
    pickle.dump(trie_cargo, f_cargo, pickle.HIGHEST_PROTOCOL)

    f_candidato.close()
    f_ocupacao.close()
    f_partido.close()
    f_cargo.close()


def search_candidato(offset, name_file):

    handler = open(name_file + 'Data.bin', 'rb')
    for i in range(offset):
        pickle.load(handler)

    r = pickle.load(handler)

    handler.close()

    return r


def list_candidato(word, tree, name_file):
    n = []
    candidatos = []

    #a função search precisa do código obtido com a função hash
    # coloca string na função hash, (Unicode-objects must be encoded before hashing)
    hash_w = hashlib.md5(word.encode())
    # Devolve o código em hexadecimal, transforma em inteiro e então em bits (string)
    hash_w_bin = bin(int(hash_w.hexdigest(), 16))
    hash_w_bin = hash_w_bin[2:]

    n = tree.search(hash_w_bin)

    if n[0]:
        for i in n[1].offsets:
            candidatos.append(search_candidato(i, name_file))
        return candidatos
    else:
        return None

#ordena os candidatos por cargo disputado, presidente, vice, governador ...
def insertion_sort(lista_registro, ordem):
   
    for i in range(len(lista_registro)):
        iterator = lista_registro[i]
        j = i
        if ordem == 1:
            ordenacao = iterator.CODcargo < lista_registro[j - 1].CODcargo
        elif ordem == 2:
            ordenacao = iterator.CODcargo > lista_registro[j - 1].CODcargo
        elif ordem == 3:
            ordenacao = iterator.Idade < lista_registro[j - 1].Idade
        elif ordem == 4:
            ordenacao = iterator.Idade > lista_registro[j - 1].Idade

        while j > 0 and ordenacao:
            lista_registro[j] = lista_registro[j-1]
            j -= 1
        lista_registro[j] = iterator


def quicksort(registro,ordem):
    if len(registro) == 1 or len(registro) == 0:
        return registro
    else:
        if ordem ==1 or ordem == 2:
           pivot = registro[0].Idade
        if ordem == 3 or ordem == 4:
           pivot = registro[0].CODcargo
        i = 0
        for j in range(len(registro) - 1):
            if ordem == 1:
               ordenacao = registro[j + 1].Idade > pivot
            elif ordem == 2:
               ordenacao = registro[j + 1].Idade < pivot
            elif ordem == 3:
               ordenacao = registro[j + 1].CODcargo > pivot
            elif ordem == 4:
               ordenacao = registro[j + 1].CODcargo < pivot
            else:
                print("COMANDO INVALIDO\n")
                print("ORDEM POR CARGO SERÁ SEGUIDA\n\n")
                ordenacao = registro[j + 1].CODcargo > pivot

            if ordenacao:
                registro[j+1], registro[i+1] = registro[i+1], registro[j+1]
                i += 1
        registro[0], registro[i] = registro[i], registro[0]
        first_part = quicksort(registro[:i],ordem)
        second_part = quicksort(registro[i+1:],ordem)
        first_part.append(registro[i])
        return first_part + second_part

def print_list(lista_registros, numMaxCandidatos,ordem):
    if(lista_registros == None):
        print("\nRegistro não encontrado.\n")
    else:
        #insertion_sort(lista_registros,ordem)
        listaOrdem = quicksort(lista_registros,ordem)
       
        for registro in listaOrdem[:numMaxCandidatos]:
           print("===========================\n")
           print("Nome: %s\n" % (registro.nome))
           print("Gênero: %s\n" % (registro.genero))
           print("Idade: %s\n" % (registro.Idade))
           print("Unidade Eleitoral: %s\n" % (registro.unidadeEleitoral))
           print("Cargo Disputado: %s\n" % (registro.cargo))
           print("Partido: %s\n" % (registro.nomePartido))
           print("Instrução: %s\n" % (registro.grauInstrucao))
           print("Ocupação: %s\n" % (registro.ocupacao))
           print("Situação após eleição: %s\n" % (registro.situacaoPosEleicao))
                
           

