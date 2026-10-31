from fastapi import APIRouter
from echo_backend.services.llm_service import get_llm_response


router = APIRouter(
    prefix = "/llm",
    tags = ["llm"]
)

@router.get("/response")
async def llm_response(message:str):
    try:
        return await get_llm_response(message)
    except Exception as e:
        print(f"Error occurred while fetching LLM response: {e}")
        raise e