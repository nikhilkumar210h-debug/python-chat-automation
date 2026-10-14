
import time 
from playwright.sync_api import sync_playwright

   
from ai_reply import ai_reply
from rules import get_reply
import json
from logger import log_event

BRAVE = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
PROFILE = r"C:\brave_profile"


try:
    with open("config.json", "r") as jsonfile:
        config = json.load(jsonfile)

    target_user = config["target_user"]
    check_interval = config["check_interval"]
    auto_send = config["auto_send"]
    ai_enabled = config.get("ai_enabled", False)           # key na ho to False
    ai_model = config.get("ai_model", "meta/llama-3.2-11b-vision-instruct")

except FileNotFoundError:
    raise SystemExit("config.json file nahi mili. File check karo.")

except json.JSONDecodeError:
    raise SystemExit("config.json ka JSON invalid hai. Syntax check karo.")

except KeyError as e:
    raise SystemExit(f"Config mein required key missing hai: {e}")

def read_messages(page, limit=10):
    rows = page.locator(".private-msg-row")
    n = rows.count()
    messages = []
    for i in range(max(0, n - limit), n):       # sirf aakhri 10 padho (fast)
        row = rows.nth(i)
        cls = row.get_attribute("class")        # "private-msg-row theirs ..."
        messages.append({
            # theirs = samne wala, mine = main. Ye uid se banta hai, naam se nahi
            "sender": target_user if "theirs" in cls else "me",
            "message": row.locator(".message-content").inner_text(),
            "time": row.locator(".message-time").inner_text().split("\n")[0],
            "id": row.get_attribute("data-msg-id"),   # har message ki unique id
        })
    return messages

def send_reply(page, reply):
    page.fill("#privateInput", reply)           # box me text
    page.press("#privateInput", "Enter")        # Enter = Send

def main(ctx):                    
    page = ctx.new_page()        
    page.goto("https://trio-day.trioday-nikhil.workers.dev/chat")
    page.wait_for_selector("#userList .nkm-chat-row")
    page.locator("#userList .nkm-chat-row") \
    .filter(has_text=target_user) \
    .locator("a.nkm-chat-row-main") \
    .click(no_wait_after=True)        
    page.wait_for_selector(".private-msg-row")  

    print("Chat automation started...")
    print(f"AUTO_SEND : {auto_send} | Dry-run mode")

    try:
        last_seen = None
        baseline_done = False
        while True:

            # M1: chat text capture
            messages = read_messages(page)
            if not messages:
                print('no new meqssages')
                time.sleep(check_interval)
                continue

            latest = messages[-1]
            sender, message = latest["sender"], latest["message"]
            print(latest)

            if not baseline_done:
                last_seen = latest["id"]     
                baseline_done = True
                print("Purana message note kar liya, naye ka wait")
                time.sleep(check_interval)
                continue

            if latest["id"] == last_seen: 
                print("Koi naya message nahi")
                time.sleep(check_interval)
                continue

            # M3: rule engine
            result = get_reply(messages, target_user)
            reply = result["reply"]          # None ya string

            if reply is None and ai_enabled and latest["sender"] == target_user:
                reply = ai_reply(messages, ai_model)
                reply = (reply)
                if reply:
                    print("AI reply:",reply)
            if reply is None:
                status = "no_reply"
            elif auto_send is False:
                status = "dry-run"
            else:
                status = "sent"

            print("Decision:")
            print(result)

            #send_reply
            if reply is not None and auto_send:
                send_reply(page, (reply))
                
                page.wait_for_timeout(1000)
                last_seen = read_messages(page)[-1]["id"]   # apna bheja hua message mark
            else:
                last_seen = latest["id"]                    # bas jo dekha wahi mark

            # M4: log event 
            log_event(sender, message, reply, status)
            time.sleep(check_interval)

    except KeyboardInterrupt:          # Ctrl+C ke liye, Exception se pehle likho
        print("\nProgram safely stopped.")
    except Exception as e:
        print("Error:", e)
        input("Enter dabao to browser band hoga...")
    


if __name__ == "__main__":
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE, executable_path=BRAVE, headless=False
        )
        main(ctx)    

        