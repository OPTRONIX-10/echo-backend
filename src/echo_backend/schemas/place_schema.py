from pydantic import BaseModel


class PlaceSchema(BaseModel):
    id: str
    name: str
    contact_number: str | None = None
    address: str
    latitude: float
    longitude: float
