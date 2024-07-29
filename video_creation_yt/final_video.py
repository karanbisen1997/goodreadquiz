#!/usr/bin/env python3
import multiprocessing
from pathlib import Path
import re
from typing import Tuple, Any
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import vfx
from rich.console import Console

from utils.console import print_step, print_substep
from utils import settings

console = Console()
W, H = 1280, 720


def name_normalize(name: str) -> str:
    name = re.sub(r'[?\\"%*:|<>]', "", name)
    name = re.sub(r"( [w,W]\s?\/\s?[o,O,0])", r" without", name)
    name = re.sub(r"( [w,W]\s?\/)", r" with", name)
    name = re.sub(r"(\d+)\s?\/\s?(\d+)", r"\1 of \2", name)
    name = re.sub(r"(\w+)\s?\/\s?(\w+)", r"\1 or \2", name)
    name = re.sub(r"\/", r"", name)

    lang = settings.config["reddit"]["thread"]["post_lang"]
    if lang:
        import translators as ts

        print_substep("Translating filename...")
        translated_name = ts.google(name, to_language=lang)
        return translated_name

    else:
        return name


def make_final_video(
    number_of_clips: int,
    length: int,
    reddit_obj: dict,
    background_config: Tuple[str, str, str, Any],
    folderNo: str,
):
    """Gathers audio clips, gathers all screenshots, stitches them together and saves the final video to assets/temp
    Args:
        number_of_clips (int): Index to end at when going through the screenshots'
        length (int): Length of the video
        reddit_obj (dict): The reddit object that contains the posts to read.
        background_config (Tuple[str, str, str, Any]): The background config to use.
    """
    # try:  # if it isn't found (i.e you just updated and copied over config.toml) it will throw an error
    #    VOLUME_MULTIPLIER = settings.config["settings"]['background']["background_audio_volume"]
    # except (TypeError, KeyError):
    #    print('No background audio volume found in config.toml. Using default value of 1.')
    #    VOLUME_MULTIPLIER = 1
    print_step("Creating the final video 🎥")
    print(number_of_clips)
    VideoFileClip.reW = lambda clip: clip.resize(width=W)
    VideoFileClip.reH = lambda clip: clip.resize(width=H)
    opacity = settings.config["settings"]["opacity"]
    title = re.sub(r"[^\w\s-]", "", reddit_obj["thread_post"])
    new_opacity = 1 if opacity is None or float(opacity) >= 1 else float(opacity)
    filename = f"{name_normalize(re.sub('[^A-Za-z0-9]+', '_', title))}.mp4"
    subreddit = settings.config["reddit"]["thread"]["subreddit"]
    Path(f"results/{subreddit}/{folderNo}").mkdir(parents=True, exist_ok=True)
    print(number_of_clips)
    for i in range(0, number_of_clips):
        # from moviepy.editor import *
        # Import the audio(Insert to location of your audio instead of audioClip.mp3)
        audio = AudioFileClip(f"assets/temp/mp3/{i}.mp3")
        # Import the Image and set its duration same as the audio (Insert the location of your photo instead of photo.jpg)
        clip = ImageClip(f"assets/temp/png/comment_{i}.png").set_duration(audio.duration).resize(width=W).set_opacity(new_opacity).fx(vfx.fadein,1).fx(vfx.fadeout,1).set_position('center')
        # Set the audio of the clip
        clip = clip.set_audio(audio)
        # Export the clip
        print(f"results/{subreddit}/{i}_{filename}")
        clip.write_videofile(f"results/{subreddit}/{folderNo}/{i}_{filename}", fps=40,audio_codec="aac",audio_bitrate="192k",verbose=False,threads=multiprocessing.cpu_count(),)


    print_step("Removing temporary files 🗑")
    # cleanups = cleanup()
    # print_substep(f"Removed {cleanups} temporary files 🗑")
    print_substep("See result in the results folder!")

    print_step(
        f'Reddit title: {reddit_obj["thread_title"]} \n Background Credit: {background_config[2]}'
    )



# from moviepy.editor import *
# # Import the audio(Insert to location of your audio instead of audioClip.mp3)
# audio = AudioFileClip("AudioClip.mp3")
# # Import the Image and set its duration same as the audio (Insert the location of your photo instead of photo.jpg)
# clip = ImageClip("photo.jpg").set_duration(audio.duration)
# # Set the audio of the clip
# clip = clip.set_audio(audio)
# # Export the clip
# clip.write_videofile("render.mp4", fps=24)