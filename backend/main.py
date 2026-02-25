from fastapi import FastAPI
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async
import ddddocr
import asyncio

app = FastAPI()
ocr = ddddocr.DdddOcr(show_ad=False)

@app.get("/")
async def index():
    return {"status": "搶票引擎運作中"}

@app.post("/grab")
async def start_grab(url: str, zone: str):
    # 這裡未來會放入完整的搶票邏輯
    return {"message": f"正在嘗試搶購 {zone}"}
