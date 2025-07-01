from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool


class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """
        Setup all tools for the calculator tool
        """

        @tool
        def estimate_total_hotel_cost(
            price_per_night: float, total_days: float
        ) -> float:
            """
            Estimate the total cost of a hotel stay.
            Args:
                price_per_night (float): The cost for one night.
                total_days (float): The total number of days for the stay.
            """
            return self.calculator.multiply(price_per_night, total_days)

        @tool
        def calculate_total_expense(*costs: float) -> float:
            """Calculate total expense of the trip"""
            return self.calculator.calculate_total(*costs)

        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(total_cost, days)

        return [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget,
        ]
