# Monday.com Business Intelligence Agent

## Overview
This project implements an AI-powered Business Intelligence Agent that connects to monday.com boards and answers founder-level business questions.

The agent integrates with:
- Deals board (Sales pipeline)
- Work Orders board (Operational execution)

It dynamically fetches live data via the monday.com API and provides conversational business insights.

---

## Features

### 1. Monday.com Integration
- Live API connection (Read-only)
- Fetches multiple boards dynamically
- No hardcoded CSV data

### 2. Data Resilience
- Handles missing/null values
- Normalizes inconsistent date formats
- Communicates data quality metrics

### 3. Business Intelligence Metrics
- Pipeline value
- Total won revenue
- Win rate
- Active & completed projects
- Leadership summary snapshot

### 4. Conversational Interface
- Founder-style query handling
- Pipeline health insights
- Leadership update generation

---

## Architecture

monday.com API → Data Cleaning → Business Metrics Engine → Streamlit UI

---

## Tech Stack
- Python
- Streamlit
- Pandas
- Requests
- OpenAI (optional extension)

---

## Deployment
Hosted via Streamlit Cloud.

---

## Assumptions
- Board structures are consistent
- Status values follow defined categories
- API keys stored securely in Streamlit Secrets

---

## Future Improvements
- LLM-powered query understanding
- Advanced sectoral breakdown
- Natural language clarification prompts
- Multi-board aggregation engine