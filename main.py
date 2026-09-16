import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai

app = FastAPI()

# Инициализация клиента Gemini (автоматически берет GEMINI_API_KEY из переменных окружения Railway)
try:
    client = genai.Client()
except Exception as e:
    print(f"Ошибка инициализации Gemini client: {e}")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/api/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        # Отправка запроса к модели (используем быструю модель gemini-2.5-flash)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.prompt,
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Раздаем статические файлы фронтенда (index.html, картинки и т.д.)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def read_index():
    return FileResponse("index.html")
