import asyncio
import flet as ft
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# FastAPI сервер
app = FastAPI()

# Разрешение на доступ с других источников (например, с клиента Flet)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    password: str

@app.post("/api/register")
async def register_user(user: User):
    # Логика для регистрации (например, сохранение в базе данных)
    return {"status": "success", "message": f"User {user.username} registered successfully!"}

@app.post("/api/login")
async def login_user(user: User):
    # Пример проверки логина и пароля
    if user.username == "test" and user.password == "password":
        return {"status": "success", "message": "Login successful!"}
    else:
        return {"status": "error", "message": "Invalid credentials"}

# Flet приложение
API_URL = "http://127.0.0.1:8000/api"  # URL для API запросов

def main(page: ft.Page):
    page.title = "Шахматная игра"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def login_action(e):
        username = login_input.value
        password = password_input.value
        if not username or not password:
            notification.content = "Пожалуйста, заполните все поля"
            page.update()
            return
        try:
            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
            response.raise_for_status()
            result = response.json()
            if result["status"] == "success":
                notification.content = "Успешная авторизация!"
                page.update()
                show_game()
            else:
                notification.content = result["message"]
        except requests.RequestException as ex:
            notification.content = f"Ошибка подключения: {ex}"
        page.update()

    def register_action(e):
        username = login_input.value
        password = password_input.value
        if not username or not password:
            notification.content = "Пожалуйста, заполните все поля"
            page.update()
            return
        try:
            response = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
            response.raise_for_status()
            result = response.json()
            notification.content = result["message"]
        except requests.RequestException as ex:
            notification.content = f"Ошибка подключения: {ex}"
        page.update()

    def show_game():
        page.controls.clear()
        page.add(
            ft.Text("Шахматная доска", size=20),
            ft.Text("Игра еще не началась. Логика игры будет реализована здесь."),
        )
        page.update()

    login_input = ft.TextField(hint_text="Введите логин")
    password_input = ft.TextField(hint_text="Введите пароль", password=True)
    notification = ft.Text(value="", size=16, color="red")

    page.add(
        ft.Text("Добро пожаловать в шахматы!", size=24, color="white"),
        login_input,
        password_input,
        ft.Row(
            [
                ft.ElevatedButton("Войти", on_click=login_action),
                ft.ElevatedButton("Зарегистрироваться", on_click=register_action),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        notification,
    )

# Запуск всех серверов
async def start_servers():
    # Запускаем FastAPI сервер в существующем цикле
    asyncio.create_task(run_fastapi())

    # Запускаем Flet приложение
    await ft.app(target=main)

# Функция для запуска FastAPI сервера
async def run_fastapi():
    # Запуск FastAPI с использованием существующего события
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Запуск приложения
if __name__ == "__main__":
    # Запуск всей программы через уже существующий цикл
    asyncio.run(start_servers())
