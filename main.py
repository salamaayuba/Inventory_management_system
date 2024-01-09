from fastapi import FastAPI
from routers import users, items
import auth


app = FastAPI(title="Inventory Management System")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def index():
    return {
        "status": "connection successful",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        # uds="/tmp/uvicorn.sock",
    )
