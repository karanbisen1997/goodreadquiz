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
from moviepy.editor import TextClip, vfx,transfx
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.compositing.transitions import slide_in, slide_out
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from playwright.sync_api import ViewportSize, sync_playwright
from rich.console import Console

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

VideoFileClip.reW = lambda clip: clip.resize(width=W)
VideoFileClip.reH = lambda clip: clip.resize(width=H)
opacity = 0.9
 
Path(f"results/test.mp4").mkdir(parents=True, exist_ok=True)


EFFECT_DURATION = 10
CLIP_DURATION = 20


clip0 = ImageClip(f"assets/temp/png1/comment_0.png").set_duration(CLIP_DURATION).resize(height=720).resize(width=1280).set_opacity(0.9)
clip1 = ImageClip(f"assets/temp/png1/comment_1.png").set_duration(CLIP_DURATION).resize(height=720).resize(width=1280).set_opacity(0.9)
clip2 = ImageClip(f"assets/temp/png1/comment_2.png").set_duration(CLIP_DURATION).resize(height=720).resize(width=1280).set_opacity(0.9)
clip3 = ImageClip(f"assets/temp/png1/comment_3.png").set_duration(CLIP_DURATION).resize(height=720).resize(width=1280).set_opacity(0.9)
clip4 = ImageClip(f"assets/temp/png1/comment_4.png").set_duration(CLIP_DURATION).resize(height=720).resize(width=1280).set_opacity(0.9)
clip5 = ImageClip(f"assets/temp/png1/comment_5.png").set_duration(CLIP_DURATION).resize(height=720).resize(width=1280).set_opacity(0.9)
# clip6 = ImageClip(f"assets/temp/png1/comment_6.png").set_duration(CLIP_DURATION).resize(width=W).set_opacity(0.9)
# clip7 = ImageClip(f"assets/temp/png1/comment_7.png").set_duration(CLIP_DURATION).resize(width=W).set_opacity(0.9)
# clip8 = ImageClip(f"assets/temp/png1/comment_8.png").set_duration(CLIP_DURATION).resize(width=W).set_opacity(0.9)
# clip9 = ImageClip(f"assets/temp/png1/comment_9.png").set_duration(CLIP_DURATION).resize(width=W).set_opacity(0.9)
# clip10 = ImageClip(f"assets/temp/png1/comment_10.png").set_duration(CLIP_DURATION).resize(width=W).set_opacity(0.9)
# clip6,clip7,clip8,clip9,clip10
clips = [clip0,clip1, clip2, clip3,clip4,clip5]

# For the first clip we will need it to start from the beginning and only add
# slide out effect to the end of it
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
video.write_videofile(
    "final_clip1.mp4",
    codec="libx264",
    audio_codec="aac",
    preset="ultrafast",
    fps=24,
    threads=24,
    ffmpeg_params=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-pix_fmt", "yuv420p"],
)

