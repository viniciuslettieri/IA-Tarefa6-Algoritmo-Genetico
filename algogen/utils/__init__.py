import pandas as pd
import numpy as np
import bisect
import random
import math


def stringToList(tString, N):
  K = math.ceil(math.log2(N))
  tList = []
  for i in range(0, N*K, K):
    tList.append( int( tString[i : i+K], 2 ) )

  return tList

def listToString(tList, N):
  K = math.ceil(math.log2(N))
  tString = ""
  for i in range(0, N):
    tString += format(tList[i], f"0{K}b")

  return tString