import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Page config
st.set_page_config(
    page_title="Spotify Liked Songs to Playlist",
    page_icon="🎵",
    layout="wide"
)

# Spotify color theme
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #121212;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #000000;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #000000;
    }
    
    /* Primary Button styling */
    .stButton > button[kind="primary"] {
        background-color: #1DB954 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 10px 24px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1ed760 !important;
        transform: scale(1.02) !important;
    }
    
    /* Secondary Button styling */
    .stButton > button[kind="secondary"] {
        background-color: #282828 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: 1px solid #535353 !important;
        padding: 10px 24px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #3e3e3e !important;
        border-color: #b3b3b3 !important;
    }
    
    /* Default Button styling */
    .stButton > button {
        background-color: #282828 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        border: 1px solid #535353 !important;
        padding: 10px 24px !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }
    .stButton > button:hover {
        background-color: #3e3e3e !important;
        border-color: #b3b3b3 !important;
    }
    
    /* Text input - complete unified styling */
    .stTextInput > div {
        background-color: transparent !important;
        gap: 0 !important;
    }
    
    /* Input wrapper - make it seamless */
    .stTextInput > div > div {
        background-color: transparent !important;
        border-radius: 4px !important;
        border: none !important;
        display: flex !important;
        align-items: center !important;
        overflow: hidden !important;
    }
    
    /* Text input field */
    .stTextInput input {
        background-color: transparent !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
        flex: 1 !important;
    }
    .stTextInput input:focus {
        outline: none !important;
    }
    
    /* Password eye icon button - blend seamlessly */
    .stTextInput button {
        background-color: transparent !important;
        border: none !important;
        margin: 0 !important;
        height: 100% !important;
        border-radius: 0 !important;
    }
    .stTextInput button:hover {
        color: #ffffff !important;
    }
    .stTextInput button:focus {
        box-shadow: none !important;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
    }
    .stTextArea textarea:focus {
        outline: none !important;
    }
    
    /* Labels */
    .stTextInput label, .stTextArea label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 8px !important;
    }
    
    /* Typography */
    h1 {
        color: #ffffff !important;
        font-weight: 900 !important;
    }
    h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    p, div, span, label, li {
        color: #b3b3b3 !important;
    }
    
    /* Links */
    a {
        color: #1DB954 !important;
        text-decoration: none !important;
    }
    a:hover {
        color: #1ed760 !important;
        text-decoration: underline !important;
    }
    
    /* Alert boxes */
    .stSuccess {
        background-color: rgba(29, 185, 84, 0.15) !important;
        border-left: 4px solid #1DB954 !important;
        color: #ffffff !important;
    }
    .stInfo {
        background-color: rgba(30, 215, 96, 0.1) !important;
        border-left: 4px solid #1DB954 !important;
        color: #ffffff !important;
    }
    .stWarning {
        background-color: rgba(255, 152, 0, 0.15) !important;
        border-left: 4px solid #ff9800 !important;
        color: #ffffff !important;
    }
    .stError {
        background-color: rgba(244, 67, 54, 0.15) !important;
        border-left: 4px solid #f44336 !important;
        color: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #181818 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: #282828 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #1DB954 !important;
    }
    
    /* Divider */
    hr {
        border-color: #282828 !important;
    }
    
    /* Code blocks */
    code {
        background-color: #282828 !important;
        color: #1DB954 !important;
        padding: 3px 8px !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'sp' not in st.session_state:
    st.session_state.sp = None
if 'liked_songs' not in st.session_state:
    st.session_state.liked_songs = []
if 'selected_songs' not in st.session_state:
    st.session_state.selected_songs = set()
if 'checkbox_key' not in st.session_state:
    st.session_state.checkbox_key = 0
if 'bulk_operation' not in st.session_state:
    st.session_state.bulk_operation = False
if 'playlist_songs' not in st.session_state:
    st.session_state.playlist_songs = []
if 'selected_playlist_songs' not in st.session_state:
    st.session_state.selected_playlist_songs = set()
if 'user_playlists' not in st.session_state:
    st.session_state.user_playlists = []
if 'cached_token' not in st.session_state:
    st.session_state.cached_token = None
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'show_auth_flow' not in st.session_state:
    st.session_state.show_auth_flow = False
if 'auth_url' not in st.session_state:
    st.session_state.auth_url = None
if 'auth_manager' not in st.session_state:
    st.session_state.auth_manager = None
if 'auto_login_attempted' not in st.session_state:
    st.session_state.auto_login_attempted = False

# Auto-login from session cache (not file-based for security)
if not st.session_state.authenticated and not st.session_state.auto_login_attempted:
    # Check if we have cached credentials in session state
    if 'cached_token' in st.session_state and st.session_state.cached_token:
        try:
            # Try to use cached token
            sp = spotipy.Spotify(auth=st.session_state.cached_token)
            # Test if it works
            user = sp.current_user()
            
            # Success! Set authenticated
            st.session_state.sp = sp
            st.session_state.authenticated = True
        except:
            # Token expired or invalid, clear it
            st.session_state.cached_token = None
    
    st.session_state.auto_login_attempted = True

def get_spotify_client(client_id, client_secret, redirect_uri):
    """Create and return Spotify client"""
    try:
        scope = 'user-library-read playlist-modify-public playlist-modify-private'
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=".spotify_cache",
            open_browser=False,
            show_dialog=True
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        # Test authentication
        sp.current_user()
        return sp
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def fetch_liked_songs(sp, progress_bar, status_text):
    """Fetch all liked songs with full details"""
    liked_songs = []
    offset = 0
    limit = 50
    
    # Get total first
    initial = sp.current_user_saved_tracks(limit=1)
    total = initial['total']
    status_text.text(f"Found {total} liked songs. Fetching...")
    
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not results['items']:
            break
        
        for item in results['items']:
            track = item['track']
            # Get album image (smallest available)
            image_url = track['album']['images'][-1]['url'] if track['album']['images'] else None
            
            # Convert duration from ms to mm:ss
            duration_ms = track['duration_ms']
            minutes = duration_ms // 60000
            seconds = (duration_ms % 60000) // 1000
            duration_str = f"{minutes}:{seconds:02d}"
            
            liked_songs.append({
                'uri': track['uri'],
                'id': track['id'],
                'name': track['name'],
                'artist': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'image': image_url,
                'duration': duration_str,
                'duration_ms': duration_ms
            })
        
        offset += limit
        progress = min(offset / total, 1.0)
        progress_bar.progress(progress)
        
        if len(results['items']) < limit:
            break
    
    return liked_songs

def create_playlist_with_tracks(sp, name, description, track_uris, progress_bar, status_text):
    """Create playlist and add tracks"""
    user_id = sp.current_user()['id']
    
    status_text.text("Creating playlist...")
    playlist = sp.user_playlist_create(
        user=user_id,
        name=name,
        public=True,
        description=description
    )
    playlist_id = playlist['id']
    
    status_text.text(f"Adding {len(track_uris)} tracks...")
    batch_size = 100
    
    for i in range(0, len(track_uris), batch_size):
        batch = track_uris[i:i + batch_size]
        sp.playlist_add_items(playlist_id, batch)
        progress = (i + len(batch)) / len(track_uris)
        progress_bar.progress(progress)
    
    return playlist_id, playlist['external_urls']['spotify']

def fetch_playlist_from_url(sp, playlist_url):
    """Fetch playlist tracks from URL"""
    try:
        # Extract playlist ID from URL
        if 'playlist/' in playlist_url:
            playlist_id = playlist_url.split('playlist/')[1].split('?')[0]
        else:
            playlist_id = playlist_url
        
        # Get playlist details
        playlist = sp.playlist(playlist_id)
        
        # Fetch all tracks
        tracks = []
        results = playlist['tracks']
        
        while results:
            for item in results['items']:
                if item['track']:
                    track = item['track']
                    image_url = track['album']['images'][-1]['url'] if track['album']['images'] else None
                    duration_ms = track['duration_ms']
                    minutes = duration_ms // 60000
                    seconds = (duration_ms % 60000) // 1000
                    duration_str = f"{minutes}:{seconds:02d}"
                    
                    tracks.append({
                        'uri': track['uri'],
                        'id': track['id'],
                        'name': track['name'],
                        'artist': ', '.join([artist['name'] for artist in track['artists']]),
                        'album': track['album']['name'],
                        'image': image_url,
                        'duration': duration_str,
                        'duration_ms': duration_ms
                    })
            
            results = sp.next(results) if results['next'] else None
        
        return playlist['name'], tracks
    except Exception as e:
        raise Exception(f"Failed to fetch playlist: {str(e)}")

def get_user_playlists(sp):
    """Get all user playlists"""
    playlists = []
    results = sp.current_user_playlists(limit=50)
    
    while results:
        for playlist in results['items']:
            playlists.append({
                'id': playlist['id'],
                'name': playlist['name'],
                'tracks_total': playlist['tracks']['total'],
                'public': playlist['public'],
                'url': playlist['external_urls']['spotify'],
                'image': playlist['images'][0]['url'] if playlist['images'] else None
            })
        results = sp.next(results) if results['next'] else None
    
    return playlists

# UI
st.title("🎵 Spotify Playlist Manager")
st.markdown("✨ Manage your Spotify playlists with ease")

# Sidebar for credentials
with st.sidebar:
    st.header("🔧 Spotify API Setup")
    
    # Show logged in user if authenticated
    if st.session_state.authenticated and st.session_state.sp:
        try:
            user = st.session_state.sp.current_user()
            st.success(f"✅ Logged in as **{user['display_name']}**")
        except:
            pass
    
    with st.expander("📖 Setup Instructions", expanded=False):
        st.markdown("""
        **Step 1:** Go to [Spotify Dashboard](https://developer.spotify.com/dashboard)
        
        **Step 2:** Create an app
        
        **Step 3:** Add this to Redirect URIs:
        ```
        http://localhost:8888/callback
        ```
        
        **Step 4:** Copy your credentials below
        """)
    
    # Only show credentials input if not authenticated
    if not st.session_state.authenticated:
        client_id = st.text_input("🔑 Client ID", type="password", value=os.getenv('SPOTIPY_CLIENT_ID', ''))
        client_secret = st.text_input("🔐 Client Secret", type="password", value=os.getenv('SPOTIPY_CLIENT_SECRET', ''))
        redirect_uri = st.text_input("🔗 Redirect URI", value="http://localhost:8888/callback")
    else:
        # If already authenticated, use dummy values
        client_id = ""
        client_secret = ""
        redirect_uri = ""
    
    # Initial connect button
    if not st.session_state.show_auth_flow and not st.session_state.authenticated:
        if st.button("🎵 Connect to Spotify", use_container_width=True, type="primary"):
            if client_id and client_secret and redirect_uri:
                try:
                    # Clear old cache to force fresh authentication
                    if os.path.exists(".spotify_cache"):
                        os.remove(".spotify_cache")
                    
                    scope = 'user-library-read playlist-modify-public playlist-modify-private'
                    auth_manager = SpotifyOAuth(
                        client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope,
                        cache_path=".spotify_cache",
                        open_browser=False
                    )
                    
                    # Get auth URL
                    auth_url = auth_manager.get_authorize_url()
                    st.session_state.auth_url = auth_url
                    st.session_state.auth_manager = auth_manager
                    st.session_state.show_auth_flow = True
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all fields")
    
    # Auth flow section
    if st.session_state.show_auth_flow and not st.session_state.authenticated:
        st.divider()
        st.markdown("### 🔐 Authentication Steps")
        
        st.markdown("**Step 1:** Click the link below to authorize")
        st.markdown(f"[🎵 Authorize on Spotify]({st.session_state.auth_url})")
        
        st.markdown("**Step 2:** After authorizing, copy the **full URL** from your browser")
        
        st.markdown("**Step 3:** Paste it here:")
        redirect_response = st.text_input("📋 Paste redirect URL:", key="redirect_url", label_visibility="collapsed")
        
        if st.button("✅ Complete Authentication", use_container_width=True, type="primary"):
            if redirect_response:
                try:
                    code = st.session_state.auth_manager.parse_response_code(redirect_response)
                    token = st.session_state.auth_manager.get_access_token(code, as_dict=False)
                    sp = spotipy.Spotify(auth=token)
                    sp.current_user()  # Test
                    
                    # Store token in session state (NOT in file for security)
                    st.session_state.sp = sp
                    st.session_state.cached_token = token
                    st.session_state.authenticated = True
                    st.session_state.show_auth_flow = False
                    
                    # Delete any file-based cache for security
                    if os.path.exists(".spotify_cache"):
                        os.remove(".spotify_cache")
                    
                    st.success("✅ Connected!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed: {str(e)}")
            else:
                st.warning("⚠️ Please paste the redirect URL")
    
    # Logout button if authenticated
    if st.session_state.authenticated:
        st.divider()
        if st.button("🚪 Logout / Switch Account", use_container_width=True, type="secondary"):
            # Clear cache file (if any exists)
            if os.path.exists(".spotify_cache"):
                os.remove(".spotify_cache")
            
            # Reset ALL session state
            st.session_state.sp = None
            st.session_state.cached_token = None
            st.session_state.authenticated = False
            st.session_state.show_auth_flow = False
            st.session_state.liked_songs = []
            st.session_state.selected_songs = set()
            st.session_state.playlist_songs = []
            st.session_state.selected_playlist_songs = set()
            st.session_state.user_playlists = []
            st.session_state.auth_url = None
            st.session_state.auth_manager = None
            st.session_state.checkbox_key = 0
            st.session_state.auto_login_attempted = False
            
            st.success("✅ Logged out! You can now connect with a different account.")
            st.rerun()

# Main content
if st.session_state.authenticated and st.session_state.sp:
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs(["📥 Liked Songs", "🔗 Copy from Playlist", "📋 My Playlists"])
    
    # TAB 1: Liked Songs
    with tab1:
        # Fetch liked songs
        if not st.session_state.liked_songs:
            st.markdown("### 📥 Step 1: Fetch Your Liked Songs")
            if st.button("🎵 Fetch My Liked Songs", use_container_width=True, type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    liked_songs = fetch_liked_songs(
                        st.session_state.sp,
                        progress_bar,
                        status_text
                    )
                    st.session_state.liked_songs = liked_songs
                    status_text.text(f"✅ Fetched {len(liked_songs)} songs!")
                    progress_bar.empty()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error fetching songs: {str(e)}")
        
        # Show liked songs and create playlist
        if st.session_state.liked_songs:
            # Initialize selected songs if empty
            if not st.session_state.selected_songs:
                st.session_state.selected_songs = set(song['id'] for song in st.session_state.liked_songs)
            
            st.markdown(f"### 🎵 Select Songs ({len(st.session_state.selected_songs)}/{len(st.session_state.liked_songs):,} selected)")
            
            # Select/Deselect all buttons
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✅ Select All", use_container_width=True, key="select_all_btn"):
                    st.session_state.bulk_operation = True
                    st.session_state.selected_songs = set(song['id'] for song in st.session_state.liked_songs)
                    st.session_state.checkbox_key += 1
                    st.rerun()
            with col2:
                if st.button("❌ Deselect All", use_container_width=True, key="deselect_all_btn"):
                    st.session_state.bulk_operation = True
                    st.session_state.selected_songs = set()
                    st.session_state.checkbox_key += 1
                    st.rerun()
            
            st.divider()
            
            # Reset bulk operation flag after rerun
            if st.session_state.bulk_operation:
                st.session_state.bulk_operation = False
            
            # Display songs with checkboxes
            for i, song in enumerate(st.session_state.liked_songs):
                col1, col2, col3 = st.columns([0.5, 1, 4])
                
                with col1:
                    # Checkbox for selection
                    is_selected = song['id'] in st.session_state.selected_songs
                    
                    def toggle_song(song_id=song['id']):
                        # Don't toggle if this is a bulk operation
                        if not st.session_state.bulk_operation:
                            if song_id in st.session_state.selected_songs:
                                st.session_state.selected_songs.discard(song_id)
                            else:
                                st.session_state.selected_songs.add(song_id)
                    
                    st.checkbox("", value=is_selected, key=f"song_{song['id']}_{st.session_state.checkbox_key}", 
                               label_visibility="collapsed", on_change=toggle_song)
                
                with col2:
                    # Album image
                    if song['image']:
                        st.image(song['image'], width=60)
                    else:
                        st.markdown("🎵")
                
                with col3:
                    # Song details
                    st.markdown(f"**{song['name']}**")
                    st.markdown(f"*{song['artist']}* · {song['album']} · {song['duration']}")
                
                if i < len(st.session_state.liked_songs) - 1:
                    st.divider()
            
            st.divider()
            
            # Create playlist form
            st.markdown("### ✨ Create Your Playlist")
            
            playlist_name = st.text_input(
                "📝 Playlist Name",
                value="My Liked Songs",
                placeholder="Enter playlist name"
            )
            
            playlist_description = st.text_area(
                "📄 Description (optional)",
                value=f"Selected {len(st.session_state.selected_songs)} songs from my liked songs",
                placeholder="Enter description",
                height=80
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✨ Create Playlist", type="primary", use_container_width=True, disabled=len(st.session_state.selected_songs) == 0):
                    if playlist_name:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            # Get only selected songs
                            selected_tracks = [song for song in st.session_state.liked_songs if song['id'] in st.session_state.selected_songs]
                            track_uris = [song['uri'] for song in selected_tracks]
                            
                            playlist_id, playlist_url = create_playlist_with_tracks(
                                st.session_state.sp,
                                playlist_name,
                                playlist_description,
                                track_uris,
                                progress_bar,
                                status_text
                            )
                            
                            progress_bar.empty()
                            status_text.empty()
                            
                            st.balloons()
                            st.success(f"🎉 Created playlist with {len(track_uris):,} songs!")
                            st.markdown(f"### [🎵 Open in Spotify →]({playlist_url})")
                            
                            # Reset
                            if st.button("🔄 Create Another Playlist"):
                                st.session_state.liked_songs = []
                                st.session_state.selected_songs = set()
                                st.rerun()
                                
                        except Exception as e:
                            st.error(f"❌ Error creating playlist: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter a playlist name")
            
            with col2:
                if st.button("🔄 Fetch Again", use_container_width=True, type="secondary"):
                    st.session_state.liked_songs = []
                    st.session_state.selected_songs = set()
                    st.session_state.checkbox_key = 0
                    st.rerun()
    
    # TAB 2: Copy from Playlist
    with tab2:
        st.markdown("### 🔗 Copy Songs from Any Playlist")
        st.markdown("Enter a Spotify playlist URL to copy songs from it")
        
        playlist_url = st.text_input("📋 Playlist URL", placeholder="https://open.spotify.com/playlist/...")
        
        if st.button("🔍 Fetch Playlist", type="primary"):
            if playlist_url:
                try:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    status_text.text("Fetching playlist...")
                    
                    playlist_name, tracks = fetch_playlist_from_url(st.session_state.sp, playlist_url)
                    st.session_state.playlist_songs = tracks
                    st.session_state.selected_playlist_songs = set(song['id'] for song in tracks)
                    
                    progress_bar.empty()
                    status_text.empty()
                    st.success(f"✅ Fetched **{playlist_name}** with {len(tracks)} songs!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {str(e)}")
            else:
                st.warning("⚠️ Please enter a playlist URL")
        
        # Show fetched playlist songs
        if st.session_state.playlist_songs:
            st.markdown(f"### 🎵 Select Songs ({len(st.session_state.selected_playlist_songs)}/{len(st.session_state.playlist_songs)} selected)")
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✅ Select All", use_container_width=True, key="pl_select_all"):
                    st.session_state.selected_playlist_songs = set(song['id'] for song in st.session_state.playlist_songs)
                    st.rerun()
            with col2:
                if st.button("❌ Deselect All", use_container_width=True, key="pl_deselect_all"):
                    st.session_state.selected_playlist_songs = set()
                    st.rerun()
            
            st.divider()
            
            # Display songs
            for song in st.session_state.playlist_songs:
                col1, col2, col3 = st.columns([0.5, 1, 4])
                
                with col1:
                    is_selected = song['id'] in st.session_state.selected_playlist_songs
                    if st.checkbox("", value=is_selected, key=f"pl_song_{song['id']}", label_visibility="collapsed"):
                        st.session_state.selected_playlist_songs.add(song['id'])
                    else:
                        st.session_state.selected_playlist_songs.discard(song['id'])
                
                with col2:
                    if song['image']:
                        st.image(song['image'], width=60)
                    else:
                        st.markdown("🎵")
                
                with col3:
                    st.markdown(f"**{song['name']}**")
                    st.markdown(f"*{song['artist']}* · {song['album']} · {song['duration']}")
                
                st.divider()
            
            # Create playlist
            st.markdown("### ✨ Create New Playlist")
            new_playlist_name = st.text_input("📝 Playlist Name", value="Copied Playlist", key="pl_name")
            new_playlist_desc = st.text_area("📄 Description", value="Copied from another playlist", key="pl_desc")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("✨ Create Playlist", type="primary", use_container_width=True, key="pl_create", disabled=len(st.session_state.selected_playlist_songs) == 0):
                    if new_playlist_name:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            selected_tracks = [song for song in st.session_state.playlist_songs if song['id'] in st.session_state.selected_playlist_songs]
                            track_uris = [song['uri'] for song in selected_tracks]
                            
                            playlist_id, playlist_url = create_playlist_with_tracks(
                                st.session_state.sp,
                                new_playlist_name,
                                new_playlist_desc,
                                track_uris,
                                progress_bar,
                                status_text
                            )
                            
                            progress_bar.empty()
                            status_text.empty()
                            
                            st.balloons()
                            st.success(f"🎉 Created playlist with {len(track_uris)} songs!")
                            st.markdown(f"### [🎵 Open in Spotify →]({playlist_url})")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
            
            with col2:
                if st.button("🔄 Fetch Another", use_container_width=True, type="secondary", key="pl_reset"):
                    st.session_state.playlist_songs = []
                    st.session_state.selected_playlist_songs = set()
                    st.rerun()
    
    # TAB 3: My Playlists
    with tab3:
        st.markdown("### 📋 Manage Your Playlists")
        
        if st.button("🔄 Refresh Playlists", type="primary"):
            try:
                playlists = get_user_playlists(st.session_state.sp)
                st.session_state.user_playlists = playlists
                st.success(f"✅ Found {len(playlists)} playlists!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        if st.session_state.user_playlists:
            st.markdown(f"### Found {len(st.session_state.user_playlists)} playlists")
            
            for playlist in st.session_state.user_playlists:
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    if playlist['image']:
                        st.image(playlist['image'], width=100)
                    else:
                        st.markdown("🎵")
                
                with col2:
                    st.markdown(f"### {playlist['name']}")
                    st.markdown(f"**{playlist['tracks_total']} tracks** · {'Public' if playlist['public'] else 'Private'}")
                    st.markdown(f"[🎵 Open in Spotify]({playlist['url']})")
                
                st.divider()
        else:
            st.info("👆 Click 'Refresh Playlists' to load your playlists")

else:
    st.markdown("### 👋 Welcome!")
    st.info("👈 Enter your Spotify API credentials in the sidebar to get started")
    
    with st.expander("📖 How to get API credentials", expanded=True):
        st.markdown("""
        **1.** Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
        
        **2.** Log in with your Spotify account
        
        **3.** Click **"Create app"**
        
        **4.** Fill in:
        - App name: *anything you want*
        - App description: *anything you want*
        - Redirect URI: `http://localhost:8888/callback`
        
        **5.** Save and copy your **Client ID** and **Client Secret**
        
        **6.** Paste them in the sidebar and click **"Connect to Spotify"**
        """)
