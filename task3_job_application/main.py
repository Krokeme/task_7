from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import application_router
from .middleware.user_agent_middleware import user_agent_middleware

app = FastAPI(title="Job Application Tracker")

# Middleware
app.middleware("http")(user_agent_middleware)

# Routers
app.include_router(application_router.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
