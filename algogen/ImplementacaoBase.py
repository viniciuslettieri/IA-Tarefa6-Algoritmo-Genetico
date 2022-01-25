import pandas as pd
import numpy as np
import bisect
import random
import math


def tabuleiro(N, Q):
  return [ [random.randrange(0, N) for j in range(0, N)] for i in range(0, Q) ]

def todosVizinhos(T):
  N = len(T)
  Vizinhos = []  
  for i in range(0, N):
    Posicao = T[i]
    for j in range(0, N):
      if (j != Posicao):
        novoT = T.copy()
        novoT[i] = j
        Vizinhos.append(novoT)
  return Vizinhos

def umVizinho(T):
  return random.choice(todosVizinhos(T))

def numeroAtaques(T):
  N = len(T)
  numAtaques = 0
  for i in range(0, N-1):
    for j in range (i+1, N):
      if (T[i] == T[j]):
        numAtaques += 1
      if (T[i] == T[j] - (j-i)):
        numAtaques += 1
      if (T[i] == T[j] + (j-i)):
        numAtaques += 1
  return numAtaques