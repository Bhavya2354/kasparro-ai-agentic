import json
from src.orchestrator.langchain_orchestrator import LangChainOrchestrator
from src.config import Config

if __name__ == "__main__":
    print("🚀 Starting Kasparro")

    orch = LangChainOrchestrator()

    # Orchestrator itself loads the product JSON
    orch.run()