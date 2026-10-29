from fastapi import FastAPI
from echo_backend.core.lifespan import lifespan
from echo_backend.routes import places


app = FastAPI(lifespan=lifespan)
app.include_router(places.router)