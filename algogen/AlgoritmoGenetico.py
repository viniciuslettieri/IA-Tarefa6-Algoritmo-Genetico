import pandas as pd
import numpy as np
import bisect
import random
import math

from algogen.utils import stringToList, listToString
from algogen.ImplementacaoBase import tabuleiro, numeroAtaques


class AlgoritmoGenetico:
    def __init__(self, tamPop, numGer, probCross, probMut, elitismo, tamTabuleiro=4):
        self.tamPop = tamPop
        self.numGer = numGer
        self.probCross = probCross
        self.probMut = probMut
        self.elitismo = elitismo
        self.tamTabuleiro = tamTabuleiro
    
    def inicializacao(self, N, Q = 4):
        return [ listToString(individuo, Q) for individuo in tabuleiro(Q,N) ]
    
    def adaptacao(self, tString, N):
        listT = stringToList(tString, N)
        return 1/(1 + numeroAtaques(listT))

    def roletaViciada(self, P, N):
        funcaoAdaptacao = []
        for individuo in P:
            funcaoAdaptacao.append( self.adaptacao(individuo, N) )

        soma = sum(funcaoAdaptacao)
        proporcao = []
        for individuo in P:
            proporcao.append( self.adaptacao(individuo, N) / soma )

        return proporcao, funcaoAdaptacao

    def intermediaria(self, P, N):
        proporcoes = self.roletaViciada(P, N)
        proporcoesAcumulada = np.cumsum(proporcoes)
        matingPool = []

        for i in range(0, len(P)):
            aleatorio = random.uniform(0, 1)
            idx = bisect.bisect_left(proporcoesAcumulada, aleatorio)
            matingPool.append( P[idx] )

        return matingPool

    def crossover(self, A, B, prob):
        aleatorio = random.uniform(0, 1)
        if aleatorio <= prob:
            corte = random.randrange(1, len(A))

            A1 = A[0:corte]
            A2 = A[corte:]
            B1 = B[0:corte]
            B2 = B[corte:]
            
            A = A1 + B2
            B = B1 + A2

        return [A, B]

    def mutacao(self, A, probBit):
        novoA = ""
        for i in range(0, len(A)):
            aleatorio = random.uniform(0, 1)
            if aleatorio <= probBit:
                novoA += '1' if A[i] == '0' else '0'
            else:
                novoA += A[i]

        return novoA

    def fit(self):
        populacao = self.inicializacao(self.tamPop, self.tamTabuleiro)

        adaptacaoGeracoes = []
        mediaAdaptacaoGeracoes = []

        for i in range(0, self.numGer):
            # Roleta Viciada
            probs, funcaoAdaptacao = self.roletaViciada(populacao, self.tamTabuleiro)

            # Pegando o melhor individuo pro elitismo
            maxprop = max(probs)
            idxmax = probs.index(maxprop)
            individuomax = populacao[idxmax]

            # Adicionando no histórico
            adaptacaoGeracoes.append(max(funcaoAdaptacao))
            mediaAdaptacaoGeracoes.append(sum(funcaoAdaptacao) / len(funcaoAdaptacao))

            # Gerando Mating Pool
            populacao = self.intermediaria(populacao, self.tamTabuleiro)

            # Crossover
            popSet = populacao.copy()
            novaPopulacao = []
            while len(popSet) > 0:
                A, B = random.sample(popSet, 2)
                popSet.remove(A)
                popSet.remove(B)
                novoA, novoB = self.crossover(A, B, self.probCross)
                novaPopulacao.append(novoA)
                novaPopulacao.append(novoB)
                populacao = novaPopulacao

            # Mutação
            for idx, individuo in enumerate(populacao):
                populacao[idx] = self.mutacao(individuo, self.probMut)

            # Elitismo
            if self.elitismo:
                eliminado = random.choice(range(0, len(populacao)))
                populacao[eliminado] = individuomax

        # Adicionando último ao histórico
        probs, funcaoAdaptacao = self.roletaViciada(populacao, self.tamTabuleiro)
        adaptacaoGeracoes.append(max(funcaoAdaptacao))
        mediaAdaptacaoGeracoes.append(sum(funcaoAdaptacao) / len(funcaoAdaptacao))

        melhorIndividuo = populacao[ funcaoAdaptacao.index(max(funcaoAdaptacao)) ]
        melhorAdaptacao = max(funcaoAdaptacao)
        
        return [adaptacaoGeracoes, mediaAdaptacaoGeracoes, melhorIndividuo, melhorAdaptacao]
    