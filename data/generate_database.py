"""
Generates synthetic_interviews.json — a realistic database of 15 customer
interviews across 3 startup types for the AI Customer Interview Platform prototype.
"""
import json, random
from datetime import datetime, timedelta

random.seed(42)

BASE_DATE = datetime(2026, 1, 15)

def rand_date(offset_days):
    d = BASE_DATE + timedelta(days=offset_days + random.randint(0, 2))
    return d.strftime("%Y-%m-%d")

def rand_duration():
    return random.randint(9, 22)

# ─────────────────────────────────────────────────────────────────────────────
# STARTUP 1: TaskFlow — project management SaaS for remote engineering teams
# ─────────────────────────────────────────────────────────────────────────────
taskflow_interviews = [
    {
        "id": "TF-001",
        "startup": "TaskFlow",
        "startup_domain": "Project Management SaaS",
        "founder_research_question": "Why do remote engineering teams switch away from Jira, and what are the top friction points?",
        "respondent": {"name": "Alex M.", "role": "Engineering Manager", "company_size": "45 employees", "industry": "FinTech"},
        "date": rand_date(0),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "Thanks for joining. I'd love to understand your experience with project management tools. Can you walk me through how your team currently tracks engineering work?"},
            {"speaker": "Customer", "text": "We use Jira but honestly it's a constant headache. Every sprint planning takes two hours just to update ticket statuses. Half the engineers don't even log in unless I remind them."},
            {"speaker": "AI", "text": "That's really telling — the two-hour sprint planning really stands out. What specifically makes it take that long?"},
            {"speaker": "Customer", "text": "The UI is just terrible for bulk updates. And Jira's search is broken — I can never find the ticket I'm looking for without knowing the exact ID. We end up having a Notion doc that duplicates everything just so people can actually find things."},
            {"speaker": "AI", "text": "Interesting — so you're maintaining a parallel system in Notion. What would it look like if you had just one tool that worked?"},
            {"speaker": "Customer", "text": "Search that actually works, updates that take one click not five, and something I can pull up on my phone in 30 seconds. My engineers are in GitHub all day — I'd love something that just pulled in their commits automatically and updated tickets without anyone touching them."},
            {"speaker": "AI", "text": "How much time per week do you think your team collectively spends on Jira admin tasks that don't involve actual thinking?"},
            {"speaker": "Customer", "text": "Conservatively? Four to five hours per person. That's 200 hours a month across my team just on busywork. It's insane when I put it that way."},
            {"speaker": "AI", "text": "One final question: if a new tool could eliminate that busywork, what would make you confident enough to switch?"},
            {"speaker": "Customer", "text": "A two-week trial that actually migrates my data cleanly. And it needs to work with GitHub and Slack natively — not through a 12-step integration."},
        ],
        "themes": ["Jira friction", "UI/UX pain", "search usability", "GitHub integration", "time waste", "onboarding friction"],
        "sentiment_scores": {"overall": 2.1, "pain_intensity": 4.6, "openness_to_switch": 4.2},
        "key_quotes": [
            "200 hours a month across my team just on busywork",
            "We end up having a Notion doc that duplicates everything",
            "A two-week trial that actually migrates my data cleanly"
        ],
        "actionable_insights": [
            "Automatic GitHub commit-to-ticket linking is a top feature request",
            "Sprint planning time is a key pain metric — target <15 min as success benchmark",
            "Data migration guarantee is a precondition for switching"
        ]
    },
    {
        "id": "TF-002",
        "startup": "TaskFlow",
        "startup_domain": "Project Management SaaS",
        "founder_research_question": "Why do remote engineering teams switch away from Jira, and what are the top friction points?",
        "respondent": {"name": "Sofia L.", "role": "CTO", "company_size": "12 employees", "industry": "HealthTech"},
        "date": rand_date(2),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "You're a CTO at a 12-person startup — I'm curious how you think about project management at this stage. What's your current setup?"},
            {"speaker": "Customer", "text": "We started with Asana, moved to Linear, and now we're trying Notion. Honestly we keep switching because nothing quite fits the way engineers actually think."},
            {"speaker": "AI", "text": "What do you mean by 'the way engineers actually think' — can you give me a concrete example?"},
            {"speaker": "Customer", "text": "Engineers think in code. They want to see the PR, the test status, the deployment — all in one place. Every PM tool treats those as afterthoughts. Linear is the closest but it still feels like two separate worlds."},
            {"speaker": "AI", "text": "You've switched tools three times. What made you finally leave each one?"},
            {"speaker": "Customer", "text": "Asana was too process-heavy — felt like I was filling out TPS reports. Linear was actually great until our product manager joined and said she couldn't figure out the roadmap view. So now we have Linear for engineers and Notion for product and they don't talk to each other."},
            {"speaker": "AI", "text": "That split between engineering and product is really interesting. Who suffers more from that disconnect — engineers or the PM?"},
            {"speaker": "Customer", "text": "The PM, definitely. She's flying blind on what's actually built vs what's planned. I end up being the translator. That's probably 5 hours a week of my time that I shouldn't be spending."},
            {"speaker": "AI", "text": "If you could wave a magic wand, what does the ideal tool look like for your team?"},
            {"speaker": "Customer", "text": "One source of truth that engineers love using AND that the PM can understand without a tutorial. That's it. Seems simple but apparently impossible."},
        ],
        "themes": ["tool switching fatigue", "engineering-PM disconnect", "roadmap visibility", "GitHub integration", "onboarding friction", "single source of truth"],
        "sentiment_scores": {"overall": 2.4, "pain_intensity": 4.1, "openness_to_switch": 4.7},
        "key_quotes": [
            "Engineers think in code — they want to see the PR, the test status, the deployment all in one place",
            "I end up being the translator. That's 5 hours a week of my time",
            "One source of truth that engineers love AND that the PM can understand"
        ],
        "actionable_insights": [
            "CTO translator role is a major hidden cost — position product as eliminating this",
            "PM-engineer gap is a stronger wedge than pure engineer productivity",
            "Linear is the closest competitor — understand its roadmap weakness specifically"
        ]
    },
    {
        "id": "TF-003",
        "startup": "TaskFlow",
        "startup_domain": "Project Management SaaS",
        "founder_research_question": "Why do remote engineering teams switch away from Jira, and what are the top friction points?",
        "respondent": {"name": "James K.", "role": "Senior Software Engineer", "company_size": "200 employees", "industry": "E-commerce"},
        "date": rand_date(5),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "As a senior engineer, you're on the receiving end of project management tools rather than choosing them. What's your honest experience with Jira day-to-day?"},
            {"speaker": "Customer", "text": "I avoid it as much as possible. If I could do my job without ever opening Jira I would. My manager knows this and basically updates tickets for me."},
            {"speaker": "AI", "text": "That's pretty strong. What specifically makes you want to avoid it?"},
            {"speaker": "Customer", "text": "The loading times alone kill me. Each page takes 3-4 seconds. Over a day, clicking around Jira probably wastes 30 minutes. And the editor for ticket descriptions is this weird pseudo-markdown that doesn't render properly half the time."},
            {"speaker": "AI", "text": "You mentioned your manager updates tickets for you — does that create any problems?"},
            {"speaker": "Customer", "text": "Yeah, status is always wrong. Tickets sit in 'In Progress' for weeks because nobody remembers to move them. Then we have these retrospective meetings where half the time is spent figuring out what actually happened vs what the board says."},
            {"speaker": "AI", "text": "If you could redesign the tool to fit how you actually work, what would it look like?"},
            {"speaker": "Customer", "text": "Honestly? Just watch my GitHub activity and update things automatically. I open a branch, move ticket to In Progress. I open a PR, move to Review. PR merges, move to Done. Zero clicks from me."},
        ],
        "themes": ["Jira friction", "UI/UX pain", "GitHub integration", "status accuracy", "time waste", "automation desire"],
        "sentiment_scores": {"overall": 1.6, "pain_intensity": 4.8, "openness_to_switch": 3.9},
        "key_quotes": [
            "If I could do my job without ever opening Jira I would",
            "Each page takes 3-4 seconds — probably wastes 30 minutes a day",
            "Just watch my GitHub activity and update things automatically"
        ],
        "actionable_insights": [
            "GitHub-driven automatic status updates is the #1 engineer feature request (confirmed 2/3 interviews)",
            "Page load speed is a real pain point — benchmark Jira vs TaskFlow on p95 load time",
            "Engineers want zero-click updates — pure automation angle resonates strongly"
        ]
    },
    {
        "id": "TF-004",
        "startup": "TaskFlow",
        "startup_domain": "Project Management SaaS",
        "founder_research_question": "Why do remote engineering teams switch away from Jira, and what are the top friction points?",
        "respondent": {"name": "Priya N.", "role": "Product Manager", "company_size": "80 employees", "industry": "EdTech"},
        "date": rand_date(7),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "As a PM, you probably have a different relationship with project management tools than engineers do. How would you describe yours?"},
            {"speaker": "Customer", "text": "I live in these tools. Jira is my second home — unfortunately. I spend probably 3 hours a day in it, which is embarrassing but that's just reality."},
            {"speaker": "AI", "text": "What are those 3 hours actually spent on?"},
            {"speaker": "Customer", "text": "Chasing engineers to update tickets, building reports for stakeholders, trying to understand sprint velocity — half of which is garbage data because the tickets aren't updated anyway. And roadmap planning, which requires exporting to Excel because Jira's roadmap view is unusable."},
            {"speaker": "AI", "text": "The Excel export for roadmaps really jumped out. Can you tell me more about that workflow?"},
            {"speaker": "Customer", "text": "It's humiliating honestly. I export Jira data, paste it into an Excel template I built, format it manually, then present it to leadership. If anything changes, I do it again. This happens every two weeks."},
            {"speaker": "AI", "text": "What would it mean for your work if roadmaps were always live and accurate without that export step?"},
            {"speaker": "Customer", "text": "I'd get maybe an hour back per day and leadership would actually trust the data. Right now they always ask me if the numbers are fresh. That's embarrassing for me and for the whole process."},
        ],
        "themes": ["roadmap visibility", "stakeholder reporting", "data accuracy", "manual workarounds", "PM time waste", "Excel dependency"],
        "sentiment_scores": {"overall": 2.0, "pain_intensity": 4.3, "openness_to_switch": 4.5},
        "key_quotes": [
            "I export Jira data, paste it into an Excel template I built — every two weeks",
            "Leadership always asks me if the numbers are fresh — that's embarrassing",
            "3 hours a day in Jira, which is embarrassing"
        ],
        "actionable_insights": [
            "Live roadmap that eliminates Excel exports is a massive PM pain point — strong product angle",
            "Stakeholder trust in data freshness is an acute problem — real-time sync is a key differentiator",
            "PMs spending 3h/day in PM tools suggests product stickiness opportunity"
        ]
    },
    {
        "id": "TF-005",
        "startup": "TaskFlow",
        "startup_domain": "Project Management SaaS",
        "founder_research_question": "Why do remote engineering teams switch away from Jira, and what are the top friction points?",
        "respondent": {"name": "Ryan C.", "role": "VP Engineering", "company_size": "350 employees", "industry": "SaaS"},
        "date": rand_date(10),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "At 350 people, you're managing project management at real scale. What does that look like and where does it break?"},
            {"speaker": "Customer", "text": "We have Jira for engineering, Confluence for docs, Slack for communication, and Figma for design. None of them talk to each other properly. I spend half my one-on-ones just trying to understand project status because nobody trusts the tickets."},
            {"speaker": "AI", "text": "When you say nobody trusts the tickets — what's the consequence of that?"},
            {"speaker": "Customer", "text": "We have shadow systems. Each team lead has their own spreadsheet. I have my own spreadsheet. The executive team has a dashboard that's manually updated. We're all triangulating from different sources and reaching different conclusions. It's chaos with a polished veneer."},
            {"speaker": "AI", "text": "What would you pay to solve the 'shadow systems' problem?"},
            {"speaker": "Customer", "text": "Honestly, if someone could give me one accurate source of truth and kill the spreadsheets, I'd pay $50 per seat per month and not think twice. The productivity loss is 10x that."},
            {"speaker": "AI", "text": "What would it take to get 350 engineers to actually adopt a new tool?"},
            {"speaker": "Customer", "text": "Executive sponsorship plus a migration team that handles the actual data move. I've been burned by 'easy migrations' before. The tool itself needs to win engineers in the first 20 minutes or they'll revolt."},
        ],
        "themes": ["shadow systems", "tool fragmentation", "data accuracy", "enterprise adoption", "migration risk", "willingness to pay"],
        "sentiment_scores": {"overall": 2.3, "pain_intensity": 4.5, "openness_to_switch": 3.8},
        "key_quotes": [
            "We're all triangulating from different sources — chaos with a polished veneer",
            "I'd pay $50/seat/month and not think twice",
            "The tool needs to win engineers in the first 20 minutes or they'll revolt"
        ],
        "actionable_insights": [
            "$50/seat price point validated by VP Eng at 350-person company",
            "Shadow spreadsheet elimination is the enterprise value prop — quantify this",
            "First 20-minute onboarding experience is make-or-break for engineer adoption"
        ]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# STARTUP 2: NourishNow — hyperlocal healthy meal delivery for offices
# ─────────────────────────────────────────────────────────────────────────────
nourishnow_interviews = [
    {
        "id": "NN-001",
        "startup": "NourishNow",
        "startup_domain": "Food Delivery / HealthTech",
        "founder_research_question": "What are the top barriers to healthy eating at work, and what would make people pay for a solution?",
        "respondent": {"name": "Michelle T.", "role": "Operations Manager", "company_size": "60 employees", "industry": "Consulting"},
        "date": rand_date(1),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "I'd love to understand lunch at your office. Walk me through a typical workday lunch — what actually happens?"},
            {"speaker": "Customer", "text": "It's a disaster. Half the team orders DoorDash, which takes 45 minutes and costs $20-25 per person. The other half brings sad desk salads. The people who order delivery end up eating at 2pm because the first order was wrong."},
            {"speaker": "AI", "text": "When you say the first order was wrong — how often does that actually happen?"},
            {"speaker": "Customer", "text": "At least twice a week for someone on our team. And it's not just wrong orders — it's cold food, missing items, and then you've spent 20 minutes on a chat with customer support. It ruins the afternoon."},
            {"speaker": "AI", "text": "You manage operations for the office. Is lunch something you've ever tried to solve at a company level?"},
            {"speaker": "Customer", "text": "We tried a catering service for a month. $18 per person per day, food was mediocre, and half the team had dietary restrictions that weren't being met. Vegetarians were eating the same sad pasta every day."},
            {"speaker": "AI", "text": "What's the magic version of office lunch for you?"},
            {"speaker": "Customer", "text": "Hot, healthy, ready at 12:30, with actual dietary options — not just 'we have salad.' And I want to not think about it. If I could set it up once and it just works every day, I'd sign a contract today."},
        ],
        "themes": ["delivery reliability", "dietary restrictions", "office catering", "convenience", "willingness to pay", "decision fatigue"],
        "sentiment_scores": {"overall": 2.2, "pain_intensity": 4.2, "openness_to_switch": 4.8},
        "key_quotes": [
            "I'd sign a contract today",
            "Half the team has dietary restrictions that weren't being met",
            "If I could set it up once and it just works every day"
        ],
        "actionable_insights": [
            "Set-and-forget subscription model is highly desired by ops managers",
            "Dietary restrictions handling is a major differentiator vs. existing catering",
            "$18/person/day is an accepted price point for corporate catering"
        ]
    },
    {
        "id": "NN-002",
        "startup": "NourishNow",
        "startup_domain": "Food Delivery / HealthTech",
        "founder_research_question": "What are the top barriers to healthy eating at work, and what would make people pay for a solution?",
        "respondent": {"name": "David W.", "role": "Software Engineer", "company_size": "150 employees", "industry": "Tech"},
        "date": rand_date(3),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "What does your lunch routine look like on a typical workday?"},
            {"speaker": "Customer", "text": "I used to be really intentional about it — meal prep on Sundays. But I've been in crunch mode for three months and I've completely fallen off. Now it's whatever is fastest, usually something terrible."},
            {"speaker": "AI", "text": "When you say 'something terrible' — what does that actually look like?"},
            {"speaker": "Customer", "text": "Chips from the vending machine or whatever is left in the kitchen. Sometimes I just don't eat lunch at all and then I'm useless in the 3pm standup. I know it's bad but when I'm in a deadline sprint I just don't have the mental bandwidth."},
            {"speaker": "AI", "text": "How does skipping lunch actually affect your afternoon performance?"},
            {"speaker": "Customer", "text": "Measurably. I can feel my focus drop around 2:30. I make more bugs, I'm less patient in code reviews. I've actually started blocking 12-12:30 on my calendar just to force myself to eat something."},
            {"speaker": "AI", "text": "You're clearly aware this is a problem. What's stopped you from solving it?"},
            {"speaker": "Customer", "text": "Decision fatigue. I make thousands of decisions at work. The last thing I want is another decision about what to eat. If something just showed up at my desk that was actually good for me, I'd pay $15 easily."},
        ],
        "themes": ["decision fatigue", "health awareness", "productivity impact", "willingness to pay", "convenience", "work-life balance"],
        "sentiment_scores": {"overall": 2.8, "pain_intensity": 3.7, "openness_to_switch": 4.3},
        "key_quotes": [
            "I can feel my focus drop around 2:30 — I make more bugs",
            "Decision fatigue — I make thousands of decisions at work",
            "If something just showed up at my desk that was actually good for me, I'd pay $15 easily"
        ],
        "actionable_insights": [
            "Engineers link food quality directly to afternoon productivity — strong ROI narrative for B2B sales",
            "$15/meal price sensitivity confirmed for individual contributors",
            "Decision fatigue is the key insight — emphasize zero-decision positioning"
        ]
    },
    {
        "id": "NN-003",
        "startup": "NourishNow",
        "startup_domain": "Food Delivery / HealthTech",
        "founder_research_question": "What are the top barriers to healthy eating at work, and what would make people pay for a solution?",
        "respondent": {"name": "Amara O.", "role": "HR Director", "company_size": "200 employees", "industry": "Finance"},
        "date": rand_date(6),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "From an HR perspective, how do you think about food and nutrition as part of employee wellbeing?"},
            {"speaker": "Customer", "text": "It's in our employee benefits strategy but honestly we haven't done it well. We have a $50/month meal stipend on Expensify but less than 30% of employees actually use it — the process is too annoying."},
            {"speaker": "AI", "text": "Only 30% using a benefit they're entitled to — that's striking. What do you think is stopping the other 70%?"},
            {"speaker": "Customer", "text": "Expense reports. Nobody wants to photograph receipts and submit them for $12. The friction is higher than the value. I've been trying to get the CFO to approve a direct corporate account with a delivery service but the audit requirements are complicated."},
            {"speaker": "AI", "text": "If you could get a corporate solution approved tomorrow, what would the CFO need to see to say yes?"},
            {"speaker": "Customer", "text": "Cost per employee per day, utilization rate, and ideally some data linking it to reduced sick days or improved engagement scores. We did an engagement survey and 'better food options at work' was the #3 most requested benefit."},
            {"speaker": "AI", "text": "What's the connection between food and the broader employee retention picture for you?"},
            {"speaker": "Customer", "text": "Enormous. We're competing with Google and Meta for talent. They have free gourmet cafeterias. I can't match that, but if I could offer daily healthy delivered lunches as a perk, that's a real differentiator in recruiting conversations."},
        ],
        "themes": ["employee benefits", "corporate procurement", "utilization friction", "recruiting competitiveness", "ROI measurement", "expense workflow"],
        "sentiment_scores": {"overall": 3.1, "pain_intensity": 3.4, "openness_to_switch": 4.6},
        "key_quotes": [
            "Less than 30% use the meal stipend — the process is too annoying",
            "'Better food options at work' was the #3 most requested benefit",
            "We're competing with Google and Meta — free cafeterias are a real differentiator"
        ],
        "actionable_insights": [
            "HR buyers need CFO-ready ROI data: cost/employee/day, utilization, and ideally engagement lift",
            "Corporate billing (not expense reimbursement) is table stakes for enterprise adoption",
            "Talent acquisition angle is a strong HR buyer motivation — not just wellness"
        ]
    },
    {
        "id": "NN-004",
        "startup": "NourishNow",
        "startup_domain": "Food Delivery / HealthTech",
        "founder_research_question": "What are the top barriers to healthy eating at work, and what would make people pay for a solution?",
        "respondent": {"name": "Carlos R.", "role": "Founder & CEO", "company_size": "8 employees", "industry": "ClimateTech"},
        "date": rand_date(8),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "As a founder with a small team, how do you handle food at the office?"},
            {"speaker": "Customer", "text": "We don't really have an office — we're remote-first with a WeWork membership people use occasionally. Lunch is completely individual. I probably spend $25 a day on food and it's almost always bad for me."},
            {"speaker": "AI", "text": "Why do you think you consistently end up with unhealthy choices despite spending $25 a day?"},
            {"speaker": "Customer", "text": "When I'm building, I'm in flow state. Stopping to figure out food feels like a context switch I can't afford. So I go for the fastest thing, which is never the healthiest thing. I've gained 15 pounds since starting this company."},
            {"speaker": "AI", "text": "That's a significant impact. Have you ever tried any solutions — meal kits, meal prep services, anything?"},
            {"speaker": "Customer", "text": "Tried HelloFresh — the cooking takes 45 minutes which defeats the purpose. Tried Factor meals — they're fine but they're designed for home not for eating at a desk in a work headspace. And they don't do lunch timing."},
            {"speaker": "AI", "text": "What would make you actually adopt something new given your remote setup?"},
            {"speaker": "Customer", "text": "Delivery timed exactly to when I want to eat, not a 3-hour window. Portioned for one person. And honestly something I feel good about eating, not just 'healthy-ish'. I'm in my 30s and I can feel the difference now."},
        ],
        "themes": ["remote work", "individual health", "founder lifestyle", "meal timing", "flow state disruption", "health consciousness"],
        "sentiment_scores": {"overall": 2.6, "pain_intensity": 4.0, "openness_to_switch": 4.1},
        "key_quotes": [
            "Stopping to figure out food feels like a context switch I can't afford",
            "I've gained 15 pounds since starting this company",
            "Delivery timed exactly to when I want to eat, not a 3-hour window"
        ],
        "actionable_insights": [
            "Precise delivery timing (not window) is a strong differentiator for knowledge workers",
            "Flow state protection is a powerful emotional hook for founder/IC personas",
            "Existing alternatives (HelloFresh, Factor) are failing on timing and office context"
        ]
    },
    {
        "id": "NN-005",
        "startup": "NourishNow",
        "startup_domain": "Food Delivery / HealthTech",
        "founder_research_question": "What are the top barriers to healthy eating at work, and what would make people pay for a solution?",
        "respondent": {"name": "Lisa H.", "role": "Chief People Officer", "company_size": "500 employees", "industry": "Biotech"},
        "date": rand_date(12),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "At 500 employees, food is probably a meaningful operational challenge. How do you currently handle it?"},
            {"speaker": "Customer", "text": "We have a subsidized cafeteria but it's expensive to run — about $600K a year in overhead. And post-pandemic, only 60% of people are in office on any given day, so we're paying for capacity we don't use."},
            {"speaker": "AI", "text": "That cost structure sounds painful. Are you actively looking for alternatives?"},
            {"speaker": "Customer", "text": "Yes, but our employees have high expectations. Half the team came from big tech where food was a major perk. We can't just remove the cafeteria and give everyone $10 a day — there'd be a revolt."},
            {"speaker": "AI", "text": "What would you need to see from an alternative to even consider replacing the cafeteria?"},
            {"speaker": "Customer", "text": "Quality that's at least comparable, coverage of all dietary needs — we have employees with serious allergies, halal and kosher requirements. And the admin burden has to be lower, not higher. Right now I have a full-time person managing food vendor relationships."},
            {"speaker": "AI", "text": "If a solution could match cafeteria quality at lower cost and lower admin burden, what would the procurement process look like?"},
            {"speaker": "Customer", "text": "6-month pilot, legal review of the vendor contract, probably a $50K annual commitment minimum to get budget approved. But if it works, we'd expand to all 3 of our campuses."},
        ],
        "themes": ["enterprise food ops", "cafeteria replacement", "dietary compliance", "procurement complexity", "post-pandemic hybrid work", "cost reduction"],
        "sentiment_scores": {"overall": 3.2, "pain_intensity": 3.8, "openness_to_switch": 3.5},
        "key_quotes": [
            "$600K a year in cafeteria overhead, 60% utilization post-pandemic",
            "I have a full-time person managing food vendor relationships",
            "If it works, we'd expand to all 3 of our campuses"
        ],
        "actionable_insights": [
            "Enterprise land-and-expand opportunity: single campus pilot → multi-campus rollout",
            "Halal/kosher/allergy compliance is non-negotiable for enterprise contracts",
            "$50K annual minimum contract size for enterprise budget approval — set pricing accordingly"
        ]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# STARTUP 3: HireIQ — AI-powered hiring platform for technical roles
# ─────────────────────────────────────────────────────────────────────────────
hireiq_interviews = [
    {
        "id": "HQ-001",
        "startup": "HireIQ",
        "startup_domain": "HR Tech / AI Recruiting",
        "founder_research_question": "What are the biggest pain points in technical hiring and where do current ATS tools fall short?",
        "respondent": {"name": "Tom B.", "role": "Head of Engineering", "company_size": "90 employees", "industry": "SaaS"},
        "date": rand_date(2),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "Technical hiring is notoriously hard. Walk me through your last engineering hire — what was the experience?"},
            {"speaker": "Customer", "text": "We posted a senior backend role in January. Got 340 applications. I spent two weeks just doing resume screens. Hired someone in March. Four months start to finish. It was brutal."},
            {"speaker": "AI", "text": "340 applications for one role — how did you decide who to actually interview?"},
            {"speaker": "Customer", "text": "Keyword matching, basically. Python, AWS, 5+ years. I know it's terrible. I probably passed on great candidates who didn't know to include buzzwords and advanced unqualified people who did."},
            {"speaker": "AI", "text": "You mentioned 4 months start to finish. What was the most time-consuming part?"},
            {"speaker": "Customer", "text": "Scheduling. I'm not kidding — scheduling alone probably took 40 hours across the whole process. Coordinating 4 interviewers, time zones, candidate no-shows. We use Calendly but it still requires someone to coordinate everything manually."},
            {"speaker": "AI", "text": "If you could get back those 4 months and 40 hours, how would that change what you're building?"},
            {"speaker": "Customer", "text": "I'd have shipped the feature we delayed by 3 months because we were short-staffed. Bad hiring process has real product consequences. I'm willing to pay serious money to fix it."},
        ],
        "themes": ["resume screening", "scheduling friction", "time-to-hire", "keyword filtering", "hiring bias", "product impact"],
        "sentiment_scores": {"overall": 2.0, "pain_intensity": 4.6, "openness_to_switch": 4.5},
        "key_quotes": [
            "Scheduling alone took 40 hours across the whole process",
            "Keyword matching, basically — I know it's terrible",
            "Bad hiring process has real product consequences"
        ],
        "actionable_insights": [
            "Scheduling automation is a massive pain point — even beyond resume screening",
            "Keyword-based screening is known to be flawed — buyers are aware and embarrassed",
            "Link hiring delay to product delay in sales narrative — concrete business cost"
        ]
    },
    {
        "id": "HQ-002",
        "startup": "HireIQ",
        "startup_domain": "HR Tech / AI Recruiting",
        "founder_research_question": "What are the biggest pain points in technical hiring and where do current ATS tools fall short?",
        "respondent": {"name": "Rachel G.", "role": "Technical Recruiter", "company_size": "1200 employees", "industry": "Enterprise Tech"},
        "date": rand_date(4),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "As a technical recruiter, you sit between engineering managers and candidates. What's the hardest part of your job that technology hasn't solved?"},
            {"speaker": "Customer", "text": "Getting engineers to give me feedback quickly. I'll send a hiring manager feedback for 3 candidates and wait a week for a response. Meanwhile the good candidate has 3 other offers."},
            {"speaker": "AI", "text": "How often do you lose candidates specifically because of slow internal feedback loops?"},
            {"speaker": "Customer", "text": "Every week. Conservatively, I lose one strong candidate per week to a faster-moving company. My current ATS — we use Greenhouse — doesn't solve this at all. It sends reminders that people ignore."},
            {"speaker": "AI", "text": "What have you tried to fix this problem?"},
            {"speaker": "Customer", "text": "Slack nudges, personal emails, even walking to desks pre-pandemic. Nothing works consistently because hiring isn't engineers' main job — they're busy. What I actually need is an AI that can draft the feedback and just ask them to confirm or edit."},
            {"speaker": "AI", "text": "If an AI could draft preliminary feedback based on the interview notes, would hiring managers actually use it?"},
            {"speaker": "Customer", "text": "Absolutely. Most of them struggle to articulate why they liked or didn't like a candidate. If the AI gave them a structured draft based on what they said in Slack or the debrief, they'd probably just hit confirm 80% of the time."},
        ],
        "themes": ["feedback latency", "candidate pipeline speed", "ATS limitations", "engineering manager adoption", "AI-assisted evaluation", "competitive offers"],
        "sentiment_scores": {"overall": 2.5, "pain_intensity": 4.4, "openness_to_switch": 4.6},
        "key_quotes": [
            "I lose one strong candidate per week to a faster-moving company",
            "Greenhouse sends reminders that people ignore",
            "If the AI gave them a structured draft, they'd hit confirm 80% of the time"
        ],
        "actionable_insights": [
            "AI-drafted feedback for engineering manager approval is a highly desired feature",
            "Speed-to-offer is a key competitive metric — position against slower ATS workflows",
            "Recruiters are the actual power users and champions — sell to them first"
        ]
    },
    {
        "id": "HQ-003",
        "startup": "HireIQ",
        "startup_domain": "HR Tech / AI Recruiting",
        "founder_research_question": "What are the biggest pain points in technical hiring and where do current ATS tools fall short?",
        "respondent": {"name": "Kevin S.", "role": "CTO", "company_size": "25 employees", "industry": "AI/ML Startup"},
        "date": rand_date(7),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "You're hiring AI/ML engineers which is probably among the most competitive roles in the market. What's your approach?"},
            {"speaker": "Customer", "text": "Mostly referrals and cold outreach on LinkedIn. Job boards give us garbage. I've gotten maybe 2 good candidates from job postings in two years versus 20 from referrals."},
            {"speaker": "AI", "text": "Why do you think job boards fail so badly for AI/ML roles specifically?"},
            {"speaker": "Customer", "text": "The best ML engineers aren't looking. They're employed, well-paid, and not refreshing LinkedIn. The ones who are actively applying are usually the ones who got laid off or couldn't pass interviews elsewhere. That sounds harsh but it's our reality."},
            {"speaker": "AI", "text": "So you're primarily doing outbound. How many hours a week do you personally spend on recruiting?"},
            {"speaker": "Customer", "text": "More than I should. Probably 10 hours a week on sourcing, messaging, and first-round screening calls. For a CTO of a 25-person company that's insane — I should be building product, not recruiting."},
            {"speaker": "AI", "text": "If a tool could handle the sourcing and initial outreach with high enough quality to replace your personal touch, would you trust it?"},
            {"speaker": "Customer", "text": "I'm skeptical but interested. The personalization bar is high — generic InMail gets zero response. If it could analyze a candidate's GitHub, their papers, their Twitter and write something that actually references their work, maybe."},
        ],
        "themes": ["sourcing quality", "passive candidates", "outbound recruiting", "personalization", "CTO time cost", "referral networks"],
        "sentiment_scores": {"overall": 2.9, "pain_intensity": 4.0, "openness_to_switch": 3.7},
        "key_quotes": [
            "10 hours a week on sourcing for a 25-person company CTO — that's insane",
            "The best ML engineers aren't looking",
            "If it analyzed their GitHub, their papers, their Twitter and wrote something that referenced their work"
        ],
        "actionable_insights": [
            "GitHub/paper analysis for personalized outreach is the key technical differentiator for AI/ML hiring",
            "Passive candidate sourcing is the real market gap — not job board optimization",
            "CTO recruiting time is a compelling cost narrative for early-stage companies"
        ]
    },
    {
        "id": "HQ-004",
        "startup": "HireIQ",
        "startup_domain": "HR Tech / AI Recruiting",
        "founder_research_question": "What are the biggest pain points in technical hiring and where do current ATS tools fall short?",
        "respondent": {"name": "Nina P.", "role": "VP People", "company_size": "400 employees", "industry": "Fintech"},
        "date": rand_date(9),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "Fintech hiring has specific compliance dimensions beyond typical tech hiring. How does that affect your process?"},
            {"speaker": "Customer", "text": "Enormously. Every hire goes through a background check, a credit check in some cases, and regulatory clearance for certain roles. Our ATS — Workday — wasn't designed for this complexity. We've built so many custom workflows that it barely resembles the out-of-box product."},
            {"speaker": "AI", "text": "What happens when those custom workflows break?"},
            {"speaker": "Customer", "text": "Candidate experience falls apart. We had an incident last quarter where a compliance step was skipped due to a workflow bug and we had to pull a job offer post-acceptance. That was a nightmare — legal, HR, and PR all involved."},
            {"speaker": "AI", "text": "What would a better-built solution need to have to even get a conversation with you?"},
            {"speaker": "Customer", "text": "SOC 2 Type II certification is non-negotiable. EEOC reporting built in, not bolted on. And an API that actually works so I don't have to rebuild my entire compliance workflow from scratch."},
            {"speaker": "AI", "text": "If all the compliance boxes were checked, what would the buying decision actually come down to?"},
            {"speaker": "Customer", "text": "Candidate experience scores and time-to-fill. Those are my two board metrics. If a new tool could show me a 20% reduction in time-to-fill and higher candidate NPS in a pilot, I'd have the business case to rip and replace Workday."},
        ],
        "themes": ["compliance requirements", "ATS customization", "candidate experience", "enterprise procurement", "board metrics", "SOC2/EEOC"],
        "sentiment_scores": {"overall": 2.7, "pain_intensity": 4.2, "openness_to_switch": 3.6},
        "key_quotes": [
            "SOC 2 Type II certification is non-negotiable",
            "We had to pull a job offer post-acceptance — legal, HR, and PR all involved",
            "20% reduction in time-to-fill and higher candidate NPS — that's my business case"
        ],
        "actionable_insights": [
            "SOC 2 Type II is table stakes for fintech buyers — must have before enterprise sales",
            "Compliance workflow reliability is a stronger pain than feature set for regulated industries",
            "Time-to-fill and candidate NPS are the two metrics that drive enterprise buying decisions"
        ]
    },
    {
        "id": "HQ-005",
        "startup": "HireIQ",
        "startup_domain": "HR Tech / AI Recruiting",
        "founder_research_question": "What are the biggest pain points in technical hiring and where do current ATS tools fall short?",
        "respondent": {"name": "Jordan M.", "role": "Software Engineer (recently hired)", "company_size": "60 employees", "industry": "Consumer Tech"},
        "date": rand_date(11),
        "duration_minutes": rand_duration(),
        "completion_status": "completed",
        "transcript": [
            {"speaker": "AI", "text": "You were recently hired — I'd love to get the candidate perspective. What was the experience of going through a technical hiring process like?"},
            {"speaker": "Customer", "text": "I applied to 12 companies over 6 weeks. The variation in process quality was shocking — some companies had me talking to a real person within 24 hours, others had me doing a 3-hour take-home before even a phone screen."},
            {"speaker": "AI", "text": "What made you ultimately choose the company you joined over the others?"},
            {"speaker": "Customer", "text": "Speed and respect for my time. They got back to me same day at every step. The technical interview was actually interesting, not just LeetCode puzzles. And the recruiter was honest about the role's challenges instead of overselling."},
            {"speaker": "AI", "text": "You mentioned 3-hour take-homes before a phone screen — how common was that and what did you think?"},
            {"speaker": "Customer", "text": "Four out of twelve companies did this. I completed two and ghosted the other two. It signals that the company doesn't value your time. If I'm senior, I shouldn't have to prove basic competency before you've even had a conversation with me."},
            {"speaker": "AI", "text": "What would your ideal technical interview process look like?"},
            {"speaker": "Customer", "text": "30-minute intro call to make sure we like each other. Then a 1-hour technical discussion about a real problem they've solved, not an algorithm puzzle. Then a team fit conversation. Total: 2 hours. I've seen it done — it's possible."},
        ],
        "themes": ["candidate experience", "interview process design", "take-home assignments", "response time", "interviewer quality", "transparency"],
        "sentiment_scores": {"overall": 3.4, "pain_intensity": 3.2, "openness_to_switch": 2.5},
        "key_quotes": [
            "Speed and respect for my time — that's why I chose them",
            "Four out of twelve companies did 3-hour take-homes — I ghosted two of them",
            "If I'm senior, I shouldn't have to prove basic competency before a conversation"
        ],
        "actionable_insights": [
            "Candidate ghosting of lengthy take-homes is quantifiable and compelling for employer branding argument",
            "Same-day response at every step is a key candidate experience differentiator — measurable",
            "Real problem discussion > LeetCode is a signal of company culture quality for senior candidates"
        ]
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Combine all interviews
# ─────────────────────────────────────────────────────────────────────────────
all_interviews = taskflow_interviews + nourishnow_interviews + hireiq_interviews

database = {
    "metadata": {
        "platform": "AI Customer Interview Platform",
        "version": "1.0",
        "generated": "2026-01-15",
        "total_interviews": len(all_interviews),
        "startups": 3,
        "description": "Synthetic customer interview database for MKTG 321 prototype demonstration"
    },
    "interviews": all_interviews
}

OUT = r"C:\Users\13nas\OneDrive\Desktop\GSB\Classes\MKTG-321- Understanding AI Technology\final project\prototype\data\synthetic_interviews.json"
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(database, f, indent=2, ensure_ascii=False)

print(f"Generated {len(all_interviews)} interviews across 3 startups")
print(f"Saved to: {OUT}")
