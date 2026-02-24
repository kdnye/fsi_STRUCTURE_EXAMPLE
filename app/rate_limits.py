"""Centralized, reusable rate-limit policies.

These limits can be used by blueprints that need tighter controls than the
application-wide defaults.
"""

# Global fallback limits configured in app factory (keep broad for general API use).
DEFAULT_DAILY_LIMIT = "200 per day"
DEFAULT_HOURLY_LIMIT = "50 per hour"

# Auth and credential-handling routes should be stricter than global defaults.
AUTH_LOGIN_PAGE_LIMIT = "30 per minute"
AUTH_LOGIN_SUBMIT_LIMIT = "5 per minute"
AUTH_LOGIN_SUBMIT_BURST_LIMIT = "2 per 10 second"
