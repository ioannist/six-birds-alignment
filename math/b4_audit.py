"""Audit copied TT declarations and source freeze; sibling repo is read-only.
Run after scratch copy/build: python3 math/b4_audit.py
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = ROOT/'lean/corpus_scratch/transcendence'
IDS = {'TTH-05', 'TTH-06', 'TTH-08', 'TTH-09', 'TTS-01', 'TTS-04'}
inventory = json.loads((SCRATCH/'lean/row_inventory.json').read_text())['rows']
legacy = list(csv.DictReader((SCRATCH/'cst-tt/registries/FINAL_THEOREM_STATUS.csv').open()))
current_rows = [r for r in inventory if r['row_id'] in IDS]
old_rows = [r for r in legacy if r['theorem_id'] in IDS]
declarations = sorted({d for r in current_rows for d in r['declarations']} |
                      {d for r in old_rows for d in r['formal_declarations'].split(';')})
assert len(current_rows) == len(old_rows) == 6
audit = SCRATCH/'lean/AlignmentB4Audit.lean'
audit.write_text('import CSTTT\n'+'\n'.join('#check '+d+'\n#print axioms '+d for d in declarations)+'\n')
result = subprocess.run(['lake', 'env', 'lean', audit.name], cwd=audit.parent,
                        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(ROOT/'math/B4_axioms_and_types.txt').write_text(result.stdout)
assert result.returncode == 0, result.stdout[-2000:]
assert 'sorryAx' not in result.stdout
axioms = {}
for name, receipt in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", result.stdout):
    axioms[name] = [] if not receipt.strip() else re.split(r',\s*', receipt.strip())
for name in re.findall(r"'([^']+)' does not depend on any axioms", result.stdout):
    axioms[name] = []
assert len(axioms) == len(declarations), (len(axioms), len(declarations))
nonstandard = sorted({a for values in axioms.values() for a in values} - {'propext', 'Classical.choice', 'Quot.sound'})
frozen = json.loads((ROOT/'math/B4_source_hashes.json').read_text())
for file, digest in frozen.items():
    assert hashlib.sha256((SCRATCH/file).read_bytes()).hexdigest() == digest
    assert hashlib.sha256((Path('/home/repos/six-birds-transcendence')/file).read_bytes()).hexdigest() == digest
out = {'scope': 'declarations actually checked in a copied current source snapshot, not automatic full row promotion',
       'toolchain': subprocess.check_output(['lean', '--version'], cwd=audit.parent, text=True).strip(),
       'current_inventory_rows': current_rows, 'historical_registry_rows': old_rows,
       'declarations_checked': declarations, 'axioms': axioms, 'nonstandard_axioms': nonstandard,
       'vendor_nonstandard_axiom_outside_audited_chains':
           'SixBirdsMetaMath.FoundationsIV.Access.HiddennessNormalForm.hiddenness_pending',
       'sources_unchanged': len(frozen), 'snapshot_inventory_sha256': hashlib.sha256((SCRATCH/'lean/row_inventory.json').read_bytes()).hexdigest()}
(ROOT/'math/B4_results.json').write_text(json.dumps(out, indent=2)+'\n')
print('PASS B4:', len(declarations), 'declarations;', len(frozen), 'frozen source hashes; nonstandard axioms:', nonstandard)
