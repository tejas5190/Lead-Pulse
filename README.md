# 🚀 LeadPulse AI — Autonomous Digital Marketing Agency & Meta Ads Platform

**LeadPulse AI** is an autonomous, full-stack digital marketing agency operating system. Built for agencies, real estate developers, dental clinics, fitness centers, and local businesses, it automates the entire growth cycle: from business page setup and 30-day organic launch roadmaps to high-converting ad creative synthesis and self-driving Meta (Instagram & Facebook) Ad campaigns.

---

## 🌟 The Four Core Agency Pillars

### 1. 📊 Master Meta Ads & Campaign Manager (`leadpulse/ad_manager/`)
- **Real-Time Performance Gauges**: Tracks Total Ad Spend, Paid Leads Generated via Click-To-WhatsApp, Average Cost-Per-Lead (CPL), and CTR.
- **AI Self-Driving Auto-Pilot**:
  - **🛑 Kill Switch**: Automatically pauses campaigns if CPL exceeds 1.4x the target or burns budget with zero leads.
  - **🚀 Auto-Scale Winner**: Automatically scales daily budget by +20% when campaigns acquire leads at $\le 75\%$ of target CPL.
  - **🎨 Creative Fatigue Alert**: Warns when CTR drops below 0.85% and advises rotating creatives.
- **Campaign Controls**: 1-click launch modal, status toggle (Active/Paused), live budget editing, and on-demand AI optimization.

### 2. 🎨 Photorealistic Creative Studio & Canva Integration (`leadpulse/creative_studio/`)
- **Photographic Ad Compositor**: Merges high-resolution 4K photography with dark frosted-glass vignettes and high-contrast WhatsApp CTA badges.
- **Dynamic Canva Integration**: 1-click shortcut opening tailored Canva templates matching the business category.
- **9:16 Reels Video Ad Synthesizer**: Uses Edge-TTS neural voiceover narration (`en-IN-NeerjaNeural`) and native FFmpeg to assemble vertical short video ads with kinetic captions and animated cards.
- **Multi-Angle Ad Copywriter**: Generates 3 CTR-optimized headlines, 3 primary ad copies (Desire, Logic/EMI, Urgency), and 15-second timestamped video narration scripts.

### 3. 📅 30-Day Growth & Launch Strategy Planner (`leadpulse/agency_marketing/`)
- Automatically builds an end-to-end 30-day marketing roadmap across 4 distinct phases:
  - **Phase 1 (Days 1–7)**: *Authority & Awareness* (Trust, doctor intro, behind-the-scenes).
  - **Phase 2 (Days 8–14)**: *Social Proof & Objection Handling* (Transformations, EMI breakdowns).
  - **Phase 3 (Days 15–21)**: *Pre-Launch Hype & Engagement* (VIP waitlist, interactive polls).
  - **Phase 4 (Days 22–30)**: *Paid Meta Ad Blitz & Conversion* (Click-To-WhatsApp direct conversion).
- Specifies daily **Headline**, **Caption**, **Visual Brief**, **Format** (Reels, Carousels, Stories), **CTA**, and **Optimal Posting Time**.

### 4. 🪄 Non-Tech Business Page Setup Concierge (`leadpulse/agency_marketing/`)
- **Done-For-You Profile Branding**:
  - SEO-optimized Instagram Profile Name and Category.
  - High-converting bulleted Instagram Bio with copy buttons.
  - Pre-filled direct WhatsApp link (`https://wa.me/...`) for instant lead tracking.
  - 5 Story Highlight cover recommendations.
- **5-Minute Non-Tech Checklist**: Simple, step-by-step guidance for non-tech business owners to configure professional accounts and auto-reply greetings.

---

## 🎯 Conversational Lead Qualification Engine

- **7 Pre-Built Industry Templates**: Real Estate, Dental Clinic, Fitness / Gym, Coaching & Education, Interior Design, Hair & Skin Clinic, and Custom.
- **Automated WhatsApp Webhook**: Meta WhatsApp Cloud API webhook receiver with bidirectional messaging and lead qualification scoring.
- **Real-Time KPI Dashboard**: Tracks daily lead volume, weekly qualification rates, and full conversational transcripts.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.12+), SQLAlchemy 2.0 (Async), SQLite / PostgreSQL
- **Frontend**: TailwindCSS, Vanilla JS (zero build step required, runs instantly in any browser)
- **Audio & Video Engine**: Microsoft Edge-TTS neural voice synthesis, FFmpeg, Pillow
- **Meta Graph API**: Marketing API v21.0 integration with high-fidelity local sandbox

---

## 🚀 Quickstart Guide

### 1. Clone & Setup
```bash
git clone https://github.com/tejas5190/Lead-Pulse.git
cd Lead-Pulse
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

### 2. Run Automated Verification Tests
```bash
python test_suite.py
```
> Runs all **19/19 automated end-to-end tests** verifying the database, auth, creative studio, marketing engine, and Meta Ads manager.

### 3. Launch Dashboard Server
```bash
uvicorn leadpulse.main:app --host 127.0.0.1 --port 8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser:
- **Email**: `demo@skylineapex.com`
- **Password**: `Password123!`

---

## 📄 License
MIT License. Built for modern digital marketing agencies and local business growth.
