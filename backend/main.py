from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allow all origins (you can restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/hand", tags=["hand"])
