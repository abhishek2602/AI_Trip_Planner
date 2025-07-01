import os
from utils.currency_converter import CurrencyConverter
from typing import List
from dotenv import load_dotenv
from langchain.tools import tool


class CurrencyConverterTool:
    def __init__(self):
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "EXCHANGE_RATE_API_KEY not found in environment variables."
            )
        self.currency_service = CurrencyConverter(api_key=self.api_key)
        self.currency_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """
        Setup all tools for the currency converter tool
        """

        @tool
        def convert_currency(
            amount: float, from_currency: str, to_currency: str
        ) -> str:
            """
            Convert a given amount from one currency to another
            """
            return self.currency_service.convert(amount, from_currency, to_currency)

        return [convert_currency]
