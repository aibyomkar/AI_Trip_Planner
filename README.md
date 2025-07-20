> ⚠️ **Disclaimer**: This project is based on the tutorial and original work by [Krish Naik](https://www.youtube.com/@KrishNaik) and the code from Sunny Sir [sunnysavita10/AI_Trip_Planner](https://github.com/sunnysavita10/AI_Trip_Planner). I followed it for learning and educational purposes and just named it 'Roamio' because It felt cool.

# 🌍 Roamio - AI Trip Planner By Omkar

**Roamio** is a full-stack AI web app that uses technologies like Groq and LangGraph to generate detailed travel itineraries based on a user’s prompt. It features a Streamlit-powered frontend and a FastAPI backend, both deployed live and kept running with uptime monitoring.

---

## 🔗 Live Demo

- **Frontend (Streamlit):** https://roamio.streamlit.app  
- **Backend API:** https://ai-trip-planner-backend-jrdl.onrender.com  

Try it live! Enter a destination or travel style and receive a personalized multi-day trip plan instantly.

---

## ⚙️ Tech Stack & Structure

| Layer      | Tech & Role |
|------------|-------------|
| Frontend   | **Streamlit**, `requests`, HTML/CSS |
| Backend    | **FastAPI**, `uvicorn`, `pydantic`, CORS |
| Agent Logic| **LangGraph**, `groq`, AI agents to build dynamic itinerary graphs |
| Hosting    | **Streamlit Cloud** (frontend) + **Render** (backend) |
| Uptime     | **UptimeRobot** pings every 5 mins to keep both services live |

---

## 📦 Features

- **Natural-language travel planning** – prompt with details like destination, duration, preferences, and budget.
- **Agentic AI workflow** leveraging Groq and LangGraph for dynamic plan generation.
- **PNG graph generation** of the itinerary structure.
- **GET/HEAD health endpoint** for uptime monitoring (`/`).
- **CORS restricted** to only allow the Streamlit frontend.
- **24/7 uptime** using UptimeRobot free-tier monitoring.

---

## 🧠 What Can Roamio Do?

Roamio is your AI-powered personal travel assistant that can:

- 🧳 Understand your travel preferences: destination, dates, budget, group type, vibe, interests, and more.
- 🧠 Intelligently reasons and takes actions based on your input
- 🧭 Generate full day-wise itineraries personalized just for you, instantly.
- 🏙️ Suggest real places to visit — including landmarks, cafes, hidden gems, museums, and local experiences.
- 🗺️ Organize the itinerary intelligently with proper ordering, timing, and proximity-based suggestions.
- ✨ Discover offbeat locations and non-touristy ideas using real-time data from Tavily and Google Places APIs.
- 🔍 Backed by **Google Maps’ dataset of over 200 million+ verified places**, Roamio gives incredibly accurate, data-rich recommendations.
- 📆 Auto-balances days with different types of activities: cultural, relaxing, adventurous, scenic, etc.
- 🌐 Fetch weather, travel tips, and even exchange rate info dynamically.
- 💡 Ideal for solo travelers, couples, family holidays, or even group adventures.
- 🌟 Live 24 X 7

Whether you're planning a weekend escape or a multi-country backpacking trip — Roamio does it all.

---

## 🚀 Getting Started – Developer Setup

### 1. Clone & install

```bash
git clone https://github.com/aibyomkar/AI_Trip_Planner.git
cd AI_Trip_Planner
pip install -r requirements.txt
````

### 2. Environment Variables

Create a `.env` file or export the vars:

```text
OPENAI_API_KEY=...
GROQ_API_KEY=...
GOOGLE_API_KEY=...
GPLACES_API_KEY=...
FOURSQUARE_API_KEY=...
TAVILY_API_KEY=...
OPENWEATHERMAP_API_KEY=...
EXCHANGE_RATE_API_KEY=...
```

### 3. Local Run

**Backend:**

```bash
uvicorn main:app --reload
```

**Frontend (in another terminal):**

```bash
streamlit run streamlit_app.py
```

Visit `http://localhost:8501`, prompt your AI, and check the backend logs.

---

## 🛠 Deployment (Already Live!)

### Backend (Render)

* Branch: `main`
* Build: `pip install -r requirements.txt`
* Start: `uvicorn main:app --host 0.0.0.0 --port 10000`
* Health Check: `/` (GET & HEAD)
* CORS: allowed origin = `https://roamio.streamlit.app`
* Auto-deploy is enabled

### Frontend (Streamlit Cloud)

* Connected to GitHub repo
* Automatically redeploys on `main` commits
* Uses correct backend URL in `streamlit_app.py`

---

## 🔐 Keeping It Alive (Free)

Use **UptimeRobot** to prevent sleep:

* Create 2 monitors (5-min intervals)

  1. **Frontend** → `https://roamio.streamlit.app/`
  2. **Backend** → `https://ai-trip-planner-backend-jrdl.onrender.com/`
* Backend monitor checks via `HEAD` → served by the `GET/HEAD /` endpoint you added
* Both services will remain awake indefinitely on free tiers

---

## 📞 Troubleshooting

* **CORS errors:** Ensure `allow_origins` matches exact frontend URL.
* **405 errors:** Your `@app.head("/")` covers monitoring pings.
* **Deployment issues:** Check Render logs; ensure env vars are set.
* **Cold starts:** Adjusted request timeouts or add onboarding messages for users.

---

## 🧑‍💻 Contribute

Contributions are welcome! Here’s how to help:

1. Fork the repo, create a branch (`feature/xyz`)
2. Make updates or add tests
3. Push and create a Pull Request
4. I’ll review and merge it in 👌

---

## 🌟 Roadmap & Ideas

* Add **authentication** to save trips (e.g., via Firebase/Google OAuth)
* Allow **exporting itineraries** to PDF or calendar
* Add **map integration** (e.g., Folium, Google Maps)
* Improve AI logic — add constraint handling, multi-city trips
* Implement **caching** of repeated queries to reduce AI costs

---

## 📄 Disclaimer & Credits

This project is not an original creation. It is built entirely by following the educational tutorials of [Krish Naik](https://www.youtube.com/c/KrishNaik) and [Sunny Sir](https://github.com/sunnysavita10/AI_Trip_Planner).
The purpose of this repository is solely for learning, practice, and educational demonstration.
**All credit for the core logic and design goes to the original creators.**

---

## 📫 Contact

* GitHub: [aibyomkar/AI\_Trip\_Planner](https://github.com/aibyomkar/AI_Trip_Planner)
* Instagram: [@omkar\_raps](https://www.instagram.com/omkar_raps?igsh=MWN5cHVuZDV3MjZ4NA%3D%3D&utm_source=qr)
* Email: reach out via GitHub

---

**Enjoy planning your adventures with AI, anytime, anywhere 🌍✈️**