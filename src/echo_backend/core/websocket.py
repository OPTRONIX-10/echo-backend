from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self,execution_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[execution_id] = websocket

    def disconnect(self, execution_id: str):
        if execution_id in self.active_connections:
            del self.active_connections[execution_id]

    async def broadcast(self, message: dict, execution_id: str):
        for websocket in self.active_connections.values():
            try:
                await websocket.send_json(message)
            except Exception as e:
                self.disconnect(execution_id)

manager = ConnectionManager()