import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Terminal de Análise Financeira")

ativos_map = {
    "IBOV": "^BVSP",
    "Dólar": "USDBRL=X",
    "Bitcoin": "BTC-USD",
    "Ouro": "GC=F",
    "SELIC (B5P211)": "B5P211.SA"
}

# --- Sidebar ---
st.sidebar.header("Configurações")
ativos_selecionados = st.sidebar.multiselect("Selecione os ativos:", list(ativos_map.keys()), default=["IBOV", "Dólar"])
periodo = st.sidebar.select_slider("Período:", options=["1mo", "3mo", "6mo", "1y", "5y", "10y"], value="3mo")

if st.sidebar.button("Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

# --- Funções ---
@st.cache_data(ttl=3600)
def buscar_dados(tickers_selecionados, period):
    codigos = [ativos_map[ativo] for ativo in tickers_selecionados]
    df = yf.download(codigos, period=period)['Close']
    return df.ffill().dropna()

@st.cache_data(ttl=3600)
def calcular_correlacao_historica(tickers_selecionados):
    ordem_desejada = ["10y", "5y", "1y", "6mo", "3mo", "1mo"]
    resultados = []
    for p in ordem_desejada:
        codigos = [ativos_map[a] for a in tickers_selecionados]
        df = yf.download(codigos, period=p)['Close'].ffill().dropna()
        if len(df.columns) >= 2:
            corr = df.iloc[:, 0].corr(df.iloc[:, 1])
            resultados.append({"Periodo": p, "Correlação": corr})
    
    df_result = pd.DataFrame(resultados)
    df_result['Periodo'] = pd.Categorical(df_result['Periodo'], categories=ordem_desejada, ordered=True)
    return df_result.sort_values('Periodo')

# --- Interface ---
if len(ativos_selecionados) >= 2:
    dados = buscar_dados(ativos_selecionados, periodo)
    
    # 1. Gráfico de Evolução (Base 100)
    st.subheader("Evolução dos Ativos (Base 100)")
    dados_norm = (dados / dados.iloc[0]) * 100
    fig_line = px.line(dados_norm, labels={'value': 'Desempenho (%)', 'index': 'Data'})
    fig_line.update_layout(hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # 2. Gráfico de Correlação Direcional
    st.subheader("Evolução Histórica da Correlação")
    df_hist = calcular_correlacao_historica(ativos_selecionados)
    media_calc = df_hist['Correlação'].mean()
    
    # Definimos a cor explicitamente para evitar erros do Plotly
    df_hist['Cor'] = df_hist['Correlação'].apply(lambda x: 'red' if x >= 0 else 'blue')
    
    fig_hist = px.bar(
        df_hist, 
        x="Periodo", 
        y="Correlação",
        title=f"Correlação Direcional (Média do Período: {media_calc:.2f})"
    )
    
    # Aplica a cor manualmente em cada barra
    fig_hist.update_traces(marker_color=df_hist['Cor'])
    
    # Força o eixo Y para ser fixo de -1.1 a 1.1 e garante a linha zero central
    fig_hist.update_layout(
        yaxis=dict(range=[-1.1, 1.1], zeroline=True, zerolinecolor="black", zerolinewidth=2)
    )
    
    # Adiciona a linha de referência da média
    fig_hist.add_hline(y=media_calc, line_dash="dash", line_color="green", annotation_text="Média")
    
    st.plotly_chart(fig_hist, use_container_width=True)

elif len(ativos_selecionados) == 1:
    st.warning("Selecione pelo menos 2 ativos para calcular a correlação.")
else:
    st.info("Selecione os ativos na barra lateral para começar.")