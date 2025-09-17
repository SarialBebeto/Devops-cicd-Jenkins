from fastapi import FastAPI
from app.db import database, User, wait_for_db


app = FastAPI(title="FastAPI, Docker, and Traefik")


@app.get("/")
async def read_root():
    return await User.objects.all()

@app.on_event("startup")
async def startup():
    # Wait for DB to be ready before connecting
    import asyncio
    loop = asyncio.get_event_loop()
    # Run the blocking wait_for_db in a thread to avoid blocking the event loop
    await loop.run_in_executor(None, wait_for_db)
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
