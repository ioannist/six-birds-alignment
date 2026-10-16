"""Make a cold-build copy inside this repo; never write to the corpus.
Run: python3 math/b4_prepare.py
"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path('/home/repos/six-birds-transcendence')
DEST = ROOT/'lean/corpus_scratch/transcendence'
FREEZE = ROOT/'math/B4_source_hashes.json'
if DEST.exists():
    assert FREEZE.exists(), 'Existing scratch is missing its source freeze'
    for relative, h in json.loads(FREEZE.read_text()).items():
        assert hashlib.sha256((DEST/relative).read_bytes()).hexdigest() == h
    print('Existing source-frozen scratch retained; use b4_audit.py to compare the corpus')
else:
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, DEST, ignore=shutil.ignore_patterns('.git', '.lake', '__pycache__'), symlinks=False)
    hashes = {str(p.relative_to(SOURCE)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in (SOURCE/'lean').rglob('*.lean') if '.lake' not in p.parts}
    for relative, h in hashes.items():
        assert hashlib.sha256((DEST/relative).read_bytes()).hexdigest() == h
    FREEZE.write_text(json.dumps(hashes, indent=2)+'\n')
    print('Copied source-frozen scratch:', len(hashes), 'Lean sources')
