from fastapi import FastAPI
from routers.auth import router
from routers.todo import todo_router
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the router
app.include_router(router)
app.include_router(todo_router, prefix="/todo")
