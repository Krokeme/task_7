from fastapi import FastAPI, Request
from app.database import init_db
from app.routers import product_router, cart_router, user_router
import time

app = FastAPI(title="E-Commerce API")

# Init DB
init_db()

# Routers
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)

# Middleware: Response Time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["X-Response-Time"] = str(round(duration, 4))
    return response
