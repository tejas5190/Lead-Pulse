"""
LeadPulse AI — AI Ad Optimization Engine & Rule Evaluator.
Implements autonomous rules:
1. Kill Switch: Auto-pause underperforming ads exceeding target CPL.
2. Scale Winner: Auto-boost daily budget on high-efficiency campaigns.
3. Creative Fatigue: Detect decaying CTR and advise creative rotation.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import enum


class AIAutoPilotRule(str, enum.Enum):
    KILL_SWITCH = "kill_switch"
    SCALE_WINNER = "scale_winner"
    CREATIVE_FATIGUE = "creative_fatigue"
    HEALTHY = "healthy"


def evaluate_campaign_performance(
    spend: float,
    impressions: int,
    clicks: int,
    leads: int,
    target_cpl: float,
    daily_budget: float,
    status: str
) -> Dict[str, Any]:
    """
    Evaluates campaign metrics and returns automated recommendations/actions.
    """
    ctr = round((clicks / impressions * 100), 2) if impressions > 0 else 0.0
    cpl = round((spend / leads), 2) if leads > 0 else 0.0

    action = "NONE"
    rule_applied = AIAutoPilotRule.HEALTHY
    new_budget = daily_budget
    new_status = status
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Rule 1: Zero Lead Burn Kill Switch
    if spend >= 350.0 and leads == 0 and status == "ACTIVE":
        action = "PAUSE_CAMPAIGN"
        new_status = "PAUSED"
        rule_applied = AIAutoPilotRule.KILL_SWITCH
        message = (
            f"🛑 Kill Switch Triggered: ₹{spend:.2f} spent with 0 leads acquired. "
            f"Campaign automatically paused to protect advertising capital."
        )

    # Rule 2: High CPL Over-Tolerance Kill Switch
    elif spend >= 450.0 and leads > 0 and cpl > (target_cpl * 1.4) and status == "ACTIVE":
        action = "PAUSE_CAMPAIGN"
        new_status = "PAUSED"
        rule_applied = AIAutoPilotRule.KILL_SWITCH
        message = (
            f"🛑 High CPL Kill Switch: Current CPL of ₹{cpl:.2f} is 40%+ above your target of ₹{target_cpl:.2f}. "
            f"Auto-paused to stop bleeding budget."
        )

    # Rule 3: Scaling Winner
    elif leads >= 4 and cpl <= (target_cpl * 0.75) and status == "ACTIVE":
        action = "SCALE_BUDGET"
        new_budget = round(daily_budget * 1.20, 2)
        rule_applied = AIAutoPilotRule.SCALE_WINNER
        message = (
            f"🚀 Auto-Scale Winner: CPL is exceptional at ₹{cpl:.2f} (25%+ cheaper than ₹{target_cpl:.2f} target) "
            f"with {leads} qualified leads. Daily budget automatically scaled +20% (₹{daily_budget:.2f} ➔ ₹{new_budget:.2f})."
        )

    # Rule 4: Creative Fatigue / Low CTR Warning
    elif impressions >= 800 and ctr < 0.85:
        action = "CREATIVE_REFRESH_ADVISED"
        rule_applied = AIAutoPilotRule.CREATIVE_FATIGUE
        message = (
            f"⚠️ Creative Fatigue Detected: CTR is {ctr:.2f}% (Benchmark is >1.2%). "
            f"Audience has seen this creative too often. Rotate in a new photo flyer or 9:16 Reels video."
        )

    else:
        message = (
            f"✅ Campaign Healthy: Running efficiently at ₹{cpl:.2f} CPL and {ctr:.2f}% CTR "
            f"within target tolerance (₹{target_cpl:.2f})."
        )

    return {
        "action": action,
        "rule_applied": rule_applied.value,
        "new_status": new_status,
        "new_budget": new_budget,
        "ctr": ctr,
        "cpl": cpl,
        "log_entry": {
            "timestamp": timestamp,
            "rule": rule_applied.value,
            "message": message,
            "action": action
        }
    }
