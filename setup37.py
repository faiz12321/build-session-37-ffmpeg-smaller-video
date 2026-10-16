"""Create only a new empty sample folder; refuse every existing path."""
from pathlib import Path

def make(path):
    Path(path).mkdir()

if __name__ == '__main__':
    try:
        make(Path(__file__).resolve().parent / 'sample')
    except FileExistsError:
        raise SystemExit('Stopped: sample already exists. Nothing was replaced or deleted.')
    print('Created new empty sample folder.')
