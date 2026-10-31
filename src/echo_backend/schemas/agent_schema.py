from pydantic import BaseModel

class AgentCallSchema(BaseModel):
    message: str
    status: str
    execution_id: str

class AgentUserDataSchema(BaseModel):
    customer_name: str
    customer_phone_number: str
    service_type: str
    customer_location: str
    service_description: str
    provider_bussiness_name: str