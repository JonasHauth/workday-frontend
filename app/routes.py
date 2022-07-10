"""Route declaration."""
from app import app
from flask import render_template, url_for, request


@app.route("/", methods=['GET', 'POST'])
def home():
    """Landing page route."""
    nav = [
        {"name": "Dein Tag", "url": "https://example.com/1", "iconName": "home"},
        {"name": "Kalender", "url": "https://example.com/2", "iconName": "calendar_month"},
        {"name": "Spaces", "url": "https://example.com/4", "iconName": "search"},
        {"name": "Buchungen", "url": "https://example.com/5", "iconName": "inventory"},
        {"name": "Profil", "url": "https://example.com/6", "iconName": "account_circle"},
    ]
    return render_template(
        "home.html",
        nav=nav,
        title="workday",
        description="Organisiere deinen Arbeitstag mit Workday.",
    )