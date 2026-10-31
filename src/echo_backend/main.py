from fastapi import FastAPI
from echo_backend.core.lifespan import lifespan
from echo_backend.routes import bolna_agent, health, places, llm, webhook, websocket


app = FastAPI(lifespan=lifespan)
app.include_router(places.router)
app.include_router(bolna_agent.router)
app.include_router(health.router)
app.include_router(llm.router)
app.include_router(webhook.router)
app.include_router(websocket.router)