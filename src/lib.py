from flask import render_template, session
from src.models import User


def render(template_name, **kwargs):
    return render_template(template_name, current_user=get_current_user(), **kwargs)


def get_current_user():
    email = session.get("email", None)
    password = session.get("password", None)
    user = User.find_one({"email": email, "password": password})
    return user
