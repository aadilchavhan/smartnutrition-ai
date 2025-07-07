# 🧠 The Smartest AI Nutrition Assistant  
### _SmartNutrition AI: Your Intelligent Nutrition Assistant_

This is a multimodal nutrition web app built with **Streamlit** and powered by **Gemini AI**, capable of analyzing text, voice, and images to deliver personalized meal plans, food insights, and expert-level advice.

---

## 🎯 Project Goal

The goal is to create an AI assistant that:
- Understands input via **text**, **voice**, and **images**
- Generates contextual answers using **LLM-based reasoning**
- Provides personalized meal plans based on dietary goals
- Simulates an expert nutritionist with adaptive learning
- Responds intelligently, just like a real dietician would

---

## 🖥️ Tech Stack

| Layer            | Tool                                           |
|------------------|------------------------------------------------|
| 🧠 AI Model       | `gemini-1.5-flash` via `google-generativeai`  |
| 🌐 Frontend       | Streamlit                                     |
| 🎤 Voice Input    | `SpeechRecognition` + `PyAudio`               |
| 🖼️ Image Input     | `Pillow`                                       |
| 🐍 Language       | Python 3.10                                   |

---

## 📦 Installation Guide

### ✅ Prerequisites

- **Python 3.10** (strictly recommended)
- OS: Windows, macOS, or Linux
- Working microphone (or WO Mic mobile integration)

---

### 🔧 Step-by-Step Setup

1. **Clone the project**
   ```bash
   git clone https://github.com/aadilchavhan/smartnutrition-ai.git
   cd smartnutrition-ai
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv nutri_env
   nutri_env\Scripts\activate   # On Windows
   # Or: source nutri_env/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **[⚠️ Windows only] Manually install PyAudio**
   ```bash
   pip install ./wheels/PyAudio-0.2.14-cp310-cp310-win_amd64.whl
   ```

5. **Configure Gemini API Key**
   Create `.streamlit/secrets.toml` and add:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   
   ```
**Important**
🔄 Please continue running all commands and launching the app in the same terminal where you activated the environment and installed dependencies.

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 🗂️ Project Structure

```
smartnutrition/
├── app.py                    # Main application logic
├── requirements.txt          # All dependencies
├── .streamlit/
│   └── secrets.toml          # Gemini API key storage
├── assets/                   # Static images
├── mealplanner.py            # Meal generation module
├── bmi_calculator.py         # BMI calculator module
├── calorie_calculator.py     # Calorie estimator
├── sidebar.py                # Navigation / layout
├── wheels/                   # PyAudio wheel (for Windows)
└── README.md                 # Project documentation
```

---

## 🔐 Requirements.txt Summary

```txt
streamlit==1.46.1
Pillow==10.3.0
google-generativeai==0.5.4
SpeechRecognition==3.10.0
PyAudio==0.2.14
```

---

## 🎤 Voice Input Tips

- Check mic permissions (Windows: Settings > Sound > Input).
- Speak clearly within 5 seconds of clicking “🎙 Speak Now”.

---

## 📷 Image Input Tips

- Upload a food photo or label.
- Optionally describe it (e.g. “low sugar?” or “good for diabetes”) for contextual analysis.

---

## ✅ Features at a Glance

- [x] Text query support
- [x] Voice transcription and analysis
- [x] AI-powered image meal analysis
- [x] Personalized meal planner
- [x] BMI & calorie calculator
- [x] User feedback system
- [x] Gemini Chat + Vision integration

---

## 🚀 Future Additions

- 🧠 Dynamic memory for user profiles/preferences
- 📩 Meal plan export (PDF/email)
- 📊 Nutrition history dashboard
- 🗨️ Chat-style follow-ups and revision capability

---

## 🙌 Credits

Built with ❤️ by **Aadil Chauhan** and team:

- [Aadil Chauhan ](https://www.linkedin.com/in/aadilchavhan)
- [Afshan Sultana ](https://www.linkedin.com/in/syeda-afshan-sultana)
- [Mohammed Aadil](https://www.linkedin.com/in/mohammed-aadil-39b2182b5/)
- [Kumar Aditya](https://www.linkedin.com/in/kumar-aditya-6374a2332/)
- [Ankit Tiwari](https://www.linkedin.com/in/ankit-tiwari-3a1a7b175/)

Using:

- [Streamlit](https://streamlit.io/)
- [Gemini API](https://makersuite.google.com/app)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Pillow](https://python-pillow.org)

---

## 📬 Feedback

Have an idea, issue, or improvement?
Open a GitHub issue or connect with the authors via LinkedIn!

---
