from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routes_contacts import router as contacts_router
from auth import router as auth_router
from middleware_logger import log_ip_middleware

app = FastAPI(title="Contact Manager API")

# CORS settings


origins = ["http://localhost:3000", "http://127.0.0.1:5500"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for logging IP
app.middleware("http")(log_ip_middleware)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(contacts_router, prefix="/contacts", tags=["Contacts"])

# Initialize DB
@app.on_event("startup")
def on_startup():
    init_db()
