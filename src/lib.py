import hashlib

from flask import render_template, session

from src.models import User

try:
    import src.local_config as config
except ImportError:
    import src.config as config


def render(template_name, **kwargs):
    return render_template(template_name, current_user=get_current_user(), **kwargs)


def get_current_user():
    email = session.get("email", None)
    password = session.get("password", None)
    user = User.find_one({"email": email, "password": password})
    return user


def hash_password(raw_data):
    m = hashlib.md5()
    m.update((config.SALT + raw_data).encode("utf-8"))
    return m.hexdigest()


def generate_confirm_code(email):
    return hash_password(email)[:10]
