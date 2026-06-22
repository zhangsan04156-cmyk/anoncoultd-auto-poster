from playwright.sync_api import Playwright, sync_playwright
import time,sys

MESSAGES = []
each_wait = 0
def ask_message():
    global MESSAGES,each_wait
    new_message = input("請輸入下一則訊息後Enter(一行內，直接Enter代表結束)")
    if new_message:
        MESSAGES.append(new_message)
        ask_message()
    elif not MESSAGES:
        print("請輸入至少一則訊息")
        ask_message()
    elif len(MESSAGES)!=1:
        each_wait = input("請輸入每個訊息間隔多久(min)")
        try:
            each_wait = int(each_wait)*60
        except:
            each_wait = 5*60
            print("輸入錯誤，預設為 5 min")


def run(playwright: Playwright,message:str) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    # 前往 ANON 投稿頁面
    page.goto("https://www.anoncoultd.com/submit")
    
    # 執行點擊與選擇流程
    page.get_by_role("button", name="同意協議，接受所有 Cookie").click()
    page.wait_for_timeout(1000)
    
    page.get_by_role("button", name="海山 HSJH").click()
    page.get_by_role("button", name="確認選擇").click()
    page.wait_for_timeout(1000)
    
    page.get_by_role("button", name="全部標為已讀").click()
    
    # 輸入獨立出來的 message 變數內容
    textarea_name = "今天發生了什麼事？你可以放心寫在這裡。"
    page.get_by_role("textbox", name=textarea_name).click()
    page.get_by_role("textbox", name=textarea_name).fill(message)
    
    # 送出投稿
    page.get_by_role("button", name="送出投稿").click()
    
    # 留 5 秒確認畫面後關閉
    page.wait_for_timeout(5000)
    context.close()
    browser.close()

def main():
    try:
        global MESSAGES,each_wait
        assert isinstance(each_wait,(float,int))
        ask_message()
        for message in MESSAGES:
            with sync_playwright() as playwright:
                run(playwright,message)
            print(f"成功發文！\n{message}")
            print(f"等待 {each_wait//60} 分鐘...",end="")
            time.sleep(each_wait)
            print()
        print("任務已經全部完畢")
    except Exception as e:
        print(f"出現問題！\n{e}")
    input("按Enter結束")
    sys.exit()


if __name__ == "__main__":
    main()