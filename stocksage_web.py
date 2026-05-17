import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="StockSage AI", page_icon="📈", layout="wide")
st.title("📊 StockSage AI - Pro")
st.markdown("**Fundamental Analysis • Portfolio • Smart AI Scoring**")

tab1, tab2, tab3 = st.tabs(["📈 Stock Analysis", "💼 Portfolio", "🔔 Alerts"])

# ===================== TAB 1: STOCK ANALYSIS =====================
with tab1:
    st.sidebar.header("Stock Analysis")
    tickers_input = st.sidebar.text_input("Enter Stock Tickers", "RELIANCE.NS, TCS.NS, HDFCBANK.NS")
    
    if st.sidebar.button("🚀 Analyze Stocks", type="primary"):
        tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
        
        for ticker in tickers[:8]:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                hist = stock.history(period="1y")
                
                current_price = info.get('currentPrice') or info.get('previousClose', 0)
                pe = info.get('trailingPE')
                roe = info.get('returnOnEquity')
                debt = info.get('debtToEquity')
                eps_g = info.get('earningsGrowth')
                div = info.get('dividendYield')
                name = info.get('longName', ticker)
                
                # ================== AI SCORING LOGIC ==================
                score = 0
                reasons = []
                
                if pe and pe < 22:
                    score += 25
                    reasons.append("✅ Attractive Valuation (Low P/E)")
                elif pe and pe < 30:
                    score += 15
                    reasons.append("⚠️ Reasonable Valuation")
                else:
                    reasons.append("❌ High Valuation")
                
                if roe and roe > 0.15:
                    score += 25
                    reasons.append("✅ Excellent ROE (>15%)")
                elif roe and roe > 0.10:
                    score += 15
                    reasons.append("⚠️ Good ROE")
                
                if debt and debt < 0.6:
                    score += 20
                    reasons.append("✅ Strong Balance Sheet")
                elif debt and debt < 1.0:
                    score += 10
                    reasons.append("⚠️ Acceptable Debt")
                
                if eps_g and eps_g > 0.10:
                    score += 20
                    reasons.append("✅ Strong Earnings Growth")
                
                if div and div > 0.01:
                    score += 10
                    reasons.append("✅ Pays Dividend")
                
                # Recommendation
                if score >= 75:
                    rec = "🚀 STRONG BUY"
                    color = "🟢"
                elif score >= 60:
                    rec = "✅ BUY"
                    color = "🟢"
                elif score >= 45:
                    rec = "⏳ HOLD"
                    color = "🟡"
                else:
                    rec = "❌ SELL / AVOID"
                    color = "🔴"
                
                # Display
                st.subheader(f"{ticker} - {name}")
                
                col1, col2, col3 = st.columns([2, 2, 3])
                with col1:
                    st.metric("Current Price", f"₹{current_price:,.2f}")
                with col2:
                    st.metric("AI Score", f"{score}/100 {color}", delta=rec)
                
                with col3:
                    st.write("**Key Reasons:**")
                    for reason in reasons:
                        st.write(reason)
                
                # Chart
                if not hist.empty:
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(hist.index, hist['Close'], color='#00f5ff', linewidth=2.5)
                    ax.set_title(f"{ticker} - 1 Year Price Trend")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                    plt.close()
                
                st.divider()
                
            except Exception as e:
                st.error(f"Could not analyze {ticker}")

st.sidebar.caption("Educational Tool Only • Not Financial Advice")
st.caption("✅ AI Scoring is now active!")

