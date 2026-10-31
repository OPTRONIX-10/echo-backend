
from fastapi import APIRouter, HTTPException, Request

from echo_backend.schemas.place_schema import PlaceSchema
from echo_backend.services.place_service import get_place_details


router = APIRouter(
    prefix="/places",
    tags=["places"]
)

@router.post("/search")
async def search_places(text_query:str,  request:Request, latitude: float, longitude: float) -> list[PlaceSchema]:
    try:
        return await get_place_details(request.app.state.http_client, text_query, latitude, longitude)
    except Exception as e:
       raise HTTPException(
            status_code=500,
            detail=str(e),
        )
