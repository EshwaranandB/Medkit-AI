# Medkit-AI

An AI-powered WhatsApp Assistant that offers **instant health information and wellness guidance**. Built with **FastAPI**, **Twilio**, and **DeepSeek V3**, this assistant provides 24/7 support to users—directly in their WhatsApp chat.



> ⚡ Demo it live: [Scan QR code or message](https://wa.me/YOUR_WHATSAPP_NUMBER)

---

## ✨ Features

- 🧠 Answers health & wellness questions using DeepSeek LLM
- 💬 Conversational memory per user (remembers name, symptoms, etc.)
- 🧾 Provides symptom insights, home remedies, emergency flags
- 📸 Ready for future upgrades like lab report parsing and image-based checks
- 🔒 Privacy-by-design: every user’s chat is isolated
- 📱 Fully integrated with Twilio WhatsApp
- ☁️ Deployable 24/7 via Railway or any cloud provider


---

## 🛠 Setup Instructions

### 1. Clone the repo


git clone https://github.com/your-username/your-healthbot.git
cd your-healthbot
pip install -r requirements.txt

2. Install dependencies
pip install -r requirements.txt

3. Create a .env file
   
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
OPENROUTER_API_KEY=your_openrouter_key

4. Run locally
uvicorn main:app --reload
Use Ngrok to expose localhost if testing with Twilio.

🚀 Deployment (Railway)
Push this repo to GitHub
Create new project on Railway → “Deploy from GitHub”
Set environment variables from .env
Get your public webhook and add to Twilio sandbox

🧪 Test Locally
You can test without WhatsApp using Postman or curl:
curl -X POST http://localhost:8000/test-api \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the symptoms of malaria?"}'


🛡 License
Licensed under the Apache 2.0 License.

👨‍⚕️ Future Scope
🧠 Medical report and prescription parsing
📸 X-ray and image-based symptom analysis
🔄 Voice input/output for accessibility
📊 Symptom dashboard for doctors/patients
⚙️ Admin panel + analytics


🤝 Contribution
Pull requests are welcome. If you’d like to add health modules, improve LLM context, or optimize Twilio usage—feel free to contribute!

🙋‍♂️ Author
Eshwar Anand Badugu
📍 BTech AIML @ Marwadi University
🚀 Building next-gen AI products
📬 [Connect on LinkedIn](https://www.linkedin.com/in/eshwar-anand-badugu/)




