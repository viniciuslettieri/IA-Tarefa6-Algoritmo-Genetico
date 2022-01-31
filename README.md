# Tarefa 6 de IA - Algoritmo Genético

Esse repositório consiste da Tarefa 6 da disciplina de Inteligência Artificial 2021.2, cujo objetivo é a implementação de um algoritmo genético para a resolução do problema das 4 rainhas.

Nele encontraremos um módulo chamado ```algogen```, que possui a implementação completa da classe ```AlgoritmoGenetico```. Neste diretório teremos a classe principal ```AlgoritmoGenetico```, o arquivo ```ImplementacaoBase```, que possui as funções básicas do funcionamento do jogo descritas no trabalho, e também o ```utils```, que possui as funções auxiliares para funcionamento do jogo.

Nosso algoritmo genético é uma classe que pode ser instanciada passando seus atributos básicos, e o único método que precisa ser chamado para executar o algoritmo é o ```.fit()```.

Em termos de algoritmo para ser avaliado, todos os códigos estão neste módulo ```algogen```, contudo, para facilitar a testagem do algoritmo criamos um dashboard no arquivo ```dashboard.py```.

Para **executar o dashboard**, é necessário instalar as bibliotecas em ```requirements``` e executar na raiz do diretório ```streamlit run dashboard.py``` e acessar o localhost na porta definida. Caso não deseje passar pelo processo, esse repositório está com deploy automático e pode ser acessado na seguinte url: **https://algoritmo-genetico.herokuapp.com/**
