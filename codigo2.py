import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

# Função para calcular a nota da autoavaliação
def calcular_nota_autoavaliacao(respostas, pesos):
    soma_ponderada = sum([respostas[i] * pesos[i] for i in range(len(respostas))])
    peso_total = sum(pesos)
    media_ponderada = soma_ponderada / peso_total
    return round(media_ponderada*20,1)  # Escala de 0 a 5

# Função para calcular a nota final
def calcular_nota_final(somativa, projeto, integradora, autoavaliacao):
    if disciplina == "projeto integrador":
        return round((somativa * 0.60)  + (integradora * 0.2) + (autoavaliacao * 0.2),1)
    else:
        return round((somativa * 0.60) + (projeto * 0.20) + (integradora * 0.15) + (autoavaliacao * 0.05),1)

# Interface Streamlit
st.title("Calculadora de Notas - SENAI ADS")

# Entrada de dados do aluno
nome_aluno = st.text_input("Nome do Aluno")
#Entrada nome da disciplina
disciplina = st.text_input("Nome da disciplina")

# Entrada das notas
nota_somativa = st.number_input("Nota Avaliação Somativa", min_value=0, max_value=100, value=75)
nota_projeto = st.number_input("Nota Projeto Integrador", min_value=0, max_value=100, value=85)
nota_integradora = st.number_input("Nota Avaliação Integradora", min_value=0, max_value=100, value=90)

# Entrada das respostas da autoavaliação
respostas_autoavaliacao = []
pesos_autoavaliacao = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

st.subheader("Autoavaliação - Escala de 1 a 5")
for i in range(10):
    resposta = st.slider(f"Pergunta {i + 1}", min_value=1, max_value=5, value=3)
    respostas_autoavaliacao.append(resposta)

# Cálculo da nota da autoavaliação
nota_autoavaliacao = calcular_nota_autoavaliacao(respostas_autoavaliacao, pesos_autoavaliacao)

# Cálculo da nota final
nota_final = calcular_nota_final(nota_somativa, nota_projeto, nota_integradora, nota_autoavaliacao)

# Exibição das notas
st.write(f"Nota da Autoavaliação: {nota_autoavaliacao:.0f}")
st.write(f"Nota Final: {nota_final:.0f}")
filename = f"notas_alunos_{disciplina}.csv"
# Verificar se o arquivo existe antes de tentar ler
if not os.path.exists(filename):
    pd.DataFrame(columns=["Nome", "Somativa", "Projeto", "Integradora", "Autoavaliação", "Nota Final"]).to_csv(filename, index=False)

# Armazenar em CSV
if st.button("Salvar Nota"):
    if nome_aluno:
        dados = {
            "Disciplina":[disciplina],
            "Nome": [nome_aluno],
            "Somativa": [nota_somativa],
            "Projeto": [nota_projeto],
            "Integradora": [nota_integradora],
            "Autoavaliação": [nota_autoavaliacao],
            "Nota Final": [nota_final]
        }
        df = pd.DataFrame(dados)
        df.to_csv(filename, mode="a", index=False, header=False)
        st.success("Nota salva com sucesso!")
    else:
        st.warning("Por favor, insira o nome do aluno antes de salvar.")

# Exibir gráfico de barras
if st.button("Exibir Gráfico"):
    df = pd.read_csv(filename)
    if df.empty:
        st.warning("Nenhum dado disponível para exibir.")
    else:
        plt.figure(figsize=(10, 6))
        plt.bar(df["Nome"], df["Nota Final"], color='blue')
        plt.xlabel("Aluno")
        plt.ylabel("Nota Final")
        plt.title("Notas Finais dos Alunos")
        plt.xticks(rotation=45)
        st.pyplot(plt)
