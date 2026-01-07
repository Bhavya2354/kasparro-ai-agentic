import json

class ComparisonAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, product, competitor):
        prompt = f"""
You are generating a comparison page.

Product:
{json.dumps(product)}

Competitor:
{json.dumps(competitor)}

Output EXACTLY this format:

{{
  "product": {{...}},
  "competitor": {{...}},
  "differences": [],
  "why_choose_this": []
}}

Rules:
- product must be the first product
- competitor must be the second
- differences must list real differences
- why_choose_this must explain why product is better
- Output ONLY valid JSON
"""

        return self.llm.invoke(prompt)