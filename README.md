# Make a smaller generated video and check it

Save setup37.py,check37.py,test_lesson37.py in a NEW empty lesson folder. Python3,ffmpeg/ffprobe with libx264/AAC are prerequisites. Use only the generated3second test card and tone.

Two Windows and two Ubuntu full replays run exact visible source versions. Final 28 small fixture tests pass (Unix pipe skips on Windows); symlink creation can skip where unavailable. Displayed stdout is first Windows output, not normalized or mixed. Visible-command pair differences are unittest time. Full raw transcripts retain runner dependency-install output before visible commands where present; installation is not a recorded lesson step.
Only link/error changes: refuse fixture input/ancestor symbolic links/reparse points, hardlinks, special files and traversal before hashing, probing and decoding. Manifest creation checks its parent and refuses every existing manifest, including dangling links. Setup refuses linked parents/traversal and existing sample paths, without reset/deletion. CLI read/metadata/subprocess/fixture errors now print a brief message and exit 2 instead of an uncaught traceback; checks still raise errors when called by tests.
Original SHA256, codecs/pixel format, duration, fixture size comparison, decoding and nonzero-tone checks are unchanged. Direct ffmpeg/ffprobe commands are NOT wrapped by these Python guards and can still follow links. Use only the NEW generated sample folder and ordinary files, not links or personal footage. Every ffmpeg output still uses -n; overwrite refusal is checked by text plus unchanged bytes/mtime because some Windows builds return 0 on refusal.
No atomic snapshot, hostile-race defense, resource limit, visual-quality judgment, audio-meaning/sync judgment or phone-playback proof. Stop editors/sync. Keep private paths/errors private. Partial NEW outputs can remain after errors; they are not deleted. Assertions require normal Python, not python -O. Small fictional fixtures are not proof on every filesystem. No phone/desktop recording. Recorder removes only its own temporary fixture folder. Decisions/feedback are teaching text, not recorded output.

## Sources and licenses

- FFmpeg options, -n and stream selection: https://ffmpeg.org/ffmpeg.html
- ffprobe: https://ffmpeg.org/ffprobe.html
- FFmpeg codecs: https://ffmpeg.org/ffmpeg-codecs.html
- FFmpeg licenses: https://ffmpeg.org/legal.html

This lesson's source code is MIT licensed (LICENSE). FFmpeg, libx264 and other codec libraries have separate licenses. FFmpeg builds can be LGPL or GPL depending on build options; libx264-enabled FFmpeg builds use GPL terms. No FFmpeg executable or codec library is included here. Generated test footage is not personal footage. No real-world videos, phones or desktop applications were tested.


Reference: https://docs.python.org/3/library/os.html

Windows paired run: https://github.com/faiz12321/lesson-lab/actions/runs/38979587913
Ubuntu paired run: https://github.com/faiz12321/lesson-lab/actions/runs/38979880837
