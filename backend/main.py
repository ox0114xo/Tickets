from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
import ddddocr
import asyncio
import os # 用來讀取帳號密碼

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
    # 從 Railway 的環境變數讀取帳號密碼
    user_account = os.getenv("KHAM_USER")
    user_password = os.getenv("KHAM_PWD")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # 1. 先去登入頁
            print("[*] 正在執行自動登入...")
            await page.goto("https://kham.com.tw/application/UTK02/UTK0201_03.aspx")
            await page.fill("#MemberID", user_account)
            await page.fill("#MemberPassword", user_password)
            
            # 登入頁也有驗證碼
            if await page.query_selector("#CaptchaImage"):
                captcha_bytes = await page.locator("#CaptchaImage").screenshot()
                login_captcha = ocr.classification(captcha_bytes)
                await page.fill("#CaptchaInput", login_captcha)
            
            await page.click("input[value='登入']")
            await page.wait_for_timeout(2000) # 等待登入跳轉
            
            # 2. 前往目標節目頁
            print(f"[*] 登入成功，前往目標：{url}")
            await page.goto(url)
            
            # 3. 立即購票
            buy_btn = "input[value='立即購票']"
            await page.wait_for_selector(buy_btn, timeout=5000)
            await page.click(buy_btn)
            
            # 4. 辨識購票驗證碼並選區
            await page.wait_for_selector("#CaptchaImage")
            ticket_captcha_bytes = await page.locator("#CaptchaImage").screenshot()
            ticket_captcha = ocr.classification(ticket_captcha_bytes)
            print(f"[*] 購票驗證碼辨識結果：{ticket_captcha}")
            
            await page.fill("#CaptchaInput", ticket_captcha)
            await page.click(f"text='{zone}'")
            
            print(f"[★] 成功進入 {zone}！請盡快接手完成後續結帳。")
            
        except Exception as e:
            print(f"[X] 搶票過程出錯：{e}")
        finally:
            await asyncio.sleep(20) # 保持一段時間讓系統反應
            await browser.close()

@app.post("/grab")
async def start_grab(task: GrabTask):
    asyncio.create_task(perform_grab(task.url, task.zone))
    return {"status": "Success", "message": "機器人已登入並出發！"}

@app.get("/")
async def root():
    return {"status": "Active", "msg": "家銘專屬搶票引擎完全體已就位"}
