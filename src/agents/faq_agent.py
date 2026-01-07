import json

class FAQAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_faq(self, product):
        prompt = f"""
You are generating FAQs.

Using this product:
{json.dumps(product)}

Generate at least 15 FAQs in EXACTLY this format:

[
  {{"question": "...", "answer": "..."}},
  ...
]

Rules:
- Questions must be relevant
- Answers must use only provided data
- Output ONLY valid JSON array
"""

        return self.llm.invoke(prompt)