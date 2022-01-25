import streamlit as st
import asyncio
import plotly.express as px
import pandas as pd
import numpy as np

from algogen import AlgoritmoGenetico
from algogen.utils import stringToList, listToString

st.set_page_config(page_title="Algoritmo Genético", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")
globalState = {}


def dashboard():
    st.markdown("# Algoritmo Genético")

    globalState["executar"] = False
    sidebar(st.sidebar)

    if globalState["executar"]:
        executa()
        imprimeAvaliacao(st)

def sidebar(sidebar):
    sidebar.markdown("# Parâmetros do Algoritmo")

    globalState["tamPop"] = sidebar.slider("Tamanho da População", 10, 100, 10, step=2)
    globalState["numGer"] = sidebar.slider("Número de Gerações", 5, 1000, 10)
    globalState["probCross"] = sidebar.slider("Probabilidade de Crossover", 0.70, 1.00, 0.8)
    globalState["probMut"] = sidebar.slider("Probabilidade de Mutação por Gene", 0.0, 0.05, 0.02)
    globalState["elitismo"] = sidebar.checkbox("Elitismo")
    globalState["tamTabuleiro"] = sidebar.slider("Tamanho do Tabuleiro", 4, 32, 4)

    if sidebar.button('Executar Algoritmo'):
        globalState["executar"] = True


def printLines(st, x, by, title=None, color=None):
    fig = px.line(x, y=by, color=color, title=title)
    fig.update_layout(hovermode="x")
    st.plotly_chart(fig, use_container_width=True)


def executa():
    algogen = AlgoritmoGenetico.AlgoritmoGenetico(
        globalState["tamPop"], 
        globalState["numGer"], 
        globalState["probCross"], 
        globalState["probMut"], 
        globalState["elitismo"], 
        globalState["tamTabuleiro"]
    )

    adaptacaoGeracoes, mediaAdaptacaoGeracoes, melhorIndividuo, melhorAdaptacao = algogen.fit()
    globalState["adaptacaoGeracoes"] = adaptacaoGeracoes
    globalState["mediaAdaptacaoGeracoes"] = mediaAdaptacaoGeracoes
    globalState["melhorIndividuo"] = melhorIndividuo
    globalState["melhorAdaptacao"] = melhorAdaptacao


def imprimeAvaliacao(st):
    st.markdown("### Melhor Adaptação para cada Geração")
    df_adaptacao = pd.DataFrame(globalState["adaptacaoGeracoes"], columns=["adaptacao"])
    printLines(st, df_adaptacao, "adaptacao")

    st.markdown("### Adaptação Média para cada Geração")
    df_adaptacao = pd.DataFrame(globalState["mediaAdaptacaoGeracoes"], columns=["adaptacao"])
    printLines(st, df_adaptacao, "adaptacao")

    st.markdown("### Melhor Indivíduo")
    listaIndividuo = []
    for elem in stringToList(globalState["melhorIndividuo"], globalState["tamTabuleiro"]):
        novaLinha = [ ( [50,50,50] if k == elem else [230,230,230] ) for k in range(0, globalState["tamTabuleiro"])]
        listaIndividuo.append(novaLinha)
    listaIndividuo = np.array(listaIndividuo, dtype=np.uint8)

    fig = px.imshow(
        listaIndividuo, 
        x=list(range(1, globalState["tamTabuleiro"]+1)), 
        y=list(range(1, globalState["tamTabuleiro"]+1)),
        width=400, height=400)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    st.plotly_chart(fig, use_container_width=False)



dashboard()