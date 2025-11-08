# TikTok Video Downloader

A full-featured Python tool to download all videos from a **public TikTok profile**. 

**Features:**
- Automatically scrolls to load all videos.
- Downloads videos using `yt-dlp` without watermark if available.
- Organizes filenames by upload date and video ID.
- Resume support & ignores duplicate URLs.

**⚠️ Disclaimer:**
- Only use this tool for **content you own** or **public content you have permission to download**.
- Unauthorized download of private or copyrighted TikTok content may violate TikTok's Terms of Service or copyright law.

## Requirements
- Python 3.8+
- Google Chrome (headless mode)
- pip install -r requirements.txt

## Usage
```bash
python downloader.py "https://www.tiktok.com/@username" --scrolls 100 --pause 2 --output my_videos
