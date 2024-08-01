#!/usr/bin/env python3
import multiprocessing
import os
import re
import time
import random
from os.path import exists
from pathlib import Path
from typing import Any, Tuple
from urllib.parse import urlparse

from moviepy.audio.AudioClip import CompositeAudioClip, concatenate_audioclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import TextClip, vfx,transfx,afx
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
    Path("assets/temp/png2").mkdir(parents=True, exist_ok=True)
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
        
        # url=input("Enter Page url  :  ")
        url=""
        if len(url)>10:
            url=url
        else:
            f= open("youtube_comics/i-have-a-mansion-in-the-post-apocalyptic-world-comics-wuxia-dao-novel.txt", 'r')
            url = f.readlines()[-1]
            f.close()

        parse=urlparse(url)
        filderno = f"{(re.sub('[^A-Za-z0-9]+', '_', parse.path))}"
        filderno =  parse.path
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
       
        # multi=page.query_selector_all("(//div[@class='text-left']//p)")
        multi=page.query_selector_all("[class='page-break no-gaps']")
        time.sleep(10.4)
        print(len(multi))
        # exit()
        if  len(multi)!=0:
            count=0
            for i in range(0, len(multi)-1):
                page.locator(f"(//div[@class='page-break no-gaps'])[{count+1}]").screenshot(path=f"assets/temp/png2/comment_{count}.png")
                # page.locator(f"(//div[@class='quoteText'])[{idx+1}]").screenshot(path=f"assets/temp/png/comment_{count}.png")
                print(count)
                count=count+1
                time.sleep(2.4)

            comment["count"] = count
            # exit(que)
            print_substep("Screenshots downloaded Successfully.", style="bold green")
            return comment
        else:
            return 0
while 1:
    comment=download_screenshots_of_reddit_posts()
    if comment:
        folderNo=comment['filderno']
        x = folderNo.split("/")
        fileName=x[-1]
        fileName=fileName+"-"+x[-2]
        folderNo="/".join(x[:-1])
        number_of_clips=comment['count']
        VideoFileClip.reW = lambda clip: clip.resize(width=W)
        VideoFileClip.reH = lambda clip: clip.resize(width=H)
        opacity = 0.9
        new_opacity = 1 if opacity is None or float(opacity) >= 1 else float(opacity)
        subreddit = "comics"
        Path(f"results/{subreddit}/{folderNo}").mkdir(parents=True, exist_ok=True)
        print(number_of_clips)
        clips=[]
        for i in range(0, number_of_clips):
            EFFECT_DURATION = 8
            CLIP_DURATION = 20
            clips.append(ImageClip(f"assets/temp/png2/comment_{i}.png").set_duration(CLIP_DURATION).resize(height=H).set_opacity(new_opacity))

    start_clip_audio = AudioFileClip(f"assets/temp/audio/start{random.randint(1,4)}.mp3").fx(afx.volumex,0.1)
    start_clip = (
        VideoFileClip(f"assets/temp/start{random.randint(1,2)}.mp4")
        .without_audio()
        .resize(width=W,height=H)
        .set_duration(start_clip_audio.duration)
    )
    start_clip.audio=CompositeAudioClip([start_clip_audio])
    start_clip.write_videofile(
        f"results/start_clip.mp4",
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        fps=24,
        threads=24,
        ffmpeg_params=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p"],
    )
    
    start_clip = (
        VideoFileClip(f"results/start_clip.mp4")
    )

    end_clip_audio = AudioFileClip(f"assets/temp/audio/end{random.randint(1,3)}.mp3").fx(afx.volumex,0.1)
    end_clip = (
        VideoFileClip(f"assets/temp/end{random.randint(1,3)}.mp4")
        .without_audio()
        .resize(width=W,height=H)
        .set_duration(end_clip_audio.duration)
    )
    end_clip.audio=CompositeAudioClip([end_clip_audio])
    end_clip.write_videofile(
        f"results/end_clip.mp4",
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        fps=24,
        threads=24,
        ffmpeg_params=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p"],
    )
    end_clip = (
        VideoFileClip(f"results/end_clip.mp4")
    )
   
    first_clip = CompositeVideoClip(
        [clips[0].fx(transfx.slide_out, duration=EFFECT_DURATION, side="top")]
    ).set_start((CLIP_DURATION - EFFECT_DURATION) * 0)

    # For the last video we only need it to start entring the screen from the left going right
    # but not slide out at the end so the end clip exits on a full image not a partial image or black screen
    last_clip = CompositeVideoClip(
        [clips[-1].fx(transfx.slide_in, duration=EFFECT_DURATION, side="bottom")]
        # -1 because we start with index 0 so we go all the way up to array length - 1
    ).set_start((CLIP_DURATION - EFFECT_DURATION) * (len(clips) - 1))

    videos = (
        [first_clip]
        # For all other clips in the middle, we need them to slide in to the previous clip and out for the next one
        + [
            (
                CompositeVideoClip(
                    [clip.fx(transfx.slide_in, duration=EFFECT_DURATION, side="bottom")]
                )
                .set_start((CLIP_DURATION - EFFECT_DURATION) * idx)
                .fx(transfx.slide_out, duration=EFFECT_DURATION, side="top")
            )
                # set start to 1 since we start from second clip in the original array
            for idx, clip in enumerate(clips[1:-1], start=1)
        ]
        + [last_clip]
    )

    video = CompositeVideoClip(videos)
    audio = AudioFileClip(f"audio/{random.randint(2, 14)}.mp3").fx(afx.volumex,0.1)
    print(audio.duration)
    print(video.duration)
    if audio.duration<video.duration:
        audio1 = AudioFileClip(f"audio/{random.randint(2, 14)}.mp3")
        audio2 = AudioFileClip(f"audio/{random.randint(2, 14)}.mp3")
        if audio1.duration+audio2.duration<video.duration:
            audio3 = AudioFileClip(f"audio/{random.randint(2, 14)}.mp3")
            concat = concatenate_audioclips([audio1, audio2,audio3])
        else:
            concat = concatenate_audioclips([audio1, audio2])
        concat.write_audiofile(f"results/audio.mp3")
        audio = AudioFileClip(f"results/audio.mp3").fx(afx.volumex,0.1)
        print(audio.duration)
        print(video.duration)
        video.audio=CompositeAudioClip([audio])
    else:
        video.audio=CompositeAudioClip([audio])

    video.write_videofile(
        f"results/comic.mp4",
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        fps=24,
        threads=24,
        ffmpeg_params=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p"],
    )
    video = (
        VideoFileClip(f"results/comic.mp4")
    )
    video = concatenate_videoclips([start_clip,video,end_clip],method="compose")
    # state=1
    # while state==1:
    #     if audio.duration>video.duration:
    #         audio.set_duration(video.duration)
    #         video.audio=CompositeAudioClip([audio])
    #         state=2
    #     else:
    #         audio = AudioFileClip(f"audio/{random.randint(1, 19)}.mp3").fx(afx.volumex,0.1)
    # video.duration
    # print(video.duration)
    # exit()
    video.write_videofile(
        f"results/{subreddit}/{folderNo}/{fileName}.mp4",
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast",
        fps=24,
        threads=24,
        ffmpeg_params=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p"],
    )


    # exit()
    #remove last line from a text line in python
    fd=open("youtube_comics/i-have-a-mansion-in-the-post-apocalyptic-world-comics-wuxia-dao-novel.txt","r")
    d=fd.read()
    fd.close()
    m=d.split("\n")
    s="\n".join(m[:-1])
    fd=open("youtube_comics/i-have-a-mansion-in-the-post-apocalyptic-world-comics-wuxia-dao-novel.txt","w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()

    print_step("Removing temporary files 🗑")

    # cleanups = cleanup()
    # print_substep(f"Removed {cleanups} temporary files 🗑")
    print_substep("See result in the results folder!")

    # https://wuxiaworld.site/novel/i-have-a-mansion-in-the-post-apocalyptic-world-comics-wuxia-dao-novel/chapter-1/
    time.sleep(10.5)