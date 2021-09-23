import random
#Tentativa de aplicar ant colony optimization
#A ideia seria alcançar o menor caminho possivel utilizando uma
#simulação de formigas depositando feromônios para atrair as outras
#os feromônios serão depositados levando em consideração o tamanho do caminho
#assim um bom caminho de menor custo terá a maior quantidade de feromônios

matrizInput = [
    [0, 13.5, 11.5, 7.4, 7.7, 4.5],
    [15.7, 0, 5.2, 12.1, 23.1, 20.0],
    [10.1, 7.2, 0, 7.8, 14.4, 12.1],
    [7.8, 11.2, 7.1, 0, 7.2, 4.9],
    [9.3, 21.0, 15.7, 9.0, 0, 6.4],
    [4.7, 16.4, 12.2, 5.5, 4.0, 0]
]

matrizFeromonios = [
    [0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0],
]

#Para cada formiga guardar quais vertices já foram percorridos
verticesJaPassados = [True, False, False, False, False, False]

def proxPasso(matrizDist, matrizFeromonios, verticeAtual, verticesJaPassados, a, b):
    #Dado um vertice a escolha do próximo vertice para uma formiga vai ser calculado por uma probabilidade
    #que como base vai levar em consideração a distancia entre o vertice e seu vizinho e tambem a quantidade de feromonios no vizinho
    #serão alocados pesos em cada uma dessas variaveis
    #para se obter um bom balanço entre a escolha de caminhos já visitados, possívelmente bons, e explorar novos caminhos
    #se o balanço estiver bom provavelmente as formigas com o tempo tenderão a seguir o mesmo bom caminho

    #A probabilidade de uma formiga escolher algum vizinho será dada da seguinte forma
    #((distancia do vizinho)^a * (feromonios no vizinho)^b)/(somatorio de vizinhos i, j((distancia do vizinho)^a * (feromonios no vizinho)^b))
    
    denominador = 0
    for i in range(len(matrizDist[0])):
        #Evitar divisão por 0
        if not verticesJaPassados[i]:
            denominador += pow((1/(matrizDist[verticeAtual][i] + 0.001)), a) * pow(((matrizFeromonios[verticeAtual][i] + 0.001)), b)
    

    listaProbabilidades = []
    listaVertices = []
    oldValue = 0
    for i in range(len(matrizDist[0])):
        if not verticesJaPassados[i]:
            #Evitar divisão por 0
            numerador = pow((1/(matrizDist[verticeAtual][i] + 0.001)), a) * pow(((matrizFeromonios[verticeAtual][i] + 0.001)), b)
            
            listaProbabilidades.append(oldValue + (numerador/denominador))
            listaVertices.append(i)
            oldValue += (numerador/denominador)

    #Escolher o vertice:
    #Se o número aleatório cair a "esquerda" de um valor da lista ele escolheu seu respectivo vertice
    numEscolhido = random.random()
    verticeEscolhido = -1
    for i in range(len(listaProbabilidades)):
        if numEscolhido <= listaProbabilidades[i]:
            #Escolheu esse vertice
            verticeEscolhido = listaVertices[i]
            return verticeEscolhido

# proxPasso(matrizInput, matrizFeromonios, 3, verticesJaPassados, 1, 1)

#Agora uma função para simular o caminho que uma formiga irá fazer
#ou seja iteração de "passos" da função anterior até ela ter que voltar para o seu inicio

#Peso padrão das arestas será "1", tenderá para escolha de arestas menores
def caminho(matrizDist, matrizFeromonios, verticeInicial, pesoFeromonios):
    #Ela deverá escolher vertices até todos os vertices serem escolhidos
    verticesRestantes = len(matrizDist)
    verticeAtual = verticeInicial
    distanciaCaminho = 0
    verticesJaPassados = []
    caminho = [verticeInicial]

    for i in range(verticesRestantes):
        if i == verticeInicial:
            verticesJaPassados.append(True)
        else:
            verticesJaPassados.append(False)
    
    while(verticesRestantes != 1):
        verticeAntigo = verticeAtual
        verticeAtual = proxPasso(matrizDist, matrizFeromonios, verticeAtual, verticesJaPassados, 1, pesoFeromonios)
        
        #Atualizar vertices passados
        caminho.append(verticeAtual)
        verticesJaPassados[verticeAtual] = True
        distanciaCaminho += matrizDist[verticeAntigo][verticeAtual]
        verticesRestantes += -1
    
    #Voltar para vertice original
    distanciaCaminho += matrizDist[verticeAtual][verticeInicial]
    
    #Atualizar feromonios nas arestas em que a formiga passou
    
    valorFeromonio = 1/distanciaCaminho
    for i in range(len(caminho)):
        if(i < len(caminho) - 1):
            matrizFeromonios[caminho[i]][caminho[i + 1]] += valorFeromonio
        else:
            matrizFeromonios[caminho[i]][verticeInicial] += valorFeromonio
    
    #Retornar matriz de feromonios atualizada
    return matrizFeromonios


caminho(matrizInput, matrizFeromonios, 0, 1.5)
