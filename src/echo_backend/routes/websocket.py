from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from echo_backend.core.websocket import manager



router = APIRouter(prefix="/websocket",tags=["websocket"])


@router.websocket("/{execution_id}")
async def call_status_websocket(
    websocket: WebSocket,
    execution_id: str
):

    await manager.connect(execution_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(execution_id)