"""Initialize Flask Application."""
from flask import Flask
from flask import render_template, url_for, request

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=['GET', 'POST'])
def home():
    """Landing page route."""

    events = [
        {"name": "Uni", "startdate": "2022-07-20", "enddate": "2022-07-20"},
        {"name": "Uni2", "startdate": "2022-07-19", "enddate": "2022-07-20"},
        {"name": "Uni3", "startdate": "2022-07-20", "enddate": "2022-07-20"},
        {"name": "Uni4", "startdate": "2022-07-19", "enddate": "2022-07-19"},
        {"name": "Uni5", "startdate": "2022-07-14", "enddate": "2022-07-14"},
    ]

    return render_template(
        "home.html",
        events=events,
        title="workday",
        description="Organisiere deinen Arbeitstag mit Workday.",
    )

@app.route("/calendar", methods=['GET', 'POST'])
def calendar():
    """Landing page route."""

    events = [
        {"title": "Uni", "start": "2022-07-20", "end": "2022-07-20"},
        {"title": "Uni2", "start": "2022-07-19", "end": "2022-07-20"},
        {"title": "Uni3", "start": "2022-07-20", "end": "2022-07-20"},
        {"title": "Uni4", "start": "2022-07-19", "end": "2022-07-19"},
        {"title": "Uni5", "start": "2022-07-14", "end": "2022-07-14"},
    ]

    return render_template(
        "calendar.html",
        events=events,
        title="workday",
        description="Organisiere deinen Arbeitstag mit Workday.",
    )

if __name__ == "__main__":
    app.run()