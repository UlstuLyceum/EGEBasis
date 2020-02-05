from flask import render_template, session


def render(template_name, **kwargs):
    return render_template(template_name, current_user=get_current_user(), **kwargs)


def get_current_user():
    email = session.get("email", None)
    password = session.get("password", None)
    return None  # TODO gettting user
