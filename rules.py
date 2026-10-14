import re

RULES = [
    {
        "name": "exact_hello",
        "type": "exact",
        "trigger": "hello",
        "reply": "Hello bhai!"
    },
    {
        "name": "hi",
        "type": "exact",
        "trigger": ["hi","hii"],
        "reply": "Hii bhai!"
    },
    {
        "name": "hy",
        "type": "exact",
        "trigger": ['hy','hyy','hyyy'],
        "reply": "Hii bhai!"
    },
    {
        "name": "study_keyword",
        "type": "keyword",
        "trigger": ["study","padhai"],
        "reply": "Padhai mode ON 📚"
    },
    {
        "name": "python_keyword",
        "type": "keyword",
        "trigger": "python",
        "reply": "Python chal rahi hai kya? 🐍"
    },
    {
        "name": "how_are_you",
        "type": "phrase",
        "trigger": ["kaise ho ","how are you","kaise ho bro"],
        "reply": "Badhiya bhai, tu bata!"
    },
    {
        "name": "what_are_you_doing",
        "type": "phrase",
        "trigger": "kya kar raha",
        "reply": "Bas code ke saath kushti chal rahi hai 😂"
    },
    {
        "name": "good_morning",
        "type": "phrase",
        "trigger": "good morning",
        "reply": "Good morning bhai ☀️"
    },
    {
        "name": "good_night",
        "type": "phrase",
        "trigger": "good night",
        "reply": "Good night bhai, kal milte hain 😴"
    },
    {
        "name": "thanks",
        "type": "keyword",
        "trigger": "thanks",
        "reply": "Koi baat nahi bhai 😎"
    },
    {
        "name": "haha",
        "type": "keyword",
        "trigger": "haha",
        "reply": "😂😂"
    },

        ]



def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text.lower())   # ! . ? , aur emoji hata deta hai 
    return " ".join(text.split())                  # extra space hata deta hai

def rule_matches(message, rule):
    triggers = rule["trigger"]
    if isinstance(triggers, str):          # ek string ho to list bana 
        triggers = [triggers]

    for t in triggers:                     # har trigger check hua
        trigger = clean_text(t)
        if rule["type"] == "exact" and message == trigger:
            return True
        elif rule["type"] == "phrase" and trigger in message:
            return True
        elif rule["type"] == "keyword" and trigger in message.split():
            return True
    return False                           # kisi se match nahi hua to
 
def get_reply(messages, target_user):
    if not messages:
        return {
            "reason": "Koi message hi nahi hai 😴",
            "reply": None
        }
    latest = messages[-1]

    if latest["sender"] != target_user:
        return {
            "reason": "Latest message target user ka nahi hai",
            "reply": None
        }

    message = clean_text(latest["message"])

    if not message:
        return {
            "reason": "Message khaali hai... bot bhi kya bole 😂",
            "reply": None
        }

    for rule in RULES:

        if rule_matches(message, rule):
            return {
                "reason": f"Rule matched: {rule['name']}",
                "reply": rule["reply"]
            }

    return {
        "reason": "Koi rule nahi mila... bot ne aaj chhutti le li 😂",
        "reply": None
    }