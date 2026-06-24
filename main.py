import os
import requests
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

def fetch_stock_data(ticker):
    """
    Connects to a public, unauthenticated market data API node
    to fetch real-time financial instrument performance structures.
    """
    ticker = ticker.strip().upper()
    # Query an open Yahoo Finance fallback API utility node
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    
    # Standard header configuration to prevent endpoint access blocks
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return None
            
        data = response.json()
        meta = data['chart']['result'][0]['meta']
        
        # Parse out core metric floats from the nested JSON response payload
        return {
            "ticker": ticker,
            "company_name": ticker,  # Fallback display name descriptor
            "price": round(meta['regularMarketPrice'], 2),
            "currency": meta['currency'],
            "previous_close": round(meta['chartPreviousClose'], 2),
            "change": round(meta['regularMarketPrice'] - meta['chartPreviousClose'], 2),
            "pct_change": round(((meta['regularMarketPrice'] - meta['chartPreviousClose']) / meta['chartPreviousClose']) * 100, 2)
        }
    except Exception:
        return None

# Combined single-file HTML layout interface string template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Real-Time Market Intelligence</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #0B0C10; color: #C5C6C7; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; background: #1F2833; padding: 30px; border-radius: 8px; border: 1px solid #45A29E; }
        h1 { color: #66FCF1; text-align: center; margin-bottom: 25px; }
        form { display: flex; gap: 10px; margin-bottom: 30px; }
        input[type="text"] { flex: 1; padding: 12px; border-radius: 4px; border: 1px solid #45A29E; background: #0B0C10; color: #FFF; font-size: 16px; }
        button { padding: 12px 24px; background: #45A29E; border: none; color: #0B0C10; font-weight: bold; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background: #66FCF1; }
        .card { background: #0B0C10; padding: 20px; border-radius: 6px; border-left: 5px solid #66FCF1; }
        .ticker-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .symbol { font-size: 28px; font-weight: bold; color: #FFF; }
        .price { font-size: 32px; font-weight: bold; color: #66FCF1; }
        .positive { color: #2ecc71; }
        .negative { color: #e74c3c; }
        .error { color: #e74c3c; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📉 Financial Instrument Dashboard</h1>
        <form method="POST" action="/">
            <input type="text" name="ticker" placeholder="Enter stock symbol (e.g., AAPL, GOOG, TSLA)" required>
            <button type="submit">Analyze</button>
        </form>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        {% if stock %}
            <div class="card">
                <div class="ticker-header">
                    <span class="symbol">{{ stock.ticker }}</span>
                    <span class="price">${{ stock.price }} <small style="font-size:14px; color:#888;">{{ stock.currency }}</small></span>
                </div>
                <hr style="border: 0; border-top: 1px solid #1F2833; margin: 15px 0;">
                <p>Previous Close: <strong>${{ stock.previous_close }}</strong></p>
                <p>Net Session Deviation: 
                    <span class="{% if stock.change >= 0 %}positive{% else %}negative{% endif %}">
                        {% if stock.change >= 0 %}+{% endif %}{{ stock.change }} ({% if stock.pct_change >= 0 %}+{% endif %}{{ stock.pct_change }}%)
                    </span>
                </p>
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    stock_info = None
    error_message = None
    
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if ticker:
            stock_info = fetch_stock_data(ticker)
            if not stock_info:
                error_message = f"Failed to retrieve structural asset parameters for symbol: '{ticker.upper()}'"
                
    return render_template_string(HTML_TEMPLATE, stock=stock_info, error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
