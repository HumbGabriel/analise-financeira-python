import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. EXTRAÇÃO E LIMPEZA DE DADOS
# ==========================================
print("Baixando dados do Yahoo Finance...")
ibov = yf.download("^BVSP", period="1y")
dolar = yf.download("USDBRL=X", period="1y")

# Tratamento do IBOV
ibov = ibov.dropna()
df_analise = ibov[['Close']].copy()
df_analise.columns = ['Fechamento_IBOV']

# Tratamento do Dólar e Mesclagem
df_analise['Fechamento_Dolar'] = dolar['Close']
df_analise = df_analise.ffill()  # Preenche buracos de feriados/finais de semana

print("\n--- Primeiras linhas dos dados mesclados ---")
print(df_analise.head())

# ==========================================
# 2. ANÁLISE ESTATÍSTICA
# ==========================================
correlacao = df_analise['Fechamento_IBOV'].corr(df_analise['Fechamento_Dolar'])

print(f"\n--- Resultado da Análise ---")
print(f"O coeficiente de correlação (IBOV x Dólar) é: {correlacao:.2f}")

if correlacao > 0:
    print("Conclusão: Existe uma correlação POSITIVA neste período.")
elif correlacao < 0:
    print("Conclusão: Existe uma correlação NEGATIVA neste período.")
else:
    print("Conclusão: Não há correlação linear clara.")

# ==========================================
# 3. VISUALIZAÇÃO PROFISSIONAL
# ==========================================
print("\nGerando gráfico...")
plt.close('all')  # Limpa qualquer gráfico "preso" na memória

fig, ax1 = plt.subplots(figsize=(12, 6))

# Eixo 1: IBOV (Linha Azul, eixo à esquerda)
ax1.plot(df_analise.index, df_analise['Fechamento_IBOV'], color='#004a99', label='IBOV', linewidth=2)
ax1.set_ylabel('IBOV (Pontos)', color='#004a99', fontsize=12, fontweight='bold')
ax1.set_xlabel('Data', fontsize=12)

# Eixo 2: Dólar (Linha Vermelha Tracejada, eixo à direita)
ax2 = ax1.twinx()
ax2.plot(df_analise.index, df_analise['Fechamento_Dolar'], color='red', linestyle='--', label='Dólar', linewidth=2)
ax2.set_ylabel('Dólar (USD/BRL)', color='red', fontsize=12, fontweight='bold')

# Adiciona a caixa de texto com a correlação APENAS UMA VEZ
ax1.text(0.05, 0.95, f'Correlação de Pearson: {correlacao:.2f}', 
         transform=ax1.transAxes, fontsize=12, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray'))

# Ajustes finais de layout e grade
plt.title('Dinâmica de Mercado: IBOV vs Dólar (Últimos 1 ano:)', fontsize=16, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)
fig.autofmt_xdate(rotation=45) # Gira as datas para não encavalarem
plt.tight_layout()

# Exibe o gráfico limpo
plt.show()