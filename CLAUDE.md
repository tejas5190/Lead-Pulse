# LeadPulse AI — Project CLAUDE.md (ECC Harness + Thinking Master Ecosystem)

This repository contains **LeadPulse AI**, the production-grade AI-powered lead qualification and autonomous creative studio for Meta & omnichannel advertising.

---

## 1. Core Operating Principles

### A. Think Before Coding & Simplicity First
- **Don't assume. Don't hide confusion. Surface tradeoffs.**
- Minimum code that solves the problem. No speculative abstractions.
- Surgical changes only: touch only what you must. Every changed line traces to the user objective.

### B. Goal-Driven Execution & Verification Loops
- Transform tasks into verifiable goals.
- Always run `python test_suite.py` before and after changes. All 19 tests must pass with 100% success.
- If modifying browser UI, visually inspect and verify the frontend with browser tools.

### C. Zero Mockup / Zero Hardcoded Fallback Rule
- **Never hardcode fake demo data, static placeholder names, or generic fallbacks (e.g. apartment/clinic fallbacks).**
- All creatives, copy, screenplays, and visual assets must be generated **live on-the-fly** via the local **Omni-tm Thinking Master** AI engine (`http://localhost:20128/v1/messages`).
- Ensure all industry CTAs, theme detection, and canvas graphics dynamically adapt to whatever topic or business the user provides.

---

## 2. ECC Harness & Skill Ecosystem

This project leverages the **ECC (Everything Claude Code)** harness optimization system (`affaan-m/ECC`):
- **Rules**: Language rules (`rules/ecc/python/`, `rules/ecc/react/`, `rules/ecc/common/`) apply across all modules.
- **Commands**: Slash commands (`/tdd`, `/plan`, `/code-review`, `/build-fix`, `/security-scan`) are active.
- **Skills Available**:
  * `omni-voicestudio`: Neural voice synthesis and commercial audio ad direction (debpalash/VoiceStudio).
  * `ai-ugc-video-creator`: Realistic AI actor UGC ads, Veo 3.1/Sora 2 screenplays (Open-AI-UGC, superCMO-skills).
  * `claude-paid-ads-ops`: 12-platform paid media management and ROAS optimization (AgriciDaniel/claude-ads).
  * `social-growth-engine`: Viral hooks, carousels, threads, and captions (rediumvex, sergebulaev).
  * `full-marketing-os`: PAS/AIDA copywriting, ad copy grading, 5-stage email sequences (ai-marketing-claude, marketing-os).
  * `motion-graphics-skills`: Code-generated 60fps canvas & FFmpeg motion graphics (charlie947/motion-graphics-skills).
  * `digital-marketing-intelligence`: Technical SEO/SEM automation, server-side CAPI tracking (advertools, awesome-marketing).

---

## 3. Architecture & Service Topology
- **FastAPI Backend**: `leadpulse/main.py` runs on `127.0.0.1:8000`.
- **OmniRoute AI Daemon**: `http://localhost:20128/v1` model `Omni-tm`.
- **Creative Studio Engine**:
  * Copy & Screenplay: `leadpulse/creative_studio/thinking_master.py`
  * Dynamic Banner Designer: `leadpulse/creative_studio/banner_designer.py`
  * Dynamic Video Producer: `leadpulse/creative_studio/video_producer.py`
  * Frontend: `leadpulse/static/index.html` (synced to `static/index.html` and root `index.html`).
