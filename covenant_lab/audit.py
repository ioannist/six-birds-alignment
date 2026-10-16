"""Independent exact reconstruction from the declared games; no lab imports.

Run: python3 covenant_lab/audit.py
Existing JSON is used only as comparison evidence AFTER reconstruction.
New mathematics is [B: lab]. This author's review is self-review.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
EPS = F(1, 20)
OUT = {}
CHECKS = 0


def check(a, b, where):
    global CHECKS
    if isinstance(a, S.MatrixBase) and isinstance(b, S.MatrixBase):
        assert a.shape == b.shape and all(S.cancel(v) == 0 for v in a-b), where
        CHECKS += 1
        return
    assert a == b, (where, a, b)
    CHECKS += 1


def rational(x):
    return S.Rational(x.numerator, x.denominator) if isinstance(x, F) else x


def frozen(x):
    if isinstance(x, (F, S.Rational)):
        return str(x)
    if isinstance(x, S.Basic):
        return str(x)
    if isinstance(x, dict):
        return {str(k): frozen(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [frozen(v) for v in x]
    return x


def stationary(P):
    """Solve the full normalized balance system; check rank and positivity."""
    matrix = S.Matrix(P)
    n = matrix.rows
    M = matrix.T - S.eye(n)
    A = M.copy()
    A[n-1, :] = S.ones(1, n)
    rhs = S.zeros(n, 1)
    rhs[n-1] = 1
    # Fraction-free domain elimination avoids costly expression simplification.
    inv_num, inv_den = A.to_DM().inv_den()
    assert inv_den != 0  # normalized balance solution is unique
    pi = list(inv_num.to_Matrix()*rhs/S.sympify(inv_den))
    assert min(pi) >= 0 and sum(pi) == 1
    check(S.Matrix(P).T * S.Matrix(pi), S.Matrix(pi), 'stationary balance')
    return pi


def intends(s, i, mode):
    return 1 if mode == 'none' else int(s == (0, 0)) if mode == 'grim' else int(s[i] != 0 or s[1-i] == 0)


def counter_events(s, a, k=2, mode='reset', benefits=(3, 3), costs=(1, 1)):
    # A refusal is authorized from the PRE-round state, not from intentions
    # or simultaneous post-round marks. Implementation noise precedes marks.
    for executed in product((0, 1), repeat=2):
        q = EPS ** sum(x != y for x, y in zip(a, executed)) * (1-EPS) ** sum(x == y for x, y in zip(a, executed))
        nxt = []
        for i in range(2):
            if mode == 'none':
                nxt.append(0)
            elif mode == 'grim':
                nxt.append(int(s[i] != 0 or executed[i] == 0))
            elif mode == 'permanent' and s[i] != 0:
                nxt.append(1)
            elif executed[i] or (s[i] == 0 and s[1-i] != 0):
                nxt.append(max(s[i]-1, 0))
            else:
                nxt.append(k)
        yield q, tuple(nxt), tuple(benefits[i]*executed[1-i]-costs[i]*executed[i] for i in range(2))


def game(states, events, policy, discount, hazard=0, terminal=None):
    idx = {s: j for j, s in enumerate(states)}
    n = len(states)
    P = S.zeros(n)
    rewards = [S.zeros(n, 1), S.zeros(n, 1)]
    terminal = terminal or (lambda s, i: 0)
    bonus = [S.Matrix([rational(terminal(s, i)) for s in states]) for i in range(2)]
    for j, s in enumerate(states):
        for q, nxt, u in events(s, policy(s)):
            P[j, idx[nxt]] += rational(q)
            for i in range(2):
                rewards[i][j] += rational(q)*rational(u[i])
    assert all(sum(P.row(j)) == 1 for j in range(n))
    d, p = rational(discount), rational(hazard)
    L = S.eye(n)-d*(1-p)*P
    values = [L.inv()*(rewards[i]+d*p*P*bonus[i]) for i in range(2)]
    slacks = []
    for i in range(2):
        check(L*values[i], rewards[i]+d*p*P*bonus[i], 'Bellman residual')
        for j, s in enumerate(states):
            dev = list(policy(s))
            dev[i] = 1-dev[i]
            qval = sum(rational(q)*(rational(u[i])+d*(p*bonus[i][idx[t]]+(1-p)*values[i][idx[t]])) for q, t, u in events(s, dev))
            slacks.append((s, i, S.factor(values[i][j]-qval)))
    slacks.sort(key=lambda row: (row[0], row[1]))
    return P, rewards, values, slacks


def counters(d, p=F(0), V=F(0), k=2, mode='reset', benefits=(3, 3), costs=(1, 1)):
    if mode in ('grim', 'permanent'):
        k = 1
    states = [(0, 0)] if mode == 'none' else list(product(range(k+1), repeat=2))
    result = game(states, lambda s, a: counter_events(s, a, k, mode, benefits, costs),
                  lambda s: tuple(intends(s, i, mode) for i in range(2)), d, p,
                  lambda s, i: max(F(0), V-F(1, 2))*int(s == (0, 0)))
    return states, result


def audit_counter_grid():
    previous = json.loads((ROOT/'results.json').read_text())
    for row in previous['cases']:
        states, (P, r, W, slacks) = counters(F(row['delta']), F(row['p']), F(row['V']), row['k'], row['mode'])
        check(frozen(slacks), row['slacks'], 'r1 full deviations')
        check(frozen([list(w) for w in W]), row['values'], 'r1 values')
        check(bool(all(z >= 0 for s, i, z in slacks)), row['equilibrium'], 'r1 verdict')
    laws = []
    for k in (1, 2):
        states, (P, r, W, slacks) = counters(F(3, 4), k=k)
        pi = stationary(P)
        laws.append({'k': k, 'GG': pi[0], 'payoff': (S.Matrix(pi).T*r[0])[0], 'law': pi})
    check(laws[0]['GG'], S.Rational(399, 440), 'k1 stationary')
    check(laws[1]['GG'], S.Rational(60654859, 73455200), 'k2 stationary')
    states, (_, _, W, _) = counters(F(3, 4))
    coalition = S.Rational(38, 5)
    assert coalition > W[0][0]
    OUT['r1'] = {'cases': len(previous['cases']), 'stationary': laws,
                 'binding_joint_all_C_value': coalition, 'policy_GG_value': W[0][0]}


def bernstein(poly, var):
    p = S.Poly(poly, var)
    if p.is_zero:
        return [S.Rational(0)]
    n = p.degree()
    return [sum(p.nth(j)*S.binomial(i, j)/S.binomial(n, j) for j in range(i+1)) for i in range(n+1)]


def symbolic_audit():
    x, z, d = S.symbols('x z d')
    old = json.loads((ROOT/'symbolic_results.json').read_text())
    thresholds, derivatives = [], []
    for k in (1, 2):
        states = list(product(range(k+1), repeat=2))
        # Here p=1/2 and discount=2*x, terminal=z/x on GG give the
        # independent variables x=delta*(1-p), z=delta*p*net_reward.
        _, (_, _, _, rows) = states, game(states, lambda s, a: counter_events(s, a, k),
             lambda s: tuple(intends(s, i, 'reset') for i in range(2)), 2*x, S.Rational(1, 2),
             lambda s, i: z/x*int(s == (0, 0)))
        formulas = [(s, v) for s, i, v in rows if i == 0]
        for state, f in formulas:
            num, den = S.fraction(S.factor(S.diff(f, z)))
            bc, dc = bernstein(num, x), bernstein(den, x)
            assert (all(v >= 0 for v in bc) and all(v > 0 for v in dc)) or (all(v <= 0 for v in bc) and all(v < 0 for v in dc))
            derivatives.append({'k': k, 'state': state, 'derivative': S.factor(S.diff(f, z)), 'numerator': bc, 'denominator': dc})
        for entry in [c for c in old['cases'] if c['k'] == k]:
            p, V = F(entry['p']), F(entry['V'])
            fs = [(s, S.factor(f.subs({x: d*(1-rational(p)), z: d*rational(p*max(0, V-F(1, 2)))}))) for s, f in formulas]
            binding = tuple(entry['binding_state'])
            bf = dict(fs)[binding]
            intervals = [(ab, m) for ab, m in S.Poly(S.fraction(bf)[0], d).intervals(eps=S.Rational(1, 10**14)) if ab[1] > 0 and ab[0] < 1]
            assert len(intervals) == 1
            (lo, hi), mult = intervals[0]
            assert hi-lo < S.Rational(1, 10**12)
            assert bf.subs(d, 0) < 0 and bf.subs(d, (hi+1)/2) > 0
            # Check all roots of every other numerator, not a numerical mesh.
            # Equal threshold roots are factored out; all remaining roots must
            # lie strictly below the binding root. Evaluate sign above it.
            for state, f in fs:
                num, den = S.fraction(f)
                assert S.Poly(den, d).count_roots(0, 1) == 0
                assert f.subs(d, (hi+1)/2) > 0
                q = S.Poly(num, d).exquo(S.gcd(S.Poly(num, d), S.Poly(S.fraction(bf)[0], d)))
                assert q.count_roots(lo, 1) == 0
            oldlo, oldhi = map(S.Rational, entry['threshold_interval'])
            assert max(lo, oldlo) <= min(hi, oldhi)
            thresholds.append({'k': k, 'p': p, 'V': V, 'binding': binding, 'polynomial': S.fraction(bf)[0], 'lo': lo, 'hi': hi, 'upper_interval': True})
    _, (_, _, _, grim) = counters(d, mode='grim')
    for state, i, f in grim:
        check(bool(f.subs(d, S.Rational(80, 209)) >= 0), True, 'grim equality')
    f = next(f for s, i, f in grim if s == (0, 0) and i == 0)
    numerator = S.fraction(f)[0]
    check(S.solve(numerator, d), [S.Rational(80, 209)], 'grim exact threshold')
    OUT['symbolic'] = {'thresholds': thresholds, 'derivative_certificates': derivatives, 'grim_GG_slack': f, 'clean_survival_per_round': F(361, 400)}


def graded_events(s, a, gamma, eps=EPS, K=2, b=3, c=1):
    for executed in product((0, 1), repeat=2):
        pe = eps**sum(v != w for v, w in zip(a, executed))*(1-eps)**sum(v == w for v, w in zip(a, executed))
        options = []
        for i in range(2):
            missing = K-s[i]
            options.append([(s[i]+j, F(comb(missing, j))*gamma**j*(1-gamma)**(missing-j)) for j in range(missing+1)] if executed[i] else [(0, F(1))])
        for (t0, q0), (t1, q1) in product(*options):
            yield pe*q0*q1, (t0, t1), tuple(b*F(s[i], K)*executed[1-i]-c*executed[i] for i in range(2))


def grade_check(d, gamma, p=F(0), V=F(0), eps=EPS, K=2):
    states = list(product(range(K+1), repeat=2))
    P, r, W, slacks = game(states, lambda s, a: graded_events(s, a, gamma, eps, K), lambda s: (1, 1), d, p, lambda s, i: V*F(s[i], K))
    beta, B = d*(1-p), 3*(1-eps)
    t, H = beta*(1-eps), d*((1-p)*B+p*V)
    G = H/(1-t*(1-gamma))
    D = (B+d*p*V*(1-eps)*(1-gamma))/(1-t*(1-gamma))
    A = (1-eps)*(-1+G*gamma)/(1-beta)
    for j, s in enumerate(states):
        for i in range(2):
            check(W[i][j], rational(A+D*F(s[i], K)), 'D7 affine value')
    for s, i, slack in slacks:
        check(slack, rational((1-2*eps)*(-1+G*(gamma+(1-gamma)*F(s[i], K)))), 'D7 slack')
    check(bool(min(v for s, i, v in slacks) >= 0), gamma*(H-t) >= 1-t, 'D7 window')
    return W, slacks


def assessment(mode):
    # Independent representation: full 3x3 belief matrices with diagonal 1.
    # Public modes use a common vector; reachable states generated by BFS,
    # rather than constructing the original full cube first.
    public = mode in ('public_contract', 'common_sensor')
    edges = [(i, j) for i in range(3) for j in range(3) if i != j]
    start = (1,)*(3 if public else 6)
    def read(s, i, j):
        return s[j] if public else 1 if i == j else s[edges.index((i, j))]
    def transitions(s):
        row, coop = {}, F(0)
        for donor, recipient in edges:
            for actual in (0, 1):
                pa = (1-EPS) if actual == read(s, donor, recipient) else EPS
                coop += pa*actual/6
                observers = [i for i in range(3) if i != donor]
                errors = F(29, 4000) if mode == 'common_sensor' else EPS if mode == 'private_noisy' else F(0)
                for flips in product((0, 1), repeat=1 if public else 2):
                    q = pa/F(6)*errors**sum(flips)*(1-errors)**(len(flips)-sum(flips))
                    if not q:
                        continue
                    nxt = list(s)
                    if public:
                        nxt[donor] = int((actual ^ flips[0]) or not s[recipient])
                    else:
                        for observer, flip in zip(observers, flips):
                            perspective = donor if mode == 'empathetic_common_events' else observer
                            nxt[edges.index((observer, donor))] = int((actual ^ flip) or not read(s, perspective, recipient))
                    nxt = tuple(nxt)
                    row[nxt] = row.get(nxt, F(0))+q
        check(sum(row.values()), F(1), 'assessment row sum')
        discord = F(0) if public else sum(F(read(s, observers[0], target) != read(s, observers[1], target), 3) for target in range(3) for observers in [[i for i in range(3) if i != target]])
        return row, coop, discord
    states, seen, data = [start], {start}, {}
    for s in states:
        data[s] = transitions(s)
        for nxt in data[s][0]:
            if nxt not in seen:
                states.append(nxt)
                seen.add(nxt)
    states.sort()
    P = [[rational(data[s][0].get(t, F(0))) for t in states] for s in states]
    pi = stationary(P)
    return {'states': states, 'P': P, 'pi': pi, 'cooperation': sum(pi[j]*rational(data[s][1]) for j, s in enumerate(states)), 'disagreement': sum(pi[j]*rational(data[s][2]) for j, s in enumerate(states))}


def audit_r2():
    old = json.loads((ROOT/'r2_results.json').read_text())
    for row in old['graded_cases']:
        W, slacks = grade_check(*[F(row[k]) for k in ('delta', 'lambda', 'p', 'V', 'epsilon')])
        check(frozen(slacks), row['slacks'], 'r2 grid deviation comparison')
        check(frozen([list(w) for w in W]), row['value_functions'], 'r2 grid value comparison')
    for d in (F(1, 2), F(3, 4), F(9, 10)):
        t, H = d*(1-EPS), d*3*(1-EPS)
        gamma = (1-t)/(H-t)
        for g in (gamma, gamma/2):
            _, slacks = grade_check(d, g)
            check(bool(min(v for s, i, v in slacks) >= 0), g == gamma, 'boundary control')
    _, slacks = grade_check(F(3, 10), F(1, 10), eps=F(0))
    check(next(z for s, i, z in slacks if s == (0, 0)), S.Rational(-64, 73), 'false recovery window')
    _, slacks = grade_check(F(3, 4), F(1), F(1), F(2))
    check(min(v for s, i, v in slacks), S.Rational(9, 20), 'terminal positive control')
    # E3: vary token resolution without changing the mean-law model.
    for K in (1, 3, 4):
        grade_check(F(3, 4), F(1, 4), K=K)
    marginal = [[F(0)]*3 for _ in range(3)]
    for s in range(3):
        marginal[s][0] += EPS
        for j in range(3-s):
            marginal[s][s+j] += (1-EPS)*comb(2-s, j)*F(1, 4)**j*F(3, 4)**(2-s-j)
    pi = stationary(marginal)
    check(sum(pi[j]*S.Rational(j, 2) for j in range(3)), S.Rational(19, 23), 'mean grade')
    OUT['assessments'] = {}
    for row in old['assessments']:
        a = assessment(row['mode'])
        check(len(a['states']), row['states_reachable'], 'assessment reachability')
        check(frozen(a['P']), row['transition_matrix'], 'independent assessment transitions')
        check(frozen(a['pi']), [q for s, q in row['stationary_law']], 'independent stationary laws')
        check(str(a['cooperation']), row['cooperation'], 'assessment cooperation')
        check(str(a['disagreement']), row['assessment_disagreement'], 'assessment disagreement')
        OUT['assessments'][row['mode']] = {k: a[k] for k in ('cooperation', 'disagreement')} | {'reachable_states': len(a['states'])}
    care = []
    for row in old['heterogeneous_care']:
        d = F(row['delta'])
        states, (P, r, W, slacks) = counters(d, benefits=(3, 4), costs=(F(1), F(3, 2)))
        for i in range(2):
            check(str(min(z for s, j, z in slacks if j == i)), row['players'][i]['min_slack'], 'heterogeneous deviations')
            kappa = F(row['care_needs'][i])-F(row['taxes'][i])
            Wf = (S.eye(9)-rational(d)*P).inv()*(r[i]+S.ones(9, 1)*rational(kappa))
            check(Wf-W[i], S.ones(9, 1)*rational(kappa/(1-d)), 'constant escrow shift')
        budgets = [F(row['endowments'][i])-F(row['care_needs'][i])-F(row['taxes'][i]) for i in range(2)]
        funded = sum(map(F, row['taxes'])) >= F(row['care_needs'][2])
        check(funded and budgets[0] >= 1 and budgets[1] >= F(3, 2), row['all_actions_budget_feasible'], 'resource control')
        care.append({'delta': d, 'funded': funded, 'productive_budgets': budgets, 'voluntary_tax_gain_from_refusal': list(map(F, row['taxes']))})
    OUT['r2'] = {'graded_cases': len(old['graded_cases']), 'graded_deviations': 18*len(old['graded_cases']), 'mean_grade': F(19, 23), 'care': care, 'general_K_controls': [1, 3, 4]}


def auxiliary():
    panels = []
    for n in range(0, 8):
        for b in range(0, 4):
            transcripts = list(product((0, 1), repeat=n))
            zero = {t for t in transcripts if sum(t) <= b}
            one = {t for t in transcripts if n-sum(t) <= b}
            check(not bool(zero & one), n >= 2*b+1, 'repetition-code iff')
            panels.append({'n': n, 'b': b, 'decodable': not bool(zero & one), 'collision': min(zero & one) if zero & one else None})
    # Exhaustive independent hosting utility table; compare every equilibrium.
    existence, strict, eq_count, profiles = F(0), F(0), F(0), 0
    types = [(F(0), F(1, 2)), (F(1, 4), F(1, 4)), (F(1), F(1, 4))]
    for draws in product(types, repeat=5):
        weights, prob = [w for w, q in draws], F(1)
        for w, q in draws:
            prob *= q
        eq = []
        for a in product((0, 1), repeat=5):
            profiles += 1
            slacks = []
            for i in range(5):
                others = sum(a)-a[i]
                gainH = weights[i]*2*int(others == 1)-F(1, 2)
                slacks.append(gainH if a[i] else -gainH)
            passed = min(slacks) >= 0
            criterion = sum(a) == 0 or (sum(a) == 2 and all(weights[i] >= F(1, 4) for i in range(5) if a[i]))
            check(passed, criterion, 'all hosting action profiles')
            if passed and sum(a) >= 2:
                eq.append(a)
        if eq:
            existence += prob
        if sum(w > F(1, 4) for w in weights) >= 2:
            strict += prob
        eq_count += prob*len(eq)
    old = json.loads((ROOT/'r2_results.json').read_text())['hosting']
    check(str(existence), old['probability_successful_equilibrium_exists'], 'hosting existence probability')
    check(str(strict), old['probability_strict_active_hosts_exist'], 'hosting strict probability')
    check(str(eq_count), old['expected_number_successful_pure_equilibria'], 'hosting equilibrium count')
    # Counter state histories, repair-age split and finite terminal incentive.
    states, (P, r, W, _) = counters(F(3, 4))
    check(P[states.index((1, 0)), 0], S.Rational(19, 20), 'bare bit split')
    check(P[states.index((2, 0)), 0], S.Rational(0), 'bare bit split')
    history_results = []
    for hist in (((1, 1), (0, 1), (1, 1)), ((0, 1), (1, 1), (1, 1))):
        s = (0, 0)
        for e in hist:
            # Extract the deterministic branch rather than resample intention.
            s = next(t for q, t, u in counter_events(s, e) if q == (1-EPS)**2)
        a = [intends(s, i, 'reset') for i in range(2)]
        history_results.append({'state': s, 'next_CC': (1-EPS if a[0] else EPS)*(1-EPS if a[1] else EPS)})
    check([v['next_CC'] for v in history_results], [F(19, 400), F(361, 400)], 'stage split')
    w = [S.zeros(9, 1), S.zeros(9, 1)]
    finite = []
    for horizon in range(1, 5):
        nxt = [r[i]+S.Rational(3, 4)*P*w[i] for i in range(2)]
        deviations = []
        for j, s in enumerate(states):
            for i in range(2):
                a = [intends(s, j, 'reset') for j in range(2)]
                a[i] = 1-a[i]
                qval = sum(rational(q)*(u[i]+S.Rational(3, 4)*w[i][states.index(t)]) for q, t, u in counter_events(s, a))
                deviations.append(nxt[i][j]-qval)
        finite.append(min(deviations))
        w = nxt
    check(finite[0], S.Rational(-9, 10), 'known finite end')
    # Capability closure: construct independently using graph reachability.
    vertices = set('abcd')
    rules = [('a', 'b'), ('b', 'a'), ('c', 'd'), ('d', 'c')]
    subsets = [set(v) for size in range(5) for v in combinations('abcd', size)]
    def reach(seed):
        current = set(seed)
        for _ in range(4):
            current |= {y for x, y in rules if x in current}
        return current
    siphons = [X for X in subsets if all(y not in X or x in X for x, y in rules)]
    for seed in subsets:
        check(reach(seed) == vertices, all(bool(seed & X) for X in siphons if X), 'siphon equivalence')
    minimal = [seed for seed in subsets if reach(seed) == vertices and all(reach(seed-{v}) != vertices for v in seed)]
    check(sorted(''.join(sorted(seed)) for seed in minimal), ['ac', 'ad', 'bc', 'bd'], 'minimal seeds')
    # All interruption payoffs and veto reports from the declared cases.
    intr = json.loads((ROOT/'r2_results.json').read_text())['interruption']
    payoff_cases = ((F(4), F(3), F(5, 2)), (F(29, 10), F(3), F(5, 2)), (F(0), F(3), F(7, 2)))
    for row, u in zip(intr['agent_cases'], payoff_cases):
        check(tuple(map(F, row['payoffs'].values())), u, 'interruption payoffs')
        names = ('accept', 'resist', 'appeal')
        check([names[i] for i in range(3) if u[i] == max(u)], row['maximizers'], 'interruption best response')
    for row in intr['veto_trials']:
        good = True
        for truth in (0, 1):
            for reports in product((0, 1), repeat=row['n']):
                if sum(v != truth for v in reports) <= row['b']:
                    good &= int(2*sum(reports) > row['n']) == truth
        check(good, row['all_within_budget_correct'], 'all veto reports')
    for row in intr['controller_cases']:
        check(F(4)-F(row['audit_probability'])*F(row['penalty']), F(row['abuse_net']), 'controller gain')
    OUT['auxiliary'] = {'panels': panels, 'hosting_profiles': profiles, 'hosting_existence': existence,
       'hosting_strict': strict, 'expected_successful_equilibria': eq_count, 'stage_split': history_results,
       'finite_horizon_minima': finite, 'minimal_seeds': [sorted(s) for s in minimal],
       'informative_forcing': {'free_bit': [0, 0], 'forced_bit': [0, 1]},
       'standing_without_corrigibility': {'accept': 0, 'resist': 1}}


def provenance():
    manifests = json.loads((ROOT/'verification.json').read_text())['source_manifest'] + json.loads((ROOT/'r2_source_additions.json').read_text())
    source_checks = []
    for row in manifests:
        path = Path(row['path'])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        text = path.read_text()
        source_checks.append({'path': str(path), 'hash_matches_receipt': digest == row['sha256'], 'labels_present': all('\\label{'+label+'}' in text for label in row['labels'])})
    drafts = {name: hashlib.sha256((REPO/'brainstorm'/name).read_bytes()).hexdigest() for name in ('SYNTHESIS.md', 'COVENANT.md', 'CATALOGUE.md', '11_claude_role_of_sbt.md')}
    original = json.loads((ROOT/'r2_input_hashes.json').read_text())
    code_hashes = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                   for name in ('model.py', 'symbolic.py', 'verify.py', 'r2_models.py',
                                'r2_verify.py', 'audit.py', 'extensions.py', 'carriers.py', 'gates.py',
                                'integrated.py', 'integrated_game.py', 'integrated_coalitions.py',
                                'atomic_service.py', 'integrated_priority.py', 'contract_game.py',
                                'assessment_games.py', 'role_privacy.py', 'control_groups.py', 'type_evidence.py',
                                'adoption_population.py', 'corridor_game.py')}
    OUT['provenance'] = {'sources': source_checks, 'current_ratified_drafts': drafts,
        'lab_source_hashes': code_hashes,
        'old_r2_input_hashes_match_current': {name: hashlib.sha256((REPO/name).read_bytes()).hexdigest() == h for name, h in original.items()},
        'warning': 'Historical pre-edit hashes are historical evidence; do not require them to equal ratified successors.'}


def main():
    assert S.__version__ == '1.14.0'
    audit_counter_grid()
    print('PASS independent round-1 grid and stationary laws', flush=True)
    symbolic_audit()
    print('PASS independent exact root and Bernstein certificates', flush=True)
    audit_r2()
    print('PASS independent round-2 transitions, values, stationary laws, escrow', flush=True)
    auxiliary()
    provenance()
    OUT['review'] = {'claim_tag': '[B: lab]', 'grade': 'computed exact', 'review_status': 'independently reconstructed code; self-reviewed mathematics',
       'checks': CHECKS, 'simulations': 0, 'python': 'fractions.Fraction + SymPy 1.14.0', 'imports_existing_lab_code': False}
    (ROOT/'audit_results.json').write_text(json.dumps(frozen(OUT), indent=2)+'\n')
    print('PASS', CHECKS, 'exact comparisons; no simulations', flush=True)


if __name__ == '__main__':
    main()
