from fastapi import FastAPI
from routes.upload_route import router as upload_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for security later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(upload_router)
