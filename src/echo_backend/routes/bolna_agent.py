from fastapi import APIRouter, HTTPException, Request
from echo_backend.schemas.agent_schema import AgentCallSchema, AgentUserDataSchema
from echo_backend.services.agent_call_service import initiate_agent_call, get_agentcall_execution


router = APIRouter(
    prefix="/bolna_agent",
    tags=["bolna_agent"]
)

@router.post("/call")
async def agent_call(request: Request, agent_id: str, recipient_phone_number: str, 
                             user_data: AgentUserDataSchema) -> AgentCallSchema:
    try:
            return await initiate_agent_call(request.app.state.http_client, agent_id, recipient_phone_number,  user_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@router.get("/execution/{execution_id}")
async def agentcall_execution(request: Request, execution_id: str):
    try:
        return await get_agentcall_execution(request.app.state.http_client, execution_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
