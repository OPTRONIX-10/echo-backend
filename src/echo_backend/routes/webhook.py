from fastapi import APIRouter, Request, HTTPException
from echo_backend.core.websocket import manager

router = APIRouter(
    prefix="/webhook",
    tags=["webhooks"]
)


@router.post("/")
async def bolna_webhook(
    request: Request,
):
    
    payload = await request.json()

    execution_id = payload.get("id")
    status = payload.get("status")

    if not execution_id or not status:
        raise HTTPException(
            status_code=400,
            detail="Missing execution ID or status"
        )

    print(f"Execution: {execution_id}")
    print(f"Status: {status}")



    await manager.broadcast(
        execution_id,
        {
            "execution_id": execution_id,
            "status": status
        }
    )

    return {"message": "Webhook received successfully"}