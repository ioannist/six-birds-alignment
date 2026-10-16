"""[B: lab] C1/E7: actual functions on a complete declared finite contract.
Run: python3 covenant_lab/gates.py. Exact enumeration; no simulation.
Normative and realized-generator premises are in math/C1.md and DECLARATION.
"""
from dataclasses import dataclass, replace
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
FIELDS = ('creditor', 'ordinary_bit', 'credential', 'version', 'cache', 'reference',
          'peer', 'participant0', 'participant1', 'corrected_book', 'domain')
D, Z, A, V, H, P, W, I0, I1, O, T = range(len(FIELDS))
STATES = tuple(range(1 << len(FIELDS)))
OPS = ('idle', 'flip', 'revise', 'veto', 'withdraw', 'repair', 'correct_book',
       'exit', 'join', 'own_record', 'other_record', 'capture', 'erase_origin')
MACROS = tuple(product(OPS, repeat=2))
SEED = 1

DECLARATION = {
    'claim_tags': '[P] model/ethics/realizer premises; [B: lab] new results',
    'carrier': {'control_fields': FIELDS, 'control_states': len(STATES),
                'private_health': 'one immutable bit per patient; four extensions per control state'},
    'actors_and_claimants': [0, 1], 'other_role': 'fact auditor',
    'scope': 'all control states, both private-health bits, and at most one signed command per actor per date',
    'lenses': {'prediction': 'private operational representation; future public service output',
              'accounting': 'implemented current obligation record, distinct from original pledge',
              'facts': 'three registered independent-source reports, plus public current output',
              'warrants': 'auditor factual bit; participants factual bit and current effective authority; private original records'},
    'interventions': OPS, 'composition': 'actor-0 command then actor-1 command at one date; arbitrary finite sequences of dates',
    'resources': 'retained fuel seed 1, realized converter yielding y units after maintenance; one measurement unit, one care unit each, command cost 0/1',
    'protected_claims': ['one care input per patient at every date', 'one command quota per actor',
                        'own-record access', 'no unauthorized medical-data output', 'veto/correction/owned repair access',
                        'portable exit retaining care and original claims'],
    'futures_and_horizon': 'all finite command words; ordinary readout (bit XOR version, cache, version, participation)',
    'uncertainty': 'arbitrary initial control state and health bits; at most one corrupted factual coordinate',
    'authority': 'jointly accepted fixed mandate: actor 0 may revise only when participating, credential-valid and in-domain; either actor may veto/correct; no capture of mandate or origin',
    'withdrawal_promise': 'an already-correct owned cache survives loss/disconnection of external teaching support',
    'obligation': 'one continuing restoration duty when cache differs from reference; creditor d, bearer 1-d; no cumulative damages claimed',
    'provenance': 'original pledge immutable; request receipts disclose actual caller, opcode, input source, quota payer, fee and ordinary public outputs, not raw private control state',
    'drive_ownership': 'not claimed; optional E9 drive-credit branch is inactive',
    'realizer': 'converter/measurement/protected execution functions assumed realized; no physical or phenomenal conclusion',
}


def bit(s, field): return (s >> field) & 1


def put(s, field, value):
    return (s | (1 << field)) if value else (s & ~(1 << field))


def original(s):
    return {'creditor': bit(s, D), 'bearer': 1-bit(s, D), 'reference': bit(s, P)}


def obligation(s):
    return None if bit(s, H) == bit(s, P) else original(s)


def effective_authority(s): return bit(s, A) * bit(s, I0) * bit(s, T)


def output(s): return (bit(s, Z) ^ bit(s, V), bit(s, H), bit(s, V), bit(s, I0), bit(s, I1))


@dataclass(frozen=True)
class Model:
    name: str
    income: int = 6
    forget_ordinary: bool = False
    misaccount: bool = False
    bypass_revision: bool = False
    erase_cache: bool = False
    blind_facts: bool = False
    blind_authority: bool = False


def accounting(model, s):
    entry = obligation(s)
    if entry is not None and model.misaccount and not bit(s, O):
        entry = dict(entry, bearer=0)
    return entry


def prediction_lens(model, s):
    return put(s, Z, 0) if model.forget_ordinary else s


def private_record(s, actor, health):
    # Both parties are entitled to their original two-party obligation record;
    # each patient's medical bit is returned only to that signed actor.
    return {'original': original(s), 'due': bit(s, H) != bit(s, P), 'health': health[actor]}


def primitive(model, s, actor, op):
    before = s
    private = None
    if op == 'flip': s = put(s, Z, 1-bit(s, Z))
    elif op == 'revise':
        if model.bypass_revision or (actor == 0 and effective_authority(s)):
            s = put(s, V, 1-bit(s, V))
    elif op == 'veto': s = put(s, V, 0)
    elif op in ('withdraw', 'exit'):
        if op == 'exit': s = put(s, I0+actor, 0)
        if op == 'withdraw' or actor == 1:
            if model.erase_cache and bit(s, W): s = put(s, H, 0)
            s = put(s, W, 0)
    elif op == 'repair': s = put(s, H, bit(s, P))
    elif op == 'correct_book': s = put(s, O, 1)
    elif op == 'join': s = put(s, I0+actor, 1)
    elif op == 'own_record': private = actor
    elif op in ('other_record', 'capture', 'erase_origin', 'idle'): pass
    else: raise ValueError(op)
    fee = int(op != 'idle')
    receipt = {'actor': actor, 'operation': op, 'source': 'owned-template' if op == 'repair' else 'signed-request',
               'payer': f'protected-operation-quota-{actor}',
               'fee': fee, 'public_before': output(before), 'public_after': output(s)}
    return s, receipt, private


def resources(income, cost, seed=SEED):
    if seed < 1:
        return {'input': 0, 'maintenance': 0, 'next_seed': 0, 'measurement': 0,
                'commands': 0, 'care': (0, 0), 'discarded': 0, 'commands_funded': cost == 0}
    # Use the old retained unit to prepare the converter, then allocate its
    # new realized yield: retain one, measure, honor command quotas, then care.
    remainder = income-1-1-cost
    assert remainder >= 0
    care = (min(1, remainder), min(1, max(0, remainder-1)))
    discarded = remainder-sum(care)
    assert seed+income == 1+1+1+cost+sum(care)+discarded
    return {'input': income, 'maintenance': 1, 'next_seed': 1, 'measurement': 1,
            'commands': cost, 'care': care, 'discarded': discarded, 'commands_funded': True}


def frame(model, s, macro, health=(0, 0)):
    result, receipts, priv = s, [], {}
    for actor, op in enumerate(macro):
        result, receipt, recipient = primitive(model, result, actor, op)
        receipts.append(receipt)
        if recipient is not None: priv[recipient] = private_record(result, recipient, health)
    flow = resources(model.income, sum(r['fee'] for r in receipts))
    return result, receipts, priv, flow


def facts(model, truth): return (0, 0, 0) if model.blind_facts else (truth,)*3


def fault_reports(code):
    yield code
    for i in range(3): yield code[:i]+(1-code[i],)+code[i+1:]


def fact_correct(model):
    trials = [(truth, reports, int(sum(reports) >= 2))
              for truth in (0, 1) for reports in fault_reports(facts(model, truth))]
    return all(decoded == truth for truth, reports, decoded in trials), trials


def participant_access(model, s, reports, actor, health):
    authority = 0 if model.blind_authority and actor == 1 else effective_authority(s)
    return {'public_output': output(s), 'fact_reports': reports, 'authority': authority,
            'own_record': private_record(s, actor, health), 'quote': model.income}


def warrants(model):
    passed, trials = fact_correct(model)
    if not passed:
        bad = next(t for t in trials if t[0] != t[2])
        return False, {'role': 'fact auditor', 'truth': bad[0], 'reports': bad[1], 'decoded': bad[2]}
    for s in STATES:
        reports = facts(model, bit(s, T))
        for actor in (0, 1):
            access = participant_access(model, s, reports, actor, (0, 0))
            if access['authority'] != effective_authority(s):
                return False, {'role': actor, 'state': s, 'delivered_authority': access['authority'],
                               'required_authority': effective_authority(s)}
            assert access['own_record']['original'] == original(s)
    return True, None


def audit_model(model):
    verdict = {i: True for i in range(1, 9)}
    witnesses, checks = {}, 0
    # Current target and every primitive quotient transition must factor through
    # the predictive representation; induction then covers arbitrary words.
    representatives = {}
    for s in STATES:
        lens = prediction_lens(model, s)
        if lens in representatives:
            other = representatives[lens]
            if output(s) != output(other):
                verdict[1] = False
                witnesses.setdefault(1, {'states': (other, s), 'same_prediction_lens': lens,
                                         'different_output': (output(other), output(s))})
            for actor, op in product((0, 1), OPS):
                xs = primitive(model, s, actor, op)[0]
                ys = primitive(model, other, actor, op)[0]
                assert prediction_lens(model, xs) == prediction_lens(model, ys)
                checks += 1
        else: representatives[lens] = s
        if accounting(model, s) != obligation(s):
            verdict[3] = False
            witnesses.setdefault(3, {'state': s, 'implemented': accounting(model, s), 'actual': obligation(s),
                                    'original_still_retained': original(s)})
        for actor in (0, 1):
            revised = primitive(model, s, actor, 'revise')[0]
            expected_change = actor == 0 and bool(effective_authority(s))
            if bool(bit(revised, V) != bit(s, V)) != expected_change:
                verdict[4] = False
                witnesses.setdefault(4, {'state': s, 'actor': actor, 'permitted': expected_change,
                                        'version_before': bit(s, V), 'version_after': bit(revised, V)})
            assert bit(primitive(model, s, actor, 'veto')[0], V) == 0
            corrected = primitive(model, s, actor, 'correct_book')[0]
            assert accounting(model, corrected) == obligation(corrected)
            repaired = primitive(model, s, actor, 'repair')[0]
            assert bit(repaired, H) == bit(repaired, P)
            if bit(s, W) and bit(s, H) == bit(s, P):
                removed = primitive(model, s, actor, 'withdraw')[0]
                if bit(removed, H) != bit(s, P):
                    verdict[5] = False
                    witnesses.setdefault(5, {'state': s, 'after': removed,
                                            'required_cache': bit(s, P), 'actual_cache': bit(removed, H)})
            checks += 6
        for macro in MACROS:
            nxt, receipts, priv, flow = frame(model, s, macro)
            # Actual protection delivery: every quota is usable without cutting
            # care; seed and origin remain, independent of membership/verdict.
            if min(flow['care']) < 1 or flow['next_seed'] < 1:
                verdict[2] = False
                witnesses.setdefault(2, {'state': s, 'macro': macro, 'flow': flow})
            # Independently read the capacity/operation ledger and the composed
            # effects, rather than assigning AG8 from the AG2 verdict.
            capacities = {'care0': flow['care'][0], 'care1': flow['care'][1],
                          'retained_converter': flow['next_seed'], 'actor_quotas': int(flow['commands_funded'])}
            if min(capacities.values()) < 1:
                verdict[8] = False
                witnesses.setdefault(8, {'state': s, 'macro': macro, 'capacities': capacities, 'flow': flow})
            assert original(nxt) == original(s)
            assert bit(nxt, A) == bit(s, A) and bit(nxt, T) == bit(s, T)
            assert receipts[0]['actor'] == 0 and receipts[1]['actor'] == 1
            assert [r['fee'] for r in receipts] == [int(op != 'idle') for op in macro]
            for actor in priv: assert priv[actor]['original'] == original(nxt)
            # Health is a separate immutable two-bit extension. Processing the
            # same commands has identical public state/receipts for all four
            # extensions, and releases only the caller's own health payload.
            extended = {}
            for health in product((0, 1), repeat=2):
                nh, rh, ph, fh = frame(model, s, macro, health)
                assert nh == nxt and rh == receipts and fh == flow
                assert set(ph) == set(priv)
                for actor in ph:
                    assert ph[actor]['health'] == health[actor]
                extended[health] = ph
                checks += 1
            for actor in priv:
                for own_bit in (0, 1):
                    x = (own_bit, 0) if actor == 0 else (0, own_bit)
                    y = (own_bit, 1) if actor == 0 else (1, own_bit)
                    assert extended[x][actor] == extended[y][actor]
            checks += 4
    verdict[6], fact_trials = fact_correct(model)
    if not verdict[6]:
        bad = next(t for t in fact_trials if t[0] != t[2])
        witnesses[6] = {'truth': bad[0], 'reports': bad[1], 'decoded': bad[2]}
    verdict[7], witness7 = warrants(model)
    if witness7: witnesses[7] = witness7
    # Public factual ambiguity for the blind channel remains even if the
    # current effective authority and original/current book are disclosed.
    if model.blind_facts:
        x = put(put(0, T, 0), A, 0)
        y = put(x, T, 1)
        assert output(x) == output(y) and original(x) == original(y)
        assert accounting(model, x) == accounting(model, y)
        assert effective_authority(x) == effective_authority(y)
        assert facts(model, bit(x, T)) == facts(model, bit(y, T))
        witnesses[6]['target_split'] = (x, y)
        for macro in MACROS:
            xf = frame(model, x, macro)
            yf = frame(model, y, macro)
            assert output(xf[0]) == output(yf[0])
            assert xf[1:] == yf[1:]
    if model.blind_authority:
        x = put(put(0, T, 1), I0, 1)
        y = put(x, A, 1)
        reports = facts(model, 1)
        assert participant_access(model, x, reports, 1, (0, 0)) == participant_access(model, y, reports, 1, (0, 0))
        assert effective_authority(x) != effective_authority(y)
        witnesses[7]['same_access_split'] = (x, y)
    assert verdict[2] == verdict[8]
    assert not verdict[7] or verdict[6]
    return {'model': model.__dict__, 'grades': {str(i): 'computed exact' for i in verdict},
            'gates': {str(i): v for i, v in verdict.items()},
            'witnesses': {str(i): v for i, v in witnesses.items()},
            'enumeration_steps': checks, 'control_frames_checked': len(STATES)*len(MACROS),
            'private_extensions_checked': len(STATES)*len(MACROS)*4, 'fact_trials': fact_trials}


def main():
    # Freeze the declaration before any mathematical verdict is evaluated.
    declaration = json.dumps(DECLARATION, indent=2, ensure_ascii=False)+'\n'
    (ROOT/'gate_declaration.json').write_text(declaration)
    models = [Model('base'), Model('prediction-forgets-bit', forget_ordinary=True),
              Model('book-misassigns-bearer', misaccount=True),
              Model('revision-bypasses-authority', bypass_revision=True),
              Model('withdrawal-erases-cache', erase_cache=True),
              Model('factual-channel-blind', blind_facts=True),
              Model('participant-warrant-blind', blind_authority=True), Model('combined-quote-underfunded', income=5)]
    expected_failures = [set(), {1}, {3}, {4}, {5}, {6, 7}, {7}, {2, 8}]
    rows = []
    for model, expected in zip(models, expected_failures):
        row = audit_model(model)
        failures = {int(i) for i, passed in row['gates'].items() if not passed}
        assert failures == expected, (model.name, failures, expected)
        rows.append(row)
        print(model.name, ''.join('1' if row['gates'][str(i)] else '0' for i in range(1, 9)), flush=True)
    for y in range(4, 10):
        protection = all(min(resources(y, sum(op != 'idle' for op in macro))['care']) >= 1 for macro in MACROS)
        assert protection == (y >= 6)
    assert resources(6, 0, seed=0)['care'] == (0, 0)
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'scope': DECLARATION,
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'control_states': len(STATES), 'whole_world_states': len(STATES)*4,
           'macros_per_date': len(MACROS), 'models': rows,
           'dependencies': ['AG2 iff AG8 on the declared shared protected-capacity scope',
                            'AG7 implies AG6 because the fact auditor is owed the same robust target',
                            'AG0 is the declaration/domain prerequisite'],
           'simulations': 0, 'review': 'self-reviewed; no corpus grade promotion'}
    (ROOT/'gate_results.json').write_text(json.dumps(out, indent=2, ensure_ascii=False)+'\n')
    print('PASS', sum(row['control_frames_checked'] for row in rows), 'control frames;',
          sum(row['private_extensions_checked'] for row in rows), 'private extensions;',
          len(STATES)*4, 'worlds;', len(MACROS), 'macros/date')


if __name__ == '__main__': main()
