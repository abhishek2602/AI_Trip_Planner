from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import logging

import os

# Load environment variables from .env file.
# This is the central point for loading all environment variables.
load_dotenv()

# Fail-fast validation for required API keys.
# This makes debugging easier if keys are missing.
REQUIRED_KEYS = [
    "GROQ_API_KEY",
    "EXCHANGE_RATE_API_KEY",
    "GPLACE_API_KEY",
    "OPENWEATHERMAP_API_KEY",
]
for key in REQUIRED_KEYS:
    if not os.getenv(key):
        raise ValueError(f"Missing required environment variable: {key}")

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the agent graph once on startup for efficiency
logger.info("Initializing agent graph...")
graph_builder = GraphBuilder(model_provider="groq")
react_app = graph_builder()
logger.info("Agent graph initialized successfully.")


class QueryRequest(BaseModel):
    query: str


@app.get("/")
async def read_root():
    return {"status": "ok", "message": "Welcome to the AI Trip Planner API!"}


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        logger.info(f"Received query: {query.query}")
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        messages = {"messages": [query.query]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)

        return {"answer": final_output}

    except Exception as e:
        logger.exception(f"An error occurred during query processing: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
