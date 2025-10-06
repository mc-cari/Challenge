from typing import Dict
from portfolio_app import portfolio
from portfolio_app.portfolio import Portfolio
from portfolio_app.stock import Stock
import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.urandom(24)

stocks_available: Dict[str, Stock] = {
  "META": Stock("META", 0.1),
  "NVDA": Stock("NVDA", 1),
  "AAPL": Stock("AAPL", 2),
  "ORCL": Stock("ORCL", 0.5),
  "PLTR": Stock("PLTR", 0.7),
}

shares_owned_per_stock: Dict[str, float] = {
  "META": 1,
  "ORCL": 1.5,
}

allocated_stocks: Dict[str, float] = {
  "ORCL": 0.2,
  "PLTR": 0.8,
}

rebalance_plan: Dict[str, float] = {}

user_portfolio = Portfolio(stocks_available, shares_owned_per_stock, allocated_stocks)

@app.route("/")
def index():
  portfolio_value = user_portfolio.calculate_portfolio_value() if shares_owned_per_stock else 0.0
  current_allocation = {}
  if portfolio_value > 0:
    for name in shares_owned_per_stock:
      stock = stocks_available[name]
      current_allocation[name] = user_portfolio.calculate_current_stock_weight(stock, portfolio_value)

  return render_template(
    "index.html",
    stocks=stocks_available,
    shares=shares_owned_per_stock,
    allocation=allocated_stocks,
    current_allocation=current_allocation,
    portfolio_value=portfolio_value,
    rebalance_plan=rebalance_plan,
  )


@app.post("/price")
def update_price():
  symbol = request.form.get("symbol", "").strip().upper()
  price_str = request.form.get("price", "").strip()
  try:
    if symbol not in stocks_available:
      flash(f"Unknown symbol {symbol}", "error")
      return redirect(url_for("index"))
    price = float(price_str)
    if price <= 0:
      raise ValueError("Price must be > 0")
    stocks_available[symbol].add_new_price(price)
    flash(f"Updated {symbol} price to {price}", "success")
  except ValueError as e:
    flash(str(e), "error")
  return redirect(url_for("index"))


@app.post("/allocation")
def update_allocation():
  try:
    new_alloc = {}
    for symbol in request.form:
      if not symbol.startswith("alloc_"):
        continue
      key = symbol.replace("alloc_", "").upper()
      value = float(request.form[symbol])
      if value < 0:
        raise ValueError("Allocation cannot be negative")
      new_alloc[key] = value

    total = sum(new_alloc.values())
    if total > 1.5: 
      new_alloc = {k: v / 100.0 for k, v in new_alloc.items()}

    user_portfolio.update_allocated_stocks(new_alloc)
    allocated_stocks.clear()
    allocated_stocks.update(new_alloc)


    user_portfolio.verify_allocated_stock_total_percentage()
    print(new_alloc)
    flash("Updated allocated stocks", "success")

  except ValueError as e:
    flash(str(e), "error")
  return redirect(url_for("index"))


@app.post("/calculate_rebalance")
def calculate_rebalance():
  global rebalance_plan
  try:
    rebalance_plan = dict(user_portfolio.calculate_rebalance_plan())
    flash("Calculated rebalance plan", "success")
  except ValueError as e:
    rebalance_plan = {}
    flash(str(e), "error")
  return redirect(url_for("index"))


@app.post("/apply_rebalance")
def apply_rebalance():
  global rebalance_plan
  if not rebalance_plan:
    flash("No rebalance plan to apply", "error")
    return redirect(url_for("index"))
  try:
    user_portfolio.apply_rebalance(rebalance_plan)
    rebalance_plan = {}
    flash("Applied rebalance plan", "success")
  except ValueError as e:
    flash(str(e), "error")
  return redirect(url_for("index"))


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=5000)


