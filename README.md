# 🚀 LeadPulse AI — Autonomous Digital Marketing Agency & Meta Ads Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-indigo?style=for-the-badge&logo=github)](https://tejas5190.github.io/Lead-Pulse/)
[![Deploy to Render](https://img.shields.io/badge/Deploy%20Backend-Render-emerald?style=for-the-badge&logo=render)](https://render.com/deploy?repo=https://github.com/tejas5190/Lead-Pulse)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **Live Preview (Mobile & Desktop)**: [https://tejas5190.github.io/Lead-Pulse/](https://tejas5190.github.io/Lead-Pulse/)  
> **100% Operational Standalone**: Includes an **Autonomous Client Engine** with zero backend setup required for immediate creation of ad copy, high-res banners, 9:16 vertical video stories, 30-day marketing calendars, and Meta Ads simulations.

---

## 🌟 The Four Core Agency Pillars

### 1. 🎨 Photorealistic Creative Studio & Canva Integration (`leadpulse/creative_studio/`)
- **1-Click Industry Presets**: Instant load for Real Estate (3BHK), Laser Dental, Fitness & Gym, UPSC Coaching, Diamond Jewellery, and Luxury Cars.
- **Dynamic HTML5 Canvas 1080x1080 Banner Designer**: Generates photorealistic feed ads with high-contrast text, glowing price pills, verified badges, and WhatsApp CTAs exportable to PNG with 1 click.
- **Dynamic Canva Integration**: Automatically generates deep links to matching Canva templates for the selected business category.
- **Kinetic 9:16 Reels Video Story Player**: Interactive vertical reel player with 4 animated slides:
  - **Slide 1**: The Hook (Attention-grabbing headline)
  - **Slide 2**: The Pain (Agitating customer frustration)
  - **Slide 3**: The Solution (Showcasing product with glowing price pill)
  - **Slide 4**: The CTA (Direct WhatsApp booking with urgency countdown)
- **Multi-Angle Ad Copywriter**: Generates 3 CTR-optimized headlines, 3 primary ad copies (Desire, Logic/EMI, Urgency), and 15-second timestamped video narration scripts.
- **Server Audio & Video Synthesis**: When running the Python backend, uses Edge-TTS neural voiceover narration (`en-IN-NeerjaNeural`, `hi-IN-SwaraNeural`) and FFmpeg to assemble vertical MP4 reels.

### 2. 📊 Master Meta Ads & Campaign Manager (`leadpulse/ad_manager/`)
- **Real-Time Performance Gauges**: Tracks Total Ad Spend, Paid Leads Generated via Click-To-WhatsApp, Average Cost-Per-Lead (CPL), and CTR.
- **AI Self-Driving Auto-Pilot**:
  - **🛑 Kill Switch**: Automatically pauses campaigns if CPL exceeds 1.4x the target or burns budget with zero leads.
  - **🚀 Auto-Scale Winner**: Automatically scales daily budget by +20% when campaigns acquire leads at $\le 75\%$ of target CPL.
  - **🎨 Creative Fatigue Alert**: Warns when CTR drops below 0.85% and advises rotating creatives.
- **Campaign Controls**: 1-click launch modal, status toggle (Active/Paused), live budget editing, and on-demand AI optimization persisted in local storage or SQLite.

### 3. 📅 30-Day Growth & Launch Strategy Planner (`leadpulse/agency_marketing/`)
- Automatically builds an end-to-end 30-day marketing roadmap across 4 distinct phases:
  - **Phase 1 (Days 1–7)**: *Authority & Awareness* (Trust, expert intro, behind-the-scenes).
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
- **Live WhatsApp Qualification Simulator**: Interactive modal to test the conversational bot in real time, see lead score calculated dynamically (Hot / Warm / Cold), and automatically inject qualified leads into the CRM table.
- **Automated WhatsApp Webhook**: Meta WhatsApp Cloud API webhook receiver with bidirectional messaging and lead qualification scoring.

---

## 🛠️ Tech Stack & Deployment

| Layer | Technologies |
|---|---|
| **Frontend** | Vanilla JS, TailwindCSS, HTML5 Canvas 2D (zero build step required, runs instantly in any browser) |
| **Backend API** | FastAPI (Python 3.11+), SQLAlchemy 2.0 (Async), SQLite / PostgreSQL |
| **Audio & Video Engine** | Microsoft Edge-TTS neural voice synthesis, FFmpeg, Pillow |
| **Meta Graph API** | Marketing API v21.0 integration with high-fidelity local sandbox |
| **Cloud Hosting** | GitHub Pages (Frontend), Render / Railway / Docker (Backend) |

---

## 🚀 How to Run

### Option A: Open Immediately in Browser (No Server Needed)
Visit [https://tejas5190.github.io/Lead-Pulse/](https://tejas5190.github.io/Lead-Pulse/) on your phone or computer. The client engine runs autonomously with zero configuration.

### Option B: Run Full Python Backend Locally
```bash
git clone https://github.com/tejas5190/Lead-Pulse.git
cd Lead-Pulse
python -m venv .venv
.\.venv\Scripts\activate   # Windows
# source .venv/bin/activate # macOS/Linux
pip install -r requirements.txt
python test_suite.py       # Runs all 19 automated tests
uvicorn leadpulse.main:app --host 127.0.0.1 --port 8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Option C: 1-Click Free Cloud Deployment (Render)
1. Fork or push this repository to your GitHub account.
2. Click **[Deploy to Render](https://render.com/deploy?repo=https://github.com/tejas5190/Lead-Pulse)**.
3. Render automatically reads `render.yaml` and launches your FastAPI backend on free tier.
4. Copy your Render URL (e.g. `https://leadpulse-api.onrender.com`), click `⚙️` in the LeadPulse top navigation, and paste your URL to connect!

---

## 📄 License
MIT License. Built for modern digital marketing agencies and local business growth.
