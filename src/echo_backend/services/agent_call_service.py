import os
from dotenv import load_dotenv
import httpx
from echo_backend.schemas.agent_execution_schema import AgentExecutionSchema
from echo_backend.schemas.agent_schema import AgentCallSchema, AgentUserDataSchema

load_dotenv()
BASE_URL = "https://api.bolna.ai/"
api_token = os.getenv("BOLNA_API_KEY")

async def initiate_agent_call(httpclient: httpx.AsyncClient, agent_id: str, recipient_phone_number: str,  
                             user_data: AgentUserDataSchema) -> AgentCallSchema:
    url = f"{BASE_URL}call"
    if not api_token:
        raise ValueError("BOLNA_API_TOKEN is not configured")

    payload = {
        "agent_id": agent_id,
        "recipient_phone_number": recipient_phone_number,
        "user_data": {
            "customer_name": user_data.customer_name,
            "customer_phone_number": user_data.customer_phone_number,
            "service_type": user_data.service_type,
            "customer_location": user_data.customer_location,
            "service_description": user_data.service_description,
            "provider_bussiness_name": user_data.provider_bussiness_name
        },
    }
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    response = await httpclient.post(url, json=payload, headers=headers)

    response.raise_for_status()
    return AgentCallSchema(**response.json())

async def get_agentcall_execution(httpclient: httpx.AsyncClient, execution_id: str) -> AgentExecutionSchema:
    url = f"{BASE_URL}executions/{execution_id}"
    if not api_token:
        raise ValueError("BOLNA_API_TOKEN is not configured")

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    response = await httpclient.get(url, headers=headers)

    response.raise_for_status()
    return AgentExecutionSchema(**response.json())

