## SimplestEdit

Video editing tool using `ffmpeg` cli from within `python`

---

### Purpose

The main idea of this tool is to script the editing of a large number of videos. The edits consist of putting an intro and outro slide as well as fading in and out the audio/video. As ffmpeg can be scripted well and the editing is extremely basic, this tool aims at ppackaging eveything.
This small tool consists of simple operations that can be performed with ffmpeg and imgmagick:

- `convert.sh` transforms the pdf slides in high resolution png
- conversion of the slides in videos (3s for intro, 5s for outro)
- conversion of the processed video in the same format as the slide videos (mp4 here)
- concatenation and filters applied to the overall video

### Installation

SimplestEdit has no dependency with external python packages. It can be installed with:
```bash
  $ git clone https://github.com/QDucasse/SimplestEdit
  $ cd SimplestEdit
```

Then, running the scripts results in a simple call:

```bash
  $ sh convert.sh
  $ python ffmpeg_handler.py
```



### Documentation

WIP
