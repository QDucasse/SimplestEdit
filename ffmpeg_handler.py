# -*- coding: utf-8 -*-
# Included in:
# ffmpeg_handler
# author - Quentin Ducasse
# https://github.com/QDucasse
# quentin.ducasse@ensta-bretagne.org

import os
import re
import math
import subprocess

processed_folder = "Processed/"
convert_folder   = "Processed-Converted/"
slides_folder    = "Slides/"
output_folder    = "Final/"
intros_folder    = "Intros-Outro/"
end_slide        = "Slides/end.png"


def vid_from_img(img_name,vid_name,duration):
    '''Converts an image to a video of a specified duration'''
    duration = str(duration)
    subprocess.call(["ffmpeg",
        "-loop", "1",
        "-i", img_name,
        "-c:v", "libx264",
        "-t", duration,
        "-vf", "scale=2520:-2",
        "-pix_fmt", "yuv420p",
        vid_name])


def process_all_slides():
    '''Transforms all the intro slides in their 3s-long video counterpart and the
       outro slide in the 5s-long video counterpart'''
    # List all the elements in the Slides/ folder
    slides = os.listdir(slides_folder)
    # Only keep the png images
    png_slides = [slide for slide in slides if slide.endswith(".png")]
    png_slides.remove("end.png")
    # Intro video creation
    for png_slide in png_slides:
        video_name = png_slide.split(".")[0] + "-intro.mp4"
        vid_from_img(slides_folder + png_slide, intros_folder + video_name, 3)
    # Outro video creation - Same for all the videos
    vid_from_img(end_slide, intros_folder + "outro.mp4", 5)


def convert_vid(vid_name, out_name):
    '''Converts a video to another format'''
    subprocess.call(["ffmpeg",
        "-i", vid_name,
        "-c:v", "libx264",
        "-vf", "scale=2520:-2",
        "-pix_fmt", "yuv420p",
        "-write_tmcd", "0",
        out_name
    ])


def get_duration(vid_name):
    '''Gets the duration of a video'''
    # Runs the command and get the output
    output = subprocess.check_output(["ffprobe",
        "-i", vid_name,
        "-show_format"
    ])
    output = output.decode('utf8')
    # Run the regex for the duration on the output
    # --> "duration=65.200" for example (.3 precision)
    res = re.search("duration=\d*.\d{3}",output).group(0)
    duration =  math.ceil(float(res[9:]))
    return duration


def concatenate_mix(intro_video,outro_video,video,output_video):
    '''Concatenates the three videos and performs the following transitions:
    VIDEO: Intro ==crossfade==> Video ==crossfade==> Outro
    AUDIO: Intro ===fade-in===> Video ===fade-out==> Outro'''
    duration = get_duration(video)

    filter_complex = "[0:v]setpts=PTS-STARTPTS,format=yuva420p,fade=out:st=2:d=1:alpha=1[1]; \
        [2:v]setpts=PTS-STARTPTS+(2/TB),format=yuva420p,fade=in:st=2:d=1:alpha=1,fade=out:st={0}:d=1:alpha=1[2]; \
        [3:v]setpts=PTS-STARTPTS+({0}/TB),format=yuva420p,fade=in:st={0}:d=1:alpha=1[3]; \
        [1:a]asetpts=PTS-STARTPTS[1a]; \
        [2:a]asetpts=PTS-STARTPTS[2a]; \
        [4:a]asetpts=PTS-STARTPTS[3a]; \
        [1][2]overlay,format=yuv420p[12]; \
        [12][3]overlay,format=yuv420p[123]; \
        [1a][2a]acrossfade=d=1[12a]; \
        [12a][3a]acrossfade=d=0.5[123a]; \
        [123][123a]concat=n=1:v=1:a=1[v][a]".format(duration+2)

    subprocess.call(["ffmpeg",
        "-i", intro_video, "-f", "lavfi", "-t", "3", "-i", "anullsrc",
        "-i", video,
        "-i", outro_video, "-f", "lavfi", "-t", "5", "-i", "anullsrc",
        "-filter_complex", str(filter_complex),
        "-map", "[v]", "-map", "[a]",
        output_video
    ])

def process_all_videos():
    '''Run the processing (concatenation, mix) for all the videos'''
    # List the processed videos
    processed_videos = os.listdir(processed_folder)
    processed_videos = [video for video in processed_videos if video.endswith(".mov")]
    # Define the outro video name
    outro_name = intros_folder + "outro.mp4"
    for video_name in processed_videos:
        # Extract the file name
        base_name    = video_name.split(".")[0]
        # Readd the folder name
        video_name = processed_folder + video_name
        # Define the converted video name
        convert_name = convert_folder + base_name + "-converted.mp4"
        # Convert the video
        convert_vid(video_name, convert_name)

        # Define the intro video name
        intro_name   = intros_folder + base_name + "-intro.mp4"
        # Define the output video name
        output_name  = output_folder + base_name + "-final.mp4"
        # Perform the concatenation and add the transitions
        concatenate_mix(intro_name, outro_name, video_name, output_name)


if __name__ == "__main__":
    # vid_from_img("end.png","end_vid.mp4", 5)
    # convert_vid("end_vid.mp4","test.mp4")
    # print(get_duration("test.mp4"))
    # complete_process("W1-LiveA-EN.png","end.png","W1-LiveA-EN.mov")
    process_all_videos()
