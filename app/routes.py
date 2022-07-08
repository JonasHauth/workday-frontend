"""Route declaration."""
from app import app
from flask import render_template


@app.route("/")
def home():
    """Landing page route."""
    nav = [
        {"name": "Home", "url": "https://example.com/1"},
        {"name": "About", "url": "https://example.com/2"},
        {"name": "Pics", "url": "https://example.com/3"},
    ]
    return render_template(
        "home.html",
        nav=nav,
        title="workday",
        description="Organisiere deinen Arbeitstag mit Workday.",
    )