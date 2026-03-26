# AI Customer Interview Platform

An end-to-end AI-powered platform for automating qualitative customer discovery interviews.

## What It Does

Founders describe their product, the AI generates research-quality interview questions, sends a sharable link to customers, and automatically analyzes the responses — delivering themes, sentiment scores, key quotes, and actionable insights.

## Features

- **Campaign Management** — Create and manage multiple interview campaigns
- **AI Question Generation** — GPT-4o generates open-ended, behavior-focused questions
- **Shareable Interview Links** — Each respondent gets a unique link
- **Dual Answer Mode** — Type responses or record voice (auto-transcribed)
- **Auto-Analysis** — Themes, sentiment, key quotes, and insights extracted automatically
- **Thematic Analysis Dashboard** — Cross-interview pattern detection
- **Insights Report** — GPT-generated executive summaries for founders

## Tech Stack

- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4o (interview agent, analysis, summaries) + Whisper (voice transcription)
- **Data**: JSON-based campaign database with 15 pre-loaded synthetic interviews
- **Visualization**: Plotly

## Setup

```bash
pip install streamlit plotly pandas openai audio-recorder-streamlit
python data/generate_database.py
python data/init_campaigns.py
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

**Interviewee link format:** `http://localhost:8501/?interview=CAMPAIGN_ID`

## Project Structure

```
prototype/
├── app.py                  # Main Streamlit application
├── data/
│   ├── generate_database.py    # Generates synthetic interview database
│   ├── init_campaigns.py       # Initializes campaign structure
│   ├── synthetic_interviews.json
│   └── campaigns_db.json
└── README.md
```
