import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="StockSage AI", page_icon="📈", layout="wide")

st.title("📊 StockSage AI - Pro")
st.markdown("**Fundamental Analysis • Portfolio Tracker • Price Alerts**")

tab1, tab2, tab3 = st.tabs(["📈 Stock Analysis", "💼 Portfolio Tracker", "🔔 Price Alerts"])

# ===================== TAB 1: STOCK ANALYSIS =====================
with tab1:
    st.sidebar.header("Stock Analysis")
    tickers_input = st.sidebar.text_input("Enter Tickers", "RELIANCE.NS, TCS.NS, HDFCBANK.NS")
    
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
                
                score = 0
                reasons = []
                if pe and pe < 22: score += 25; reasons.append("✅ Attractive Valuation")
                elif pe and pe < 30: score += 15; reasons.append("⚠️ Reasonable Valuation")
                else: reasons.append("❌ High Valuation")
                
                if roe and roe > 0.15: score += 25; reasons.append("✅ Excellent ROE")
                elif roe and roe > 0.10: score += 15; reasons.append("⚠️ Good ROE")
                
                if debt and debt < 0.6: score += 20; reasons.append("✅ Strong Balance Sheet")
                if eps_g and eps_g > 0.10: score += 20; reasons.append("✅ Strong Growth")
                if div and div > 0.01: score += 10; reasons.append("✅ Good Dividend")
                
                if score >= 75: rec = "🚀 STRONG BUY"
                elif score >= 60: rec = "✅ BUY"
                elif score >= 45: rec = "⏳ HOLD"
                else: rec = "❌ SELL / AVOID"
                
                st.subheader(f"{ticker} - {name}")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric("Current Price", f"₹{current_price:,.2f}")
                    st.metric("AI Score", f"{score}/100", rec)
                with col2:
                    for r in reasons:
                        st.write(r)
                
                if not hist.empty:
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(hist.index, hist['Close'], color='#00f5ff', linewidth=2.5)
                    ax.set_title(f"{ticker} - 1 Year Trend")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                    plt.close()
                
                st.divider()
            except:
                st.error(f"Could not fetch {ticker}")

# ===================== TAB 2: PORTFOLIO TRACKER (with Delete) =====================
with tab2:
    st.header("💼 My Portfolio")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = pd.DataFrame(columns=['Ticker', 'Quantity', 'Buy Price'])
    
    # Add new stock
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        ticker_add = st.text_input("Stock Ticker", "RELIANCE.NS").upper()
    with col2:
        qty = st.number_input("Quantity", min_value=1, value=10)
    with col3:
        buy_price = st.number_input("Buy Price ₹", min_value=1.0, value=2400.0)
    
    if st.button("➕ Add to Portfolio"):
        new_row = pd.DataFrame({'Ticker': [ticker_add], 'Quantity': [qty], 'Buy Price': [buy_price]})
        st.session_state.portfolio = pd.concat([st.session_state.portfolio, new_row], ignore_index=True)
        st.success(f"Added {ticker_add}")
    
    # Show Portfolio
    if not st.session_state.portfolio.empty:
        st.subheader("Current Holdings")
        portfolio = st.session_state.portfolio.copy()
        
        # Fetch current prices
        current_prices = {}
        for t in portfolio['Ticker']:
            try:
                current_prices[t] = yf.Ticker(t).info.get('currentPrice', 0)
            except:
                current_prices[t] = 0
        
        portfolio['Current Price'] = portfolio['Ticker'].map(current_prices)
        portfolio['Investment'] = portfolio['Quantity'] * portfolio['Buy Price']
        portfolio['Current Value'] = portfolio['Quantity'] * portfolio['Current Price']
        portfolio['P&L'] = portfolio['Current Value'] - portfolio['Investment']
        portfolio['P&L %'] = (portfolio['P&L'] / portfolio['Investment']) * 100
        
        # Add Delete Column
        portfolio = portfolio.reset_index()
        portfolio = portfolio.rename(columns={'index': 'idx'})
        
        # Display with delete buttons
        for i, row in portfolio.iterrows():
            colA, colB, colC, colD = st.columns([2, 1, 1, 1])
            with colA:
                st.write(f"**{row['Ticker']}**")
            with colB:
                st.write(f"Qty: {row['Quantity']}")
            with colC:
                st.write(f"₹{row['Current Value']:,.2f}")
            with colD:
                if st.button("🗑️ Delete", key=f"del_{i}"):
                    st.session_state.portfolio = st.session_state.portfolio.drop(i)
                    st.rerun()
        
        # Summary
        total_invest = portfolio['Investment'].sum()
        total_value = portfolio['Current Value'].sum()
        total_pl = total_value - total_invest
        
        colA, colB, colC = st.columns(3)
        colA.metric("Total Invested", f"₹{total_invest:,.2f}")
        colB.metric("Current Value", f"₹{total_value:,.2f}", f"₹{total_pl:,.2f}")
        colC.metric("Overall Return", f"{(total_pl/total_invest)*100:.2f}%" if total_invest > 0 else "0%")

# ===================== TAB 3: ALERTS =====================
with tab3:
    st.header("🔔 Price Alerts")
    # (Same as previous version)
    st.info("Alert feature coming in next update.")

st.caption("Educational Tool Only • Not Financial Advice")
