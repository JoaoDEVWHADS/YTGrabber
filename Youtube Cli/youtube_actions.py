import os
import yt_dlp
import ytmusicapi
import shutil
import re
from config import (
    MPV_REL_PATH,
    FFPROBE_REL_PATH,
    FFMPEG_REL_PATH,
    DOWNLOADS_DIR,
    CHANNELS_DIR,
    ALBUNS_DIR,
    PLAYLISTS_DIR,
    COOKIES_FILE,
    DEFAULT_DOWNLOAD_LIMIT,
    YOUTUBE_SEARCH_PREFIX,
    YOUTUBE_MUSIC_SEARCH_PREFIX
)

def check_cookies_file():
    return os.path.exists(COOKIES_FILE)

def create_dirs():
    dirs = [
        DOWNLOADS_DIR,
        CHANNELS_DIR,
        ALBUNS_DIR,
        PLAYLISTS_DIR
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

def get_yt_dlp_options(audio_only=False, cookies_path=None):
    options = {
        'format': 'bestaudio/best' if audio_only else 'best',
        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'ignoreerrors': True,
        'no_warnings': True,
    }
    if cookies_path:
        options['cookiefile'] = cookies_path
    return options

def search_youtube(query, music_search=False):
    create_dirs()
    search_prefix = YOUTUBE_MUSIC_SEARCH_PREFIX if music_search else YOUTUBE_SEARCH_PREFIX
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
    }
    
    if not os.path.exists(COOKIES_FILE):
        ydl_opts.pop('cookiefile', None)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            search_query = f"{search_prefix}{query}"
            results = ydl.extract_info(search_query, download=False)['entries'] or []
            
            formatted_results = []
            for entry in results[:10]:
                if entry:
                    formatted = {
                        'title': entry.get('title', 'Título desconhecido'),
                        'uploader': entry.get('uploader', 'Canal desconhecido'),
                        'url': entry.get('url'),
                        'webpage_url': entry.get('webpage_url'),
                        'duration': entry.get('duration'),
                        'view_count': entry.get('view_count')
                    }
                    formatted_results.append(formatted)
            
            return formatted_results
            
        except Exception as e:
            print(f"Erro na busca: {str(e)}")
            return []

def play_video(url):
    if not os.path.exists(MPV_REL_PATH):
        print("MPV não encontrado!")
        return
    
    try:
        cmd = [MPV_REL_PATH, url]
        import subprocess
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"Erro ao reproduzir: {str(e)}")

def download_as_mp3(url, title):
    create_dirs()
    
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    output_path = os.path.join(DOWNLOADS_DIR, f"{safe_title}.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
        'noplaylist': True,
    }
    
    if not os.path.exists(COOKIES_FILE):
        ydl_opts.pop('cookiefile', None)
    
    if not os.path.exists(FFMPEG_REL_PATH):
        print("FFmpeg não encontrado!")
        return
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download concluído!")
    except Exception as e:
        print(f"Erro no download: {str(e)}")

def setup_ytmusic():
    try:
        if os.path.exists(COOKIES_FILE):
            ytmusic = ytmusicapi.YTMusic('oauth.json')
            return ytmusic
        else:
            print("cookies.txt não encontrado para YTMusic")
            return None
    except Exception as e:
        print(f"Erro ao configurar YTMusic: {str(e)}")
        return None

def download_playlist(ytmusic, playlist_id, playlist_title):
    try:
        playlist = ytmusic.get_playlist(playlist_id, limit=DEFAULT_DOWNLOAD_LIMIT)
        tracks = playlist['tracks']
        
        safe_title = re.sub(r'[<>:"/\\|?*]', '', playlist_title)
        playlist_dir = os.path.join(PLAYLISTS_DIR, safe_title)
        os.makedirs(playlist_dir, exist_ok=True)
        
        downloaded_count = 0
        
        for i, track in enumerate(tracks):
            if not track or 'videoDetails' not in track:
                continue
                
            video_id = track['videoDetails']['videoId']
            title = track['videoDetails']['title']
            safe_track_title = re.sub(r'[<>:"/\\|?*]', '', title)
            track_path = os.path.join(playlist_dir, f"{safe_track_title}.%(ext)s")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': track_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://music.youtube.com/watch?v={video_id}"])
                downloaded_count += 1
                print(f"Download {downloaded_count}: {title}")
                
            except Exception as e:
                print(f"Erro ao baixar {title}: {str(e)}")
                continue
        
        return downloaded_count
        
    except Exception as e:
        print(f"Erro ao processar playlist: {str(e)}")
        return 0

def download_channel_videos(url, channel_name):
    create_dirs()
    
    safe_channel_name = re.sub(r'[<>:"/\\|?*]', '', channel_name)
    channel_dir = os.path.join(CHANNELS_DIR, safe_channel_name)
    os.makedirs(channel_dir, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(channel_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'playlistend': DEFAULT_DOWNLOAD_LIMIT,
        'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
    }
    
    if not os.path.exists(COOKIES_FILE):
        ydl_opts.pop('cookiefile', None)
    
    downloaded_count = 0
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info and 'entries' in info:
                total_videos = len([e for e in info['entries'] if e])
                print(f"Baixando {total_videos} vídeos do canal...")
                
                ydl.download([url])
                downloaded_count = len(os.listdir(channel_dir)) if os.path.exists(channel_dir) else 0
                
    except Exception as e:
        print(f"Erro ao baixar canal: {str(e)}")
    
    return downloaded_count

def download_album(ytmusic, album_id, album_title):
    try:
        album = ytmusic.get_album(album_id)
        tracks = album['tracks']
        
        safe_title = re.sub(r'[<>:"/\\|?*]', '', album_title)
        album_dir = os.path.join(ALBUNS_DIR, safe_title)
        os.makedirs(album_dir, exist_ok=True)
        
        downloaded_count = 0
        
        for i, track in enumerate(tracks):
            if not track or 'videoDetails' not in track:
                continue
                
            video_id = track['videoDetails']['videoId']
            title = track['videoDetails']['title']
            safe_track_title = re.sub(r'[<>:"/\\|?*]', '', title)
            track_path = os.path.join(album_dir, f"{safe_track_title}.%(ext)s")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': track_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://music.youtube.com/watch?v={video_id}"])
                downloaded_count += 1
                print(f"Download {downloaded_count}: {title}")
                
            except Exception as e:
                print(f"Erro ao baixar {title}: {str(e)}")
                continue
        
        return downloaded_count
        
    except Exception as e:
        print(f"Erro ao processar álbum: {str(e)}")
        return 0

def extract_type_from_url(url):
    patterns = {
        'video': r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|music\.youtube\.com/watch\?v=)([a-zA-Z0-9_-]{11})',
        'playlist': r'(?:youtube\.com/playlist\?list=|music\.youtube\.com/playlist\?list=)([a-zA-Z0-9_-]+)',
        'channel': r'(?:youtube\.com/(?:c|channel)/|youtube\.com/user/|music\.youtube\.com/channel/)([a-zA-Z0-9_-]+)',
        'album': r'(?:music\.youtube\.com/(?:browse|channel)/(?:MPREB|UC)[a-zA-Z0-9_-]{22})',
    }
    
    for link_type, pattern in patterns.items():
        match = re.search(pattern, url)
        if match:
            return link_type, match.group(1)
    
    return 'unknown', None

def download_by_link(url):
    create_dirs()
    
    link_type, identifier = extract_type_from_url(url)
    
    if link_type == 'unknown':
        print("Tipo de link não reconhecido!")
        return None
    
    if link_type == 'video':
        try:
            title = "Vídeo Individual"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
            }
            
            if not os.path.exists(COOKIES_FILE):
                ydl_opts.pop('cookiefile', None)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            return 'video', DOWNLOADS_DIR, 1
            
        except Exception as e:
            print(f"Erro ao baixar vídeo: {str(e)}")
            return None
    
    elif link_type == 'playlist':
        ytmusic = setup_ytmusic()
        if ytmusic:
            try:
                playlist = ytmusic.get_playlist(identifier, limit=1)
                playlist_title = playlist.get('title', 'Playlist Desconhecida')
                count = download_playlist(ytmusic, identifier, playlist_title)
                
                if count > 0:
                    return 'playlist', PLAYLISTS_DIR, count
                else:
                    return None
            except Exception as e:
                print(f"Erro ao baixar playlist: {str(e)}")
                return None
        else:
            print("YTMusic não configurado para playlists!")
            return None
    
    elif link_type == 'channel':
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
            }
            
            if not os.path.exists(COOKIES_FILE):
                ydl_opts.pop('cookiefile', None)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                channel_name = info.get('title', 'Canal Desconhecido') if info else 'Canal Desconhecido'
            
            count = download_channel_videos(url, channel_name)
            
            if count > 0:
                return 'channel', CHANNELS_DIR, count
            else:
                return None
                
        except Exception as e:
            print(f"Erro ao baixar canal: {str(e)}")
            return None
    
    elif link_type == 'album':
        ytmusic = setup_ytmusic()
        if ytmusic:
            try:
                album = ytmusic.get_album(identifier)
                album_title = album.get('title', 'Álbum Desconhecido')
                count = download_album(ytmusic, identifier, album_title)
                
                if count > 0:
                    return 'album', ALBUNS_DIR, count
                else:
                    return None
            except Exception as e:
                print(f"Erro ao baixar álbum: {str(e)}")
                return None
        else:
            print("YTMusic não configurado para álbuns!")
            return None
    
    return None
