from app import create_app, limiter
from app.rate_limits import (
    AUTH_LOGIN_PAGE_LIMIT,
    AUTH_LOGIN_SUBMIT_BURST_LIMIT,
    AUTH_LOGIN_SUBMIT_LIMIT,
)


def _decorated_key(view_func) -> str:
    return f"{view_func.__module__}.{view_func.__qualname__}.{view_func.__name__}"


def _endpoint_limits(app, endpoint: str) -> set[str]:
    view_func = app.view_functions[endpoint]
    key = _decorated_key(view_func)
    route_limits = limiter.limit_manager._decorated_limits.get(key)
    assert route_limits is not None, f"No decorated limits found for endpoint: {endpoint}"
    return {item.limit_provider for item in route_limits}


def test_login_page_has_route_level_limit():
    app = create_app({"TESTING": True})

    limits = _endpoint_limits(app, "auth.login_page")

    assert AUTH_LOGIN_PAGE_LIMIT in limits


def test_login_submit_has_minute_and_burst_limits():
    app = create_app({"TESTING": True})

    limits = _endpoint_limits(app, "auth.login_submit")

    assert AUTH_LOGIN_SUBMIT_LIMIT in limits
    assert AUTH_LOGIN_SUBMIT_BURST_LIMIT in limits
