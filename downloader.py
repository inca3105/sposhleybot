import yt_dlp
import os

YDL_COMMON_OPTS = {
    "quiet": True,
    "noplaylist": True,
    "cookiefile": "cookies.txt",
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    },
}

def search_youtube(query, max_results=5):
    try:
        opts = YDL_COMMON_OPTS.copy()
        opts["skip_download"] = True
        with yt_dlp.YoutubeDL(opts) as ydl:
            results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
            return [
                {
                    "title": entry["title"],
                    "url": entry["webpage_url"],
                    "duration": entry.get("duration", 0)
                }
                for entry in results["entries"]
            ]
    except Exception as e:
        return []

def download_by_url(url, output_folder="downloads"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, "%(title).50s.%(ext)s")
    opts = YDL_COMMON_OPTS.copy()
    opts["outtmpl"] = output_path
    opts["postprocessors"] = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ]

    with yt_dlp.YoutubeDL(opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")
        except Exception as e:
            return f"Ошибка: {e}"