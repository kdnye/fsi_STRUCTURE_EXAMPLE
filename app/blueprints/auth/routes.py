from flask import Blueprint, abort, g, redirect, render_template, request, session, url_for

from app import limiter
from app.blueprints.auth.guards import _load_current_user, require_employee_approval
from models import Role, User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.before_app_request
def attach_current_user():
    g.current_user = _load_current_user()


@auth_bp.get("/login")
def login_page():
    return render_template("auth/login.html")


@auth_bp.post("/login")
@limiter.limit("10 per minute")
def login_submit():
    email = request.form.get("email", "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(401)

    session["current_user_id"] = user.id
    return redirect(url_for("auth.post_login"))


@auth_bp.get("/pending-approval")
def pending_approval():
    return render_template("auth/pending_approval.html"), 403


@auth_bp.get("/post-login")
@require_employee_approval(redirect_endpoint="auth.pending_approval")
def post_login():
    return {"message": "Welcome to the employee portal."}


@auth_bp.get("/internal/dashboard")
@require_employee_approval(redirect_endpoint="auth.pending_approval")
def internal_dashboard():
    return {"dashboard": "internal-tools"}


@auth_bp.get("/gate/<role>")
@require_employee_approval()
def gate(role: str):
    allowed_roles = {item.value for item in Role}
    if role.upper() not in allowed_roles:
        abort(403)
    return {"role": role.upper(), "allowed": True}
