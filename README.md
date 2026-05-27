# Terminal de Análise Quantitativa Financeira

Este terminal é uma ferramenta robusta desenvolvida em Python para análise de correlação e comportamento de ativos financeiros. Diferente de soluções estáticas, este projeto foi desenhado para ser um motor de análise extensível, permitindo o estudo de diversos pares de ativos e indicadores macroeconômicos.

## 📈 Propósito do Projeto
A ferramenta foi criada para preencher a lacuna entre dados brutos e tomada de decisão. Através da computação de correlações dinâmicas, o terminal identifica mudanças em regimes de mercado, permitindo que o usuário visualize como diferentes ativos se comportam em cenários de estresse ou euforia.

## 🛠 Arquitetura e Funcionalidades
- **Análise Multiativos:** Motor flexível capaz de processar não apenas IBOV e Dólar, mas qualquer par de ativos disponível via `yfinance`.
- **Dinâmica Temporal:** Cálculo de correlação em múltiplas janelas (1mo, 3mo, 6mo, 1y, 5y, 10y), facilitando a identificação de reversão à média.
- **Visualização Inteligente:** Dashboards interativos que categorizam regimes de correlação (direta vs. inversa) com indicadores visuais intuitivos.
- **Data-Driven:** Estrutura pronta para integração com indicadores macroeconômicos (Selic, Inflação, etc.) e indicadores técnicos.

## 🚀 Como rodar localmente

1. Clone o repositório:
   ```bash
   git clone [https://github.com/HumbGabriel/analise-financeira-python.git](https://github.com/HumbGabriel/analise-financeira-python.git)
