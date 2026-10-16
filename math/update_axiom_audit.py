"""[B] Generate type/axiom audit commands for every local exported theorem.
Run: python3 math/update_axiom_audit.py; then bash lean/build.sh.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
names = []
for file in sorted((ROOT/'lean/Alignment').glob('*.lean')):
    source = file.read_text()
    namespace = re.search(r'^namespace ([\w.]+)', source, re.M)[1]
    names += [namespace+'.'+name for name in re.findall(r'^theorem (\w+)', source, re.M)]
assert len(names) == len(set(names))
body = 'import Alignment\n'+'\n'.join('#check '+name+'\n#print axioms '+name for name in names)+'\n'
(ROOT/'lean/AxiomAudit.lean').write_text(body)
print('Generated checks for', len(names), 'local theorems')
