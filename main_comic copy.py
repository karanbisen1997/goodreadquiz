#!/usr/bin/env python3
import multiprocessing
import os
import re
import time
from os.path import exists
from pathlib import Path
from typing import Any, Tuple
from urllib.parse import urlparse

from moviepy.audio.AudioClip import CompositeAudioClip, concatenate_audioclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import TextClip, vfx
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from playwright.sync_api import ViewportSize, sync_playwright
from rich.console import Console
from moviepy.video.compositing.transitions import slide_in, slide_out

from utils import settings
from utils.cleanup import cleanup
from utils.console import print_step, print_substep
from utils.videos import save_data

# do not remove the above line


storymode = False
console = Console()
W, H = 1280, 720

def name_normalize(name: str) -> str:
    name = re.sub(r'[?\\"%*:|<>]', "", name)
    name = re.sub(r"( [w,W]\s?\/\s?[o,O,0])", r" without", name)
    name = re.sub(r"( [w,W]\s?\/)", r" with", name)
    name = re.sub(r"(\d+)\s?\/\s?(\d+)", r"\1 of \2", name)
    name = re.sub(r"(\w+)\s?\/\s?(\w+)", r"\1 or \2", name)
    name = re.sub(r"\/", r"", name)

def download_screenshots_of_reddit_posts():
    """Downloads screenshots of reddit posts as seen on the web. Downloads to assets/temp/png

    Args:
        reddit_object (Dict): Reddit object received from reddit/subreddit.py
        screenshot_num (int): Number of screenshots to download
    """
    print_step("Downloading screenshots of reddit posts...")

    # ! Make sure the reddit screenshots folder exists
    Path("assets/temp/png1").mkdir(parents=True, exist_ok=True)
    file_folder_name='youtube_comics'
    Path(file_folder_name).mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print_substep("Launching Headless Browser...")

        browser = p.firefox.launch(headless=True)
        context = browser.new_context()

        # if settings.config["settings"]["theme"] == "dark":
        #     cookie_file = open("./video_creation/data/cookie-dark-mode.json", encoding="utf-8")
        # else:
        #     cookie_file = open("./video_creation/data/cookie-light-mode.json", encoding="utf-8")
        # cookies = json.load(cookie_file)
        # context.add_cookies(cookies)  # load preference cookies

        # Get the thread screenshot
        page = context.new_page()
        
        url=input("Enter Page url  :  ")
        if len(url)>10:
            url=url
        else:
            exit()

        parse=urlparse(url)
        filderno = f"{(re.sub('[^A-Za-z0-9]+', '_', parse.path))}"
        # print(filderno)
        # exit()
        
        # print(last_line)
        # exit()
        print(url)
        # url="https://lakshyaeducation.in/topic/tally/16305448225876caacbdd21/"
        # exit()
        # page.set_viewport_size(ViewportSize(width=400, height=529))
        page.goto(url, timeout=0)
        print(page)
        
        comment={}
        # title= ["You know     ", "Someone says    ", "Here we go    ","people says   ","Do enjoy    "]
        comment['filderno']=f"{file_folder_name}/{filderno}"
        comment['thread_title']="Do enjoy    "
        comment["thread_id"] = comment['thread_title']
        comment["thread_post"] = comment['thread_title']
        
        # multi=page.query_selector_all("(//div[@class='text-left']//p)")
        multi=page.query_selector_all("[class='page-break no-gaps']")
        time.sleep(2.4)
        print(len(multi))
        # exit()
        if  len(multi)!=0:
            count=0
            for i in range(0, len(multi)-1):
                page.locator(f"(//div[@class='page-break no-gaps'])[{count+2}]").screenshot(path=f"assets/temp/png1/comment_{count}.png")
                # page.locator(f"(//div[@class='quoteText'])[{idx+1}]").screenshot(path=f"assets/temp/png/comment_{count}.png")
                print(count)
                count=count+1
                time.sleep(1.4)

            comment["count"] = count
            # exit(que)
            print_substep("Screenshots downloaded Successfully.", style="bold green")
            return comment
        else:
            return 0

comment=download_screenshots_of_reddit_posts()
if comment:
    folderNo=comment['filderno']
    number_of_clips=comment['count']
    VideoFileClip.reW = lambda clip: clip.resize(width=W)
    VideoFileClip.reH = lambda clip: clip.resize(width=H)
    opacity = 0.9
    title = re.sub(r"[^\w\s-]", "", comment["thread_post"])
    new_opacity = 1 if opacity is None or float(opacity) >= 1 else float(opacity)
    filename = f"{name_normalize(re.sub('[^A-Za-z0-9]+', '_', title))}.mp4"
    subreddit = "comics"
    Path(f"results/{subreddit}/{folderNo}").mkdir(parents=True, exist_ok=True)
    audiocount=1
    print(number_of_clips)
    for i in range(0, number_of_clips):
        # from moviepy.editor import *
        # Import the audio(Insert to location of your audio instead of audioClip.mp3)
        if audiocount>11:
            audiocount=1

        audio = AudioFileClip(f"audio/{audiocount}.mp3").set_duration(15)
        audiocount=audiocount+1
        # audio = AudioFileClip(f"assets/temp/mp3/{i}.mp3")
        # audio = audio.subclip(start_time, end_time)
        # Import the Image and set its duration same as the audio (Insert the location of your photo instead of photo.jpg) clip.fx(transfx.slide_in, 1, "left")
        
        # clip = ImageClip(f"assets/temp/png1/comment_{i}.png").set_duration(audio.duration).resize(width=W).set_opacity(new_opacity).fx(vfx.fadein,1).fx(vfx.fadeout,1).set_position('center')

        clip = ImageClip(f"assets/temp/png1/comment_{i}.png").set_duration(audio.duration).resize(width=W).set_opacity(new_opacity).set_position('center')
        
        new_clip = CompositeVideoClip([slide_in(clip, 10, "bottom")])
        # Set the audio of the clip
        clip = new_clip.set_audio(audio)
        # Export the clip
        print(f"results/{subreddit}/{i}_{filename}")
        clip.write_videofile(f"results/{subreddit}/{folderNo}/{i}_{filename}", fps=40,audio_codec="aac",audio_bitrate="192k",verbose=False,threads=multiprocessing.cpu_count(),)
        time.sleep(2.4)

print_step("Removing temporary files 🗑")
# cleanups = cleanup()
# print_substep(f"Removed {cleanups} temporary files 🗑")
print_substep("See result in the results folder!")

# https://wuxiaworld.site/novel/the-beautiful-wife-of-the-whirlwind-marriage-comics-wuxia-dao-novel/chapter-1/