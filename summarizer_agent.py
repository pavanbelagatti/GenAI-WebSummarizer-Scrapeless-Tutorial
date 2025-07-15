import os
from dotenv import load_dotenv
import trafilatura

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()


def extract_readable_text(html: str) -> str:
    """
    Extracts readable text from raw HTML using trafilatura.
    Returns None if nothing meaningful is extracted.
    """
    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        favor_recall=True
    )
    return text or "No readable content found."


def summarize_html(html: str) -> str:
    """
    Extract readable text from HTML and summarize it using OpenAI + LangChain.
    """
    # Step 1: Clean and extract main text
    extracted_text = extract_readable_text(html)

    # Step 2: Truncate if too long (safe limit for GPT-3.5: ~4000 characters)
    truncated_text = extracted_text[:4000]

    # Step 3: Set up the model
    llm = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
        temperature=0.3
    )

    # Step 4: Define summarization prompt
    prompt = ChatPromptTemplate.from_template("""
You are an intelligent assistant.

Summarize the following article into 5 concise, informative bullet points.

Article Content:
{text}
""")

    # Step 5: Run chain
    chain = prompt | llm
    result = chain.invoke({"text": truncated_text})

    return result.content