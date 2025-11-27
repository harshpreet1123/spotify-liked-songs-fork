# Spotify Playlist Manager

A powerful Spotify playlist management tool with a beautiful web interface. Copy liked songs, fork public playlists, and manage all your playlists in one place!

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

The app will open in your browser automatically. Enter your API credentials in the sidebar, connect to Spotify, and choose from three powerful features:

1. **Liked Songs** - Copy your liked songs to a new playlist
2. **Copy from Playlist** - Fork any public playlist by URL
3. **My Playlists** - View and manage all your playlists

## Features

### 📥 Liked Songs Manager
- 🎨 Beautiful Spotify-themed UI
- 🖼️ Album artwork for every song
- ✅ Select/deselect individual songs
- �  Select all / Deselect all buttons
- 📊 Real-time selection counter
- 🎵 Full song details (artist, album, duration)

### 🔗 Playlist Forking
- Copy songs from any public Spotify playlist
- Just paste the playlist URL
- Select which songs to copy
- Create your own version

### 📋 Playlist Management
- View all your playlists
- See track counts and privacy settings
- Quick links to open in Spotify
- Easy playlist overview

### ✨ General Features
- 📝 Custom playlist names and descriptions
- 🚀 Handles large libraries (batched requests)
- 🔗 Direct links to open playlists in Spotify
- 💾 Auto-login from cache
- 🔄 Easy account switching

## Notes

- Spotify requires API credentials (free to create)
- First run will open a browser for Spotify authorization
- All liked songs are fetched regardless of library size
- All songs are selected by default - uncheck the ones you don't want
