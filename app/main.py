print("main.py loaded")

from flask import Blueprint, render_template, request, redirect, session, url_for
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.recommendation import get_recommendations
import time

bp = Blueprint('main', __name__)

print("Blueprint created")

print("Starting application...")

load_dotenv()
print("Environment variables loaded.")

# Remove this line
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read user-top-read"
)
print("SpotifyOAuth object created.")

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login')
def login():
    clear_spotipy_cache()
    print("Login route accessed")
    session.clear()  # Clear any existing session data
    try:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Generated auth URL: {auth_url}")
        return redirect(auth_url)
    except Exception as e:
        print(f"Error in login route: {str(e)}")
        return f"Error during login: {str(e)}", 400

@bp.route('/callback')
def callback():
    print("Callback received")
    code = request.args.get('code')
    print(f"Code: {code}")
    try:
        token_info = sp_oauth.get_access_token(code, check_cache=False)
        print(f"Token info: {token_info}")
        session.clear()  # Clear any existing session data
        session["token_info"] = token_info
        return redirect('/recommendations')
    except Exception as e:
        print(f"Error in callback: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error args: {e.args}")
        return f"Error: {str(e)}<br>Type: {type(e).__name__}<br>Args: {e.args}", 400

@bp.route('/recommendations')
def recommendations():
    if "token_info" not in session:
        print("No token info in session, redirecting to login")
        return redirect('/login')
    
    print(f"Token info in session: {session['token_info']}")
    
    # Always refresh the token
    token_info = sp_oauth.refresh_access_token(session['token_info']['refresh_token'])
    session['token_info'] = token_info
    print("Token refreshed")

    sp = spotipy.Spotify(auth=session['token_info']['access_token'])
    print_current_user_info(sp)
    
    print("Fetching top tracks...")
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')['items']
    print(f"Number of top tracks fetched: {len(top_tracks)}")
    print(f"First top track: {top_tracks[0]['name']} by {top_tracks[0]['artists'][0]['name']}")
    
    print("Getting recommendations...")
    recommended_tracks = get_recommendations(sp, top_tracks)
    print(f"Number of recommended tracks: {len(recommended_tracks)}")
    
    return render_template('recommendations.html', top_tracks=top_tracks[:10], recommended_tracks=recommended_tracks)

@bp.route('/check_oauth')
def check_oauth():
    try:
        auth_url = sp_oauth.get_authorize_url()
        return f"OAuth object initialized successfully. Auth URL: {auth_url}"
    except Exception as e:
        return f"Error initializing OAuth object: {str(e)}"

@bp.route('/logout')
def logout():
    clear_spotipy_cache()
    print("Logging out...")
    session.clear()
    return redirect(url_for('index'))

def print_current_user_info(sp):
    try:
        user_info = sp.current_user()
        print(f"Current user: {user_info['display_name']} (ID: {user_info['id']})")
    except Exception as e:
        print(f"Error getting current user info: {str(e)}")

def clear_spotipy_cache():
    cache_path = '.cache'
    if os.path.exists(cache_path):
        os.remove(cache_path)
        print("Spotipy cache cleared")

if __name__ == '__main__':
    print("Checking OAuth initialization...")
    try:
        auth_url = sp_oauth.get_authorize_url()
        print(f"OAuth object initialized successfully. Auth URL: {auth_url}")
    except Exception as e:
        print(f"Error initializing OAuth object: {str(e)}")
    
    print("Starting Flask app...")
    app.run(debug=True, port=5000)