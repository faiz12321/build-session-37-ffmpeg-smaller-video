# Make a smaller generated video and check it

A recorded lesson, not a live terminal. Use only a new empty lesson folder and the generated 3-second test card and tone. Python 3, ffmpeg and ffprobe with libx264/AAC are prerequisites. No installation or phone playback is tested by the lesson.

The visible lesson provides setup37.py, check37.py, test_lesson37.py and every command. Setup refuses existing paths. Every ffmpeg output uses -n to refuse replacement; snapshot creates its digest manifest exclusively. Do not use -y, delete old data to force a retry, or use a source file as output. New outputs can remain partial after an error.

Checks cover the input SHA256, expected H.264/yuv420p and AAC streams, near-three-second duration, this fixture getting smaller, full decoding and enough nonzero tone samples. A stream codec alone does not prove good sound. Checks do not judge audio meaning, sync, visual quality or phone playback. Watch and listen on the receiving device before sharing. No size-saving percentage is promised for other footage. Only the selected first video/audio streams are carried over; other tracks/subtitles are outside the lesson.

Run ordinary Python, not python -O: check37.py uses assertions. Reports can disclose paths and errors; keep private output private. Source-file links and concurrent filesystem changes are not comprehensively tested. Keep originals.

## Evidence

12 small temporary-fixture tests cover setup collisions, input bytes/mtime, refused existing and empty outputs, audio extraction, a missing input, source digest changes, and decode/nonzero-tone checks. They are not a general safety or media-quality proof. Two Windows and two Ubuntu full replays pass all 12 tests. Within each platform visible command output matches except unittest time. Windows raw run 1 also includes dependency-install output before the visible commands. Full raw transcripts retain it; the page does not claim installation is a lesson step. Windows recorded FFmpeg 9.0.2. Exact encoded sizes vary by build. Local decoded source/output frames at 0, 1 and 2 seconds were inspected; no phone playback was tested.

The recorder creates a unique temporary folder, writes the exact visible source files and runs the exact visible command argument lists. It removes only its own recording folder afterward. Full outputs and return codes are preserved, including expected refusals. Some Windows builds report exit 0 on a refused output, so the recorder checks refusal text and unchanged output bytes/mtime rather than assuming a nonzero return. Decoder error text is checked as well as the return code. Build/version differences can change encoded bytes and sizes.

## Sources and licenses

- FFmpeg options, -n and stream selection: https://ffmpeg.org/ffmpeg.html
- ffprobe: https://ffmpeg.org/ffprobe.html
- FFmpeg codecs: https://ffmpeg.org/ffmpeg-codecs.html
- FFmpeg licenses: https://ffmpeg.org/legal.html

This lesson's source code is MIT licensed (LICENSE). FFmpeg, libx264 and other codec libraries have separate licenses. FFmpeg builds can be LGPL or GPL depending on build options; libx264-enabled FFmpeg builds use GPL terms. No FFmpeg executable or codec library is included here. Generated test footage is not personal footage. No real-world videos, phones or desktop applications were tested.
