
from pydantic import BaseModel, Field


class ServiceDetailsSchema(BaseModel):
    service_description: str = Field(..., description="The description of the customer problem or service request")
    service_category: str = Field(..., description="The category of the service. Example: plumbing, electrical.")
