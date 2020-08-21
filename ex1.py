from scipy.stats import chisquare

def aplica_fit(observed_freq,original_freq):# usa chi-square para testar as 26 possíveis chaves
    for i in range(26):
        r=chisquare(observed_freq,original_freq)
        if i==0:
            minimo=r[0]
            chave=0
        else:
            if r[0]<minimo:
                minimo=r[0]
                chave=i
        observed_freq.append(observed_freq[0])
        del observed_freq[0]
    return chave

def tenta_chaves():
    chars = {}
    original_freq=[8.12,1.49,2.71,4.32,12.02,2.3,2.03,5.92,7.31,0.1,0.69,3.98,2.61,6.95,7.68,1.82,0.11,6.02,6.28,9.1,2.88,1.11,2.09,0.17,2.11,0.07]
    texto=""
    outros_carac=[]
    numchars=0
    numcharsparcial=0
    possiveis_textos=[]
    possiveis=[]
    contador=0
    with open("texto.txt") as arq:
        for line in arq:
            for i in line:
                if 97<=ord(i)<=122:
                    numchars+=1
                    texto+=i
                else:
                    outros_carac.append([contador,i])
                contador+=1
    for i in range(1,numchars):#todas os tamanhos possiveis de chave
        total=0
        for l in range(i):#todas as sequencias com salto da chave
            for j in range(97,123):
                chars[chr(j)]=0
            numcharsparcial=0
            for k in range(l,numchars,i):#pega a sequencia
                x=texto[k]
                chars[x]+=1
                numcharsparcial+=1
                freq=0
            for v in chars.values():#aplica fórmula de index of coincidence
                freq+=(v*(v-1)/(numcharsparcial*(numcharsparcial-1)))
            if 0.04>freq or 0.09<freq:#margens para ignorar chaves que fogem muito da média
                total=0
                break
            total+=freq
        a=total/i#media das frequencias para o fluxo
        if 0.06<=a<=0.075:#margens
            print(f"Possível tamanho de chave = {i}")
            possiveis.append(i)
    contador=0
    while contador!=len(possiveis): #retira múltiplos
        inicial=possiveis[contador]
        possiveis=[item for item in possiveis if item%inicial!=0 or item==inicial]
        contador+=1
    for tamanho_chave in possiveis:
        print("Decifrando chave de tamanho =",tamanho_chave)
        chave=""
        texto_retorno=[None]*numchars
        for inicio in range(tamanho_chave):#cada fluxo
            for j in range(97,123):
                chars[chr(j)]=0
            for k in range(inicio,numchars,tamanho_chave):#pega a sequencia
                x=texto[k]
                chars[x]+=1
            coef=aplica_fit(list(chars.values()),original_freq) #acha o caracter da chave
            chave+=chr(coef+97)
            for k in range(inicio,numchars,tamanho_chave):
                texto_retorno[k]=chr((ord(texto[k])-97-coef)%26+97)
        parcial=""
        contador_carac=0
        contador_lista=0
        tam_lista=len(outros_carac)
        for k in texto_retorno:
            while contador_lista < tam_lista and contador_carac==outros_carac[contador_lista][0]:
                parcial+=outros_carac[contador_lista][1]
                contador_lista+=1
                contador_carac+=1
            parcial+=k
            contador_carac+=1
        possiveis_textos.append((chave,parcial))    
    for n,i in enumerate(possiveis_textos,1):
        print("Texto",n)
        print("Chave =",i[0])
        print(i[1])
        #pass
    return possiveis
tenta_chaves()
