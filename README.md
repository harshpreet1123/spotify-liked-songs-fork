# Spotify Liked Songs to Playlist

Copy all your Spotify liked songs to a new playlist with a web interface.

## Quick Start

**Option 1: Automated Setup (Recommended)**

Windows:
```cmd
setup_and_run.bat
```

Mac/Linux:
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

**Option 2: Manual Setup**

Windows:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

**Quick Run (after setup):**
- Windows: `run.bat`
- Mac/Linux: `./run.sh`

## Spotify API Setup

1. Go to https://developer.spotify.com/dashboard
2. Log in and create a new app
3. Copy your Client ID and Client Secret
4. Add `http://localhost:8888/callback` to Redirect URIs in app settings
5. Enter credentials in the web app sidebar
6. Follow the manual authentication flow (copy/paste the redirect URL)

## Usage

The app will open in your browser automatically. Enter your API credentials in the sidebar, connect to Spotify, and follow the on-screen instructions to copy your liked songs to a new playlist.

## Features

- Web interface with real-time progress tracking
- Preview your liked songs before creating playlist
- Custom playlist name and description
- Handles large libraries (batched requests)
- Direct link to open playlist in Spotify

## Notes

- First run will open a browser for Spotify authorization
- All liked songs are fetched regardless of library size
