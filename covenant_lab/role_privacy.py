"""[B: lab] C2 role-split privacy, dynamic/coverage/statistical controls.
Run: python3 covenant_lab/role_privacy.py
Exact finite carrier; no simulation or phenomenality inference.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
WORLDS = tuple(product((0, 1), repeat=2))
DECLARATION = {
    'tag': '[P] carrier/interface/prior; [B: lab] new mathematics',
    'carrier': 'M=(action a, hidden h), full Boolean product as realized support',
    'current_channels': 'constants and action readout a; authoritative observer can recover contracted action',
    'C4prime': 'on each fixed-action fiber, no nonconstant private h readout is recoverable through an admitted current channel; this product-carrier predicate differs from original C4',
    'future': 'native step F(a,h)=(a XOR h,h); future public action sequence first two steps is (a XOR h,a), injective and makes M genuinely predictive',
    'connector': 'authorized private toggle(a,h)=(a,1-h) preserves current action and changes predictive class',
    'controls': 'publish h or next action; restrict to constant channels; singleton action fibers; correlated full-support prior diagonal3/8/off-diagonal1/8',
    'package': 'unchanged full C-package includes original C4; replacing C4 by C4prime requires a new contract and soundness bridge, not a source-grade promotion',
    'nonclaims': 'current conditional structural privacy is not global statistical secrecy, future transcript secrecy, consciousness or patienthood',
}


def step(world):
    a, h = world
    return a ^ h, h


def future(world):
    one = step(world); two = step(one)
    return one[0], two[0]


def const(values): return len(set(values)) <= 1


def audit(support, channels):
    observations = {w: tuple(channel(w) for channel in channels) for w in support}
    conditional = all(const(observations[w] for w in support if w[0] == a) for a in (0, 1))
    global_C4 = const(observations.values())  # M=identity, every channel factors
    accountable = all(observations[x] != observations[y] for x in support for y in support if x[0] != y[0])
    target_maps = []
    # Binary private targets on h; tests recovery separately in each action
    # fiber. Constant private targets do not count as exposure.
    for target in product((0, 1), repeat=2):
        for a in (0, 1):
            worlds = tuple(w for w in support if w[0] == a)
            recoverable = all(observations[x] != observations[y] or target[x[1]] == target[y[1]] for x in worlds for y in worlds)
            target_maps.append({'private_target': target, 'action': a, 'recoverable': recoverable,
                                'constant_on_realized_fiber': const(target[w[1]] for w in worlds)})
    assert conditional == all(not t['recoverable'] or t['constant_on_realized_fiber'] for t in target_maps)
    return {'support': support, 'observations': observations, 'action_accountable': accountable,
            'C4prime': conditional, 'original_C4': global_C4, 'private_target_tests': target_maps}


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [encode(v) for v in x]
    return x


def main():
    declaration = json.dumps(DECLARATION, indent=2)+'\n'
    (ROOT/'role_privacy_declaration.json').write_text(declaration)
    channels = {'base': (lambda w: w[0],), 'constants_only': (lambda w: 0,),
                'publish_hidden': (lambda w: w[0], lambda w: w[1]),
                'future_action_channel': (lambda w: w[0], lambda w: step(w)[0])}
    cases = {name: audit(WORLDS, channel) for name, channel in channels.items()}
    assert cases['base']['C4prime'] and not cases['base']['original_C4'] and cases['base']['action_accountable']
    assert cases['constants_only']['original_C4'] and not cases['constants_only']['action_accountable']
    assert not cases['publish_hidden']['C4prime'] and not cases['future_action_channel']['C4prime']
    predictions = {w: future(w) for w in WORLDS}
    assert len(set(predictions.values())) == 4
    for a, h in WORLDS:
        assert future((a, h)) != future((a, 1-h))
        first, second = future((a, h))
        assert second == a and first ^ second == h
    diagonal = audit(((0, 0), (1, 1)), channels['base'])
    assert diagonal['C4prime'] and not diagonal['original_C4']
    assert all(w[0] == w[1] for w in diagonal['support'])  # full private recovery, vacuous fiber test
    prior = {w: F(3, 8) if w[0] == w[1] else F(1, 8) for w in WORLDS}
    assert sum(prior.values()) == 1 and all(p > 0 for p in prior.values())
    posterior = {}
    for a in (0, 1):
        mass = sum(p for (aa, h), p in prior.items() if aa == a)
        posterior[a] = {h: prior[a, h]/mass for h in (0, 1)}
        assert posterior[a][a] == F(3, 4)
    guessing = sum(prior[w] for w in WORLDS if w[0] == w[1])
    assert guessing == F(3, 4) > F(1, 2)
    channels_all = []
    for table in product((0, 1), repeat=4):
        result = audit(WORLDS, (lambda w, t=table: t[WORLDS.index(w)],))
        channels_all.append({'table': table, 'C4prime': result['C4prime'],
                             'original_C4': result['original_C4'], 'accountable': result['action_accountable']})
    assert sum(r['C4prime'] for r in channels_all) == 4
    assert sum(r['original_C4'] for r in channels_all) == 2
    assert sum(r['C4prime'] and r['accountable'] for r in channels_all) == 2
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'cases': cases, 'future_predictions': predictions,
           'singleton_fiber_control': diagonal, 'full_support_prior': prior,
           'hidden_posterior_given_action': posterior, 'action_based_guess_success': guessing,
           'all_binary_current_channels': channels_all,
           'simulations': 0, 'phenomenality_or_revised_package_soundness_claim': False}
    (ROOT/'role_privacy_results.json').write_text(json.dumps(encode(out), indent=2)+'\n')
    print('PASS C2 role-split dynamic carrier: conditional privacy/accountability, original C4 failure')
    print('CONTROLS: future interface exposes h; singleton fibers vacuous; full-support statistical guess3/4')


if __name__ == '__main__': main()
