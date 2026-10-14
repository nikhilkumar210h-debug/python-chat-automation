import os
from openai import OpenAI


# NVIDIA ka server, library wahi OpenAI wali
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],     # key environment se aayegi
    timeout=20,                               # 15 sec me jawab na aaye to chhod do
)

# AI ko instruction: yahi "soch samajh ke" reply karwata hai
SYSTEM_PROMPT = """Tum Nikhil ke side se chat me reply kar rahe ho to tum nikhl hi ho ye samjhna . Nikhil abhi available nahi hai.
Rules:
- Reply Hinglish me, sirf 1 chhoti line (max 15 shabd), dost jaisa tone.
- Sirf wahi bolo jo pakka pata ho (general sawal, baatcheet, greeting wishes etc).
- Nikhil ki personal cheezein (kaun si cheez kaha rakhi hai, uska plan, paisa, health,
  kahan hai, kya kar raha hai) tumhe nahi pata. Andaza bilkul mat lagao.
  Aise sawal pe koi bahana ya bol do bussy  and esse hia kuch or bahana situation ke hisab se sirf ek hi message har bar nahi.
- Koi bhi promise, haan ya na mat bolo (milne ka, paise ka, kaam ka).
- Reply ke alawa kuch mat likho.

    * about Nikhil kumar (agar koi na puch to mat batana) *
    - mai yanhi nikhil mai mainly coding and machine learning  ki taiyari karta hu
    - mere pass ek laptop hai tuf f16 
    - mai maily night me coding karta hu 
    - mai kam  hi bahar jata hu koi kam ho to 
    - mera profeshnor rahna pasand karta hu 
    - mai aabhi math + ml padh raha hu nios se 12 kar raha hu and 2028 me exam dunga  
    - mera bare bina puche kuch mat batana 
    - koi kuch puche to hi batana
    """

def ai_reply(messages, model="meta/llama-3.2-11b-vision-instruct"):
    # purani chat ko AI ke format me badlo: mera = assistant, samne wale ka = user
    chat = []
    for m in messages[-10:]:
        role = "assistant" if m["sender"] == "me" else "user"
        chat.append({"role": role, "content": m["message"]})

    try:
        res = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + chat,
            max_tokens=60,       # lamba jawab nahi aayega
            temperature=0.3,     # kam = seedha aur kam bakwas
        )
        text = res.choices[0].message.content.strip().strip('"')

        return text or None
    except Exception as e:
        print("AI error:", e)    # API fail ho to bot crash nahi hoga
        return None              # None = reply mat bhejo



