import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Título do aplicativo
st.title("Previsão Inteligente - Aviator1")

# Entrada dos dados do usuário
st.subheader("Inserir valores (ex: 1.25, 2.34, 3.0)")
user_input = st.text_area("Valores separados por vírgula:", height=150)

# Botão para apagar os dados
if st.button("Apagar dados"):
    st.experimental_rerun()

# Processar os dados inseridos
if user_input:
    try:
        # Converter texto em lista de floats
        values = [float(x.strip().replace('x', '')) for x in user_input.split(',') if x.strip()]
        df = pd.DataFrame({'Valores': values})
        
        # Gráfico de tendência
        st.subheader("Gráfico com Linha de Tendência")
        x = np.arange(len(values)).reshape(-1, 1)
        y = np.array(values).reshape(-1, 1)
        model = LinearRegression().fit(x, y)
        trend = model.predict(x)

        fig, ax = plt.subplots()
        ax.plot(values, label="Valores Inseridos", marker='o')
        ax.plot(trend, label="Tendência", linestyle='--')
        ax.set_xlabel("Tentativas")
        ax.set_ylabel("Multiplicador")
        ax.legend()
        st.pyplot(fig)

        # Exibir estatísticas
        st.subheader("Estatísticas")
        media_geral = round(np.mean(values), 2)
        media_ultimos_10 = round(np.mean(values[-10:]), 2)
        minimo_ultimos_10 = round(np.min(values[-10:]), 2)
        st.markdown(f"**Média geral:** {media_geral}x")
        st.markdown(f"**Média dos últimos 10:** {media_ultimos_10}x")
        st.markdown(f"**Mínimo dos últimos 10:** {minimo_ultimos_10}x")

        # Previsão
        st.subheader("Previsão Inteligente")
        st.markdown(f"**Próximo valor provável mínimo:** {minimo_ultimos_10}x")
        st.markdown(f"**Próxima média provável:** {media_ultimos_10}x")

        # Alerta de risco
        st.subheader("Alertas")
        ultimos = values[-5:]
        if all(v < 2 for v in ultimos):
            st.warning("Alerta: Muitos valores baixos seguidos! Possível queda forte em breve.")
        elif values[-1] > 10 or values[-1] > media_geral * 2:
            st.warning("Alerta: Valor alto recente! Próxima rodada pode ser de queda.")

    except Exception as e:
        st.error("Erro ao processar os dados. Verifique o formato dos valores.")
