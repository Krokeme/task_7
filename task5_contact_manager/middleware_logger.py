from fastapi import Request
import logging

logging.basicConfig(filename="ip_logs.txt", level=logging.INFO)

async def log_ip_middleware(request: Request, call_next):
    ip = request.client.host
    logging.info(f"IP: {ip}, Path: {request.url.path}")
    response = await call_next(request)
    return response
