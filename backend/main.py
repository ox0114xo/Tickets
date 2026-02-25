from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ddddocr
# 我們暫時把報錯的 stealth 換成基礎引入，確保大腦能先開機
import asyncio

app = FastAPI()
ocr = ddddocr.DdddOcr(show_ad=False)

# 補上這段，你的 Vercel 網頁才能連進來
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GrabTask(BaseModel):
    url: str
    zone: str

@app.get("/")
async def index():
    return {"status": "大腦運作中", "msg": "家銘，你的搶票機已經在線了！"}

@app.post("/grab")
async def start_grab(task: GrabTask):
    # 這裡就是未來執行 Playwright 搶票邏輯的地方
    print(f"啟動搶購指令：{task.url} / 區域：{task.zone}")
    return {"status": "Success", "message": f"已接收指令：前往搶購 {task.zone}"}
