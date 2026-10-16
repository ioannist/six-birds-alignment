"""[B: lab] D8 donation-game incentives for the five declared assessment laws.
Run: python3 covenant_lab/assessment_games.py
Independent law reconstruction; exact arithmetic, no simulations.
Private full-state slacks are diagnostic only. Observable private deviations
are evaluated from the publicly specified all-good initial prior.
"""
from fractions import Fraction as F
from itertools import product
from collections import deque
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
EDGES = tuple((i, j) for i in range(3) for j in range(3) if i != j)
EDGE = {pair: k for k, pair in enumerate(EDGES)}
MODES = ('private_noisy', 'common_events_only', 'public_contract', 'common_sensor', 'empathetic_common_events')
EPS, OBS, SENSOR = F(1, 20), F(1, 20), F(29, 4000)
B, C, DELTA = F(3), F(1), F(3, 4)
DECLARATION = {
    'tag': '[P] game/information hypotheses; [B: lab] mathematical results',
    'payoff_chosen_before_incentives': 'one uniformly chosen ordered donor/recipient pair/date; actual executed C gives recipient3 and costs donor1; D gives0; common discount3/4; no moral utility or assessment cost added',
    'timing': 'ordered pair observed before donor intent; independent implementation flip1/20; payoffs from actual execution; assessment update then next date',
    'rule': 'simple-standing-style: observer labels donor good iff observed C OR its specified recipient assessment is bad; not Stern judging and not a literature replication',
    'initial': 'all-good labels; self assessments fixed good; carrier closed under BOTH donor intents and all positive-probability observation outcomes',
    'public_contract': '3 public eligibility bits; actual C observed; update donor good iff C or public recipient bad',
    'common_sensor': 'same public bits; common action report independently wrong29/4000; recipient eligibility read correctly; private actual payoff observations reveal no persistent hidden state',
    'common_events_only': '6 observer->other bits; all executed actions public and initial/rules known, so entire assessment matrix reconstructible from public history despite private interpretation',
    'empathetic_common_events': 'same common action facts; observer update uses DONOR recipient assessment; consensus carrier from all-good is invariant under every intent, equivalent to public-contract dynamics',
    'private_noisy': 'each non-donor privately observes actual action with independent flip1/20; actor sees its own row/own signals and current pair, not others rows; no clairvoyant full-state verdict allowed',
    'deviations': 'public/reconstructible laws: every selected donor C/D at every closed-carrier state. Private law: predefined observable stationary policies for actor0, others original; exact initial-prior returns, not perfect Bayesian certification from hidden-state diagnostics.',
    'parameters': {'b': '3', 'c': '1', 'discount': '3/4', 'implementation': '1/20', 'private_observation': '1/20', 'common_sensor': '29/4000'},
    'nonclaims': 'no subjective moral legitimacy/calibration/people experiment, population ESS or private-history equilibrium from label balance',
}


def public(mode): return mode in ('public_contract', 'common_sensor')


def read(mode, state, observer, target):
    if public(mode): return state[target]
    return 1 if observer == target else state[EDGE[observer, target]]


def prescribed(mode, state, donor, recipient): return read(mode, state, donor, recipient)


def outcomes(mode, state, donor, recipient, intention):
    for executed in (0, 1):
        qa = 1-EPS if executed == intention else EPS
        reward = [F(0)]*3
        reward[donor], reward[recipient] = -C*executed, B*executed
        if public(mode):
            error = SENSOR if mode == 'common_sensor' else F(0)
            for flip in (0, 1):
                q = qa*(error if flip else 1-error)
                if not q: continue
                reported = executed ^ flip
                nxt = list(state)
                nxt[donor] = int(bool(reported) or not state[recipient])
                yield q, tuple(nxt), tuple(reward)
        else:
            observers = tuple(i for i in range(3) if i != donor)
            error = OBS if mode == 'private_noisy' else F(0)
            for flips in product((0, 1), repeat=2):
                q, nxt = qa, list(state)
                for observer, flip in zip(observers, flips):
                    q *= error if flip else 1-error
                    perspective = donor if mode == 'empathetic_common_events' else observer
                    seen = executed ^ flip
                    nxt[EDGE[observer, donor]] = int(bool(seen) or not read(mode, state, perspective, recipient))
                if q: yield q, tuple(nxt), tuple(reward)


def carrier(mode):
    initial = (1,)*(3 if public(mode) else 6)
    seen, todo = {initial}, deque([initial])
    while todo:
        state = todo.popleft()
        for donor, recipient in EDGES:
            for intention in (0, 1):
                for q, nxt, reward in outcomes(mode, state, donor, recipient, intention):
                    if nxt not in seen: seen.add(nxt); todo.append(nxt)
    return tuple(sorted(seen))


def build(mode, states, deviation=None):
    index = {s: i for i, s in enumerate(states)}
    P, rewards = [], []
    for state in states:
        row, reward = [F(0)]*len(states), [F(0)]*3
        for donor, recipient in EDGES:
            intended = prescribed(mode, state, donor, recipient) if deviation is None or donor != 0 else deviation(state, recipient)
            for q, nxt, rr in outcomes(mode, state, donor, recipient, intended):
                row[index[nxt]] += q/6
                for i in range(3): reward[i] += q*rr[i]/6
        assert sum(row) == 1
        P.append(row); rewards.append(reward)
    return P, rewards, index


def rat(x): return S.Rational(x.numerator, x.denominator)


def solve(P, rewards, discount=DELTA):
    matrix = S.eye(len(P))-rat(discount)*S.Matrix([[rat(x) for x in row] for row in P])
    v = matrix.inv(method='DM')*S.Matrix([[rat(x) for x in row] for row in rewards])
    W = [[F(v[j, i]) for j in range(len(P))] for i in range(3)]
    for i in range(3):
        for j in range(len(P)):
            assert W[i][j] == rewards[j][i]+discount*sum(q*W[i][k] for k, q in enumerate(P[j]))
    return W


def slacks(mode, states, W, index, discount=DELTA):
    rows = []
    for state in states:
        for donor, recipient in EDGES:
            a = prescribed(mode, state, donor, recipient)
            values = []
            for intention in (0, 1):
                values.append(sum(q*(rr[donor]+discount*W[donor][index[nxt]])
                                  for q, nxt, rr in outcomes(mode, state, donor, recipient, intention)))
            rows.append({'state': state, 'donor': donor, 'recipient': recipient, 'prescribed': a,
                         'slack': values[a]-values[1-a]})
    return rows


def public_formula(error):
    d = S.Symbol('d', real=True)
    eps, nu = rat(EPS), rat(error)
    eta = eps+(1-2*eps)*nu
    q = 1-2*eps
    A, D = 1-2*d/3, 1-2*d/3+d*eta/6
    det = S.factor(A*D-d*d*eta*eta/18)
    x = S.factor(q*(rat(B)*D/3+d*eta*rat(C)/18)/det)
    y = S.factor(-q*(rat(C)*A/6+d*eta*rat(B)/18)/det)
    constant = S.factor((eps*(rat(B)-rat(C))/3+d*(x+2*y)/3)/(1-d))
    margin = S.factor(d*(1-2*nu)*x-rat(C))
    numerator, denominator = S.fraction(margin)
    roots = S.Poly(numerator, d).intervals(eps=S.Rational(1, 10**13))
    interior = [(interval, multiplicity) for interval, multiplicity in roots if 0 < interval[0] < interval[1] < 1]
    assert len(interior) == 1
    lo, hi = interior[0][0]
    assert numerator.subs(d, lo) < 0 < numerator.subs(d, hi)
    assert S.Poly(numerator, d).degree() == 2
    # Exact derivative minimum on [0,1] for this quadratic and positive
    # denominator factors: no floating point classifies a sign or a root.
    derivative = S.diff(numerator, d)
    assert min(derivative.subs(d, 0), derivative.subs(d, 1)) > 0
    assert numerator.subs(d, 0) < 0 < numerator.subs(d, 1)
    assert det == (1-d*(2-eta)/3)*(1-d*(4+eta)/6).expand() or S.expand(det-(1-d*(2-eta)/3)*(1-d*(4+eta)/6)) == 0
    return {'observation_error': error, 'effective_bad_report': F(eta),
            'x': x, 'y': y, 'constant': constant, 'promotion_margin': margin,
            'binding_numerator': numerator, 'denominator': denominator,
            'threshold_isolation': (F(lo), F(hi)), 'root_multiplicity': interior[0][1]}, (d, x, y, constant)


def private_deviations(states, baseline, initial, index):
    def bits(s, recipient):
        other = 3-recipient  # donor0, recipients1/2
        return read('private_noisy', s, 0, recipient), read('private_noisy', s, 0, other)
    policies = {
        'always_C': lambda s, r: 1,
        'always_D': lambda s, r: 0,
        'opposite_recipient': lambda s, r: 1-bits(s, r)[0],
        'both_good_only': lambda s, r: int(all(bits(s, r))),
        'either_good': lambda s, r: int(any(bits(s, r))),
        'other_only': lambda s, r: bits(s, r)[1],
        'help_when_both_bad': lambda s, r: int(bits(s, r)[0] or not bits(s, r)[1]),
        'recipient1_only': lambda s, r: int(r == 1),
        'recipient2_only': lambda s, r: int(r == 2),
    }
    results = []
    for name, policy in policies.items():
        P, rewards, _ = build('private_noisy', states, deviation=policy)
        W = solve(P, [[r[0]]*3 for r in rewards])[0]
        gain = W[index[initial]]-baseline[0][index[initial]]
        table = []
        for ownrow in product((0, 1), repeat=2):
            s = [1]*6
            s[EDGE[0, 1]], s[EDGE[0, 2]] = ownrow
            table.append({'own_row_to1_to2': ownrow, 'intent_to1': policy(s, 1), 'intent_to2': policy(s, 2)})
        results.append({'policy': name, 'observation_feasible': True, 'table': table,
                        'initial_value': W[index[initial]], 'initial_gain': gain})
    return results


def common_history_witness(W, index):
    state, probability, trace = (1,)*6, F(1), []
    for donor, recipient in ((0, 1), (2, 1), (1, 0)):
        intention = prescribed('common_events_only', state, donor, recipient)
        options = [(q, nxt) for q, nxt, reward in outcomes('common_events_only', state, donor, recipient, intention)
                   if reward[donor] == 0]
        assert len(options) == 1
        q, nxt = options[0]
        probability *= q/6
        trace.append({'state_before': state, 'donor': donor, 'recipient': recipient,
                      'intention': intention, 'public_executed_action': 0,
                      'event_probability': q/6, 'state_after': nxt})
        state = nxt
    assert state == (0, 0, 0, 0, 0, 1) and probability == F(19, 1728000)
    donor, recipient = 0, 1
    qq = []
    for a in (0, 1):
        qq.append(sum(q*(reward[donor]+DELTA*W[donor][index[nxt]])
                      for q, nxt, reward in outcomes('common_events_only', state, donor, recipient, a)))
    gain = qq[1]-qq[0]
    assert gain == F(404653, 1138590) > 0
    initial_gain = probability*F(1, 6)*DELTA**3*gain
    assert initial_gain > 0
    return {'public_trace': trace, 'trace_probability': probability, 'target_pair': (donor, recipient),
            'one_shot_C_gain': gain, 'triggered_initial_gain': initial_gain,
            'strategy': 'deviate only at date3/pair0->1 following these three public events; otherwise original policy',
            'hidden_assessment_access_needed': False}


def encode(x):
    if isinstance(x, (F, S.Basic)): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [encode(v) for v in x]
    return x


def main():
    declaration = json.dumps(DECLARATION, indent=2)+'\n'
    (ROOT/'assessment_game_declaration.json').write_text(declaration)
    old = {row['mode']: row for row in json.loads((ROOT/'r2_results.json').read_text())['assessments']}
    results = []
    for mode in MODES:
        states = carrier(mode)
        P, rewards, index = build(mode, states)
        assert [[str(q) for q in row] for row in P] == old[mode]['transition_matrix']
        W = solve(P, rewards)
        rows = slacks(mode, states, W, index)
        minimum = min(rows, key=lambda row: row['slack'])
        result = {'mode': mode, 'states': states, 'transition': P, 'stage_rewards': rewards, 'values': W,
                  'all_selected_donor_slacks': rows, 'minimum': minimum,
                  'full_state_information_available': mode != 'private_noisy'}
        if mode in ('public_contract', 'common_sensor', 'empathetic_common_events'):
            formula, (d, x, y, constant) = public_formula(SENSOR if mode == 'common_sensor' else F(0))
            for actor in range(3):
                for state in states:
                    if public(mode): g, k = state[actor], sum(state)-state[actor]
                    else:
                        labels = [read(mode, state, (i+1)%3, i) for i in range(3)]
                        assert all(read(mode, state, (i+2)%3, i) == labels[i] for i in range(3))
                        g, k = labels[actor], sum(labels)-labels[actor]
                    expected = (constant+x*g+y*k).subs(d, rat(DELTA))
                    assert F(expected) == W[actor][index[state]]
                    lhs = constant+x*g+y*k
                    continued = F(0)
                    for j, nxt in enumerate(states):
                        if public(mode): ng, nk = nxt[actor], sum(nxt)-nxt[actor]
                        else:
                            nl = [read(mode, nxt, (t+1)%3, t) for t in range(3)]
                            ng, nk = nl[actor], sum(nl)-nl[actor]
                        continued += rat(P[index[state]][j])*(constant+x*ng+y*nk)
                    assert S.cancel(lhs-rat(rewards[index[state]][actor])-d*continued) == 0
            result['symbolic_formula'] = formula
            result['symbolic_bellman_identities_checked'] = 3*len(states)
            result['markov_perfect_at_discount'] = minimum['slack'] >= 0
        elif mode == 'common_events_only':
            result['markov_perfect_at_discount'] = minimum['slack'] >= 0
            result['public_initial_nash_refutation'] = common_history_witness(W, index)
        else:
            initial = (1,)*6
            result['private_observable_deviations'] = private_deviations(states, W, initial, index)
            result['private_nash_refuted_by_feasible_policy'] = any(z['initial_gain'] > 0 for z in result['private_observable_deviations'])
            result['full_state_slacks_are_private_equilibrium_verdict'] = False
            best = next(z for z in result['private_observable_deviations'] if z['policy'] == 'help_when_both_bad')
            assert F(1, 2500) < best['initial_gain'] < F(1, 2000)
            result['feasible_policy_gain_interval'] = (F(1, 2500), F(1, 2000))
        results.append(result)
        print(mode, 'states', len(states), 'full-state diagnostic minimum', minimum['slack'])
        if mode == 'private_noisy':
            for z in result['private_observable_deviations']: print('observable', z['policy'], 'gain', z['initial_gain'])
        elif 'symbolic_formula' in result: print('threshold numerator', result['symbolic_formula']['binding_numerator'])
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'original_transition_sha256': hashlib.sha256((ROOT/'r2_results.json').read_bytes()).hexdigest(),
           'results': results, 'simulations': 0}
    (ROOT/'assessment_game_results.json').write_text(json.dumps(encode(out), indent=2)+'\n')


if __name__ == '__main__': main()
