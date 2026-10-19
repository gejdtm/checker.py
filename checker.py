import random
import string
import requests
import threading

TOKEN = "8480653939:AAETmdrqWjqOl9GmFqzXqbrzAv3CVnzpYvM"
CHAT_ID = "7702458407"

letters = string.ascii_lowercase
all_chars = string.ascii_lowercase + string.digits

BLOCKED_KEYWORDS = ["admin", "support", "help", "official", "snapchat", "tiktok", "instagram", "root", "api", "test"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def send_msg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": text}, timeout=3)
    except:
        pass

def filtered_checker(platform):
    session = requests.Session()
    while True:
        username = random.choice(letters) + ''.join(random.choices(all_chars, k=3))
        
        if any(word in username for word in BLOCKED_KEYWORDS):
            continue
        
        try:
            if platform == "tiktok":
                res = session.get(f"https://www.tiktok.com/@{username}", headers=headers, timeout=3)
                if res.status_code == 404 and ("Couldn't find this account" in res.text or "account not found" in res.text.lower()):
                    send_msg(f"🔥 صيد حقيقي | تيك توك:\n@{username}")

            elif platform == "instagram":
                res = session.get(f"https://www.instagram.com/{username}/", headers=headers, timeout=3)
                if res.status_code == 404 and ("The link you followed may be broken" in res.text or "page isn't available" in res.text.lower()):
                    send_msg(f"🔥 صيد حقيقي | إنستغرام:\n@{username}")

            elif platform == "snapchat":
                res = session.get(f"https://www.snapchat.com/add/{username}", headers=headers, timeout=3)
                if res.status_code == 200:
                    text_lower = res.text.lower()
                    if "sign up" in text_lower or "create your account" in text_lower:
                        if "this username is not available" not in text_lower and "not found" not in text_lower:
                            send_msg(f"🔥 صيد حقيقي | سناب شات:\n@{username}")
        except:
            pass

print("🚀 جاري بدء الفحص المنضبط...")
send_msg("🛡️ تم تفعيل المستودع الجديد بنجاح والبوت جاهز!")

threads = []
for _ in range(15):
    t_tk = threading.Thread(target=filtered_checker, args=("tiktok",))
    t_ig = threading.Thread(target=filtered_checker, args=("instagram",))
    t_sc = threading.Thread(target=filtered_checker, args=("snapchat",))
    threads.extend([t_tk, t_ig, t_sc])

for t in threads:
    t.start()
