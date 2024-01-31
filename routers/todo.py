from fastapi import Depends, HTTPException, Path, APIRouter, Request, Form
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from starlette import status
from starlette.responses import RedirectResponse
from models import Todos
from database import engine, SessionLocal
from .auth import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

todo_router = APIRouter()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@todo_router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request:Request, db: db_dependency):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    todos = db.query(Todos).filter(Todos.ower_id == user.get("id")).all()
    
    return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})

@todo_router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request:Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})

@todo_router.post("/add-todo", response_class=HTMLResponse)
async def add_new_todo_post(request:Request, db: db_dependency, title: str = Form(...), description: str = Form(...),
                            priority: int = Form(...)):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    todo_model = Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.completed = False
    todo_model.ower_id = user.get("id")
    
    db.add(todo_model)
    db.commit()
    
    return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)


@todo_router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request:Request, todo_id: int, db: db_dependency):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

@todo_router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(request:Request, todo_id: int, db: db_dependency, title: str = Form(...),
                           description: str = Form(...),priority: int = Form(...)):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    todo.title = title
    todo.description = description
    todo.priority = priority
    
    db.add(todo)
    db.commit()
    
    return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)


@todo_router.get("/delete/{todo_id}", response_class=HTMLResponse)
async def delete_todo(request:Request, todo_id: int, db: db_dependency):
    
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.ower_id == user.get("id")).first()
    
    if todo_model is None:
        return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)
    
    db.delete(todo_model)
    db.commit()
    
    return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)

@todo_router.get("/complete/{todo_id}", response_class=HTMLResponse)
async def complete_todo(request:Request, todo_id: int, db: db_dependency):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse("/auth", status_code=status.HTTP_302_FOUND)
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.ower_id == user.get("id")).first()
    
    if todo_model is None:
        return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)
    
    todo_model.completed = not todo_model.completed
    
    db.add(todo_model)
    db.commit()
    
    return RedirectResponse("/todo", status_code=status.HTTP_302_FOUND)









# class TodoRequest(BaseModel):
#     title: str = Field(min_length=3)
#     description: str = Field(min_length=3, max_length=50)
#     priority: int = Field(gt=0, lt=6)
#     completed: bool
    
# @todo_router.get("/test")
# async def test(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})
# @todo_router.get("/", status_code=status.HTTP_200_OK)
# async def read_all(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
    
#     all_todos = db.query(Todos).filter(Todos.ower_id == user.get('id')).all()
#     return all_todos

# @todo_router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
# async def read_one(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
    
#     todo_model = db.query(Todos).filter(Todos.id == todo_id)\
#     .filter(Todos.ower_id == user.get('id')).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404, detail="Todo not found")


# # Create a new todo
# @todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
# async def create_todo(user: user_dependency,
#                       db: db_dependency, todo_request: TodoRequest):
    
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
    
#     todo_model = Todos(**todo_request.model_dump(), ower_id=user.get('id'))
#     print(todo_model)
    
#     db.add(todo_model)
#     db.commit()
#     db.refresh(todo_model)
    
#     return todo_model

# # Update a todo
# @todo_router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
# async def update_todo(user: user_dependency, db: db_dependency, 
#                        todo_request: TodoRequest,
#                        todo_id: int = Path(gt=0)):
    
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
    
#     todo_model = db.query(Todos).filter(Todos.id == todo_id)\
#     .filter(Todos.ower_id == user.get('id')).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
    
#     todo_model.title = todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.completed = todo_request.completed
    
#     db.add(todo_model)
#     db.commit()
    
# # Delete a todo
# @todo_router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
#     if user is None:
#         raise HTTPException(status_code=401, detail="Authentication Failed")
    
#     todo_model = db.query(Todos).filter(Todos.id == todo_id)\
#         .filter(Todos.ower_id == user.get('id')).first()
#     if todo_model is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
    
#     db.delete(todo_model)
#     db.commit()
    
      
