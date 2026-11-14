"""
LeadPulse AI — Meta Ads & Social Media Autonomous Manager
Autonomous campaign creation, real-time performance monitoring,
and self-driving AI optimization rules (Kill Switch, Auto-Scale, CTR fatigue).
"""

from .optimizer import evaluate_campaign_performance, AIAutoPilotRule
from .meta_client import MetaAdsManager

__all__ = ["MetaAdsManager", "evaluate_campaign_performance", "AIAutoPilotRule"]
