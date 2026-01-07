import json

class ProductAgent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, product):
        prompt = f"""
You are generating a product page JSON.

Convert this input:
{json.dumps(product)}

Into EXACTLY this format:

{{
  "name": "...",
  "description": "...",
  "ingredients": [],
  "benefits": [],
  "how_to_use": "",
  "side_effects": "",
  "price": ""
}}

Rules:
- Use product_name as name
- Build a short ecommerce description
- key_ingredients → ingredients
- benefits → benefits
- how_to_use → how_to_use
- side_effects → side_effects
- price → price
- Output ONLY valid JSON
"""

        return self.llm.invoke(prompt)