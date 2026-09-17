
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from google import genai

app = FastAPI()

# НАСТРОЙКА CORS: разрешаем вашему сайту (фронтенду) обращаться к этому серверу
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы с любых доменов
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
        # Используем потоковый метод генерации
        response_stream = client.models.generate_content_stream(
            model="gemini-3.5-flash",
            contents=request.prompt,
        )
        
        # Генератор для отправки кусочков текста клиенту по мере поступления
        def generate():
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

        return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")
        
    except Exception as e:
        print(f"Ошибка при генерации контента: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Главная страница: открывает index.html интерфейс
@app.get("/", response_class=HTMLResponse)
async def read_index():
    html_path = "index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "<h3>Файл index.html не найден в корне проекта!</h3>"

# Автоматический запуск через Uvicorn, если файл запускается напрямую
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
