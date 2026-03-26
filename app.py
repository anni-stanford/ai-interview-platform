"""
AI Customer Interview Platform — Prototype v2.0

Modes:
  - Founder mode  : http://localhost:8501/
  - Interviewee   : http://localhost:8501/?interview=CAMPAIGN_ID
"""
import streamlit as st
import json, os, uuid, datetime, base64, tempfile
from collections import Counter
from dotenv import load_dotenv
load_dotenv()
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from openai import OpenAI

# ── Config ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit default toolbar items (Deploy button, etc.)
st.markdown("""
<style>
  [data-testid="stToolbar"] { display: none !important; }
  #MainMenu { display: none !important; }
  footer { display: none !important; }
</style>
""", unsafe_allow_html=True)

OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
DB_PATH   = os.path.join(os.path.dirname(__file__), "data", "campaigns_db.json")
BASE_URL  = "http://localhost:8501"

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  body, .stApp { background: #f8f9fb; }
  .main-title  { font-size:2.2rem; font-weight:800; color:#1a1a2e; margin-bottom:0; }
  .subtitle    { font-size:1rem; color:#6b7280; margin-top:0.2rem; margin-bottom:1rem; }
  .card { background:white; border-radius:12px; padding:20px; border:1px solid #e5e7eb;
          box-shadow:0 1px 4px rgba(0,0,0,.06); margin-bottom:12px; }
  .metric-value { font-size:2rem; font-weight:700; color:#4f46e5; }
  .metric-label { font-size:0.82rem; color:#6b7280; margin-top:3px; }
  .theme-chip { display:inline-block; background:#ede9fe; color:#5b21b6;
                padding:2px 9px; border-radius:20px; font-size:0.76rem; margin:2px; font-weight:500; }
  .quote-box { background:#f8fafc; border-left:4px solid #4f46e5;
               padding:10px 14px; border-radius:0 8px 8px 0;
               font-style:italic; color:#374151; margin:6px 0; font-size:0.93rem; }
  .insight-item { background:#f0fdf4; border:1px solid #bbf7d0;
                  border-radius:8px; padding:9px 13px; margin:5px 0; font-size:0.91rem; color:#166534; }
  .q-box { background:#f0f9ff; border:1px solid #bae6fd; border-radius:10px;
           padding:16px 18px; margin:10px 0; font-size:1.05rem; font-weight:600; color:#0c4a6e; }
  .a-box { background:#fafafa; border:1px solid #e5e7eb; border-radius:8px;
           padding:12px 16px; margin:6px 0; font-size:0.95rem; color:#374151; }
  .progress-dot-done { display:inline-block; width:12px; height:12px; border-radius:50%;
                        background:#4f46e5; margin:0 3px; }
  .progress-dot-todo { display:inline-block; width:12px; height:12px; border-radius:50%;
                        background:#e5e7eb; margin:0 3px; }
  .campaign-badge { display:inline-block; background:#ede9fe; color:#4f46e5;
                    padding:3px 10px; border-radius:12px; font-size:0.78rem; font-weight:600; }
  .link-box { background:#1e293b; color:#86efac; font-family:monospace; font-size:0.9rem;
              padding:12px 16px; border-radius:8px; word-break:break-all; margin:8px 0; }
  div[data-testid="stCheckbox"] label { font-size:0.95rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Data helpers ─────────────────────────────────────────────────────────────
def load_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

def get_client():
    return OpenAI(api_key=OPENAI_KEY)

# ─────────────────────────────────────────────────────────────────────────────
# INTERVIEWEE MODE  (URL: ?interview=CAMPAIGN_ID)
# ─────────────────────────────────────────────────────────────────────────────
def show_interview_page(campaign_id: str):
    db = load_db()
    campaign = db["campaigns"].get(campaign_id)
    if not campaign:
        st.error("❌ Interview link not found. Please contact the researcher.")
        return

    questions = [q for q in campaign["questions"] if q["enabled"]]
    total_q   = len(questions)

    # Session state
    if "iv_step"    not in st.session_state: st.session_state.iv_step    = 0
    if "iv_answers" not in st.session_state: st.session_state.iv_answers = {}
    if "iv_name"    not in st.session_state: st.session_state.iv_name    = ""
    if "iv_done"    not in st.session_state: st.session_state.iv_done    = False
    if "iv_mode"    not in st.session_state: st.session_state.iv_mode    = "type"  # or "voice"

    step = st.session_state.iv_step

    # ── Welcome screen ──
    if step == 0:
        st.markdown('<p class="main-title">👋 Welcome to the Interview</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="subtitle">You\'ve been invited to share your experience. This interview is conducted by an AI and takes about 10–15 minutes.</p>', unsafe_allow_html=True)

        with st.container():
            st.markdown(f'<div class="card"><strong>About this research:</strong><br>{campaign["product_description"]}</div>', unsafe_allow_html=True)

        st.markdown("**📝 Before we start — your name (optional):**")
        name = st.text_input("", placeholder="e.g. Alex M.", label_visibility="collapsed")

        st.markdown("**🎙️ How would you like to answer?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⌨️  Type my answers", use_container_width=True,
                         type="primary" if st.session_state.iv_mode=="type" else "secondary"):
                st.session_state.iv_mode = "type"
        with col2:
            if st.button("🎤  Record my voice", use_container_width=True,
                         type="primary" if st.session_state.iv_mode=="voice" else "secondary"):
                st.session_state.iv_mode = "voice"

        st.caption(f"Selected: **{'⌨️ Typing' if st.session_state.iv_mode=='type' else '🎤 Voice recording'}**")

        if st.button("▶  Start Interview", type="primary", use_container_width=True):
            st.session_state.iv_name = name or "Anonymous"
            st.session_state.iv_step = 1
            st.rerun()

    # ── Completed ──
    elif st.session_state.iv_done:
        st.balloons()
        st.markdown('<p class="main-title">🎉 Thank you!</p>', unsafe_allow_html=True)
        st.success("Your responses have been recorded and are being analyzed. The researcher will review your answers shortly.")
        st.markdown(f"**{total_q} questions answered** · Your contribution is greatly appreciated.")

    # ── Questions ──
    elif 1 <= step <= total_q:
        q_idx = step - 1
        q     = questions[q_idx]

        # Progress bar
        progress = step / total_q
        st.progress(progress)
        dots_html = "".join([
            f'<span class="progress-dot-done"></span>' if i < step else f'<span class="progress-dot-todo"></span>'
            for i in range(total_q)
        ])
        st.markdown(f'<div style="text-align:center;margin-bottom:8px">{dots_html}</div>', unsafe_allow_html=True)
        st.caption(f"Question {step} of {total_q}")

        # Question
        st.markdown(f'<div class="q-box">💬 {q["text"]}</div>', unsafe_allow_html=True)
        st.markdown("")

        # Answer input
        answer_text = ""
        audio_b64   = None

        if st.session_state.iv_mode == "type":
            answer_text = st.text_area(
                "Your answer:",
                value=st.session_state.iv_answers.get(q["id"], {}).get("text", ""),
                height=130,
                placeholder="Share your thoughts here… Be as specific as possible.",
                key=f"ans_{q['id']}"
            )

        else:  # voice mode
            st.markdown("**🎤 Record your answer:**")
            try:
                from audio_recorder_streamlit import audio_recorder
                audio_bytes = audio_recorder(
                    text="Click to record",
                    recording_color="#4f46e5",
                    neutral_color="#e5e7eb",
                    icon_name="microphone",
                    icon_size="2x",
                    key=f"rec_{q['id']}"
                )
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/wav")
                    # Transcribe with Whisper
                    if st.button("✅ Transcribe & Use Answer", key=f"trans_{q['id']}"):
                        with st.spinner("Transcribing..."):
                            client = get_client()
                            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                                tmp.write(audio_bytes)
                                tmp_path = tmp.name
                            with open(tmp_path, "rb") as f:
                                transcript = client.audio.transcriptions.create(
                                    model="whisper-1", file=f
                                )
                            answer_text = transcript.text
                            audio_b64   = base64.b64encode(audio_bytes).decode()
                            st.success(f"**Transcribed:** {answer_text}")
                            os.unlink(tmp_path)
            except ImportError:
                st.warning("Voice recording requires `audio-recorder-streamlit`. Falling back to text input.")
                answer_text = st.text_area("Your answer:", height=130, key=f"fallback_{q['id']}")

        # Navigation
        col_back, col_next = st.columns([1, 3])
        with col_back:
            if step > 1:
                if st.button("← Back"):
                    st.session_state.iv_step -= 1
                    st.rerun()
        with col_next:
            btn_label = "Next Question →" if step < total_q else "Submit Interview ✓"
            btn_type  = "primary"
            if st.button(btn_label, type=btn_type, use_container_width=True):
                if not answer_text.strip():
                    st.warning("Please provide an answer before continuing.")
                else:
                    st.session_state.iv_answers[q["id"]] = {
                        "text": answer_text,
                        "audio_b64": audio_b64
                    }
                    if step < total_q:
                        st.session_state.iv_step += 1
                        st.rerun()
                    else:
                        # Save & analyze
                        _save_interview(db, campaign_id, questions)

    # ── Fallback ──
    else:
        st.session_state.iv_step = 0
        st.rerun()


def _save_interview(db, campaign_id, questions):
    """Save completed interview answers and trigger auto-analysis."""
    answers_list = []
    for q in questions:
        saved = st.session_state.iv_answers.get(q["id"], {})
        answers_list.append({
            "question_id": q["id"],
            "question_text": q["text"],
            "answer_text": saved.get("text", ""),
            "has_audio": saved.get("audio_b64") is not None,
            "audio_b64": saved.get("audio_b64")
        })

    interview_id = f"IV-{uuid.uuid4().hex[:6].upper()}"
    new_interview = {
        "id": interview_id,
        "respondent_name": st.session_state.iv_name,
        "respondent_role": "Interviewee",
        "respondent_company_size": "",
        "respondent_industry": "",
        "completed_date": datetime.date.today().isoformat(),
        "duration_minutes": 0,
        "answers": answers_list,
        "analysis": None
    }

    # Auto-analyze with GPT
    with st.spinner("Analyzing your responses... this takes a few seconds."):
        try:
            transcript_text = "\n".join([
                f"Q: {a['question_text']}\nA: {a['answer_text']}"
                for a in answers_list
            ])
            client = get_client()
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"""Analyze this customer interview and return ONLY valid JSON (no markdown, no code block):
{{
  "themes": ["theme1", "theme2", "theme3", "theme4", "theme5"],
  "sentiment_scores": {{"overall": 3.0, "pain_intensity": 4.0, "openness_to_switch": 3.5}},
  "key_quotes": ["exact quote 1", "exact quote 2", "exact quote 3"],
  "actionable_insights": ["insight 1", "insight 2", "insight 3"]
}}

Interview transcript:
{transcript_text}"""}]
            )
            raw = resp.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            new_interview["analysis"] = json.loads(raw)
        except Exception as e:
            new_interview["analysis"] = {
                "themes": ["customer discovery"],
                "sentiment_scores": {"overall": 3.0, "pain_intensity": 3.0, "openness_to_switch": 3.0},
                "key_quotes": [],
                "actionable_insights": [f"Analysis pending: {str(e)}"]
            }

    db["campaigns"][campaign_id]["interviews"].append(new_interview)
    save_db(db)
    st.session_state.iv_done = True
    st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# FOUNDER MODE
# ─────────────────────────────────────────────────────────────────────────────
def show_founder_app():
    db = load_db()
    campaigns = db["campaigns"]

    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🎯 AI Interview Platform")
        st.divider()

        # Campaign selector
        st.markdown("**📁 Campaign**")
        campaign_names = {cid: c["name"] for cid, c in campaigns.items()}
        campaign_names["__new__"] = "➕  Create New Campaign"

        selected_cid = st.selectbox(
            "Select campaign",
            options=list(campaign_names.keys()),
            format_func=lambda x: campaign_names[x],
            key="selected_campaign",
            label_visibility="collapsed"
        )

        if selected_cid != "__new__":
            camp = campaigns[selected_cid]
            n_iv = len(camp["interviews"])
            st.caption(f"✅ {n_iv} interview{'s' if n_iv!=1 else ''} · {camp['status']}")

        st.divider()

        # Navigation
        page = st.radio("Navigate to", [
            "🏠  Dashboard",
            "⚙️  Campaign Setup",
            "📋  Interview Results",
            "🔍  Thematic Analysis",
            "💡  Insights Report",
        ], label_visibility="collapsed")

        st.divider()
        total_iv = sum(len(c["interviews"]) for c in campaigns.values())
        st.caption(f"**Platform stats**")
        st.caption(f"📁 {len(campaigns)} campaigns")
        st.caption(f"🎤 {total_iv} interviews conducted")

    # ─── Page routing ─────────────────────────────────────────────────────────
    if selected_cid == "__new__" or "Setup" in page:
        show_campaign_setup(db, selected_cid if selected_cid != "__new__" else None)
    elif "Dashboard" in page:
        show_dashboard(db)
    elif "Results" in page:
        show_results(campaigns.get(selected_cid, {}), selected_cid)
    elif "Thematic" in page:
        show_thematic(campaigns.get(selected_cid, {}))
    elif "Insights" in page:
        show_insights(campaigns.get(selected_cid, {}))


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
def show_dashboard(db):
    campaigns = db["campaigns"]
    all_ivs   = [iv for c in campaigns.values() for iv in c["interviews"]]

    st.markdown('<p class="main-title">🎯 Platform Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Overview across all campaigns</p>', unsafe_allow_html=True)

    # KPI row
    c1,c2,c3,c4 = st.columns(4)
    for col, val, lbl in [
        (c1, len(campaigns), "Active Campaigns"),
        (c2, len(all_ivs), "Total Interviews"),
        (c3, sum(len(iv["analysis"]["themes"]) for iv in all_ivs if iv.get("analysis")), "Themes Coded"),
        (c4, sum(len(iv["analysis"]["actionable_insights"]) for iv in all_ivs if iv.get("analysis")), "Actionable Insights"),
    ]:
        with col:
            st.markdown(f'<div class="card" style="text-align:center"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.divider()

    # Campaign cards — 3 per row
    st.markdown("### Your Campaigns")
    camp_list = list(campaigns.items())
    for row_start in range(0, len(camp_list), 3):
        row_items = camp_list[row_start:row_start + 3]
        cols = st.columns(3)
        for col, (cid, camp) in zip(cols, row_items):
            with col:
                ivs = camp["interviews"]
                pain_scores = [iv["analysis"]["sentiment_scores"]["pain_intensity"] for iv in ivs if iv.get("analysis")]
                avg_pain = sum(pain_scores)/len(pain_scores) if pain_scores else 0

                st.markdown(f"""
<div class="card">
  <div style="font-weight:700;font-size:1rem;margin-bottom:6px">{camp['name']}</div>
  <span class="campaign-badge">{camp['status']}</span><br><br>
  <div>🎤 <strong>{len(ivs)}</strong> interview{'s' if len(ivs)!=1 else ''}</div>
  <div>🔥 Pain score: <strong>{avg_pain:.1f}/5</strong></div>
  <div style="font-size:0.8rem;color:#6b7280;margin-top:8px">{camp['research_goal'][:90]}...</div>
</div>""", unsafe_allow_html=True)

    # Pain chart across all campaigns
    st.divider()
    st.markdown("### Pain Intensity by Campaign")
    plot_data = []
    for cid, camp in campaigns.items():
        for iv in camp["interviews"]:
            if iv.get("analysis"):
                plot_data.append({
                    "Campaign": camp["name"].split("—")[0].strip(),
                    "Pain":     iv["analysis"]["sentiment_scores"]["pain_intensity"],
                    "Switch":   iv["analysis"]["sentiment_scores"]["openness_to_switch"],
                    "Respondent": iv["respondent_name"]
                })
    if plot_data:
        df = pd.DataFrame(plot_data)
        col_l, col_r = st.columns(2)
        with col_l:
            fig = px.box(df, x="Campaign", y="Pain", color="Campaign", points="all",
                         color_discrete_sequence=["#4f46e5","#059669","#d97706"])
            fig.update_layout(showlegend=False, height=300, margin=dict(t=10,b=10))
            st.plotly_chart(fig, use_container_width=True)
        with col_r:
            fig2 = px.scatter(df, x="Pain", y="Switch", color="Campaign",
                              hover_data=["Respondent"],
                              color_discrete_sequence=["#4f46e5","#059669","#d97706"])
            fig2.add_hline(y=4, line_dash="dot", line_color="gray")
            fig2.add_vline(x=4, line_dash="dot", line_color="gray")
            fig2.update_layout(height=300, margin=dict(t=10,b=10))
            st.plotly_chart(fig2, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: CAMPAIGN SETUP
# ─────────────────────────────────────────────────────────────────────────────
def show_campaign_setup(db, existing_cid=None):
    campaigns = db["campaigns"]
    is_new    = existing_cid is None or existing_cid not in campaigns

    st.markdown(f'<p class="main-title">{"➕ Create New Campaign" if is_new else "⚙️ Campaign Setup"}</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Configure your research campaign and AI-generated interview questions</p>', unsafe_allow_html=True)

    existing = campaigns.get(existing_cid, {}) if not is_new else {}

    # ── Step 1: Campaign Info ──────────────────────────────────────────────
    st.markdown("### Step 1 — Campaign Information")
    col1, col2 = st.columns(2)
    with col1:
        camp_name = st.text_input("Campaign name", value=existing.get("name", ""), placeholder="e.g. TaskFlow — Customer Discovery Q1 2026")
        target_resp = st.text_input("Target respondent", value=existing.get("target_respondent", ""),
                                    placeholder="e.g. Engineering managers at 20-200 person tech startups")
    with col2:
        research_goal = st.text_area("Research goal / hypothesis", value=existing.get("research_goal", ""),
                                      height=100, placeholder="What do you want to learn from these interviews?")

    st.markdown("### Step 2 — Product Description")
    product_desc = st.text_area(
        "Describe your product and the problem it solves",
        value=existing.get("product_description", ""),
        height=130,
        placeholder="e.g. TaskFlow is a project management tool for remote engineering teams that auto-syncs with GitHub to eliminate manual ticket updates..."
    )

    # ── Step 2: Generate Questions ─────────────────────────────────────────
    st.markdown("### Step 3 — Interview Questions")

    if "generated_questions" not in st.session_state:
        st.session_state.generated_questions = [
            {"id": q["id"], "text": q["text"], "enabled": q["enabled"], "source": q["source"]}
            for q in existing.get("questions", [])
        ]

    col_gen, col_info = st.columns([2, 1])
    with col_gen:
        if st.button("✨ Generate Questions with AI", type="primary", disabled=not product_desc.strip()):
            with st.spinner("AI is generating interview questions following Stanford Startup Garage best practices..."):
                client = get_client()
                resp = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "system",
                        "content": """You are an expert at crafting customer discovery interview questions following Stanford d.school and Startup Garage best practices.

Rules for good questions:
- Short, open-ended questions (≤10 words ideal)
- Ask about PAST BEHAVIOR not hypotheticals ("Tell me about a time..." not "Would you...")
- Ask for specifics, not generalizations
- Probe emotions: "What was the most frustrating part?"
- Never leading, never binary yes/no
- Include: opener (rapport), behavior questions, emotion probes, implication questions, closing
- Follow "Mom Test" principles — no questions that fish for compliments

Return ONLY a JSON array of 10 question strings. No numbering, no markdown."""
                    }, {
                        "role": "user",
                        "content": f"""Generate 10 customer discovery interview questions for:

Product: {product_desc}
Target respondent: {target_resp}
Research goal: {research_goal}

Include questions that uncover: past behavior, pain points, emotional impact, current workarounds, and willingness to change."""
                    }]
                )
                raw = resp.choices[0].message.content.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"):
                        raw = raw[4:]
                q_texts = json.loads(raw)
                st.session_state.generated_questions = [
                    {"id": f"q{i+1}", "text": t, "enabled": True, "source": "ai"}
                    for i, t in enumerate(q_texts)
                ]
                st.success("✅ 10 questions generated! Review and select below.")
                st.rerun()
    with col_info:
        st.info("💡 AI generates research-quality questions: open-ended, behavior-focused, non-leading")

    # ── Question checklist ─────────────────────────────────────────────────
    if st.session_state.generated_questions:
        st.markdown("**Select questions to include** *(check = include in interview)*")

        updated_qs = []
        for i, q in enumerate(st.session_state.generated_questions):
            col_cb, col_q, col_del = st.columns([0.5, 8, 0.5])
            with col_cb:
                enabled = st.checkbox("", value=q["enabled"], key=f"cb_{q['id']}_{i}", label_visibility="collapsed")
            with col_q:
                new_text = st.text_input("", value=q["text"], key=f"qt_{q['id']}_{i}",
                                          label_visibility="collapsed",
                                          disabled=not enabled)
            with col_del:
                if st.button("🗑", key=f"del_{i}", help="Remove this question"):
                    continue  # skip = delete
            updated_qs.append({"id": q["id"], "text": new_text, "enabled": enabled, "source": q.get("source","manual")})

        # Add custom question
        st.markdown("**➕ Add your own question:**")
        col_new, col_add = st.columns([5, 1])
        with col_new:
            new_q_text = st.text_input("", placeholder="Type a new question...", key="new_q_input", label_visibility="collapsed")
        with col_add:
            if st.button("Add", key="add_q_btn"):
                if new_q_text.strip():
                    new_id = f"q{len(updated_qs)+1}"
                    updated_qs.append({"id": new_id, "text": new_q_text.strip(), "enabled": True, "source": "manual"})
                    st.rerun()

        st.session_state.generated_questions = updated_qs
        enabled_count = sum(1 for q in updated_qs if q["enabled"])
        st.caption(f"**{enabled_count}** questions selected out of {len(updated_qs)} total")

    # ── Save & Get Link ────────────────────────────────────────────────────
    st.divider()
    st.markdown("### Step 4 — Save & Share")

    if st.button("💾 Save Campaign & Get Interview Link", type="primary",
                 disabled=not (camp_name.strip() and st.session_state.generated_questions)):
        if is_new:
            cid = camp_name.lower().replace(" ","_").replace("—","").replace("–","")[:20] + "_" + uuid.uuid4().hex[:4]
        else:
            cid = existing_cid

        db["campaigns"][cid] = {
            "id": cid,
            "name": camp_name,
            "product_description": product_desc,
            "target_respondent": target_resp,
            "research_goal": research_goal,
            "created_date": datetime.date.today().isoformat(),
            "status": "active",
            "questions": st.session_state.generated_questions,
            "interview_token": cid,
            "interviews": campaigns.get(cid, {}).get("interviews", [])
        }
        save_db(db)

        interview_link = f"{BASE_URL}/?interview={cid}"
        st.success("✅ Campaign saved!")
        st.markdown("**📎 Interview link — copy and send to your interviewees:**")
        st.markdown(f'<div class="link-box">{interview_link}</div>', unsafe_allow_html=True)
        st.code(interview_link, language=None)
        st.info("💡 Share this link via email or messaging. Each interviewee completes it independently.")

        if is_new:
            st.session_state.selected_campaign = cid
            st.session_state.generated_questions = []


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: INTERVIEW RESULTS
# ─────────────────────────────────────────────────────────────────────────────
def show_results(campaign, campaign_id):
    if not campaign:
        st.warning("Please select a campaign from the sidebar.")
        return

    ivs = campaign.get("interviews", [])
    st.markdown(f'<p class="main-title">📋 Interview Results</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{campaign["name"]} · {len(ivs)} interviews</p>', unsafe_allow_html=True)

    if not ivs:
        st.info("No interviews yet. Share your interview link to start collecting responses.")
        link = f"{BASE_URL}/?interview={campaign_id}"
        st.markdown(f'<div class="link-box">{link}</div>', unsafe_allow_html=True)
        return

    # Summary metrics
    analyzed = [iv for iv in ivs if iv.get("analysis")]
    if analyzed:
        c1,c2,c3,c4 = st.columns(4)
        avg_pain   = sum(iv["analysis"]["sentiment_scores"]["pain_intensity"] for iv in analyzed)/len(analyzed)
        avg_switch = sum(iv["analysis"]["sentiment_scores"]["openness_to_switch"] for iv in analyzed)/len(analyzed)
        avg_ov     = sum(iv["analysis"]["sentiment_scores"]["overall"] for iv in analyzed)/len(analyzed)
        for col,v,l in [(c1,len(ivs),"Total Interviews"),(c2,f"{avg_pain:.1f}/5","Avg Pain"),(c3,f"{avg_switch:.1f}/5","Switch Intent"),(c4,f"{avg_ov:.1f}/5","Avg Sentiment")]:
            with col:
                st.markdown(f'<div class="card" style="text-align:center"><div class="metric-value">{v}</div><div class="metric-label">{l}</div></div>', unsafe_allow_html=True)
        st.markdown("")

    # Interview link
    with st.expander("📎 Share interview link"):
        link = f"{BASE_URL}/?interview={campaign_id}"
        st.markdown(f'<div class="link-box">{link}</div>', unsafe_allow_html=True)
        st.code(link, language=None)

    st.divider()

    # Each interview
    for iv in ivs:
        analysis = iv.get("analysis") or {}
        pain_lbl = f"🔥 {analysis.get('sentiment_scores',{}).get('pain_intensity','-')}/5 pain" if analysis else ""
        with st.expander(f"**{iv['id']}** — {iv['respondent_name']} · {iv['completed_date']} · {len(iv.get('answers',[]))} Q&A {pain_lbl}"):
            col_left, col_right = st.columns([3, 2])
            with col_left:
                st.markdown("**📝 Transcript:**")
                for ans in iv.get("answers", []):
                    st.markdown(f'<div class="q-box" style="font-size:0.9rem;padding:10px">{ans["question_text"]}</div>', unsafe_allow_html=True)
                    if ans.get("has_audio"):
                        st.caption("🎤 Voice answer transcribed")
                    st.markdown(f'<div class="a-box">{ans["answer_text"]}</div>', unsafe_allow_html=True)

            with col_right:
                if analysis:
                    st.markdown("**🏷️ Themes:**")
                    for t in analysis.get("themes", []):
                        st.markdown(f'<span class="theme-chip">{t}</span>', unsafe_allow_html=True)
                    st.markdown("")

                    if analysis.get("key_quotes"):
                        st.markdown("**💬 Key Quotes:**")
                        for q in analysis["key_quotes"]:
                            st.markdown(f'<div class="quote-box">"{q}"</div>', unsafe_allow_html=True)

                    if analysis.get("actionable_insights"):
                        st.markdown("**💡 Insights:**")
                        for ins in analysis["actionable_insights"]:
                            st.markdown(f'<div class="insight-item">💡 {ins}</div>', unsafe_allow_html=True)

                    scores = analysis.get("sentiment_scores", {})
                    if scores:
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=["Overall","Pain","Switch Intent"],
                            y=[scores.get("overall",0), scores.get("pain_intensity",0), scores.get("openness_to_switch",0)],
                            marker_color=["#818cf8","#f87171","#34d399"]
                        ))
                        fig.update_layout(yaxis=dict(range=[0,5]), height=180, margin=dict(t=10,b=10,l=10,r=10))
                        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: THEMATIC ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def show_thematic(campaign):
    if not campaign:
        st.warning("Please select a campaign.")
        return

    ivs = [iv for iv in campaign.get("interviews", []) if iv.get("analysis")]
    st.markdown(f'<p class="main-title">🔍 Thematic Analysis</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{campaign["name"]} · Automated pattern detection across {len(ivs)} interviews</p>', unsafe_allow_html=True)

    if not ivs:
        st.info("No analyzed interviews yet.")
        return

    all_themes = [t for iv in ivs for t in iv["analysis"]["themes"]]
    tc = Counter(all_themes).most_common(15)
    df_tc = pd.DataFrame(tc, columns=["Theme","Count"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Theme Frequency")
        fig = px.bar(df_tc, x="Theme", y="Count", color="Count", color_continuous_scale="Purples")
        fig.update_layout(xaxis_tickangle=-35, height=320, margin=dict(t=10), coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Theme Map")
        fig2 = px.treemap(df_tc, path=["Theme"], values="Count", color="Count", color_continuous_scale="Purples")
        fig2.update_layout(height=320, margin=dict(t=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Pain by theme
    st.markdown("#### Pain Intensity by Theme")
    theme_pain = {}
    for iv in ivs:
        for t in iv["analysis"]["themes"]:
            theme_pain.setdefault(t, []).append(iv["analysis"]["sentiment_scores"]["pain_intensity"])
    df_tp = pd.DataFrame([{"Theme":t,"Avg Pain":round(sum(v)/len(v),2),"Count":len(v)} for t,v in theme_pain.items()]).sort_values("Avg Pain",ascending=False)
    fig3 = px.scatter(df_tp, x="Theme", y="Avg Pain", size="Count", color="Avg Pain", color_continuous_scale="RdYlGn_r")
    fig3.update_layout(xaxis_tickangle=-35, height=300, margin=dict(t=10))
    st.plotly_chart(fig3, use_container_width=True)

    # Live GPT analysis
    st.divider()
    st.markdown("#### 🤖 AI Cross-Interview Analysis")
    if st.button("Run GPT-4o Analysis Across All Interviews", type="primary"):
        all_quotes = [q for iv in ivs for q in iv["analysis"].get("key_quotes", [])]
        client = get_client()
        with st.spinner("GPT-4o analyzing patterns..."):
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role":"user","content":f"""Analyze customer interviews for: {campaign['name']}
Research goal: {campaign['research_goal']}

Key quotes collected:
{chr(10).join('- ' + q for q in all_quotes)}

Provide:
1. Top 3 recurring pain points (with evidence)
2. The single most surprising / non-obvious insight
3. Jobs-to-be-done that emerged
4. First product feature to build based on evidence
5. Who NOT to build for (anti-customer)"""}]
            )
        st.markdown(resp.choices[0].message.content)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE: INSIGHTS REPORT
# ─────────────────────────────────────────────────────────────────────────────
def show_insights(campaign):
    if not campaign:
        st.warning("Please select a campaign.")
        return

    ivs = [iv for iv in campaign.get("interviews", []) if iv.get("analysis")]
    st.markdown(f'<p class="main-title">💡 Insights Report</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{campaign["name"]} · {len(ivs)} analyzed interviews</p>', unsafe_allow_html=True)

    if not ivs:
        st.info("No analyzed interviews yet.")
        return

    # All insights
    all_insights = [ins for iv in ivs for ins in iv["analysis"].get("actionable_insights", [])]
    st.markdown("### Consolidated Actionable Insights")
    for i, ins in enumerate(all_insights, 1):
        st.markdown(f'<div class="insight-item">💡 <strong>#{i}</strong> {ins}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### Top Quotes")
    all_quotes = [q for iv in ivs for q in iv["analysis"].get("key_quotes", [])]
    col1, col2 = st.columns(2)
    for i, q in enumerate(all_quotes):
        with (col1 if i%2==0 else col2):
            st.markdown(f'<div class="quote-box">"{q}"</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🤖 Executive Summary (GPT-4o)")
    if st.button("Generate Executive Summary", type="primary"):
        summary_data = "\n\n".join([
            f"Interview {iv['id']} ({iv['respondent_name']}):\n"
            f"Key quotes: {'; '.join(iv['analysis'].get('key_quotes',[]))}\n"
            f"Themes: {', '.join(iv['analysis'].get('themes',[]))}\n"
            f"Insights: {'; '.join(iv['analysis'].get('actionable_insights',[]))}"
            for iv in ivs
        ])
        client = get_client()
        with st.spinner("Generating..."):
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role":"system","content":"You are a world-class customer research analyst. Write clear, concise, actionable reports for startup founders. Follow Stanford Startup Garage best practices."},
                    {"role":"user","content":f"""Write an executive summary for the {campaign['name']} team.

Research goal: {campaign['research_goal']}

Interview data:
{summary_data}

Include:
1. TL;DR (3 sentences max)
2. The single most important finding
3. Top 3 validated pain points with supporting evidence
4. POV statement: "[User] needs [need] because/but/surprisingly [insight]"
5. Recommended next steps"""}
                ]
            )
        st.markdown(resp.choices[0].message.content)

    # Timeline chart
    st.divider()
    df = pd.DataFrame([{"Date": iv["completed_date"],
                         "Pain": iv["analysis"]["sentiment_scores"]["pain_intensity"],
                         "Switch": iv["analysis"]["sentiment_scores"]["openness_to_switch"],
                         "Name": iv["respondent_name"]} for iv in ivs]).sort_values("Date")
    fig = px.line(df.melt(id_vars=["Date","Name"], value_vars=["Pain","Switch"]),
                  x="Date", y="value", color="variable", markers=True,
                  labels={"value":"Score (1-5)","variable":"Metric"})
    fig.update_layout(height=280, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
params = st.query_params
if "interview" in params:
    # Interviewee view
    show_interview_page(campaign_id=params["interview"])
else:
    # Founder view
    show_founder_app()
