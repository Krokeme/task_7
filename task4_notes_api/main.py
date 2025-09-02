from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import notes
from database import init_db
import logging

# Initialize DB
init_db()

app = FastAPI(title="Notes API")

# CORS settings for multiple origins
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware: count requests & log them
request_count = 0
logging.basicConfig(filename="requests.log", level=logging.INFO, format="%(asctime)s - %(message)s")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    global request_count
    request_count += 1
    logging.info(f"Request {request_count}: {request.method} {request.url}")
    response = await call_next(request)
    return response

# Include routes
app.include_router(notes.router)
