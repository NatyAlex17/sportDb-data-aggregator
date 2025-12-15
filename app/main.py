from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.events import router as events_router

app = FastAPI(title="Soccer Events API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # TODO: Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(events_router)
