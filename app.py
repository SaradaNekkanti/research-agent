# ============================================================
# app.py — AI Research Brief Agent (FastAPI Backend)
# ============================================================
# This is the main server file. It:
#   1. Serves the HTML frontend page
#   2. Receives the user's topic from the form
#   3. Sends a structured prompt to OpenAI
#   4. Returns the AI-generated brief to the browser
#   5. Saves the brief as a Markdown file in /reports
# ============================================================

import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI, RateLimitError, AuthenticationError, APIError

# ── Load environment variables from .env file ──────────────────────────────
# Create a .env file in this folder with: OPENAI_API_KEY=sk-...
load_dotenv()

# ── Initialise the FastAPI app ─────────────────────────────────────────────
app = FastAPI(title="AI Research Brief Agent")

# ── Mount static files (CSS, images, etc.) ────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── Point Jinja2 at the templates folder ──────────────────────────────────
templates = Jinja2Templates(directory="templates")

# ── Initialise the OpenAI client ──────────────────────────────────────────
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── Ensure the reports directory exists ───────────────────────────────────
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


# ── Helper: build the prompt sent to OpenAI ───────────────────────────────
def build_prompt(topic: str) -> str:
    """
    Returns a structured prompt that asks the AI to produce a research
    brief in four clearly labelled sections.
    """
    return f"""
You are an expert research analyst. Generate a comprehensive research brief for the following topic or company:

**Topic / Company:** {topic}

Please structure your response with these exact headings:

## Summary
A concise 3-5 sentence overview of the topic or company.

## Key Insights
- Bullet-point list of the 5 most important insights, trends, or facts.

## Risks
- Bullet-point list of 4-5 key risks, challenges, or concerns.

## Action Items
- Bullet-point list of 4-5 concrete, actionable next steps for someone researching this topic.

Keep the language clear and beginner-friendly. Be specific and informative.
"""


# ── Helper: slugify a topic name for use as a filename ────────────────────
def slugify(text: str) -> str:
    """Converts 'Apple Inc.' → 'apple_inc' for safe filenames."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)   # remove special chars
    text = re.sub(r"[\s-]+", "_", text)     # spaces → underscores
    return text


# ── Helper: save the brief as a Markdown file ─────────────────────────────
def save_report(topic: str, content: str) -> str:
    """
    Saves the AI-generated brief to reports/<slug>_<timestamp>.md
    Returns the file path as a string.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{slugify(topic)}_{timestamp}.md"
    filepath = REPORTS_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Research Brief: {topic}\n")
        f.write(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}*\n\n")
        f.write(content)

    return str(filepath)


# ══════════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════════

# ── GET / ─── Serve the main HTML page ────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renders the main research brief input page."""
    return templates.TemplateResponse("index.html", {"request": request})


# ── GET /reports ─── List all saved reports ───────────────────────────────
@app.get("/reports-list")
async def list_reports():
    """Returns a list of all saved report filenames."""
    files = sorted(REPORTS_DIR.glob("*.md"), reverse=True)
    return {"reports": [f.name for f in files]}


# ── POST /generate ─── Generate a research brief ─────────────────────────
@app.post("/generate")
async def generate_brief(topic: str = Form(...)):
    """
    Receives the topic from the HTML form, calls OpenAI, saves the
    report, and returns the brief content as JSON.

    The frontend (index.html) reads this JSON and displays it on the page.
    """

    # Validate: make sure the topic is not empty
    if not topic.strip():
        return JSONResponse(
            content={"error": "Please enter a topic or company name."},
            status_code=400,
        )

    # Build the prompt
    prompt = build_prompt(topic.strip())

    # Call the OpenAI Chat Completions API
    # "gpt-4o-mini" is cost-effective and great for structured text tasks
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional research analyst who writes clear, "
                        "structured, and insightful research briefs."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,     # slight creativity while staying factual
            max_tokens=1500,     # enough for a thorough brief
        )

    except RateLimitError:
        # 429: No billing credits or rate limit hit
        return JSONResponse(
            status_code=402,
            content={
                "error": (
                    "OpenAI quota exceeded (429). Your API key has no remaining credits. "
                    "Please add billing at https://platform.openai.com/account/billing"
                )
            },
        )

    except AuthenticationError:
        # 401: API key is wrong or missing
        return JSONResponse(
            status_code=401,
            content={
                "error": (
                    "Invalid OpenAI API key (401). "
                    "Check the OPENAI_API_KEY value in your .env file."
                )
            },
        )

    except APIError as exc:
        # Any other OpenAI API error
        return JSONResponse(
            status_code=502,
            content={"error": f"OpenAI API error: {exc.message}"},
        )

    # Extract the text from the API response
    brief_content = response.choices[0].message.content

    # Save the report to disk
    saved_path = save_report(topic.strip(), brief_content)

    # Return the brief and save path to the frontend
    return JSONResponse(
        content={
            "topic": topic.strip(),
            "brief": brief_content,
            "saved_to": saved_path,
        }
    )
