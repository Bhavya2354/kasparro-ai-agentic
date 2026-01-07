1️⃣ Create .env file (VERY IMPORTANT)

In the root of your Kasparro project, create a file named:

.env


Inside it, add:

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant


Example:

GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.1-8b-instant


This is the small, fast, cheap Groq model you should use.

2️⃣ Install dependencies

In project root:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
