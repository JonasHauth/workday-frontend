"""Initialize Flask Application."""
from csv import excel
from flask import Flask, jsonify
from flask import redirect, request, url_for, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauthlib.oauth2 import WebApplicationClient
import os
import requests
import datetime
from datetime import date
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


# Python standard libraries
import json
import os
import sqlite3

# Internal imports
from db import init_db_command
from user import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# To-Do: Make it go to User DB
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()












# ----------------------- Routes

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():

    """Landing page route."""
    
    spaces = [

        {"img": "img/Space1.jpg", 
        "name": "SteamWork", 
        "description": "Auf fast 3.000 qm Fläche erwartet euch geballte Innovationspower: Unternehmen und Gründende unterschiedlicher Branchen sowie vielfältige Veranstaltungen unter einem Dach. Kommt an Board – gemeinsam bringen wir die Next Work Culture nach Karlsruhe.", 
        "street": "Roonstraße 23 a",
        "city": "Karlsruhe",
        "price": "39 € pro Tag",
        "pay": "#"},

        {"img": "img/Space2.jpg", 
        "name": "Karlsruhe Park Arkaden", 
        "description": "A modern low-rise building set in a superbly landscaped and laid out office park is the location for the Karlsruhe City business centre.", 
        "street": "Ludwig-Erhard-Allee Nr. 10",
        "city": "Karlsruhe",
        "price": "249 € pro Monat",
        "pay": "#"},

        {"img": "img/Space3.jpg", 
        "name": "Regus", 
        "description": "Auf fast 5.000 qm Fläche erwartet euch geballte Innovationspower: Unternehmen und Gründende unterschiedlicher Branchen sowie vielfältige Veranstaltungen unter einem Dach. Kommt an Board – gemeinsam bringen wir die Next Work Culture nach Karlsruhe.", 
        "street": "Waldhornstraße 49",
        "city": "Karlsruhe",
        "price": "39 € pro Tag",
        "pay": "#"},

        
    ]



    events_for_display = []

    if current_user.is_authenticated:

        credentials = Credentials(
                token=client.access_token,
                token_uri="https://www.googleapis.com/oauth2/v3/token", 
                client_id=os.environ['GOOGLE_CLIENT_ID'],
                client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
            )

        try:
            
            dictToSend = {
                'token': client.access_token,
                'token_uri': "https://www.googleapis.com/oauth2/v3/token",
                'client_id': os.environ['GOOGLE_CLIENT_ID'],
                'client_secret': os.environ['GOOGLE_CLIENT_SECRET']
            }

            # Sync google calendars
            res = requests.post('http://127.0.0.1:8080/sync/google', json=dictToSend)
            print("Sync calendar request " + str(res.status_code))

            # Get all entries
            res = requests.get('http://127.0.0.1:8080/calendar')
            print("Get calendar request " + str(res.status_code))
            events_for_display = res.json()

        except HttpError as error:
            print('An error occurred: %s' % error)


        return render_template(
            "home.html",
            events=events_for_display,
            spaces=spaces,
            title="workday",
            description="Organisiere deinen Arbeitstag mit Workday.",
        )

    else:
        return redirect(url_for("login"))


    

@app.route("/calendar", methods=['GET', 'POST'])
def calendar():
    """Landing page route."""

    events_for_display = []

    if current_user.is_authenticated:

        credentials = Credentials(
                token=client.access_token,
                token_uri="https://www.googleapis.com/oauth2/v3/token", 
                client_id=os.environ['GOOGLE_CLIENT_ID'],
                client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
            )

        try:
            
            dictToSend = {
                'token': client.access_token,
                'token_uri': "https://www.googleapis.com/oauth2/v3/token",
                'client_id': os.environ['GOOGLE_CLIENT_ID'],
                'client_secret': os.environ['GOOGLE_CLIENT_SECRET']
            }

            # Sync google calendars
            res = requests.post('http://127.0.0.1:8080/sync/google', json=dictToSend)


            # Get all entries
            res = requests.get('http://127.0.0.1:8080/calendar')

            events_for_display_change = res.json()

            for event in events_for_display_change:
                id = event['_id']
                print(id)
                summary = event['summary']
                start = event['start']
                end = event['end']
                
                event_dict = {
                    "id": id,
                    "title": summary,
                    "start": start,
                    "end": end
                }
                events_for_display.append(event_dict)
                
                print(event_dict)


        except HttpError as error:
            print('An error occurred: %s' % error)

        return render_template(
            "calendar.html",
            login=current_user.is_authenticated,
            events=events_for_display,
            title="workday",
            description="Organisiere deinen Arbeitstag mit Workday.",
        )

    else:
        return redirect(url_for("login"))






# Space buchen und in den Kalender eintragen
@app.route("/calendar/insertspace/",methods=["POST","GET"])
def insertspaceincalender():

    if request.method == 'GET':

        print("test")
        
        try:
            summary = "SteamWork"
            start = "2022-07-20T08:00:00+02:00"
            dtobj = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            dtstart = dtobj.isoformat()

            end = "2022-07-20T17:00:00+02:00"
            dtobj = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            dtend = dtobj.isoformat()

            
        except:
            print("Converting failed") 

        dictToSend = {
            'token': client.access_token,
            'token_uri': "https://www.googleapis.com/oauth2/v3/token",
            'client_id': os.environ['GOOGLE_CLIENT_ID'],
            'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
            'summary': summary,
            'start': dtstart,
            'end': dtend,
        }


        # Sync google calendars
        res = requests.post('http://127.0.0.1:8080/calendar', json=dictToSend)

        events_for_display = []

        try:
            # Get all entries
            res = requests.get('http://127.0.0.1:8080/calendar')

            events_for_display_change = res.json()

            for event in events_for_display_change:
                id = event['_id']
                summary = event['summary']
                start = event['start']
                end = event['end']
                
                event_dict = {
                    "id": id,
                    "title": summary,
                    "start": start,
                    "end": end
                }
                events_for_display.append(event_dict)
                
                print(event_dict)


        except HttpError as error:
            print('An error occurred: %s' % error)

        return render_template(
            "calendar.html",
            login=current_user.is_authenticated,
            events=events_for_display,
            title="workday",
            description="Organisiere deinen Arbeitstag mit Workday.",
        )








# Kalendereintrag hinzufügen
"""
Kalendereintrag hinzufügen
"""
@app.route("/calendar/insert",methods=["POST","GET"])
def insert():

    if request.method == 'POST':
        
        try:
            summary = request.form['title']

            start = request.form['start']
            if len(start) > 12:
                dtobj = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                dtstart = dtobj.isoformat()

            else:
                start = start + "T00:00:00+02:00"
                dtobj = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                dtstart = dtobj.isoformat()

            end = request.form['end']
            if len(end) > 12:
           
                dtobj = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                dtend = dtobj.isoformat()

            else: 
                end = end + "T00:00:00+02:00"
                dtobj = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                dtend = dtobj.isoformat()

        except:
            print("Converting failed") 

        dictToSend = {
            'token': client.access_token,
            'token_uri': "https://www.googleapis.com/oauth2/v3/token",
            'client_id': os.environ['GOOGLE_CLIENT_ID'],
            'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
            'summary': summary,
            'start': dtstart,
            'end': dtend,
        }

        res = requests.post('http://127.0.0.1:8080/calendar', json=dictToSend)

        events_for_display = []

        try:
            # Get all entries
            res = requests.get('http://127.0.0.1:8080/calendar')

            events_for_display_change = res.json()

            for event in events_for_display_change:
                id = event['_id']
                summary = event['summary']
                start = event['start']
                end = event['end']
                
                event_dict = {
                    "id": id,
                    "title": summary,
                    "start": start,
                    "end": end
                }
                events_for_display.append(event_dict)
                
                print(event_dict)


        except HttpError as error:
            print('An error occurred: %s' % error)

        return render_template(
            "calendar.html",
            login=current_user.is_authenticated,
            events=events_for_display,
            title="workday",
            description="Organisiere deinen Arbeitstag mit Workday.",
        )
    


"""
Kalendereintrag editieren
"""
@app.route("/calendar/update",methods=["PUT","GET"])
def update():
    if request.method == 'PUT':       
        try:
            summary = request.form['title']
            id = request.form['id']

            start = request.form['start']
            if len(start) > 12:
                dtobj = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                dtstart = dtobj.isoformat()

            else:
                start = start + "T00:00:00+02:00"
                dtobj = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                dtstart = dtobj.isoformat()

            end = request.form['end']
            if len(end) > 12:
           
                dtobj = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                dtend = dtobj.isoformat()

            else: 
                end = end + "T00:00:00+02:00"
                dtobj = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                dtend = dtobj.isoformat()

        except:
            print("Converting failed") 

        dictToSend = {
            'token': client.access_token,
            'token_uri': "https://www.googleapis.com/oauth2/v3/token",
            'client_id': os.environ['GOOGLE_CLIENT_ID'],
            'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
            'id': id,
            'summary': summary,
            'start': dtstart,
            'end': dtend,
        }

        res = requests.put('http://127.0.0.1:8080/calendar', json=dictToSend)

        


    return jsonify("Success")

"""
Kalendereintrag löschen
"""
@app.route("/calendar/delete",methods=["POST","DELETE"])
def ajax_delete():


    if request.method == 'DELETE':
        try:            
            id = request.form['id']
            print(id)
        except:
            print("Converting failed") 

        dictToSend = {
            'token': client.access_token,
            'token_uri': "https://www.googleapis.com/oauth2/v3/token",
            'client_id': os.environ['GOOGLE_CLIENT_ID'],
            'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
            'id': id
        }

        res = requests.delete('http://127.0.0.1:8080/calendar', json=dictToSend)


    return jsonify("Success")



"""
Profil anzeigen
"""
@app.route("/profil")
def profil():
    if current_user.is_authenticated:
        return render_template(
            "successfullogin.html",
            title="workday",
            description="Organisiere deinen Arbeitstag mit Workday.",
        )
        
    else:
        return render_template(
            "login.html",
            title="workday",
            description="Organisiere deinen Arbeitstag mit Workday.",
        )

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile", 'https://www.googleapis.com/auth/calendar'],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    
    credentials = Credentials(
            token=client.access_token,
            token_uri="https://www.googleapis.com/oauth2/v3/token", 
            client_id=os.environ['GOOGLE_CLIENT_ID'],
            client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
        )


    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("profil"))




if __name__ == "__main__":
    app.run(ssl_context="adhoc", host="0.0.0.0") #  