import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from algogen import AlgoritmoGenetico
from algogen.utils import stringToList, listToString

st.set_page_config(page_title="Algoritmo Genético", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")
globalState = {}


def dashboard():
    st.markdown("# Algoritmo Genético")

    barra_progresso = st.progress(0)

    globalState["adaptacaoGeracoes"] = []
    globalState["mediaAdaptacaoGeracoes"] = []
    globalState["melhorIndividuo"] = []
    globalState["melhorAdaptacao"] = []
    globalState["executar"] = False
    sidebar(st.sidebar)

    if globalState["executar"]:
        for i in range(0,globalState["quantTentativas"]):
            executa()
            barra_progresso.progress( (i+1)/globalState["quantTentativas"] )

        barra_progresso.empty()
        imprimeAvaliacao(st)

        
def sidebar(sidebar):
    sidebar.markdown("# Parâmetros do Algoritmo")

    globalState["quantTentativas"] = sidebar.slider("Quantidade de tentativas", 1, 20, 1)
    globalState["tamPop"] = sidebar.slider("Tamanho da População", 10, 200, 10, step=2)
    globalState["numGer"] = sidebar.slider("Número de Gerações", 5, 5000, 100)
    globalState["probCross"] = sidebar.slider("Probabilidade de Crossover", 70.0, 100.0, 80.0, step=1.0) / 100
    globalState["probMut"] = sidebar.slider("Probabilidade de Mutação por Gene", 0.0, 5.0, 2.0, step=0.5) / 100
    globalState["elitismo"] = sidebar.checkbox("Elitismo")
    globalState["tamTabuleiro"] = sidebar.slider("Tamanho do Tabuleiro", 4, 32, 4)


    if sidebar.button('Executar Algoritmo'):
        globalState["executar"] = True


def printLines(st, x, title=None, color=None):
    fig = px.line(x, color=color, title=title)
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
    globalState["adaptacaoGeracoes"].append( adaptacaoGeracoes )
    globalState["mediaAdaptacaoGeracoes"].append( mediaAdaptacaoGeracoes )
    globalState["melhorIndividuo"].append( melhorIndividuo )
    globalState["melhorAdaptacao"].append( melhorAdaptacao )


def imprimeAvaliacao(st):
    st.markdown("### Melhor Adaptação para cada Geração")
    df_adaptacao = pd.DataFrame(globalState["adaptacaoGeracoes"]).transpose()
    printLines(st, df_adaptacao)

    st.markdown("### Adaptação Média para cada Geração")
    df_adaptacao = pd.DataFrame(globalState["mediaAdaptacaoGeracoes"]).transpose()
    printLines(st, df_adaptacao)

    st.markdown("### Melhor Indivíduo da Última Geração")
    for idx, tentativa in enumerate(globalState["melhorIndividuo"]):
        listaIndividuo = []
        for elem in stringToList(tentativa, globalState["tamTabuleiro"]):
            novaLinha = [ ( [50,50,50] if k == elem else [230,230,230] ) for k in range(0, globalState["tamTabuleiro"])]
            listaIndividuo.append(novaLinha)
        listaIndividuo = np.array(listaIndividuo, dtype=np.uint8)

        fig = px.imshow(
            listaIndividuo, 
            x=list(range(1, globalState["tamTabuleiro"]+1)), 
            y=list(range(1, globalState["tamTabuleiro"]+1)),
            width=400, height=400,
            title=f"Tentativa {idx} [adaptação = { globalState['adaptacaoGeracoes'][idx][-1] }]")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)

        st.plotly_chart(fig, use_container_width=False)



dashboard()