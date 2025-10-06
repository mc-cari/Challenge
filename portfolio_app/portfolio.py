from enum import verify
from portfolio_app.stock import Stock
from portfolio_app.utils import merge_lists, compare_float_numbers_equality
from typing import List, Dict
from collections import defaultdict

class Portfolio:
  def __init__(self, stocks_avaliable: Dict[str, Stock], shares_owned_per_stock: Dict[str, float], allocated_stocks: Dict[str, float]):
    
    
    self.allocated_stocks = allocated_stocks
    self.stocks_available = stocks_avaliable
    self.shares_owned_per_stock = shares_owned_per_stock

    self.verify_allocated_stock_total_percentage()

  def calculate_portfolio_value(self) -> float:
    portfolio_value: float = 0
    for stock_name in self.shares_owned_per_stock.keys():
      portfolio_value += self.stocks_available[stock_name].get_current_price() * self.shares_owned_per_stock[stock_name]

    return portfolio_value

  def calculate_current_stock_weight(self, stock: Stock, portfolio_value: float) -> float:
    return stock.get_current_price() * self.shares_owned_per_stock[stock.get_name()] / portfolio_value

  def calculate_rebalance_plan(self) -> Dict[str, float]:
    portfolio_value = self.calculate_portfolio_value()
    rebalance_plan: Dict[str, float] = defaultdict(float)
    current_stock_allocation: Dict[str, float] = {}

    for stock_name in self.shares_owned_per_stock:
      stock = self.stocks_available[stock_name]
      stock_weight = self.calculate_current_stock_weight(stock, portfolio_value)
      current_stock_allocation[stock.get_name()] = stock_weight

    stocks_considered: List[str] = merge_lists(self.allocated_stocks.keys(), current_stock_allocation.keys())

    for stock_name in stocks_considered:

      if stock_name in self.allocated_stocks.keys():
        rebalance_plan[stock_name] += self.calculate_shares_to_buy(portfolio_value, stock_name)

      if stock_name in current_stock_allocation.keys() :
        rebalance_plan[stock_name] -= self.calculate_shares_to_sell(portfolio_value, stock_name, current_stock_allocation)

    return rebalance_plan
  
  def apply_rebalance(self, rebalance_plan: Dict[str, float]):
    old_portfolio_value = self.calculate_portfolio_value()

    for stock_name in rebalance_plan:
      if stock_name not in self.shares_owned_per_stock.keys():
        self.shares_owned_per_stock[stock_name] = 0
      
      self.shares_owned_per_stock[stock_name] += rebalance_plan[stock_name]

    self.verify_rebalanced_stocks_owned(old_portfolio_value)

  def calculate_shares_to_buy(self, portfolio_value: float, stock_name: str):
    return portfolio_value * self.allocated_stocks[stock_name] / self.stocks_available[stock_name].get_current_price()

  def calculate_shares_to_sell(self, portfolio_value: float, stock_name: str, current_stock_allocation: Dict[str, float]):
    return portfolio_value * current_stock_allocation[stock_name]  / self.stocks_available[stock_name].get_current_price()

  def update_allocated_stocks(self, new_allocated_stocks: Dict[str, float]):
    self.allocated_stocks = new_allocated_stocks
    self.verify_allocated_stock_total_percentage()

  def verify_rebalanced_stocks_owned(self, old_portfolio_value: float):
    portfolio_value = self.calculate_portfolio_value()
    
    for stock_name in self.allocated_stocks.keys():
      stock_weight = self.calculate_current_stock_weight(self.stocks_available[stock_name], portfolio_value)

      if not compare_float_numbers_equality(stock_weight, self.allocated_stocks[stock_name]):
        raise ValueError(f"The stock weight {stock_weight * 100}% of {stock_name} does not correspond with allocated stock weight {self.allocated_stocks[stock_name]}")
      
    if not compare_float_numbers_equality(self.calculate_portfolio_value(), old_portfolio_value):
      raise ValueError(f"The old portfolio value of {old_portfolio_value} USD changed to {self.calculate_portfolio_value()} USD")

  def verify_allocated_stock_total_percentage(self):
    accumulated_allocation_percentage: float = 0

    for allocated_stock_percentage in self.allocated_stocks.values():
      accumulated_allocation_percentage += allocated_stock_percentage

    if not compare_float_numbers_equality(1, accumulated_allocation_percentage):
      raise ValueError(f"Accumulated percentage of allocation is not 100%, currently it is: {accumulated_allocation_percentage}%")

  def get_shares_owned_per_stock(self) -> Dict[str, float]:
    return self.shares_owned_per_stock