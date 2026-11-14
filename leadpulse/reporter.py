"""
LeadPulse AI — Weekly PDF Report Generator and Scheduler.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

import jinja2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .config import settings
from .database import Lead, LeadStatus, MetricsCache, Project, Tenant

logger = logging.getLogger("leadpulse.reporter")

# ────────────────────────────────────────────────────────
#  Jinja2 Template Setup
# ────────────────────────────────────────────────────────

_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(_TEMPLATES_DIR)),
    autoescape=jinja2.select_autoescape(["html", "xml"]),
)


# ────────────────────────────────────────────────────────
#  Executive Summary Builder
# ────────────────────────────────────────────────────────

def _build_executive_summary(
    total_leads: int,
    qualified_count: int,
    disqualified_count: int,
    qualification_rate: float,
    avg_score: float,
    company_name: str,
    project_name: str,
) -> list[str]:
    """Generate 3 analytical paragraphs for the executive summary."""
    # Paragraph 1: What went well
    if total_leads == 0:
        p1 = (
            f"During this reporting period, the {project_name} campaign was active for {company_name}. "
            "No new inbound leads were recorded during this specific window. "
            "Ongoing ad delivery and webhook integrations remain ready to capture incoming prospects."
        )
    elif qualification_rate >= 30.0:
        p1 = (
            f"Strong qualification performance was recorded this week for {project_name}. "
            f"Out of {total_leads} total prospects engaged by LeadPulse AI, {qualified_count} successfully "
            f"passed all criteria—achieving an above-average qualification rate of {qualification_rate}%. "
            f"Qualified leads exhibited high engagement with an average qualification score of {avg_score}/100."
        )
    else:
        p1 = (
            f"Lead acquisition remained active for {project_name} with {total_leads} incoming prospects. "
            f"Our AI qualification assistant screened all conversations and identified {qualified_count} verified "
            f"high-intent leads (qualification rate: {qualification_rate}%). "
            f"Average prospect score across all interactions stood at {avg_score}/100."
        )

    # Paragraph 2: Areas of concern / Observations
    if total_leads == 0:
        p2 = (
            "We recommend verifying that Meta Ad campaigns are actively delivering impressions and that "
            "the Click-to-WhatsApp (CTWA) destination URLs and instant forms are properly connected."
        )
    elif disqualified_count > (total_leads * 0.6):
        p2 = (
            f"A notable portion of incoming leads ({disqualified_count} out of {total_leads}) were disqualified. "
            "Primary disqualification factors typically include budget mismatches, out-of-service locations, "
            "or non-responsive contacts. Reviewing Meta ad targeting parameters and exclusion filters can help "
            "filter out low-intent traffic before the click."
        )
    else:
        p2 = (
            f"Lead screening maintained consistent quality with {disqualified_count} low-fit prospects filtered out. "
            "The AI agent successfully handled objections, gathered key requirements, and prevented sales team "
            "bandwidth from being spent on unqualified inquiries."
        )

    # Paragraph 3: Recommendations
    p3 = (
        "Recommendations for the upcoming week: (1) Ensure prompt sales follow-up on all qualified leads "
        "within 2 hours to maximize appointment conversion. (2) Review any custom qualification criteria "
        "in your project settings to align with recent product or pricing updates. (3) Continue monitoring "
        "cost-per-qualified-lead to allocate ad spend towards top-performing creative sets."
    )

    return [p1, p2, p3]


# ────────────────────────────────────────────────────────
#  Report Generator
# ────────────────────────────────────────────────────────

async def generate_weekly_report(
    db: AsyncSession,
    tenant: Tenant,
    project: Project,
    week_start: date | datetime,
    week_end: date | datetime,
) -> bytes:
    """Generate a weekly PDF report for a given tenant and project.

    Steps:
      a. Query leads table for the date range, grouped by status
      b. Query metrics_cache for daily spend/CPL data
      c. Calculate totals, rates, and scores
      d. Build a 3-paragraph executive summary
      e. Render the Jinja2 HTML template
      f. Convert HTML to PDF via WeasyPrint
      g. Return the PDF bytes
    """
    # Normalize dates to datetime boundaries
    if isinstance(week_start, datetime):
        start_dt = week_start
        start_date = week_start.date()
    else:
        start_dt = datetime.combine(week_start, time.min, tzinfo=timezone.utc)
        start_date = week_start

    if isinstance(week_end, datetime):
        end_dt = week_end
        end_date = week_end.date()
    else:
        end_dt = datetime.combine(week_end, time.max, tzinfo=timezone.utc)
        end_date = week_end

    # a. Query leads in date range
    leads_stmt = (
        select(Lead)
        .where(
            Lead.tenant_id == tenant.id,
            Lead.project_id == project.id,
            Lead.created_at >= start_dt,
            Lead.created_at <= end_dt,
        )
        .order_by(Lead.created_at.desc())
    )
    leads_res = await db.execute(leads_stmt)
    leads = leads_res.scalars().all()

    # b. Query metrics cache
    metrics_stmt = (
        select(MetricsCache)
        .where(
            MetricsCache.tenant_id == tenant.id,
            MetricsCache.project_id == project.id,
            MetricsCache.date >= start_date,
            MetricsCache.date <= end_date,
        )
        .order_by(MetricsCache.date.asc())
    )
    metrics_res = await db.execute(metrics_stmt)
    spend_data = metrics_res.scalars().all()

    # c. Calculate metrics
    total_leads = len(leads)
    qualified_leads = [
        l for l in leads
        if l.status in (LeadStatus.qualified, LeadStatus.appointment_booked)
    ]
    disqualified_leads = [
        l for l in leads
        if l.status == LeadStatus.disqualified
    ]

    qualified_count = len(qualified_leads)
    disqualified_count = len(disqualified_leads)
    qualification_rate = (
        round((qualified_count / total_leads) * 100, 1) if total_leads > 0 else 0.0
    )
    avg_score = (
        round(sum(l.lead_score for l in leads) / total_leads, 1) if total_leads > 0 else 0.0
    )

    # d. Build executive summary
    executive_summary = _build_executive_summary(
        total_leads=total_leads,
        qualified_count=qualified_count,
        disqualified_count=disqualified_count,
        qualification_rate=qualification_rate,
        avg_score=avg_score,
        company_name=tenant.company_name,
        project_name=project.name,
    )

    # e. Render HTML template
    template = _jinja_env.get_template("report.html")
    html_content = template.render(
        company_name=tenant.company_name,
        project_name=project.name,
        week_start=start_date.strftime("%d %b %Y"),
        week_end=end_date.strftime("%d %b %Y"),
        generated_at=datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC"),
        total_leads=total_leads,
        qualified_count=qualified_count,
        qualification_rate=qualification_rate,
        avg_lead_score=avg_score,
        qualified_leads=qualified_leads,
        executive_summary=executive_summary,
        spend_data=spend_data,
    )

    # f. Convert HTML to PDF using WeasyPrint
    try:
        from weasyprint import HTML
        pdf_bytes = HTML(string=html_content).write_pdf()
        return pdf_bytes
    except Exception as exc:
        logger.warning(
            "WeasyPrint rendering unavailable or failed (%s). Falling back to HTML document.",
            exc,
        )
        return html_content.encode("utf-8")


# ────────────────────────────────────────────────────────
#  Report Dispatcher (Resend API)
# ────────────────────────────────────────────────────────

async def send_weekly_report(
    db: AsyncSession,
    tenant: Tenant,
    project: Project,
    week_start: date | None = None,
    week_end: date | None = None,
) -> bool:
    """Generate and email the weekly PDF report to tenant's owner_email."""
    # Default to past 7 complete days (Monday-Sunday or last 7 days)
    today = datetime.now(timezone.utc).date()
    if week_end is None:
        week_end = today - timedelta(days=1)
    if week_start is None:
        week_start = week_end - timedelta(days=6)

    try:
        # a. Generate PDF
        pdf_bytes = await generate_weekly_report(
            db=db,
            tenant=tenant,
            project=project,
            week_start=week_start,
            week_end=week_end,
        )

        # b. Send via Resend API
        filename = f"LeadPulse_Report_{project.name.replace(' ', '_')}_{week_start.strftime('%Y%m%d')}.pdf"
        recipient = tenant.owner_email

        if settings.RESEND_API_KEY:
            try:
                import resend
                resend.api_key = settings.RESEND_API_KEY

                params: dict[str, Any] = {
                    "from": "LeadPulse AI <reports@leadpulse.ai>",
                    "to": [recipient],
                    "subject": f"Weekly Lead Qualification Report — {project.name}",
                    "html": (
                        f"<p>Hello,</p>"
                        f"<p>Attached is your weekly lead qualification report for <strong>{project.name}</strong> "
                        f"covering the period from {week_start.strftime('%d %b %Y')} to {week_end.strftime('%d %b %Y')}.</p>"
                        f"<p>Best regards,<br>The LeadPulse AI Team</p>"
                    ),
                    "attachments": [
                        {
                            "filename": filename,
                            "content": list(pdf_bytes),
                        }
                    ],
                }
                # Run synchronous resend call in executor
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(None, lambda: resend.Emails.send(params))
                logger.info("Weekly report sent via Resend to %s for project %s", recipient, project.name)
            except Exception as resend_err:
                logger.error("Failed to send email via Resend API: %s", resend_err)
                return False
        else:
            logger.info(
                "[MOCK EMAIL] RESEND_API_KEY not configured. Would send %d bytes to %s for project %s",
                len(pdf_bytes),
                recipient,
                project.name,
            )

        # c. Log delivery
        logger.info(
            "Weekly report delivery completed successfully: tenant=%s, project=%s, email=%s",
            tenant.company_name,
            project.name,
            recipient,
        )
        return True

    except Exception as exc:
        logger.error("Error generating/sending weekly report: %s", exc, exc_info=True)
        return False


# ────────────────────────────────────────────────────────
#  APScheduler Integration
# ────────────────────────────────────────────────────────

def schedule_weekly_reports(scheduler: Any, db_session_factory: Any) -> None:
    """Register an APScheduler job that runs every Monday at 08:00 AM IST (02:30 UTC).

    Iterates through all active tenants and their active projects, generating and
    dispatching the weekly report.
    """
    async def _process_all_weekly_reports() -> None:
        logger.info("Starting scheduled weekly report generation...")
        async with db_session_factory() as session:
            try:
                stmt = (
                    select(Tenant)
                    .where(Tenant.is_active == True)
                    .options(selectinload(Tenant.projects))
                )
                result = await session.execute(stmt)
                tenants = result.scalars().all()

                for tenant in tenants:
                    for project in tenant.projects:
                        if project.is_active:
                            logger.info(
                                "Dispatching weekly report for tenant '%s', project '%s'",
                                tenant.company_name,
                                project.name,
                            )
                            await send_weekly_report(
                                db=session,
                                tenant=tenant,
                                project=project,
                            )
            except Exception as exc:
                logger.error("Scheduled weekly report run failed: %s", exc, exc_info=True)

    def _sync_wrapper() -> None:
        """Helper to run async process inside threaded schedulers."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(_process_all_weekly_reports())
            else:
                loop.run_until_complete(_process_all_weekly_reports())
        except RuntimeError:
            asyncio.run(_process_all_weekly_reports())

    # Schedule: Monday at 08:00 AM IST = 02:30 UTC
    scheduler.add_job(
        _sync_wrapper,
        trigger="cron",
        day_of_week="mon",
        hour=2,
        minute=30,
        timezone="UTC",
        id="weekly_reports_job",
        replace_existing=True,
        name="LeadPulse AI Weekly Report Generator",
    )
    logger.info("Weekly report job scheduled for every Monday at 02:30 UTC (08:00 AM IST)")
