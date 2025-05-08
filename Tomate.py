import streamlit as st import matplotlib.pyplot as plt import numpy as np import pandas as pd from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Aviator1 - Previsão Inteligente", layout="wide")

st.header("Previsão Inteligente - Aviator1")

Entrada dos dados do usuário

st.subheader("1. Inserir Dados de Rodadas (ex: 1.25x)") dados_input = st.text_area("Cole os valores separados por linhas", height=200)

Processar dados

if dados_input: try: dados = [float(x.replace('x','').strip()) for x in dados_input.strip().splitlines() if x.strip()] df = pd.DataFrame({'Rodada': range(1, len(dados)+1), 'Valor': dados})

# Gráfico
    st.subheader("2. Análise Visual dos Dados")
    fig, ax = plt.subplots(figsize=(12, 4))
    cores = ['red' if v <= 1.5 else 'orange' if v <= 2.0 else 'green' for v in df['Valor']]
    ax.bar(df['Rodada'], df['Valor'], color=cores)
    ax.axhline(y=2.0, color='blue', linestyle='--', label='Limite Médio')
    ax.set_xlabel("Rodada")
    ax.set_ylabel("Multiplicador (x)")
    ax.set_title("Gráfico das Últimas Rodadas")
    ax.legend()
    st.pyplot(fig)

    # Previsão Inteligente
    st.subheader("3. Previsão Inteligente")
    ultimos_10 = dados[-10:] if len(dados) >= 10 else dados
    media_simples = np.mean(ultimos_10)

    # Remover outliers (acima de 10x) para média ponderada
    dados_sem_extremos = [v for v in ultimos_10 if v <= 10]
    media_ponderada = round(np.mean(dados_sem_extremos), 2) if dados_sem_extremos else media_simples

    # Prever mínima com base na sequência
    ultimos_3 = ultimos_10[-3:] if len(ultimos_10) >= 3 else ultimos_10
    alertas = []
    previsao_min = 1.0
    if all(v < 1.3 for v in ultimos_3):
        alertas.append("Alerta de possível explosão: 3 quedas consecutivas abaixo de 1.3x")
        previsao_min = 2.5
    elif any(v > 10 for v in ultimos_3):
        alertas.append("Alerta de queda provável após valor extremo acima de 10x")
        previsao_min = 1.0
    elif sum(1 for v in ultimos_3 if v > 2.6) >= 2:
        alertas.append("Muitos valores acima de 2.6x: tendência de queda próxima")
        previsao_min = 1.1

    st.write(f"**Valor mínimo provável:** {previsao_min:.2f}x")
    st.write(f"**Valor médio estimado:** {media_ponderada:.2f}x")

    if alertas:
        st.warning("\n".join(alertas))

    # Apagar dados
    if st.button("Apagar Dados"):
        st.experimental_rerun()

except Exception as e:
    st.error("Erro ao processar os dados. Verifique se estão no formato correto.")

else: st.info("Insira os dados acima para iniciar a análise.")

