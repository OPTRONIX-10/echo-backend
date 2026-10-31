import os
from dotenv import load_dotenv
from openai import OpenAI

from echo_backend.schemas.llm_service_datails_schema import ServiceDetailsSchema

load_dotenv()

async def get_llm_response(message: str) -> str:
    system_prompt = """
    You are a home service query detail extractor.
    Your task is to extract the following details from the user's message:
    1. Service Description: A brief description of the service or problem the user is facing.
    2. Service Category: The category of the service. Example: plumbing, electrical, cleaning, etc.
    Please provide the extracted details in the following JSON format:
    {
        "service_description": "<extracted service description>",
        "service_category": "<extracted service category>"
    }
    
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured")

    client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    response = client.chat.completions.parse(
        model="gemini-3.5-flash-lite",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ], response_format = ServiceDetailsSchema
    )
    return response.choices[0].message.parsed

