import os
from dotenv import load_dotenv
import httpx
from echo_backend.schemas.place_schema import PlaceSchema



load_dotenv()
BASE_URL = "https://places.googleapis.com/v1/places:searchText"

async def get_place_details(http_client: httpx.AsyncClient, text_query: str, latitude: float, longitude: float):
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PLACES_API_KEY is not configured")
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "places.id,places.displayName,places.formattedAddress,"
            "places.nationalPhoneNumber,places.location"
        )
    }
    
    payload = {
        "textQuery": text_query,
        "maxResultCount": 5,
        "rankPreference": "DISTANCE",  
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 15000.0  
            }
        }}

  
    response = await http_client.post(
            BASE_URL,
            headers=headers,
            json=payload,
        )
    response.raise_for_status()
    places = []
    for place in response.json().get("places", []):
        display_name = place.get("displayName", {})
        location = place.get("location", {})
        places.append(
            PlaceSchema(
                id=place["id"],
                name=display_name["text"],
                contact_number=place.get("nationalPhoneNumber"),
                address=place["formattedAddress"],
                latitude=location["latitude"],
                longitude=location["longitude"],
            )
        )

    return places
    

    

    

    
