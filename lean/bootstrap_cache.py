"""Copy a pinned local import closure; never build/write in sibling repos.

Usage: python3 lean/bootstrap_cache.py
This is an offline convenience. Cache sources/objects are ignored by git;
cache_manifest.json pins upstream commits and source/object SHA256 hashes.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
PACKAGES = Path('/home/repos/six-birds-currency/lean/.lake/packages')
START = ['Mathlib.Algebra.Order.Field.Basic', 'Mathlib.Data.Finset.Card',
         'Mathlib.Tactic.Ring', 'Mathlib.Tactic.Linarith', 'Mathlib.Tactic.FieldSimp',
         'Mathlib.Tactic.NormNum', 'Mathlib.Analysis.SpecificLimits.Basic',
         'Mathlib.Analysis.SpecialFunctions.Pow.Real']
TARGET = HERE/'vendor_cache'
packages = [p for p in PACKAGES.iterdir() if (p/'.lake/build/lib/lean').is_dir()]
seen, rows, todo = set(), [], list(START)
commits = {}
while todo:
    module = todo.pop()
    if module in seen:
        continue
    seen.add(module)
    relative = Path(*module.split('.'))
    matches = [p for p in packages if (p/relative.with_suffix('.lean')).is_file()]
    if not matches:
        if module.startswith(('Lean', 'Init', 'Std')):
            continue
        raise RuntimeError('Unresolved import '+module)
    assert len(matches) == 1, (module, matches)
    package = matches[0]
    source = package/relative.with_suffix('.lean')
    contents = source.read_text()
    # Imports occur in the module header. Ignore prose/code in doc comments.
    clean, depth, j = [], 0, 0
    while j < len(contents):
        if contents[j:j+2] == '/-':
            depth += 1
            j += 2
        elif depth and contents[j:j+2] == '-/':
            depth -= 1
            j += 2
        elif not depth and contents[j:j+2] == '--':
            end = contents.find('\n', j)
            j = len(contents) if end < 0 else end
        else:
            if not depth or contents[j] == '\n':
                clean.append(contents[j])
            j += 1
    header = ''.join(clean)
    todo += re.findall(r'^\s*(?:(?:public|private|meta)\s+)*import\s+(?:all\s+)?([\w.]+)', header, re.M)
    if package.name not in commits:
        commits[package.name] = subprocess.check_output(['git', '-C', str(package), 'rev-parse', 'HEAD'], text=True).strip()
    for origin, dest in [(source, TARGET/'src'/relative.with_suffix('.lean'))] + [
        (package/'.lake/build/lib/lean'/relative.with_suffix(ext), TARGET/'lib/lean'/relative.with_suffix(ext))
        for ext in ('.olean', '.olean.private', '.olean.server', '.ilean', '.ir')]:
        if not origin.is_file():
            if origin.suffix == '.olean':
                raise RuntimeError('Missing compiled import '+str(origin))
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(origin.read_bytes()).hexdigest()
        if not dest.exists() or hashlib.sha256(dest.read_bytes()).hexdigest() != digest:
            shutil.copyfile(origin, dest)
        rows.append({'file': str(dest.relative_to(HERE)), 'sha256': digest})
expected = '8f9d9cff6bd728b17a24e163c9402775d9e6a365'
assert commits['mathlib'] == expected
manifest = {'toolchain': 'leanprover/lean4:v4.28.0', 'commits': commits, 'initial_imports': START,
            'module_count': len(seen), 'files': rows, 'scope': 'copied cached import closure; no dependency builds in sibling repos'}
(HERE/'cache_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
# Lake resets LEAN_PATH. Install the external import objects in the local
# output search path; Lake has no source targets for these external modules.
import os
for src in (TARGET/'lib/lean').rglob('*'):
    if src.is_file():
        dest = HERE/'.lake/build/lib/lean'/src.relative_to(TARGET/'lib/lean')
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            os.link(src, dest)
print('Copied', len(seen), 'modules; Mathlib', expected, 'offline')
