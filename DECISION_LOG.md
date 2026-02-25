# Decision Log — Monday.com BI Agent

## Key Assumptions
- monday.com boards contain messy real-world data.
- Status values represent sales lifecycle stages (Open, Won, Dead, etc.).
- Leadership primarily needs high-level summaries rather than raw tables.

---

## Trade-offs

### 1. Rule-based Query Interpretation
Given the 6-hour constraint, I implemented keyword-based founder-level query recognition instead of a full LLM reasoning engine. This ensured reliability and time efficiency.

### 2. Streamlit for Hosting
Chose Streamlit for rapid deployment and interactive conversational UI with minimal infrastructure overhead.

### 3. Read-Only Integration
Maintained strict read-only interaction with monday.com API as required.

---

## Data Resilience Strategy
- Used safe datetime conversion with error coercion.
- Handled null revenue values.
- Exposed missing data metrics visibly in UI.
- Prevented crashes due to incomplete records.

---

## Interpretation of "Leadership Updates"
Implemented a structured Leadership Snapshot that includes:
- Open Pipeline Value
- Win Rate
- Active Projects
- Overall business health commentary

This satisfies the optional requirement by transforming raw metrics into executive-friendly summaries.

---

## What I Would Improve With More Time
- LLM-powered semantic query understanding
- Automated sectoral performance breakdown
- Clarification question engine
- Board schema auto-detection
- Advanced trend analysis (MoM / QoQ)

---

## Final Reflection
The system prioritizes robustness, clarity, and executive usability while maintaining clean API-driven architecture within the 6-hour timeline.