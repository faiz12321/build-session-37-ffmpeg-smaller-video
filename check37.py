"""Limited checks for this generated fixture, not arbitrary footage or playback."""
import array
import hashlib
import json
import math
import subprocess
import sys
import stat
from pathlib import Path


def safe_input(value, directory=False):
    path = Path(value).absolute()
    if '..' in path.parts:
        raise OSError('Parent-traversal paths are unsupported.')
    for part in [*reversed(path.parents), path]:
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise OSError('Links/reparse points are unsupported.')
    info = path.lstat()
    if directory:
        if not stat.S_ISDIR(info.st_mode):
            raise NotADirectoryError('Expected an ordinary directory.')
    elif not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise OSError('Expected an ordinary singly linked file.')
    return path


def digest(path):
    h = hashlib.sha256()
    with safe_input(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def probe(path):
    safe_input(path)
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,codec_name,pix_fmt:format=duration,size', '-of', 'json', str(path)],
        capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def check(root):
    root = safe_input(root, directory=True)
    original = root / 'input.mp4'
    smaller = root / 'small.mp4'
    assert digest(original) == safe_input(root / 'input.sha256').read_text().strip(), 'Input changed'
    info = probe(smaller)
    streams = info['streams']
    assert any(x['codec_type'] == 'video' and x['codec_name'] == 'h264' and x['pix_fmt'] == 'yuv420p' for x in streams), 'Expected video missing'
    assert any(x['codec_type'] == 'audio' and x['codec_name'] == 'aac' for x in streams), 'Expected audio missing'
    assert 2.9 < float(info['format']['duration']) < 3.2, 'Unexpected fixture duration'
    assert smaller.stat().st_size < original.stat().st_size, 'This fixture did not get smaller'
    decoded = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(smaller), '-map', '0:v:0',
        '-map', '0:a:0', '-f', 'null', '-'], capture_output=True, check=True)
    assert not decoded.stderr.strip(), 'Decoder reported an error'
    audio = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(smaller), '-vn', '-ac', '1',
        '-ar', '8000', '-f', 's16le', '-'], capture_output=True, check=True)
    assert not audio.stderr.strip(), 'Audio decoder reported an error'
    pcm = audio.stdout
    values = array.array('h')
    values.frombytes(pcm)
    if sys.byteorder != 'little':
        values.byteswap()
    assert len(values) > 22000, 'Too few decoded audio samples'
    rms = math.sqrt(sum(v*v for v in values) / len(values))
    assert rms > 100, 'Tone is absent or too quiet for this fixture'
    print('PASS: source SHA256 unchanged; H.264/yuv420p and AAC present; fixture duration near 3 seconds.')
    print('PASS: output smaller for this fixture; both streams decoded; decoded tone RMS exceeds 100.')
    print('These checks do not prove audio meaning, visual quality or playback on a phone. Watch and listen before sharing.')


def main(argv):
    if argv not in (['snapshot'], ['verify']):
        print('Usage: python check37.py snapshot|verify', file=sys.stderr)
        return 2
    try:
        root = safe_input(Path(__file__).absolute().parent / 'sample', directory=True)
        if argv == ['snapshot']:
            manifest = root / 'input.sha256'
            try:
                manifest.lstat()
            except FileNotFoundError:
                pass
            else:
                raise FileExistsError(manifest)
            with manifest.open('x', encoding='ascii') as handle:
                handle.write(digest(root / 'input.mp4') + '\n')
            print('Saved input digest in a new input.sha256 file; existing manifests are refused.')
        else:
            check(root)
    except (OSError, subprocess.SubprocessError, ValueError, AssertionError) as error:
        print('Stopped: ' + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
