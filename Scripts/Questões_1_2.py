# Função da questão 1
def IntervalosDistintos(ListaConjuntos):
    
    intervalosDistintos = []
    lista = []
    
    # Criando os intervalos dos conjuntos
    for i in ListaConjuntos:
        lista.append(list(range(i[0],i[1])))
    for l in lista:
        l.pop(0)
    
    for l in lista:
        for numero in l:
            if numero not in intervalosDistintos:
                intervalosDistintos.append(numero)
    
    intervalosDistintos.sort()
    
    # Numeros Consecutivos - sem o import mit iterpools
    intervalos = []

    primeiroElemento = intervalosDistintos.pop(0)
    intervalos.append([primeiroElemento])

    for numero in intervalosDistintos:
        for lis in intervalos:

            consecutivo = lis[-1] + 1

            if numero == consecutivo:
                lis.append(numero)

            if numero != consecutivo:
                if lis == intervalos[-1]:
                    intervalos.append([numero])
                    # iterar prox lista dps de add nova lista
                    break
                else:
                    #iterar prox lista
                    continue
            # iterar prox numero
            continue
                 
    # Numeros Consecutivos - com o import mit iterpools = quantidadeIntervalos no comentario abaixo
    # quantidadeIntervalos = [list(group) for group in mit.consecutive_groups(intervalosDistintos)]
    
    print('Intervalos Distintos :', intervalos)
    print('Quantidade de Intervalos Distintos :', len(intervalos))
    
    return len(intervalos)
############################################################################################################################################
# Função Questão 2

def Q2(numeroA,numeroB):
    
    numeros = [numeroA,numeroB]
    
    numeroMax = max(numeros)
    numeroMin = min(numeros)
    #print(numeroMax,'-',numeroMin)
    
    palavra = ""
    
    # Começo da Sequencia com caracter a
    if numeroMax == numeroA:
        if numeroMax%numeroMin == 0:
            while len(palavra) < (numeroA+numeroB):
                
                for i in range(2):
                    if(palavra.count('a') < numeroA):
                        palavra = palavra + 'a'
                        if 'aaa' in palavra:
                            return 'Não Foi possivel criar uma sequencia!'
                
                if(palavra.count('b') < numeroB):
                    palavra = palavra + 'b'
                    if 'bbb' in palavra:
                            return 'Não Foi possivel criar uma sequencia!'
        else:
            for i in range(2):
                   if(palavra.count('a') < numeroA):
                        palavra = palavra + 'a'
                        if 'aaa' in palavra:
                            return 'Não Foi possivel criar uma sequencia!'
            
            while len(palavra) < (numeroA+numeroB):
                
                if numeroMax - numeroMin < 4:
                
                    if(palavra.count('b') < numeroB):
                        palavra = palavra + 'b'
                        if 'bbb' in palavra:
                                return 'Não Foi possivel criar uma sequencia!'

                    if(palavra.count('a') < numeroA):
                        palavra = palavra + 'a'
                        if 'aaa' in palavra:
                                return 'Não Foi possivel criar uma sequencia!'
                
                else:
                    if(palavra.count('b') < numeroB):
                        palavra = palavra + 'b'
                        if 'bbb' in palavra:
                                return 'Não Foi possivel criar uma sequencia!'
                            
                    
                    for i in range(2):
                           if(palavra.count('a') < numeroA):
                                palavra = palavra + 'a'
                                if 'aaa' in palavra:
                                    return 'Não Foi possivel criar uma sequencia!'
                        
    
    
    # Começo da Sequencia com caracter b
    if numeroMax == numeroB:
        if numeroMax%numeroMin == 0:
            while len(palavra) < (numeroA+numeroB):
                
                for i in range(2):
                    if(palavra.count('b') < numeroB):
                        palavra = palavra + 'b'
                        if 'bbb' in palavra:
                            return 'Não Foi possivel criar uma sequencia!'
                
                if(palavra.count('a') < numeroA):
                    palavra = palavra + 'a'
                    if 'aaa' in palavra:
                            return 'Não Foi possivel criar uma sequencia!'
        else:
            for i in range(2):
                   if(palavra.count('b') < numeroB):
                        palavra = palavra + 'b'
                        if 'bbb' in palavra:
                            return 'Não Foi possivel criar uma sequencia!'
            
            while len(palavra) < (numeroA+numeroB):
                
                if numeroMax - numeroMin < 4:
                    if(palavra.count('a') < numeroA):
                        palavra = palavra + 'a'
                        if 'aaa' in palavra:
                                return 'Não Foi possivel criar uma sequencia!'

                    if(palavra.count('b') < numeroB):
                        palavra = palavra + 'b'
                        if 'bbb' in palavra:
                                return 'Não Foi possivel criar uma sequencia!'
                else:
                    if(palavra.count('a') < numeroA):
                        palavra = palavra + 'a'
                        if 'aaa' in palavra:
                                return 'Não Foi possivel criar uma sequencia!'

                    
                    for i in range(2):
                           if(palavra.count('b') < numeroB):
                                palavra = palavra + 'b'
                                if 'bbb' in palavra:
                                    return 'Não Foi possivel criar uma sequencia!'

            
   
    #if numeroMax == numeroB:
        
    return palavra







