import csv
from csvArq import *
import numpy as np
# Para ler arquivo de artigos, aonde se extráira os dados        {.reader()}
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
     
        self.nascimento = info[0]
        self.cargo = info[1]
        self.numero = info[2]
        self.nome = info[3]
        self.cpf = info[4]
        self.numeroPartido = info[5]
        self.siglaPartido = info[6]
        self.nomePartido = info[7]
        self.municipioNascimento = info[8]
        self.dataNascimento= info[9]
        self.Idade = info[10]
        self.genero = info[11]
        self.grauInstrucao = info[12]
        self.cor = info[13]
        self.ocupacao = info[14]
        self.situacaoPosEleicao = info[15]
########

    def __repr__(self):
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (str(self.nascimento), str(self.cargo), str(self.numero), str(self.nome), str(self.cpf), str(self.numeroPartido), str(self.siglaPartido), str(self.nomePartido), str(self.municipioNascimento), str(self.dataNascimento), str(self.Idade), str(self.genero), str(self.grauInstrucao), str(self.cor), str(self.ocupacao), str(self.situacaoPosEleicao))

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

#Definição das funções


def normalize(title):
    aux_title = title.lower()  # normaliza o título, todas letras em minusculo

    word_list = re.sub("[\W]", " ", aux_title).split()

    return word_list


def intercession(listas):
    result = []
    a = listas[0]
    if len(listas[1:]) > 0:
        b = listas[1]
        for obj in a:
            if obj in b:
                result.append(obj)
        if len(listas[2:]) > 0:
            c = listas[2:]
            c.append(result)
            return intercession(c)
        else:
            return result
    else:
        return result


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

        nomeCandidato = registro.nome  # pega o título do artigo
        candidatoN = normalize(nomeCandidato)
        # para cada palavra, insere-a na Trie ou (se já existe) dá um novo offset
        for word in candidatoN:
            trie_candidato.AddNodeWord(word, registro.offset)

        nomePartido = registro.nomePartido
        nomePartido = [x.lower() for x in nomePartido]
        for partido in nomePartido:
            trie_partido.AddNodeWord(partido, registro.offset)

        trie_ocupacao.AddNodeWord(registro.ocupacao.lower(), registro.offset)

        trie_cargo.AddNodeWord(str(registro.cargo), registro.offset)

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



def insertion_sort(lista_registro):
    for i in range(len(lista_registro)):
        iterator = lista_registro[i]
        j = i
        while j > 0 and iterator.nome < lista_registro[j-1].nome:
            lista_registro[j] = lista_registro[j-1]
            j -= 1
        lista_registro[j] = iterator

def print_list(lista_registros):
    if(lista_registros == None):
        print("\nRegistro não encontrado.\n")
    else:
        if(len(lista_registros) > 15):
            sorted(lista_registros, key=lambda Register: Register.nome.lower())
        else:
            insertion_sort(lista_registros)

        for registro in lista_registros:

            print("Nome: %s\n" % (registro.nome))
            print("Cargo Disputado: %s\n" % (registro.cargo))
            print("Partido: %s\n" % (registro.nomePartido))
            print("Idade: %s\n" % (registro.genero))
            print("Gênero: %s\n" % (registro.Idade))
            print("Instrução: %s\n" % (registro.grauInstrucao))
            print("Ocupação: %s\n" % (registro.ocupacao))
            print("Situação após eleição: %s\n" % (registro.situacaoPosEleicao))
            print("===========================\n")

