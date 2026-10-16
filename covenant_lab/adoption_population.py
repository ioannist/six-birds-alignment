"""[B: lab] D14 exact finite-person adoption, entry and founder withdrawal.
Run: python3 covenant_lab/adoption_population.py
The myopic update is declared. Absorption/stationary laws are exact, not samples
or equilibrium claims about forward-looking people.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
DECLARATION = {
    'tag': '[P] matching/update/cost/control/funding hypotheses; [B: lab] mathematics',
    'population': 'N fixed productive/self-supported actors, binary participation, each other actor equally likely match; no self match; care/protected outsider support independent of optional participation and founder subsidy',
    'stage_payoff': 'adopter matched to adopter gets a, participation costs c, founder subsidy s per active adopter/date; nonadopter0; new participation additionally pays entry fee e once, exit0, re-entry pays e again',
    'timing': 'uniform random focal actor first compares current expected matching payoff with a unilateral change, then next membership counted; tie retains membership; matching/noise/utility are not inferred from SBT labels',
    'choice': 'myopic expected one-date strict best response; future known withdrawal/discounted learning not considered by this update. Not a Markov-perfect or empirical learning theorem.',
    'margins': 'incumbent keep-minus-exit = a*(k-1)/(N-1)-c+s; outsider join-minus-stay = a*k/(N-1)-c+s-e; entry and participation costs separate',
    'noise': 'optional independent choice tremble zeta1/100 flips selected actor preferred keep/change; type-change rho and repair gamma are separate quantities',
    'founder': 'subsidy1/2 lasts a declared T updates; worst budget N*s*T pre-reserved from founder cash32 for T<=8, pay on actual resulting memberships; funded schedule is a premise, not a financer best response',
    'control': 'withdrawal may only stop subsidy (benefit continues under independent protocol) or may also revoke a founder-exclusive operational license (benefit becomes0). Care/protection unchanged in either case; actual title/maintenance realization needs its own evidence.',
    'parameters': {'N': 6, 'a': '2', 'c': '1', 'entry': '1/10', 'subsidy': '0 or1/2', 'stay_on_ties': True},
    'nonclaims': 'no strategic population equilibrium/ESS, compulsory dependence, actual-human tipping, full X/Y or physical self-carriage. Population probabilities differ from equilibrium existence/host selection.',
}


def margins(N, k, a=F(2), c=F(1), entry=F(1, 10), subsidy=F(0), alive=True):
    benefit = a if alive else F(0)
    return benefit*F(k-1, N-1)-c+subsidy, benefit*F(k, N-1)-c+subsidy-entry


def rates(N, k, a=F(2), c=F(1), entry=F(1, 10), subsidy=F(0), alive=True, tremble=F(0)):
    keep, join = margins(N, k, a, c, entry, subsidy, alive)
    up = F(N-k, N)*(tremble+(1-2*tremble)*int(join > 0))
    down = F(k, N)*(tremble+(1-2*tremble)*int(keep < 0))
    assert 0 <= up and 0 <= down and up+down <= 1
    return up, down


def potential(N, k, a=F(2), c=F(1), subsidy=F(0), alive=True):
    return (a if alive else F(0))*F(k*(k-1), 2*(N-1))-(c-subsidy)*k


def matrix(N, **kw):
    P = []
    for k in range(N+1):
        up, down = rates(N, k, **kw)
        row = [F(0)]*(N+1)
        if k < N: row[k+1] += up
        if k: row[k-1] += down
        row[k] += 1-up-down
        assert sum(row) == 1
        P.append(row)
    return P


def rat(x): return S.Rational(x.numerator, x.denominator)


def absorption(P):
    n = len(P)
    absorbing = tuple(k for k, row in enumerate(P) if row[k] == 1)
    transient = tuple(k for k in range(n) if k not in absorbing)
    assert absorbing
    H = [[F(int(k == j)) for j in absorbing] for k in range(n)]
    times = [F(0)]*n
    if transient:
        Q = S.Matrix([[rat(P[i][j]) for j in transient] for i in transient])
        R = S.Matrix([[rat(P[i][j]) for j in absorbing] for i in transient])
        inverse = (S.eye(len(transient))-Q).inv(method='DM')
        h, tt = inverse*R, inverse*S.ones(len(transient), 1)
        for pos, k in enumerate(transient):
            H[k] = [F(h[pos, j]) for j in range(len(absorbing))]
            times[k] = F(tt[pos, 0])
    for k in range(n):
        assert sum(H[k]) == 1 and all(q >= 0 for q in H[k]) and times[k] >= 0
        if k not in absorbing:
            for j in range(len(absorbing)):
                assert H[k][j] == sum(P[k][l]*H[l][j] for l in range(n))
            assert times[k] == 1+sum(P[k][l]*times[l] for l in range(n))
    return {'absorbing': absorbing, 'probabilities': H, 'expected_updates': times}


def stationary_birth_death(P):
    w = [F(1)]
    for k in range(1, len(P)):
        assert P[k-1][k] > 0 and P[k][k-1] > 0
        w.append(w[-1]*P[k-1][k]/P[k][k-1])
    pi = [x/sum(w) for x in w]
    assert sum(pi) == 1 and all(x > 0 for x in pi)
    for k in range(len(P)):
        assert sum(pi[j]*P[j][k] for j in range(len(P))) == pi[k]
    return pi


def propagate(distribution, P):
    return [sum(distribution[k]*P[k][j] for k in range(len(P))) for j in range(len(P))]


def micro_lumping(N, **kw):
    checks = 0
    for membership in product((0, 1), repeat=N):
        k = sum(membership)
        mass = [F(0)]*(N+1)
        for focal in range(N):
            # Direct average of all N-1 physical match partners verifies the
            # two counterfactual margins, rather than only reusing k formulas.
            partners = sum(membership[j] for j in range(N) if j != focal)
            keep = sum(kw.get('a', F(2))*membership[j]-kw.get('c', F(1))+kw.get('subsidy', F(0))
                       for j in range(N) if j != focal)/F(N-1)
            joined = keep-kw.get('entry', F(1, 10))
            expected_keep, expected_join = margins(N, k, **kw)
            if membership[focal]:
                assert keep == expected_keep
                new = 0 if keep < 0 else 1
            else:
                assert joined == expected_join
                new = 1 if joined > 0 else 0
            mass[k-membership[focal]+new] += F(1, N)
            checks += 1
        assert mass == matrix(N, **kw)[k]
    return checks


def audit():
    N = 6
    plain, funded = matrix(N), matrix(N, subsidy=F(1, 2))
    plain_a, funded_a = absorption(plain), absorption(funded)
    assert plain_a['absorbing'] == funded_a['absorbing'] == (0, 6)
    assert [row[1] for row in plain_a['probabilities']] == [0, 0, 0, F(1, 2), 1, 1, 1]
    assert plain_a['expected_updates'][3] == 10
    assert funded_a['probabilities'][2][1] == F(2, 3)
    assert funded_a['expected_updates'][2] == F(31, 3)
    micro = micro_lumping(N)+micro_lumping(N, subsidy=F(1, 2))
    family = []
    for n, cost, fee, subsidy in product(range(2, 13), (F(1, 2), F(1), F(3, 2)),
                                        (F(0), F(1, 10), F(1, 2), F(4, 5), F(1)),
                                        (F(0), F(1, 4), F(1, 2))):
        P = matrix(n, c=cost, entry=fee, subsidy=subsidy)
        result = absorption(P)
        assert all(t <= n*n for t in result['expected_updates'])
        for k in range(n+1):
            for nxt in (k-1, k+1):
                if 0 <= nxt <= n and P[k][nxt] > 0:
                    assert potential(n, nxt, c=cost, subsidy=subsidy) > potential(n, k, c=cost, subsidy=subsidy)
        width = F(2, n-1)-fee
        bidirectional = [k for k in range(1, n) if P[k][k+1] > 0 and P[k][k-1] > 0]
        if width <= 0: assert not bidirectional
        else: assert len(bidirectional) <= 1
        family.append({'N': n, 'participation_cost': cost, 'entry': fee, 'subsidy': subsidy,
                       'absorbing': result['absorbing'], 'prob_all_adopt': [row[result['absorbing'].index(n)] for row in result['probabilities']],
                       'expected_updates': result['expected_updates'], 'bidirectional_states': bidirectional})
    withdrawals, spent = [], F(0)
    d = [F(0)]*7; d[2] = 1
    for t in range(9):
        success = sum(d[k]*plain_a['probabilities'][k][1] for k in range(7))
        assert success == F(2, 3)*(1-F(1, 2)**t)
        withdrawals.append({'subsidized_updates': t, 'population_distribution_at_withdrawal': d,
                            'eventual_all_adopt_probability': success,
                            'expected_subsidy_paid': spent,
                            'worst_reserved_subsidy': F(3)*t, 'initial_founder_cash': F(32)})
        assert F(3)*t <= 32
        d = propagate(d, funded)
        spent += F(1, 2)*sum(k*d[k] for k in range(7))
    assert withdrawals[0]['eventual_all_adopt_probability'] == 0
    assert withdrawals[1]['eventual_all_adopt_probability'] == F(1, 3)
    high_entry = absorption(matrix(N, entry=F(4, 5)))
    assert high_entry['absorbing'] == (0, 4, 6)
    revoked = absorption(matrix(N, alive=False))
    assert revoked['absorbing'] == (0,) and revoked['expected_updates'][6] == F(147, 10)
    noisyP = matrix(N, tremble=F(1, 100))
    noisy_pi = stationary_birth_death(noisyP)
    assert all(noisyP[k][k] < 1 for k in range(7))
    assert noisy_pi[0] == noisy_pi[6]
    return {'plain': {'transition': plain, **plain_a}, 'subsidy_half': {'transition': funded, **funded_a},
            'micro_actor_matching_checks': micro, 'families': family, 'temporary_subsidy': withdrawals,
            'high_entry_hysteresis': high_entry, 'founder_license_revoked': revoked,
            'independent_protocol_after_founder_exit': plain_a,
            'tremble': {'zeta': F(1, 100), 'transition': noisyP, 'stationary': noisy_pi,
                        'permanent_all_adoption': False, 'uniform_hit0_block_bound': F(1, 600)**6},
            'care_floor_depends_on_participation_or_founder': False}


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [encode(v) for v in x]
    return x


def main():
    declaration = json.dumps(DECLARATION, indent=2)+'\n'
    (ROOT/'adoption_population_declaration.json').write_text(declaration)
    result = audit()
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           **result, 'simulations': 0, 'forward_looking_population_equilibrium_claim': False}
    (ROOT/'adoption_population_results.json').write_text(json.dumps(encode(out), indent=2)+'\n')
    print('PASS finite adoption:', len(result['families']), 'parameter families;', result['micro_actor_matching_checks'], 'micro matching checks')
    print('N6 tipping: k3 gives probability1/2, expected10 updates; subsidy k2 gives2/3')
    print('CONTROLS: high-entry partial absorption; license loss collapse; trembles remove permanent adoption')


if __name__ == '__main__': main()
