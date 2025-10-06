import pytest

from portfolio_app.portfolio import Portfolio
from portfolio_app.stock import Stock

def test_portfolio_rebalance_example():
  stocks_available = {
    "META": Stock("META", 0.1),
    "NVDA": Stock("NVDA", 1),
    "AAPL": Stock("AAPL", 2),
    "ORCL": Stock("ORCL", 0.5),
    "PLTR": Stock("PLTR", 0.7),
  }

  shares_owned_per_stock = {
    "META": 1,
    "ORCL": 1.5,
  }

  allocated_stocks = {
    "ORCL": 0.2,
    "PLTR": 0.8,
  }

  portfolio = Portfolio(stocks_available, shares_owned_per_stock, allocated_stocks)

  initial_value = portfolio.calculate_portfolio_value()
  rebalance_plan = portfolio.calculate_rebalance_plan()

  assert pytest.approx(rebalance_plan.get("META", 0), abs=1e-9) == -1.0
  assert pytest.approx(rebalance_plan.get("ORCL", 0), abs=1e-9) == -1.16
  assert pytest.approx(rebalance_plan.get("PLTR", 0), abs=1e-9) == 0.9714285714285714

  portfolio.apply_rebalance(rebalance_plan)

  assert portfolio.calculate_portfolio_value() == pytest.approx(initial_value, abs=1e-9)

  expected_shares_owned_per_stock = {
    "PLTR": 0.9714285,
    "ORCL": 0.34,
  }

  actual = portfolio.get_shares_owned_per_stock()
  assert set(actual.keys()) == set(expected_shares_owned_per_stock.keys())
  for symbol, expected_shares in expected_shares_owned_per_stock.items():
    assert actual[symbol] == pytest.approx(expected_shares, abs=1e-6)
