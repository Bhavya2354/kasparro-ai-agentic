import json
import os

from langchain.agents import create_structured_chat_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool

from src.llm.groq_client import get_llm
from src.config import Config
from src.agents.product_agent import ProductAgent
from src.agents.faq_agent import FAQAgent
from src.agents.comparison_agent import ComparisonAgent


class LangChainOrchestrator:
    def __init__(self):
        print("🚀 Groq Agentic Pipeline")

        # ---- LLM ----
        self.llm = get_llm()

        # ---- Agents ----
        self.product_agent = ProductAgent(self.llm)
        self.faq_agent = FAQAgent(self.llm)
        self.compare_agent = ComparisonAgent(self.llm)

        # ---- Tool state (prevents infinite loops) ----
        self.tool_state = {
            "product": False,
            "faq": False,
            "comparison": False
        }

        # ---- Tools ----
        self.tools = [
            Tool(
                name="generate_product",
                func=self.product_tool,
                description="Generate product JSON"
            ),
            Tool(
                name="generate_faq",
                func=self.faq_tool,
                description="Generate FAQ JSON with minimum 15 questions"
            ),
            Tool(
                name="generate_comparison",
                func=self.comparison_tool,
                description="Generate product comparison JSON"
            )
        ]

        # ---- Prompt (Shashank style, STRICT JSON tool calling) ----
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a deterministic tool calling AI.\n\n"
             "You must call ALL tools exactly once.\n"
             "Order:\n"
             "1) generate_product\n"
             "2) generate_faq\n"
             "3) generate_comparison\n\n"

             "Available tools:\n{tools}\n\n"
             "Tool names:\n{tool_names}\n\n"

             "You must reply ONLY in JSON.\n\n"

             "Tool call format:\n"
             "{{\"action\":\"tool_name\",\"action_input\":\"json\"}}\n\n"

             "Final format:\n"
             "{{\"action\":\"Final\",\"action_input\":\"done\"}}\n\n"

             "Rules:\n"
             "- Never explain\n"
             "- Never output English\n"
             "- Never output python\n"
             "- Never repeat a tool that already returned DONE\n"
             "- After all tools return DONE, output Final"
            ),
            ("human", "{input}"),
            ("ai", "{agent_scratchpad}")
        ])

        # ---- Structured Agent ----
        self.agent = create_structured_chat_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=6
        )

    # ================= TOOLS =================

    def product_tool(self, product_json: str):
        if self.tool_state["product"]:
            return "PRODUCT_ALREADY_DONE"

        print("🟢 PRODUCT TOOL")
        product = json.loads(product_json)
        result = self.product_agent.run(product)

        with open(Config.OUTPUT_PRODUCT, "w", encoding="utf-8") as f:
            f.write(result)

        self.tool_state["product"] = True
        return "PRODUCT_DONE"

    def faq_tool(self, product_json: str):
        if self.tool_state["faq"]:
            return "FAQ_ALREADY_DONE"

        print("🟢 FAQ TOOL")
        product = json.loads(product_json)
        faqs = self.faq_agent.generate_faq(product)

        with open(Config.OUTPUT_FAQ, "w", encoding="utf-8") as f:
            f.write(faqs)

        self.tool_state["faq"] = True
        return "FAQ_DONE"

    def comparison_tool(self, product_json: str):
        if self.tool_state["comparison"]:
            return "COMPARE_ALREADY_DONE"

        print("🟢 COMPARISON TOOL")
        product = json.loads(product_json)
        result = self.compare_agent.run(product, product)

        with open(Config.OUTPUT_COMPARISON, "w", encoding="utf-8") as f:
            f.write(result)

        self.tool_state["comparison"] = True
        return "COMPARE_DONE"

    # ================= RUN =================

    def run(self):
        # 🔥 THIS WAS THE CRITICAL FIX
        os.makedirs("outputs", exist_ok=True)

        with open(Config.INPUT_PRODUCT, "r", encoding="utf-8") as f:
            product = json.load(f)

        self.executor.invoke({
            "input": json.dumps(product),
            "agent_scratchpad": ""
        })

        print("\n🛑 All pages generated")