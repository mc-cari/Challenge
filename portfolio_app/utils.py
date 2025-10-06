from typing import List, Set

FLOAT_PRECISION = 1e-9

def merge_lists(list1: List[str], list2: List[str]) -> List[str]:
  merged_set: Set[int] = set()
  
  for element in list1:
    merged_set.add(element)

  for element in list2:
    merged_set.add(element)

  return list(merged_set)

def compare_float_numbers_equality(number1: float, number2: float) -> bool:
  return abs(number1 - number2) <= FLOAT_PRECISION