# bibliotecas utilizdas para redirecionar o output (print) do método grade
import sys, os
from Node import *


# definição de estados para busca em profundidade
WHITE = 0
GRAY = 1
BLACK = 2


class Graph():  # classe para o grafo e seus métodos

    def __init__(self, nodes='', edges='', edgesW=[]):

        self.nodes = []
        self.directed = True

        # percorre os nodos e encontra os que ele tem conexão
        for node in nodes:
            tempD = []
            tempND = []
            tempW = []

            for edge in edges:
                
                # descreve relação para direcionado ou não direcionado
                if edge[0] == node:
                    tempD.append(edge[1])
                    tempND.append(edge[1])
                
                if edge[1] == node:
                    tempND.append(edge[0])

            for edgeW in edgesW:
                if edgeW[0] == node:
                    tempW.append([edgeW[1], edgeW[2]])
                '''if edgeW[1] == node:
                    tempW.append([edgeW[0], edgeW[2]])'''
            # cria nodo e adiciona a lista de nodos
            self.nodes.append(Node(node, tempD, tempND, tempW))

        

    # método para inserir um novo nodo a um grafo já existente
    def push(self, label):
        for i in range(len(self.nodes)):
            if label == self.nodes[i].label:
                print('\nERRO! Este nodo já existe.\n')
                return

        self.nodes.append(Node(label, [], []))
       
        print('\nOperação bem sucedida.\n')

    # remove um nodo.
    def pop(self, label):
        # variável para armazenar posição do nodo a ser deletado
        indexLabel = -1
        # chama o método para remover arestas ligadas ao nodo (se houver)
        for i in range(len(self.nodes)):
            if self.nodes[i].label != str(label):
                j = 0
                while j < (len(self.nodes[i].edgesD)):
                    if self.nodes[i].edgesD[j] == label:
                        # exclui aresta
                        self.remove(self.nodes[i].label+" "+self.nodes[i].edgesD[j])
                        # condição para saída da repetição
                        j = len(self.nodes[i].edgesD)
                    j += 1
            # índice no nodo a ser excluído
            else:
                indexLabel = i

        # exclui nodo
        if indexLabel != -1:
            self.nodes.pop(indexLabel)
            print('\nOperação bem sucedida.\n')
        else:
            print('\nERRO! Nodo não existe no grafo.\n')

    # método para inserir arestras entre dois nodos já existentes
    def insert(self, edge):  
        # verifica se existem nodos no grafo
        if len(self.nodes) == 0:
            print('\nERRO! Não existem nodos neste grafo.\n')
            return

        edge = edge.split(" ")

        # procura pelos índices dos nodos
        self.exitNodeIndex = self.index(edge[0])
        self.entryNodeIndex = self.index(edge[1])
        
        # se um deles não existir mostra mensagem de erro
        if self.entryNodeIndex == -1 or self.exitNodeIndex == -1:
            print('\nERRO! Um dos nodos não existe.\n')
            return

        # veririca se a aresta já existe e, caso não exista, adicioná-las ao nodo

        if edge[1] not in self.nodes[self.exitNodeIndex].edgesD:
                self.nodes[self.exitNodeIndex].edgesD.append(edge[1])
                self.nodes[self.exitNodeIndex].edgesND.append(edge[1])
                self.nodes[self.entryNodeIndex].edgesND.append(edge[0])
                print('\nOperação bem sucedida.\n')
        else:
            print('\nERRO! Esta aresta já existe.\n')

    # remove arestas
    def remove(self, edge):
        # verifica se o grafo não está vazio
        if len(self.nodes) == 0:
            print('\nERRO! Não existem nodos no grafo.\n')
            return
            
        # trata entrada
        edge = edge.split(" ")
        label, edge = edge[0], edge[1]

        self.indLabel = self.index(label)
        self.indEdge = self.index(edge)

        if self.indLabel == -1 or self.indEdge == -1:
            print('\nERRO! Um dos nodos não não existe.\n')
            return              

        # percorre os nodos
        for i in range(len(self.nodes)):

            # busca label em nodos
            if self.nodes[i].label == label and edge in self.nodes[i].edgesD:                
                self.nodes[i].edgesD.remove(edge)
                self.nodes[i].edgesND.remove(edge)

                # remoção do grado não direcionado
                self.nodes[self.indEdge].edgesND.remove(label)

                print('\nOperação bem sucedida.\n')           
                return
        
        print('\nERRO! A aresta não existe.\n')
        
    # mostra lista com os nodos e suas arestas
    def view(self):
        print()
        for i in range(len(self.nodes)):
            print(f'{self.nodes[i].label}: ', end='')

            if self.directed:
                if self.nodes[i].edgesD:
                    for j in range(len(self.nodes[i].edgesD)):
                        print(f'--> {self.nodes[i].edgesD[j]}', end='  ')
            else:
                if self.nodes[i].edgesND:
                    for j in range(len(self.nodes[i].edgesND)):
                        print(f'--> {self.nodes[i].edgesND[j]}', end='  ')
            print()
        print()

    # identifica as fontes e sumidouros do grafo
    def identify(self):
        self.source = [] # nodos fonte não têm arestas de entrada
        self.sink = [] # nodos sumidouros não têm aresta de saída

        # como a função grade tem um output desnessário usa-se
        # as funções sys para bloquear e liberar a saída
        sys.stdout = open(os.devnull, 'w')

        for i in range(len(self.nodes)):
            # chamamos o método grade para identificar os graus do nodo
            self.grade(self.nodes[i].label)
            # checa-se condição de fonte e sumidouro
            if  self.nodes[i].gradeIn == 0 and self.nodes[i].gradeOut == 0:
                continue
            else:
                if self.nodes[i].gradeIn == 0:
                    self.source.append(self.nodes[i].label)
                if self.nodes[i].gradeOut == 0:
                    self.sink.append(self.nodes[i].label)

        sys.stdout = sys.__stdout__

        print()

        if len(self.source) == 0:
            print('Não existem nodos fonte no grafo.')
        else:
            print('Nodo(s) fonte: ', end='')
            for i in range(len(self.source)):
                print(f'{self.source[i]} ', end='')
            print()            

        if len(self.sink) == 0:
            print('Não existem nodos sumidouro no grafo.')
        else:
            print('Nodo(s) sumidouro: ', end='')
            for i in range(len(self.sink)):
                print(f'{self.sink[i]} ', end='')
            print()
        
        print()

    # mostra o grau do nodo
    def grade(self, label):        
        self.indexTemp = self.index(label)        

        if self.indexTemp == None:
            print('\nERRO! O nodo não existe.\n')
            return
        else:
            # o grau de saída é o tamanho da varíavel que controla as arestas do nodo
            if self.directed:
                self.exit = len(self.nodes[self.indexTemp].edgesD)
                self.entry = 0
                
                # para o grau de entrada é necessário percorrer todos os nodos
                # veriicando a ocorrência do nodo informado nas arestas dos outros nodos
                for i in range(len(self.nodes)):
                    if label in self.nodes[i].edgesD:
                        self.entry += 1
            else:
                self.exit = len(self.nodes[self.indexTemp].edgesND)
                self.entry = len(self.nodes[self.indexTemp].edgesND)
            
            # salvando informação de grau na classe nodo
            self.nodes[self.indexTemp].gradeIn = self.entry
            self.nodes[self.indexTemp].gradeOut = self.exit

            print(f'\nGrau de entrada do nodo {label}: {self.entry}')
            print(f'Grau de saída do nodo {label}: {self.exit}\n')

    # mostra a matriz de adjacência do grafo
    def adjacencyMatrix(self):
        print()

        # mostra os nodos na horizontal - primeira linha
        print('     ', end='')
        for i in range(len(self.nodes)):
            print(f'{self.nodes[i].label}  ', end='')            

        print('\n')

        # procura pelos nodos que possuem arestas entre si
        for i in range(len(self.nodes)):
            # mostra os nodos na vertical - primeira coluna
            print(f'{(self.nodes[i].label)}    ', end='')
            for j in range(len(self.nodes)):
                if self.directed:
                    if self.nodes[j].label in self.nodes[i].edgesD:
                        print('1  ', end='')
                    else:
                        print('0  ', end='')
                else:
                    if self.nodes[j].label in self.nodes[i].edgesND:
                        print('1  ', end='')
                    else:
                        print('0  ', end='')
                        
            print()
        print()


    # método para mudar a definição do grafo 
    def guidance(self):        
        self.directed = not self.directed

        if self.directed:
            print('\nGrafo orientado.\n')
        else:
            print('\nGrafo não orientado.\n')
        

    #ATENÇÃO! CASO COM ERRO
    # algoritmo de busca em largura BFS
    def breadthSearch(self, s):
        # 's' é o label do nodo inicial
        # bibliografia https://www.youtube.com/watch?v=cUlDbC0KrQo

        # inicializa set de todos elementos
        for elem in self.nodes:
            elem.set = False
        
        line = []

        # índice de s
        indexS = self.index(s)
        # marca nodo
        self.nodes[indexS].set = True
        # add a fila
        line.append(indexS)

        # percorre todos os valores que possuem conexão com ramo de 's'
        while(len(line) != 0):
            # define primeiro valor da fila para analisar arestas
            u = line[0]

            line.pop(0)
            #processa(u) faz alguma coisa com o nodo percorrido

            # percorre arestas do nodo u e checa se já foram setadas
            # se não seta e adiciona a fila
            for i in range (len(self.nodes[u].edgesD)):
                indexTemp = self.index(self.nodes[u].edgesD[i])
                if self.nodes[indexTemp].set == False:
                    self.nodes[indexTemp].set = True
                    line.append(indexTemp)

    # algoritmo de busca em largura DFS-1
    def depthSearch(self):
        # bibliografia https://www.youtube.com/watch?v=0B6VfRbppkE

        # inicializa set de todos elementos
        for elem in self.nodes:
            elem.set = WHITE
        
        # tempo de abertura e fechamento
        self.time = 0
        # percorre todos os nodos
        for i in range(len(self.nodes)):
            if self.nodes[i].set == WHITE:
                self.depthSearchVisit(i)

    # algoritmo de busca em largura DFS-2
    def depthSearchVisit(self, u):
        # marca primeira passagem sobre o nodo (cinza)
        self.nodes[u].set = GRAY

        # incrementa e adiciona tempo de entrada do nodo
        self.time += 1
        self.nodes[u].time.append(self.time)

        # busca nodos vizinhos
        for i in range(len(self.nodes[u].edgesD)):
            indexTemp = self.index(self.nodes[u].edgesD[i])
            # se não tiver sido 'aberto' (nodo branco) acessa e chama recursão
            if self.nodes[indexTemp].set == WHITE:
                # define pai do nodo encontrado
                self.nodes[indexTemp].father = self.nodes[u].label
                self.depthSearchVisit(indexTemp)

        # fecha nodo (seta cor preto) e adiciona tempo de saída
        self.nodes[u].set = BLACK
        self.time += 1
        self.nodes[u].time.append(self.time)

    #ATENÇÃO! MELHORAR
    # printa informações de cada nodo pós busca por profundidade
    def infosDepthSearch(self):
        for elem in self.nodes:
            print(f'label: {elem.label}')
            print(f'pai {elem.father}')
            print(f'tempo {elem.time}')
            print(f'cor {elem.set}')
            print()
    
    def prim(self, label):
        self.nodo = label
        self.indice = self.index(self.nodo)

        if self.indice == -1:
            print('\nERRO! Este nodo não existe.\n')
            return
        
        # a chave do nodo de partida é sempre 0
        self.nodes[self.indice].key = 0
        self.firstRun = True
        tmp = 0

        self.size = len(self.nodes)            
                   
        while self.size > 0:

            self.size -= 1
            
            self.pai = self.nodes[tmp].label            

            for edgeW in self.nodes[tmp].edgesWH:
                print(edgeW[0])
                indice = self.index(edgeW[0])
                print(indice)                
                                
                if int(edgeW[1]) < self.nodes[indice].key:
                    # acessamos o nodo na posição encontrada e setamos o pai e o valor da chave (peso da aresta)
                    self.nodes[indice].parent = self.pai
                    self.nodes[indice].key = int(edgeW[1])
            
            #print('saiu')
            self.firstRun = False
            tmp = self.extractMin()
            print(f'temp = {tmp}')
            '''print('run')
            for i in range(len(self.nodes)):
                print(self.nodes[i].key)'''

        for i in range(len(self.nodes)):
            print(self.nodes[i].parent)
            print(self.nodes[i].key)

    def kruskal(self):
        print('\nYou wish...\n')

    def dijkstra(self):
        print('\nYou wish...\n')

    def bellmanFord(self):
        print('\nYou wish...\n')

    # retorna índice (da lista self.grafos) de algum nodo
    def index(self, label):
        for i in range(len(self.nodes)):
            if self.nodes[i].label == str(label):
                return i
        
        # caso não encontre o elemento procurado
        return -1

    # ver ligação dos nodos e o peso destas ligações
    def view2(self):
        print()
        for i in range(len(self.nodes)):
            print(f'{self.nodes[i].label}: ', end='')
            if self.nodes[i].edgesWH:                
                for j in range(len(self.nodes[i].edgesWH)):
                    print(f'{self.nodes[i].edgesWH[j]} ', end='  ')

            print()
        print()

    # método auxiliar para Prim
    def extractMin(self):

        self.huh = -1
        self.menor = float('inf')

        for node in self.nodes:
            #print(node.key)
            if node.key < self.menor and node.key > 0:                
                self.menor = node.key
                self.huh = self.index(node.label)
                #print(f'self.huh = {self.huh}')

        return self.huh