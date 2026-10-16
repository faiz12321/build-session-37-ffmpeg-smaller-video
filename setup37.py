"""Create only a new empty sample folder; refuse every existing path."""
from pathlib import Path
import stat

def make(path):
    root = Path(path).absolute()
    if '..' in root.parts:
        raise OSError('Parent-traversal paths are unsupported.')
    for parent in reversed(root.parents):
        info = parent.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise OSError('Linked/reparse-point parents are unsupported.')
    Path(path).mkdir()

if __name__ == '__main__':
    try:
        make(Path(__file__).absolute().parent / 'sample')
    except FileExistsError:
        raise SystemExit('Stopped: sample already exists. Nothing was replaced or deleted.')
    print('Created new empty sample folder.')
