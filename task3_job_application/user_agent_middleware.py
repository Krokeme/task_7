from fastapi import Request, HTTPException

async def user_agent_middleware(request: Request, call_next):
    user_agent = request.headers.get("User-Agent")
    if not user_agent:
        raise HTTPException(status_code=400, detail="User-Agent header required")
    response = await call_next(request)
    return response
