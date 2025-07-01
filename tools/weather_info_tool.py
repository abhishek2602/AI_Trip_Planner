import os
from typing import List
from utils.weather_info import WeatherForecastTool
from langchain.tools import tool


class WeatherInfoTool:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENWEATHERMAP_API_KEY not found in environment variables."
            )
        self.weather_service = WeatherForecastTool(api_key=self.api_key)
        self.weather_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """
        Setup all tools for the weather forcast tool
        """

        @tool
        def get_current_weather(city: str) -> str:
            """
            Get the current weather in a given location
            """
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                temp = weather_data.get("main", {}).get("temp", "N/A")
                desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
                return f"Current weather in {city}: {temp}°C, {desc}"
            return f"Unable to fetch weather data for {city}"

        @tool
        def get_weather_forecast(city: str) -> str:
            """
            Get the weather forecast for a given location
            """
            forecast_data = self.weather_service.get_weather_forecast(city)
            if forecast_data and "list" in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data["list"])):
                    item = forecast_data["list"][i]
                    date = item["dt_txt"].split(" ")[0]
                    temp = item["main"]["temp"]
                    desc = item["weather"][0]["description"]
                    forecast_summary.append(f"{date}: {temp}°C, {desc}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Unable to fetch weather forecast data for {city}"

        return [get_current_weather, get_weather_forecast]
