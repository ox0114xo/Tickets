from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
import ddddocr
import asyncio

app = FastAPI()
ocr = ddddocr.DdddOcr(show_ad=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GrabTask(BaseModel):
    url: str
    zone: str

async def perform_grab(url, zone):
    """這是在雲端運行的實戰搶票邏輯"""
    async with async_playwright() as p:
        # 雲端必須使用 headless=True
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print(f"[*] 機器人出發：{url}")
            await page.goto(url)
            
            # 1. 尋找並點擊立即購票
            buy_btn = "input[value='立即購票']"
            await page.wait_for_selector(buy_btn, timeout=10000)
            await page.click(buy_btn)
            
            # 2. 辨識驗證碼 (寬宏常見 ID)
            captcha_sel = "#CaptchaImage"
            if await page.query_selector(captcha_sel):
                img_bytes = await page.locator(captcha_sel).screenshot()
                res = ocr.classification(img_bytes)
                print(f"[*] AI 辨識驗證碼：{res}")
                await page.fill("#CaptchaInput", res)
            
            # 3. 點選區域
            await page.click(f"text='{zone}'")
            print(f"[+] 已進入 {zone} 選擇頁面！")
            
        except Exception as e:
            print(f"[X] 搶票失敗：{e}")
        finally:
            # 保持一段時間觀察結果再關閉
            await asyncio.sleep(10)
            await browser.close()

@app.post("/grab")
async def start_grab(task: GrabTask):
    # 使用 create_task 讓搶票在背景執行，不阻塞網頁回傳
    asyncio.create_task(perform_grab(task.url, task.zone))
    return {"status": "Success", "message": f"雲端機器人已出發前往搶購 {task.zone}！"}

@app.get("/")
async def root():
    return {"status": "Active", "user": "張家銘", "msg": "搶票引擎準備就緒"}
