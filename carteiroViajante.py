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
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
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


#Agora uma função para simular o caminho que uma formiga irá fazer
#ou seja iteração de "passos" da função anterior até ela ter que voltar para o seu inicio

#Peso padrão das arestas será "1", tenderá para escolha de arestas menores se o peso dos feromonios também for igual a 1
def caminho(matrizDist, matrizFeromonios, verticeInicial, pesoAlfa, pesoFeromonios):
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
        verticeAtual = proxPasso(matrizDist, matrizFeromonios, verticeAtual, verticesJaPassados, pesoAlfa, pesoFeromonios)
        
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


# caminho(matrizInput, matrizFeromonios, 0, 1.5)

#Agora uma função para fazer a iteração de n formigas, ou seja aplicação n vezes da função anterior
#para tentar obter um caminho bom
#Após as n iterações, uma ultima formiga elegerá qual o caminho final baseado apenas na quantidade de feromonios presente nele
def colonia(matrizDist, matrizFeromoniosInicial, verticeInicial, quantidadeDeFormigas, pesoAlfa, pesoFeromonios):
    matrizFeromoniosAtual = matrizFeromoniosInicial
    for i in range(quantidadeDeFormigas):
        matrizFeromoniosAtual = caminho(matrizDist, matrizFeromoniosAtual, verticeInicial, pesoAlfa, pesoFeromonios)
    
    verticeAtual = verticeInicial
    caminhoFinal = []
    distCaminhoFinal = 0
    listaVerticesPassados = []
    for i in range(len(matrizDist)):
        if i == verticeInicial:
            listaVerticesPassados.append(True)
        else:
            listaVerticesPassados.append(False)

    for i in range(len(matrizDist)):
        #Decidindo melhor vizinho
        melhorVizinho = matrizFeromonios[verticeAtual][verticeAtual]
        proxVertice = verticeAtual
        for j in range(len(matrizDist[verticeAtual])):
            if not listaVerticesPassados[j]:
                arestaAtual = matrizFeromonios[verticeAtual][j]
                if(arestaAtual > melhorVizinho):
                    melhorVizinho = arestaAtual
                    proxVertice = j
        
        if i < len(matrizDist) - 1:
            distCaminhoFinal += matrizDist[verticeAtual][proxVertice]
            verticeAtual = proxVertice
            caminhoFinal.append(proxVertice)     
        else:
            caminhoFinal.append(verticeInicial)
            distCaminhoFinal += matrizDist[verticeAtual][verticeInicial]
    
    print(caminhoFinal)
    print(distCaminhoFinal)
    

colonia(matrizInput, matrizFeromonios, 0, 10000, 1, 4)

#Com 10000 iterações e os pesos apresentados, as formigas tendem ao caminho [5, 4, 3, 1, 2, 0] com distancia 44.0