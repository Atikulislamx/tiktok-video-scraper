import os
import time
import argparse
from yt_dlp import YoutubeDL
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def collect_video_urls(profile_url, scroll_times=50, scroll_pause=2):
    """Collect all video URLs from a public TikTok profile."""
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(profile_url)
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    urls = set()

    for _ in range(scroll_times):
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        
        # Collect video URLs
        videos = driver.find_elements("css selector", "a[href*='/video/']")
        for v in videos:
            urls.add(v.get_attribute("href"))

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    return list(urls)

def download_videos(urls, output_folder):
    """Download videos via yt-dlp with organized filenames."""
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(upload_date)s_%(id)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'ignoreerrors': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

def main():
    parser = argparse.ArgumentParser(description="TikTok Video Downloader (No Watermark if available)")
    parser.add_argument('profile', type=str, help="TikTok profile URL (public profile)")
    parser.add_argument('--scrolls', type=int, default=50, help="Number of scrolls to load videos")
    parser.add_argument('--pause', type=int, default=2, help="Seconds to wait between scrolls")
    parser.add_argument('--output', type=str, default='tiktok_backup', help="Output folder for videos")
    args = parser.parse_args()

    print(f"[INFO] Collecting video URLs from: {args.profile}")
    urls = collect_video_urls(args.profile, args.scrolls, args.pause)
    print(f"[INFO] Found {len(urls)} videos.")
    
    if urls:
        print("[INFO] Downloading videos...")
        download_videos(urls, args.output)
        print(f"[INFO] Download complete. Videos saved in '{args.output}'")
    else:
        print("[WARN] No videos found. Make sure the profile is public and valid.")

if __name__ == "__main__":
    main()
