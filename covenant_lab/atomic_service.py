"""[B: lab] D15 exact negative/positive controls for an atomic-service variant.
Run: python3 covenant_lab/atomic_service.py
Written arbitrary-history coalition proof is in math/D15.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
ACTIONS = ('exit', 'D', 'C')
EPS = (F(1, 20), F(1, 20))
B, A, DELTA = (F(2), F(2)), (F(1, 4), F(1, 4)), F(3, 4)
DECLARATION = {
    'tag': '[P] atomicity/calibration/care premises; [B: lab] mathematics',
    'roles': 'two service actors; any passive protected interests have action-independent funded baseline utility',
    'action': 'exit gives executed-offer probability0; participating D probability epsilon; C probability1-epsilon',
    'timing': 'history-dependent intended offers before fresh independent implementation errors; verified matching only after both executed offers known; no coalition sees future errors before choosing',
    'atomic_execution': 'elective service runs iff both executed offers are1; net matched output to actor i is b_i-c_i; its own executed offer incurs preparation a_i even if match fails',
    'payoffs': 'actual realized payoff (b_i-c_i)*x_i*x_j-a_i*x_i; exact expectation p_i*((b_i-c_i)*p_j-a_i)',
    'parameters': {'b': [3, 3], 'c': [1, 1], 'epsilon': ['1/20', '1/20'], 'preparation': ['1/4', '1/4'], 'discount': '3/4'},
    'scope': 'arbitrary bounded history-dependent/randomized offers and binding coalition plans, balanced transfers internal to coalition only; actual matching/noise/care/title are premises; no attacks or outside subsidies outside declared actions',
    'exit_care': 'exit cancels elective preparation/service and retains fixed care, record, debt and appeal claims; funding of that baseline is purchased, not derived here',
    'target': 'all-C maximizes each actor stage expectation; written discounted cap rules out every profitable binding coalition and therefore any internally stable such deviation',
    'nonclaims': 'changes ordinary service mechanism from original donation game; equilibrium selection, full covenant finance and physical atomic realization not established',
}


def p(i, action): return F(0) if action == 'exit' else EPS[i] if action == 'D' else 1-EPS[i]


def stage(profile):
    return tuple(p(i, profile[i])*(B[i]*p(1-i, profile[1-i])-A[i]) for i in (0, 1))


def realized_expected(profile):
    totals = [F(0), F(0)]
    for x in product((0, 1), repeat=2):
        probability = F(1)
        for i in (0, 1): probability *= p(i, profile[i]) if x[i] else 1-p(i, profile[i])
        for i in (0, 1): totals[i] += probability*(B[i]*x[i]*x[1-i]-A[i]*x[i])
    return tuple(totals)


def enc(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): enc(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [enc(v) for v in x]
    return x


def main():
    declaration = json.dumps(DECLARATION, indent=2)+'\n'
    (ROOT/'atomic_service_declaration.json').write_text(declaration)
    cap = stage(('C', 'C'))
    table, coalitions = [], []
    equilibria = []
    for profile in product(ACTIONS, repeat=2):
        payoff = stage(profile)
        assert payoff == realized_expected(profile)
        assert all(payoff[i] <= cap[i] for i in (0, 1))
        table.append({'profile': profile, 'stage_payoff': payoff,
                      'constant_policy_value': tuple(v/(1-DELTA) for v in payoff)})
        if all(stage(tuple(action if j == i else profile[j] for j in (0, 1)))[i] <= payoff[i]
               for i in (0, 1) for action in ACTIONS): equilibria.append(profile)
        for members in ((0,), (1,), (0, 1)):
            slack = sum(cap[i]-payoff[i] for i in members)/(1-DELTA)
            assert slack >= 0
            coalitions.append({'members': members, 'joint_profile': profile, 'constant_plan_sum_slack': slack})
    assert cap == (F(627, 400), F(627, 400))
    assert set(equilibria) == {('C', 'C'), ('exit', 'exit')}
    # Ablation: a non-atomic donor can receive while withholding its own offer.
    ordinary_cc = F(3)*p(1, 'C')-F(5, 4)*p(0, 'C')
    ordinary_dc = F(3)*p(1, 'C')-F(5, 4)*p(0, 'D')
    assert ordinary_dc-ordinary_cc == F(9, 8)
    # A heterogeneous exact family checks the symbolic hypothesis boundary.
    family = []
    epsilon_pairs = tuple(product((F(0), F(1, 20), F(1, 2)), repeat=2))
    benefit_pairs = tuple(product((F(0), F(1), F(2)), repeat=2))
    ratios = tuple(product((F(0), F(1, 2), F(1)), repeat=2))
    for ee, net, ratio in product(epsilon_pairs, benefit_pairs, ratios):
        q = tuple(1-e for e in ee)
        costs = tuple(ratio[i]*net[i]*q[1-i] for i in (0, 1))
        maximum = tuple(q[i]*(net[i]*q[1-i]-costs[i]) for i in (0, 1))
        for profile in product(ACTIONS, repeat=2):
            pp = tuple(F(0) if profile[i] == 'exit' else ee[i] if profile[i] == 'D' else q[i] for i in (0, 1))
            rr = tuple(pp[i]*(net[i]*pp[1-i]-costs[i]) for i in (0, 1))
            assert all(rr[i] <= maximum[i] for i in (0, 1))
        family.append({'epsilon': ee, 'net_matched_benefit': net, 'preparation': costs, 'cap': maximum})
    bad_prep = F(2)
    bad_cc = (1-EPS[0])*(B[0]*(1-EPS[1])-bad_prep)
    assert bad_cc == -F(19, 200) < 0
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'stage_cap': cap, 'table': table, 'pure_stage_equilibria': equilibria,
           'coalition_constant_plan_checks': coalitions,
           'heterogeneous_families': family, 'family_profiles_checked': len(family)*9,
           'non_atomic_unilateral_gain': ordinary_dc-ordinary_cc,
           'excess_preparation_exit_gain': -bad_cc,
           'arbitrary_history_proof': 'written in math/D15.md, not inferred from constant-plan enumeration',
           'simulations': 0, 'self_carrying_claim': False}
    (ROOT/'atomic_service_results.json').write_text(json.dumps(enc(out), indent=2)+'\n')
    print('PASS atomic service:', len(table), 'profiles;', len(family), 'families;',
          len(family)*9, 'family profiles; all-C stage cap', cap[0])
    print('CONTROL: all-exit also equilibrium; non-atomic deviation gain', ordinary_dc-ordinary_cc)


if __name__ == '__main__': main()
