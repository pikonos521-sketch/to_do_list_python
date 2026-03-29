from fastapi import FastAPI, Form,  Request
from fastapi.templating import Jinja2Templates
import json
import datetime

def ault_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

filename = "data/tasks.json"

@app.get("/") # +
def menu(request: Request):
    """главное меню, приветствие и перанаправления"""
    return templates.TemplateResponse("menu.html", {"request": request})


@app.get("/help") # +
def help(request: Request):
    """страница помощи"""
    return templates.TemplateResponse("help.html", {"request": request})


@app.get("/todo") # +
def todo_page(request: Request):
    """1страница с формой для добавления задачи"""
    return templates.TemplateResponse("todo.html", {"request": request})

@app.post("/todo") # +
def todo(request: Request, name: str = Form(...), task: str = Form(...), done: str = Form(...)):
    """1добовления задач"""
    new_task = {
    "время создания": ault_time(),
    "имя": name,
    "сделана": done,
    "info": {
        "task": task
        }
    }

    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except:
        tasks = []

    tasks.append(new_task)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)
    
    return templates.TemplateResponse("todo.html", {"request": request, "message": "Задача добавлена!"})

    

@app.get("/all") # +
def all_tasks(request: Request):
    """для вывода всех задач"""
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    return templates.TemplateResponse(
        "all.html",
        {
            "request": request,
            "tasks": tasks
        }
    )


@app.get("/name") # +
def name_page(request: Request):
    """2"""
    return templates.TemplateResponse("name.html", {"request": request})

@app.post("/name") # +
def search_task(request: Request, name: str = Form(...)):
    """2- страница для поиска задачи по имени"""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    found_task = None

    for task in tasks:
        if task["имя"].lower() == name.lower():
            found_task = task
            break

    if not found_task:
        return templates.TemplateResponse(
            "name.html",
            {"request": request, "message": "Задача не найдена"}
        )
    
    return templates.TemplateResponse(
        "name.html",
        {
            "request": request,
            "task": found_task
        }
    )


@app.get("/del") # +
def delete(request: Request):
    """страница для удаления задачи по имени"""
    return templates.TemplateResponse("delete.html", {"request": request})

@app.post("/del") # +
def delete_task(request: Request, name: str = Form(...)):
    """удалить задачу по имени"""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    new_tasks = [task for task in tasks if task["имя"].lower() != name.lower()]

    if len(new_tasks) == len(tasks):
        return templates.TemplateResponse(
            "delete.html",
            {"request": request, "message": "Задача не найдена"}
        )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(new_tasks, file, ensure_ascii=False, indent=4)

    return templates.TemplateResponse(
        "delete.html",
        {"request": request, "message": "Задача удалена!"}
    )
    

@app.get("/update") # +
def update_page(request: Request):
    """3"""
    return templates.TemplateResponse("update.html", {"request": request})

@app.post("/update") # +
def update_task(request: Request, name: str = Form(...)):
    """3-отметить задачу как выполненную по имени"""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []

    updated = False

    for task in tasks:
        if task["имя"] == name:
            task["сделана"] = "да"
            updated = True
            break

    if not updated:
        return templates.TemplateResponse(
            "update.html",
            {"request": request, "message": "Задача не найдена"}
        )

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

    return templates.TemplateResponse(
        "update.html",
        {"request": request, "message": "Задача обновлена!"}
    )
   


"""uvicorn main:app --reload"""  