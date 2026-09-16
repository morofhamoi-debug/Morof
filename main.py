import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

# НАСТРОЙКА CORS: разрешаем вашему сайту (фронтенду) обращаться к этому серверу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых доменов (GitHub Pages, PythonAnywhere и т.д.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация клиента Gemini
try:
    client = genai.Client()
except Exception as e:
    print(f"Ошибка инициализации Gemini client: {e}")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/api/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        # Используем современную и быструю gemini-3.5-flash
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=request.prompt,
        )
        return {"response": response.text}
    except Exception as e:
        print(f"Ошибка при генерации контента: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Простая проверка работоспособности сервера
@app.get("/")
def read_index():
    return {"status": "Сервер MOROF успешно работает на Railway!"}
