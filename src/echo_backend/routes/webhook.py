from fastapi import APIRouter, Request, Header, HTTPException

router = APIRouter(
    prefix="/webhook",
    tags=["webhooks"]
)

# WEBHOOK_SECRET = os.getenv("BOLNA_WEBHOOK_SECRET")


@router.post("/")
async def bolna_webhook(
    request: Request,
    # x_bolna_webhook_secret: str | None = Header(default=None)
):
    # Verify webhook authentication
    # if not WEBHOOK_SECRET or x_bolna_webhook_secret != WEBHOOK_SECRET:
    #     raise HTTPException(status_code=401, detail="Unauthorized")

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

    # Update database
    # await update_call_status(execution_id, status)

    # Notify connected Flutter clients
    # await manager.broadcast(
    #     execution_id,
    #     {
    #         "execution_id": execution_id,
    #         "status": status
    #     }
    # )

    return status