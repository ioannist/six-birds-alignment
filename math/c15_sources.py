"""[B] C15 exact statement snapshots plus reviewed applicability guards.
Run: python3 math/c15_sources.py
Reads sibling sources only. This is not a corpus promotion/build or deployment
certificate. Guards were reviewed against the statements, not inferred from labels.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
GUARDS = {
 'V6/thm:PGT6': 'Use its scalar-policy clause on a finite nonempty feasible candidate family with a strict scalar policy (all coordinate weights positive). Zero weights lose strictness; positive linear weighting need not attain every efficient point. Exact transport needs bijections/order reflection; costed transport is forward only.',
 'V15/ex:mixture': 'This is the stated binary depth-two learner, b=0, sampler, eighteen-sign cycle and alternating unlabelled source drive. Its non-attribution/unfaithful shadow is a scoped witness, not a theorem about every preference mixture or RLHF method.',
 'V1/thm:R6': 'A purchase-compilation record already includes the gate/source/price/bridge/audit/history and residual data. It preserves historical purchase/external origin when becoming a current primitive; it does not prove that a training artifact implements the declared principle.',
 'V1/thm:R7': 'Verified purchase receipt occurs in append-only history and a source-preserving presentation equivalence transports protected coordinates/identifiers. Renaming/deleting or changing price/disposition is not such an equivalence.',
 'V10/thm:ECT2': 'Finite coordinate cover and domain-valued compatible sections. Gluing yields a unique assignment; independently required admission P needs P(glue(a)), not compatibility alone.',
 'V12/thm:obstruction': 'Declared rational linear restriction/cochain system. A closed datum is solvable iff its Cech class vanishes. Forest surjectivity requires both overlap restrictions onto each edge to be surjective; graph shape alone is insufficient.',
 'V4/thm:TDR5': 'Declared tolerance, admissible independent factors and reached center catalogues. Empty reached catalogue defeats every repair; finite feasibility gives minimal repairs, not generally a least one. Inclusion, price, edge count and radius are separate orders.',
 'V5/thm:ERVERIFIER': 'Fixed verifier V/base oracle A and sound generator. Its outputs are contained in L_V; equality needs completeness. Oracle-relative non-finality concerns both signs of K_A and effectiveness/soundness/completeness, not universal failure of finite oversight.',
 'V14/thm:corruption': 'Worlds/target/calibrated grouped transcript code with target distance d_T. Unknown corruptions need d_T>=2b+1; known erasures need b+1; mixed known erasures e and unknown corruptions s need e+2s+1. Aliases are not independent groups.',
 'F4/thm:F28': 'Declare surjective part/interface quotient kappa, raw composition, outcome, residual and admission. All three must be constant on kappa fibers independently. Associativity and identity are separate coherence checks.',
 'V10/thm:MOT2': 'Replacement acceptance, new realization, backward behavior and guarantee transport are all required. Operational version matches every positive new branch/protected output/fault/work, related initials and a per-step overhead; word overhead is n*gamma.',
 'V8/thm:EOT2': 'Finite enablement laboratory and its ready-session/reusable calibrated/one-shot policies. A priced rollback returns a summary, not an identical full timed session or zero-budget/path-length information.',
 'V10/thm:MOT5': 'Typed co-growth books require every key and equal values on overlaps; absent field is missing evidence. Work/residual sums require linked compatible continuations. Paid rollback restores native/observer/active-code projection, not histories, balances or acquired code.',
 'AD/cor:xi:same-family-saturation': 'Declared legal linear energy quotient/probes and actual linear dependence M=B L. The extra family then leaves Xi unchanged; non-linear learned features or a changed native source require a new bridge, not this corollary by name.',
 'C/def:cpackage': 'Definition of the eight-clause conjunction plus cross-clause coherence and promotion panel. It is not an existence/soundness theorem for a record populated with assertions, and ethical/phenomenal bridges do not follow from a C4 privacy witness.',
 'C/T2': 'Exact finite privacy wheel, declared channel family, non-exposure and predictive witness content. Adding a predictive-state reading dissolves the split. No absolute privacy/phenomenality result; canonical label thm:t2 inside sec:interface (D17/D20).',
 'V14/thm:identifiable': 'Declared target and calibrated transcript maps. Every target-different pair must be separated; target then factors uniquely on the reached transcript image. Label bijections preserve separation while decoder calibration may change; reward authority is additional.',
 'F4/thm:F17': 'Each access and public quotient is surjective and public quotient has the common-quotient universal property. Actual common target descent, rather than common words/consensus, is the conclusion; pairing public/target repairs representation, not normative authority.',
 'REF/prop:cx1_ladder': 'Specific two-atom sparse linear dictionary ladder with N_j=2^(j+1), epsilon_j=2^(-j), atom localization vanishing and two-sparse synthesis localization1. Transfer to legal reachable coalition programs requires its actual harm/resource map; not arbitrary coalitions from span alone.',
 'F4/thm:F15a': 'Selection descends iff fiber split absent. Fixed-point/equivariant-section obstruction additionally needs actual orbit quotient and induced trivial orbit action. A breaker extension carries selectedness but does not itself construct a selector.',
 'SPEND/thm:duality': 'Finite row-stochastic entropy/Gibbs setting, fixed row weights and declared cost, lambda>=0; budget optimality needs feasibility plus complementary slackness. Only positive-weight rows are unique. Physical resource law and economic-fee correspondence are separate hypotheses.',
 'V13/thm:atlas': 'Six explicit rational/finite non-implication witnesses: time/charge, charge/transfer, balanced postings/potential, storage/conservation, generator/unique form, conserved readout/storage factorization. It classifies structural roles, not general market optimality.',
 'C/T13': 'Eight-state/four-public-class finite descent-fixing gauge; modeled descent-visible rigidifier makes global-swap Z2 trivial and reduces two transports to one. Broader quality-space rigidification is schema-grade, not measured legal/subjective interpretation.',
 'PT/thm:trap': 'Protocol scheduler reversible w.r.t. s and every state kernel reversible w.r.t. the same pi; lifted law is product pi*s. Zero path-reversal divergence for coordinatewise observations under these hypotheses does not settle meaning, intent or other irreversible protocols.',
 'INST/prop:coercion-null-probe': 'Declared finite carrier, same source history, same final fully forced profile and equal Pi1 endpoint readout. It is the scoped no-witness enumeration; unilateral/free-response probes can preserve memory. No universal statement about coercion/intent.',
 'V11/thm:carriage': 'Realized capability rules/seed/reach fixed-point/lifetimes. Necessity holds for every capacity/lifetime. Sufficiency needs UNBOUNDED capacity and each seed lifetime>=realized reach height+1; finite-capacity funding needs a separately witnessed run.',
 'V15/thm:audit': 'Behavior finite index n_beta and host reachable-state bound m give pointed word cutoff n_beta+m-2. Without host size bound no finite pointed test certifies all hosts. Actual alphabet, behavior and counted reachability are required; stochastic/raw-history traces are not silently deterministic finite behaviors.',
}


def snapshot(key, label, paths, synthesis):
    path = paths[key]
    text = path.read_text()
    if label in ('T2', 'T13'):
        anchor = 'sec:interface' if label == 'T2' else 'sec:structure'
        assert text.count('\\label{'+anchor+'}') == 1
        # D17/D20: the canonical text carries its own theorem labels (thm:t2, thm:t13); the legacy
        # name T2/T13 is kept only for matching the ratified grade index.
        section = anchor
        anchor = 'thm:'+label.lower()
        position = text.index('\\label{'+anchor+'}')
        assert text.count('\\label{thm:'+label.lower()+'}') == 1
        assert text.index('\\label{'+section+'}') < position
        match = list(re.finditer(r'\\begin\{theorem\}', text[:position]))[-1]
        begin = match.start(); env = 'theorem'
    else:
        anchor = label; section = None
        assert text.count('\\label{'+anchor+'}') == 1
        position = text.index('\\label{'+anchor+'}')
        begins = list(re.finditer(r'\\begin\{(theorem|proposition|corollary|lemma|definition|example)\}', text[:position]))
        assert begins
        begin, env = begins[-1].start(), begins[-1][1]
    end = text.index('\\end{'+env+'}', begin)+len('\\end{'+env+'}')
    grades = []
    for line in synthesis.split('## Appendix: theorem index', 1)[1].splitlines():
        parts = line.split('|')
        matches = bool(re.search(r'\b'+label+r'\b', parts[1])) if label in ('T2', 'T13') and len(parts) >= 6 else label in parts[1] if len(parts) >= 6 else False
        if len(parts) >= 6 and key == parts[2].strip().split()[0] and matches:
            grades.append(parts[3].strip())
    return {'key': key, 'name_or_label': label, 'exact_anchor': anchor,
            'has_own_statement_label': True, 'section_anchor': section,
            'path': str(path), 'line': text[:begin].count('\n')+1, 'environment': env,
            'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'statement': text[begin:end], 'grade_as_recorded_in_ratified_index': grades,
            'reviewed_guard': GUARDS[key+'/'+label], 'source_grade_promoted': False}


def examples():
    codewords = {0: (0, 0, 0), 1: (1, 1, 1)}
    distance = sum(a != b for a, b in zip(codewords[0], codewords[1]))
    assert distance == 3
    reports = []
    for world, word in codewords.items():
        for report in product((0, 1), repeat=3):
            faults = sum(a != b for a, b in zip(word, report))
            if faults <= 1:
                decoded = int(sum(report) >= 2)
                assert decoded == world
                reports.append({'world': world, 'report': report, 'decoded': decoded})
    predictions = []
    for g in range(3):
        row = [F(0)]*3; row[0] += F(1, 20)
        for k in range(3-g): row[g+k] += F(19, 20)*comb(2-g, k)*F(1, 2)**(2-g)
        assert sum(row) == 1
        predictions.append(tuple(row))
    assert len(set(predictions)) == 3
    decoder = {p: g for g, p in enumerate(predictions)}
    assert all(decoder[p] == g for g, p in enumerate(predictions))
    return {'factual_quorum': {'outcome': 'pass on declared lab bit target', 'target_distance': distance,
                              'b': 1, 'reports': reports, 'calibration_and_groups': '[P] physical hypotheses'},
            'public_grade_hiddenness': {'outcome': 'witnessed failure of C4 on declared three-state future language',
                                       'future_language': 'honest next-grade distribution',
                                       'public_current_readout': 'grade g', 'predictive_classes': predictions,
                                       'nonconstant_public_readout_factors_through_predictive_class': True,
                                       'not_a_claim_about_subjecthood': True}}


def enc(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): enc(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [enc(v) for v in x]
    return x


def main():
    synthesis = (ROOT/'brainstorm/SYNTHESIS.md').read_text()
    paths = {}
    for line in synthesis.splitlines():
        match = re.match(r'\| ([^|]+) \| `([^`]+\.tex)` \|$', line)
        if match: paths[match[1].strip()] = (ROOT/match[2]).resolve()
    records = []
    for identifier in GUARDS:
        key, label = identifier.split('/', 1)
        records.append(snapshot(key, label, paths, synthesis))
    assert len(records) == 27
    catalogue = (ROOT/'math/C15.md').read_text().split('| Target | Invoked source', 1)[1].split('[B] Local construction links:', 1)[0]
    targets = []
    for line in catalogue.splitlines():
        cells = line.split('|')
        if len(cells) != 6 or not cells[1].strip() or cells[1].strip().startswith('---'): continue
        target, invoked, bridge, ethics = (c.strip() for c in cells[1:5])
        refs = []
        for part in invoked.split(';'):
            key = part.strip().split()[0]
            labels = re.findall(r'`([^`]+)`', part)
            if key == 'C' and 'T2' in part: labels = ['T2', 'def:cpackage']
            elif key == 'C' and 'T13' in part: labels = ['T13']
            refs += [key+'/'+label for label in labels]
        assert refs and all(ref in GUARDS for ref in refs), (target, refs)
        targets.append({'target': target, 'source_refs': refs, 'representation_bridge': bridge,
                        'ethical_scope': ethics, 'named_deployment_outcome': 'missing mapping',
                        'source_statement_review': 'complete for invoked anchors'})
    assert len(targets) == 17
    out = {'tag': '[B]', 'grade': 'scoped', 'review': 'self-reviewed',
           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'source_records': records, 'targets': targets, 'lab_examples': examples(),
           'no_corpus_files_written': True, 'no_corpus_grade_promotions': True,
           'no_named_deployment_pass': True}
    (ROOT/'math/C15_source_results.json').write_text(json.dumps(enc(out), indent=2)+'\n')
    md = ['# C15 — exact source statement snapshot', '',
          '[B] Statements below are frozen source text, with exact anchors and the ratified index grade where available. New reviewed guards are bridges; no source grade is promoted and no named deployment is certified.', '']
    for row in records:
        md += [f'## {row["key"]} {row["name_or_label"]}', '',
               f'[F] Source [{row["exact_anchor"]}]({row["path"]}:{row["line"]}); kind: {row["environment"]}. Grade recorded in index: '+('; '.join(row['grade_as_recorded_in_ratified_index']) or 'not separately indexed; preserve the printed source scope above the application')+'.', '',
               '[B] Reviewed applicability guard: '+row['reviewed_guard'], '', '```tex', row['statement'], '```', '']
    (ROOT/'math/C15_SOURCE_STATEMENTS.md').write_text('\n'.join(md)+'\n')
    print('PASS C15 source audit:', len(records), 'statements;', len(targets), 'named-target obligation rows; no deployment promotions')
    print('PASS conditional factual-bit decoder; WITNESSED FAILURE public-grade C4 hiddenness; both lab scopes explicit')


if __name__ == '__main__': main()
