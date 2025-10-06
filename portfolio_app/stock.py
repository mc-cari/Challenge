class Stock:
  def __init__(self, name: str, current_price: float):
    self.name = name
    self.price_record = [current_price]
    
  def get_current_price(self) -> float:
    return self.price_record[-1]
  
  def get_name(self) -> str:
    return self.name
  
  def add_new_price(self, new_price: float):
    self.price_record.append(new_price)