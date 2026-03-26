"""
Initializes campaigns_db.json from the existing synthetic interviews.
Creates 3 campaigns (TaskFlow, NourishNow, HireIQ) with all 15 interviews.
"""
import json, uuid, os

BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, "synthetic_interviews.json"), encoding="utf-8") as f:
    raw = json.load(f)

def make_questions(interview_list):
    """Extract unique question texts from transcripts and build question objects."""
    seen, questions = set(), []
    for iv in interview_list:
        for turn in iv["transcript"]:
            if turn["speaker"] == "AI":
                q_text = turn["text"]
                if q_text not in seen:
                    seen.add(q_text)
                    questions.append({
                        "id": f"q{len(questions)+1}",
                        "text": q_text,
                        "enabled": True,
                        "source": "ai"
                    })
    return questions[:10]  # keep top 10


def build_interviews(interview_list):
    built = []
    for iv in interview_list:
        answers = []
        q_turns = [t for t in iv["transcript"] if t["speaker"] == "AI"]
        a_turns = [t for t in iv["transcript"] if t["speaker"] == "Customer"]
        for i, (q, a) in enumerate(zip(q_turns, a_turns)):
            answers.append({
                "question_id": f"q{i+1}",
                "question_text": q["text"],
                "answer_text": a["text"],
                "has_audio": False,
                "audio_path": None
            })
        built.append({
            "id": iv["id"],
            "respondent_name": iv["respondent"]["name"],
            "respondent_role": iv["respondent"]["role"],
            "respondent_company_size": iv["respondent"]["company_size"],
            "respondent_industry": iv["respondent"]["industry"],
            "completed_date": iv["date"],
            "duration_minutes": iv["duration_minutes"],
            "answers": answers,
            "analysis": {
                "themes": iv["themes"],
                "sentiment_scores": iv["sentiment_scores"],
                "key_quotes": iv["key_quotes"],
                "actionable_insights": iv["actionable_insights"],
                "auto_analyzed": True
            }
        })
    return built


# Group by startup
startups = {}
for iv in raw["interviews"]:
    s = iv["startup"]
    if s not in startups:
        startups[s] = []
    startups[s].append(iv)

campaign_configs = {
    "TaskFlow": {
        "product_description": (
            "TaskFlow is a project management SaaS built specifically for remote engineering teams. "
            "It auto-syncs with GitHub to update ticket status from commits and PRs, eliminating manual "
            "updates. It provides a unified view for both engineers and product managers with a live "
            "roadmap that never needs an Excel export. We're researching why teams switch away from Jira "
            "and what the top friction points are."
        ),
        "target_respondent": "Engineering managers, CTOs, PMs, and senior engineers at tech companies",
        "research_goal": "Understand why remote engineering teams switch away from Jira and what the top friction points are"
    },
    "NourishNow": {
        "product_description": (
            "NourishNow is a hyperlocal healthy meal delivery service for offices. "
            "Employers set up a recurring subscription and employees get fresh, "
            "chef-prepared healthy lunches delivered to their desks at a precise time — "
            "no 3-hour delivery windows, no decision fatigue, no expense reports. "
            "We're researching the barriers to healthy eating at work and willingness to pay."
        ),
        "target_respondent": "Office workers, HR directors, operations managers, and founders",
        "research_goal": "Understand barriers to healthy eating at work and what would make people pay for a solution"
    },
    "HireIQ": {
        "product_description": (
            "HireIQ is an AI-powered hiring platform for technical roles. "
            "It uses candidate GitHub profiles, papers, and online presence to write personalized outreach, "
            "automates scheduling, and drafts structured interview feedback for hiring managers to approve "
            "in one click. We're researching the biggest pain points in technical hiring and where current "
            "ATS tools fall short."
        ),
        "target_respondent": "Engineering managers, CTOs, technical recruiters, and VP People at tech companies",
        "research_goal": "Understand biggest pain points in technical hiring and where current ATS tools fall short"
    }
}

campaigns = {}
for startup_name, ivs in startups.items():
    cid = startup_name.lower().replace(" ", "_") + "_001"
    cfg = campaign_configs[startup_name]
    campaigns[cid] = {
        "id": cid,
        "name": f"{startup_name} — Customer Discovery",
        "product_description": cfg["product_description"],
        "target_respondent": cfg["target_respondent"],
        "research_goal": cfg["research_goal"],
        "created_date": ivs[0]["date"],
        "status": "active",
        "questions": make_questions(ivs),
        "interview_token": cid,
        "interviews": build_interviews(ivs)
    }

db = {"campaigns": campaigns}
OUT = os.path.join(BASE, "campaigns_db.json")
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Created {len(campaigns)} campaigns with {sum(len(c['interviews']) for c in campaigns.values())} interviews")
print(f"Saved: {OUT}")
