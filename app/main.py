# uvicorn app.main:app --reload
from fastapi import FastAPI, Depends, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_
import redis
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0)

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def serialize_sqlalchemy_obj(obj):
    obj_dict = obj.__dict__.copy()
    obj_dict.pop('_sa_instance_state', None)
    return obj_dict

templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/task-create')
def create(request: schemas.TaskCreate, db: Session = Depends(get_db)):
    task_item = models.Task(title=request.title, description=request.description, completed=request.completed)
    db.add(task_item)
    db.commit()
    db.refresh(task_item)
    return task_item

@app.get('/task-list')
def task_list(db: Session = Depends(get_db)):
    task_item = db.query(models.Task).all()
    return task_item

@app.put('/task-update/{id}')
def task_update(id: int, request: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task_item = db.query(models.Task).filter(models.Task.id == id)
    if not task_item.first():
        raise HTTPException(status_code=404, detail="Item não encontrado")
    update_data = request.dict(exclude_unset=True)
    task_item.update(update_data)
    db.commit()
    return 'Atualizado com sucesso...'

@app.delete('/task-delete/{id}')
def task_delete(id: int, db: Session = Depends(get_db)):
    task_item = db.query(models.Task).filter(models.Task.id == id).first()
    if not task_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    db.delete(task_item)
    db.commit()
    return 'Excluido com sucesso...'

@app.get('/task-search')
def task_search(query: str, db: Session = Depends(get_db)):
    cache_key = f"search:{query}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
    task_item = db.query(models.Task).filter(
        or_(models.Task.title.contains(query), models.Task.description.contains(query))
    ).all()
    if task_item:
        serialized_items = [serialize_sqlalchemy_obj(item) for item in task_item]
        redis_client.set(cache_key, json.dumps(serialized_items), ex=3600)
    return task_item

@app.patch('/task-update-partial/{id}')
def task_update_partial(id: int, request: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task_item = db.query(models.Task).filter(models.Task.id == id).first()
    if not task_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task_item, key, value)
    db.commit()
    db.refresh(task_item)
    return task_item

@app.get('/test-redis')
def test_redis():
    try:
        redis_client.set("test_key", "test_value", ex=60)
        value = redis_client.get("test_key")
        return {"status": "success", "value": value.decode("utf-8")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get('/task/{id}')
def task_search_by_id(id: int, db: Session = Depends(get_db)):
    cache_key = f"task:{id}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    task_item = db.query(models.Task).filter(models.Task.id == id).first()
    if not task_item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    serialized_item = serialize_sqlalchemy_obj(task_item)
    redis_client.set(cache_key, json.dumps(serialized_item), ex=3600)
    return task_item

