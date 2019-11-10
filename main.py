'''
    Tarefa sobre Grafos
    Augusto
    Murilo
'''

# bibliotecas utilizdas para redirecionar o output (print) do método grade
import io
from contextlib import redirect_stdout

class Graph():  # classe para o grafo e seus métodos

    def __init__(self, nodes='', edges=''):

        self.nodes = []
        # percorre os nodos e encontra os que ele tem conexão (já direcionado)
        for node in nodes:
            edgeReal = []
            for edge in edges:
                if edge[0] == node:
                    edgeReal.append(edge[1])
            self.nodes.append(Node(node, edgeReal))

    # método para inserir um novo nodo a um grafo já existente
    def push(self, label):
        for i in range(len(self.nodes)):
            if label == self.nodes[i].label:
                print('\nERRO! Este nodo já existe.\n')
                return

        self.nodes.append(Node(label))
        print('\nOperação bem sucedida.\n')

    # remove um nodo.
    def pop(self, label):
        # chama o método para remover arestas ligadas ao nodo (se houver)
        for i in range(len(self.nodes)):
            if self.nodes[i].label != str(label):
                j = 0
                while j < (len(self.nodes[i].edges)):
                    if self.nodes[i].edges[j] == label:
                        # exclui aresta
                        self.remove(self.nodes[i].label, self.nodes[i].edges[j])
                        # condição para saída da repetição
                        j = len(self.nodes[i].edges)
                    j += 1
            # índice no nodo a ser excluído
            else:
                indexLabel = i

        # exclui nodo
        self.nodes.pop(indexLabel)

        print('\nOperação bem sucedida.\n')

    # método para inserir arestras entre dois nodos já existentes
    def insert(self, edge):           
        # verifica se existem nodos no grafo
        if len(self.nodes) == 0:
            print('\nERRO! Não existem nodos neste grafo.\n')
            return

        edge = edge.split(" ")
        
        self.exitNodeIndex = -1
        self.entryNodeIndex = -1

        # procura pelos índices dos nodos
        for i in range(len(self.nodes)):
            if self.nodes[i].label == edge[0]:
                self.exitNodeIndex = i

            if self.nodes[i].label == edge[1]:
                self.entryNodeIndex = i
        
        # se um deles não existirem mostra mensamge de erro e so método
        if self.entryNodeIndex == -1 or self.exitNodeIndex == -1:
            print('\nERRO! Um dos nodos não existe.\n')
            return

        # veririca se a aresta já existe e, caso não exista, adiciona as arestas do nodo
        if edge[1] not in self.nodes[self.exitNodeIndex].edges:
            self.nodes[self.exitNodeIndex].edges.append(edge[1])
            print('\nOperação bem sucedida.\n')
        else:
            print('\nERRO! Esta aresta já existe.\n')


    # remove arestas (verifica se existem arestas no grafo e
    # se a aresta informada existe no grafo
    def remove(self, label, edge):
        label, edge = str(label), str(edge)
  
        # percorre os nodos
        for i in range(len(self.nodes)):
            # condição de grafo vazio
            if len(self.nodes) == 0:
                print('\nERRO! Não existem nodos no grafo.\n')
            # busca label em nodos
            if self.nodes[i].label == label:
                try:
                    self.nodes[i].edges.remove(edge)
                except:
                    print('\nERRO! Aresta não exite.\n')
                return
        # se o nodo não for encontrado
        print('\nERRO! Nodo não existe.\n')
    
    
    # mostra lista com os nodos e suas arestas
    def view(self):
        for i in range(len(self.nodes)):
            print(f'{self.nodes[i].label}: ', end='')
            if self.nodes[i].edges:
                for j in range(len(self.nodes[i].edges)):
                    print(f'--> {self.nodes[i].edges[j]}', end='  ')
            
            print()

    # identifica as fontes e sumidouros do grafo
    def identify(self):
        self.source = [] # nodos fonte não têm arestas de entrada
        self.sink = [] # nodos sumidouros não têm aresta de saída

        # utilizamos o método grade da classe para identificar os nodos
        # como a função grade tem um output desnessário neste caso
        # redirecionamos para uma variável, neste caso 'f'
        f = io.StringIO()
        with redirect_stdout(f):

            for node in self.nodes:
                self.grade(node)
                if self.entry == 0:
                    self.source.append(node)
                if self.exit == 0:
                    self.sink.append(node)
        
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
    def grade(self, node):        
        self.index = -1

        # procura o índice do nodo
        for i in range(len(self.nodes)):
            if node == self.nodes[i].label:
                self.index = i
                break

        # caso o índide seja -1 é porque o nodo informado não está na lista - volta para main()
        if self.index == -1:
            print('\nERRO! O nodo não existe.\n')
            return
        else:
            # o grau de saída é o tamanho da varíavel que controla as arestas do nodo
            self.exit = len(self.nodes[self.index].edges)
            self.entry = 0
            
            # para o grau de entrada é necessário percorrer todos os nodos
            # veriicando a ocorrência do nodo informado nas arestas dos outros nodos
            for i in range(len(self.nodes)):
                if node in self.nodes[i].edges:
                    self.entry += 1            

            print(f'\nGrau de entrada do nodo {node}: {self.entry}')
            print(f'Grau de saída do nodo {node}: {self.exit}\n')

    # mostra a matriz de adjacência do grafo
    def adjacencyMatrix(self):
        # mostra os nodos na horizontal - primeira linha
        print('     ', end='')
        for i in range(len(self.nodes)):
            print(f'{self.nodes[i].label}  ', end='')            

        print('\n')

        # procura pelos nodos que possuem arestas entre si
        for i in range(len(self.nodes)):
            # mostra os nodos na vertical - primeira coluna
            print(f'{self.nodes[i].label}    ', end='')

            for j in range(len(self.nodes)):
                if self.nodes[j].label in self.nodes[i].edges:
                    print('1  ', end='')
                else:
                    print('0  ', end='')

            print()
        print()

    # método para mudar a definição do grafo
    # não-orientado -> orientado e orientado -> não-orientado
    # NOME do método pode ser melhorado
    def direction(self):
        self.directed = not self.directed
        print('\nOperação bem sucedida.\n')


class Node():  # classe para os nodos e suas características
    def __init__(self, label='', edges=''):
        self.label = label
        self.edges = edges


def readFile(): # função para receber entrada do arquivo
    with open('entrada.txt') as file:
        lines = [line.rstrip() for line in file]
    for i in range(len(lines)):
        lines[i] = lines[i].split(" ")
    file.close()

    return lines[0], lines


def menu(): # menu do programa
    print('===============Opções===============')
    print('1 - Mostrar lista de adjacências')
    print('2 - Mostrar matriz de adjacências')
    print('3 - Inserir um nodo')
    print('4 - Remover um nodo')
    print('5 - Inserir uma aresta')
    print('6 - Remover uma aresta')
    print('7 - Informar o grau de um nodo')
    print('8 - Informar fontes e sumidouros do grafo')
    print('9 - Não-orientado -> orientado (e vice-versa)')
    print('0 = Encerra o programa')
    print('====================================')
    option = input('Opção: ')

    return option


def main():

    # lê os dados do arquivo de entrada e cria uma lista com
    # os nodos na posição 0 e as arestas nas posições seguintes
    nodes, data = readFile()


    # as linhas seguintes são as arestas
    edges = []
    for linha in data[1:]:
        edges.append([linha[0], linha[1]])


    # cria o objeto passando como parâmetro os nodos e arestas
    g = Graph(nodes, edges)

    g.adjacencyMatrix()#teste
    #g.grade('2')
    g.identify()

'''

    # testes
    op = -1

    while op != 0:
        try:
            op = int(menu())

            if op == 1:
                g.view()
            elif op == 2:
                g.adjacencyMatrix()
            elif op == 3:
                g.push(input('Informe o novo nodo: '))
            elif op == 4:
                g.pop(input('Informe o nodo a ser excluído: '))
            elif op == 5:
                g.insert(input('Informe a aresta a ser incluída ([nodo1] [nodo2]): '))
            elif op == 6:
                g.remove(input('Informe a aresta a ser excluída ([nodo1] [nodo2]): '))
            elif op == 7:
                g.grade(input('Informe o nodo: '))
            elif op == 8:
                g.identify()
            elif op == 9:
                g.direction()
            elif op < 0 or op > 9:
                print('\nERRO! Favor informar um valor entre 0 e 7.\n')

        except ValueError:
            print('\nFavor informar um valor válido.\n')
        

'''
main()