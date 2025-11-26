# Spotify Liked Songs to Playlist

Copy your Spotify liked songs to a new playlist with a beautiful web interface. Select exactly which songs you want with album art, artist info, and duration!

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

- 🎨 Beautiful Spotify-themed UI
- 🖼️ Album artwork for every song
- ✅ Select/deselect individual songs
- 🔘 Select all / Deselect all buttons
- 📊 Real-time selection counter
- 🎵 Full song details (artist, album, duration)
- 📝 Custom playlist name and description
- 🚀 Handles large libraries (batched requests)
- 🔗 Direct link to open playlist in Spotify

## Notes

- Spotify requires API credentials (free to create)
- First run will open a browser for Spotify authorization
- After first login, you'll be automatically logged in on subsequent runs
- Use "Logout / Switch Account" button to change accounts
- All liked songs are fetched regardless of library size
- All songs are selected by default - uncheck the ones you don't want
