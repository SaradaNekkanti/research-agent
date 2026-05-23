# 🔬 AI Research Brief Agent

> **An AI-powered tool that generates structured research briefs in seconds — built with Python, FastAPI, and OpenAI.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📌 The Problem

Researchers, analysts, and product managers spend **hours** manually compiling briefs on companies, markets, and trends — reading dozens of tabs, summarising findings, and identifying risks before making decisions.

## 💡 The Solution

**AI Research Brief Agent** takes any topic or company name and generates a fully structured research brief in under 15 seconds — automatically saving it as a Markdown file for future reference.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Instant AI Briefs** | Enter any topic or company → get a structured 4-section brief |
| 📋 **Summary** | Concise 3–5 sentence overview |
| 💡 **Key Insights** | 5 most important facts, trends, or findings |
| ⚠️ **Risks** | Key challenges and concerns to be aware of |
| ✅ **Action Items** | Concrete next steps for decision-making |
| 💾 **Auto-Save Reports** | Every brief saved as a `.md` file in `/reports` |
| 📋 **Copy & Download** | One-click copy to clipboard or download as Markdown |
| 📁 **Reports History** | Browse all previously generated briefs |
| 🎨 **Premium UI** | Dark mode glassmorphism design with smooth animations |

---

## 🖥️ Demo

> *Enter a topic like "Tesla", "Climate Change", or "Quantum Computing" — the AI generates a full brief in ~10 seconds.*

```
Topic: OpenAI

📋 Summary
OpenAI is an AI research company founded in 2015...

💡 Key Insights
- GPT-4 powers over 100 enterprise applications
- Revenue exceeded $1.6B in 2023...

⚠️ Risks
- Regulatory scrutiny increasing globally
- High compute costs limit profitability...

✅ Action Items
- Monitor OpenAI's enterprise pricing changes
- Evaluate API rate limits for production use...
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Browser (User)                       │
│          HTML + Vanilla CSS + Vanilla JS                 │
└──────────────────────┬──────────────────────────────────┘
                       │ POST /generate (FormData)
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (app.py)                     │
│   • Validates input                                      │
│   • Builds structured prompt                             │
│   • Calls OpenAI Chat Completions API                    │
│   • Saves report as .md to /reports                      │
│   • Returns JSON to frontend                             │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   OpenAI API                  /reports/
 (gpt-4o-mini)            (Markdown files)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys) (requires billing — ~$0.0001 per brief)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/research-agent.git
cd research-agent

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Open .env and replace the placeholder with your real key:
# OPENAI_API_KEY=sk-your-key-here

# 5. Run the server
uvicorn app:app --reload
```

### Open in browser
```
http://localhost:8000
```

---

## 📁 Project Structure

```
research-agent/
├── app.py                  # FastAPI backend — routes, OpenAI calls, report saving
├── requirements.txt        # Python dependencies
├── .env.example            # Template for environment variables (safe to commit)
├── .gitignore              # Excludes .env, venv, __pycache__, etc.
├── templates/
│   └── index.html          # Frontend — form, result cards, reports list
├── static/
│   └── style.css           # Dark glassmorphism design system
└── reports/                # Auto-generated .md research briefs saved here
```

---

## 🔐 Security

- **API keys are never committed to Git** — stored only in `.env` (excluded by `.gitignore`)
- The `.env.example` file shows the required variable names with a placeholder value
- Reports are stored locally and never sent to any third party beyond OpenAI

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python · FastAPI · Uvicorn |
| **AI** | OpenAI `gpt-4o-mini` via Chat Completions API |
| **Frontend** | HTML5 · Vanilla CSS · Vanilla JavaScript |
| **Templating** | Jinja2 |
| **Config** | python-dotenv |
| **Reports** | Markdown (`.md`) files |

---

## 📈 PM Case Study

### Problem
Knowledge workers waste significant time on manual research aggregation before meetings, pitches, and product decisions.

### Hypothesis
If I can reduce research brief creation from ~2 hours to <15 seconds, teams can move faster and make better-informed decisions.

### Solution Built
A beginner-friendly AI agent with a clean web UI that accepts a topic, sends a structured prompt to GPT-4o-mini, and returns a 4-section structured brief — automatically saved locally.

### Key Decisions
- **`gpt-4o-mini` over GPT-4**: 95% quality at 10x lower cost for structured text output
- **Markdown output**: Universal format — readable in Notion, GitHub, Obsidian, VS Code
- **No database**: Local file storage keeps the tool simple and portable for solo users
- **Structured prompt with exact headings**: Forces consistent output that the frontend can parse reliably

### Metrics (Hypothetical KPIs)
| Metric | Target |
|---|---|
| Time to generate brief | < 15 seconds |
| Cost per brief | < $0.001 |
| User actions to get result | 1 (type + click) |
| Sections per brief | 4 (consistent) |

---

## 🗺️ Roadmap

- [ ] Add Google Gemini / Groq support (free tier alternatives)
- [ ] Export briefs as PDF
- [ ] Compare two companies side-by-side
- [ ] Add source citations via web search integration
- [ ] Multi-user support with login

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT License — feel free to use this in your own projects.

---

*Built with ❤️ using FastAPI and OpenAI · Designed for researchers, analysts, and PMs*
