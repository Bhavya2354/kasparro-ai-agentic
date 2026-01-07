import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # =========================
    # API
    # =========================
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # =========================
    # LLM
    # =========================
    GROQ_MODEL = "llama-3.3-70b-versatile"

    # =========================
    # Files
    # =========================
    INPUT_PRODUCT = "data/product.json"

    OUTPUT_FAQ = "outputs/faq_page.json"
    OUTPUT_PRODUCT = "outputs/product_page.json"
    OUTPUT_COMPARISON = "outputs/comparison_page.json"

    # =========================
    # Templates
    # =========================
    TEMPLATE_FAQ = "src/templates/faq.jinja"
    TEMPLATE_PRODUCT = "src/templates/product.jinja"
    TEMPLATE_COMPARISON = "src/templates/comparison.jinja"

    # =========================
    # Validation
    # =========================
    MIN_FAQS = 15
