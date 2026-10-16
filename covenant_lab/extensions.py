"""[B: lab] E1/E2 exact preregistered families, including negative controls.
Run: python3 covenant_lab/extensions.py. No simulation or floating verdicts.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
pi, beta, d = S.symbols('pi beta d', real=True)
# E1. After stage payoffs, pre mortality acts first (survival 1/3),
# then availability pi, willing paid host, conditional success 1.
# Success preserves service calendar/branch and enters survival-one post phase.
# No terminal reward; paid hosting is a fixed separately funded premise.
T = S.Matrix([[S.Rational(1, 3)*(1-pi), S.Rational(1, 3)*pi], [0, 1]])
weights = [(S.Matrix([[1, 0]])*(beta*T)**n*S.ones(2, 1))[0].expand() for n in range(5)]
post_weights = [beta**n for n in range(5)]
# Four-stage repeating investment/donation block, chosen before solving.
# C pays an initial cost one; later ordinary net payoff differences vs D
# are -10/9, +32, -32. Add common baseline 40 (all payoffs positive) and
# current benefit to the other player. Decision repeats after four stages.
# Future states rejoin at the same date/phase law under either action.
differences = [S.Rational(-1), S.Rational(-10, 9), S.Rational(32), S.Rational(-32)]
pre_margin = S.factor(sum(a*w for a, w in zip(differences, weights)))
post_margin = S.factor(sum(a*w for a, w in zip(differences, post_weights)))
pre_at_beta = S.factor(pre_margin.subs(beta, S.Rational(3, 4)))
post_at_beta = post_margin.subs(beta, S.Rational(3, 4))
assert S.expand(pre_at_beta - (pi**2-pi+S.Rational(2, 9))) == 0
assert post_at_beta == S.Rational(8, 3)
assert pre_at_beta.subs(pi, 0) > 0
assert pre_at_beta.subs(pi, S.Rational(1, 2)) == -S.Rational(1, 36)
assert pre_at_beta.subs(pi, 1) > 0
# All other service states have a singleton maintenance action. Hosting H
# is strictly optimal on an opportunity: paid 1, readiness cost 1/2.
assert F(1)-F(1, 2) > 0
# Adversarial pass: independently solve the complete 26-state repeated game,
# including branches reachable only after deviations. The matrix formulation
# above is not used to construct its service transitions or rewards.
def full_cycle_check(prospect):
    from itertools import product
    service = [(0, (0, 0))] + [(j, a) for j in (1, 2, 3) for a in product((0, 1), repeat=2)]
    states = [(phase, j, a) for phase in (0, 1) for j, a in service]
    index = {s: i for i, s in enumerate(states)}
    def branches(s, action):
        phase, j, a = s
        active = tuple(action) if j == 0 else a
        utilities = [S.Rational(40) + differences[j]*active[i] +
                     (active[1-i] if j == 0 else 0) for i in range(2)]
        nxt_j = (j+1) % 4
        nxt_a = active if nxt_j else (0, 0)
        survival = [(0, (1-prospect)/3), (1, prospect/3)] if phase == 0 else [(1, S.Rational(1))]
        for nxt_phase, q in survival:
            yield q, (nxt_phase, nxt_j, nxt_a), utilities
    P = S.zeros(len(states))
    r = [S.zeros(len(states), 1) for i in range(2)]
    for row, s in enumerate(states):
        for q, t, u in branches(s, (1, 1)):
            P[row, index[t]] += q
        phase, j, a = s
        active = (1, 1) if j == 0 else a
        for i in range(2):
            r[i][row] = 40+differences[j]*active[i]+(active[1-i] if j == 0 else 0)
    W = [(S.eye(len(states))-S.Rational(3, 4)*P).inv()*u for u in r]
    slacks = []
    for row, (phase, j, a) in enumerate(states):
        if j != 0: continue  # singleton action: no alternative
        for i in range(2):
            dev = [1, 1]
            dev[i] = 0
            stage = 40+differences[0]*dev[i]+dev[1-i]
            Q = stage + S.Rational(3, 4)*sum(q*W[i][index[t]] for q, t, u in branches(states[row], dev))
            margin = S.factor(W[i][row]-Q)
            assert margin == (pre_at_beta.subs(pi, prospect) if phase == 0 else post_at_beta)
            slacks.append({'phase': phase, 'player': i, 'margin': margin})
    return {'pi': prospect, 'public_states': len(states), 'all_nonsingleton_deviations': slacks,
            'singleton_states_checked': len(states)-2,
            'policy_passes': all(row['margin'] >= 0 for row in slacks)}

full_cycle_cases = [full_cycle_check(p) for p in (S.Rational(0), S.Rational(1, 2), S.Rational(1))]
# Survival-weight monotonicity is checked symbolically on the finite witness.
weight_derivatives = []
for w in weights[1:]:
    f = S.factor(S.diff(w, pi).subs(beta, S.Rational(3, 4)))
    # exact positivity over [0,1] follows from no interior roots + endpoints
    if f != 0:
        assert min(f.subs(pi, 0), f.subs(pi, 1)) >= 0
        assert S.Poly(f, pi).count_roots(0, 1) == 0
    weight_derivatives.append(f)
# Positive family: grim noisy-free donation, b=3/2,c=1/2, pure time
# preference beta, pre/post survival as above. Punishment pays zero.
r, g = S.Rational(1), S.Rational(1, 2)
Wpost = r/(1-beta)
Wpre = S.factor((r+beta*pi*Wpost/3)/(1-beta*(1-pi)/3))
grim_pre = S.factor(Wpre-r-g)
grim_post = S.factor(Wpost-r-g)
assert S.cancel(grim_pre.subs(beta, S.Rational(3, 4)) - (5*pi-1)/(2*(3+pi))) == 0
# A subjective prior on a fixed unknown availability rate mixes likelihoods,
# not a plug-in average of pi. Bayesian beliefs update after no availability.
prior_margin = (pre_at_beta.subs(pi, 0)+pre_at_beta.subs(pi, S.Rational(1, 2)))/2
assert prior_margin == S.Rational(7, 72)
# E2. One elective resource has total bundle one. Own productive capacity
# 1-d, no substitute, external share d. Protected care and exit are fixed.
# Membership: sunk fee 1/2; C cost one; full optional bundle utility 2.
# Exit: own utility 2(1-d); payer/provider fees and refundable rights declared.
membership_margin = 2*d-S.Rational(3, 2)
service_margin = 2*d-1
provider_margin = S.Rational(1, 2)-d/4
assert provider_margin.subs(d, 1) > 0
assert S.solve_univariate_inequality(membership_margin >= 0, d) == (S.Rational(3, 4) <= d)
# Negative comparison with ownership-dependent outside production: an admitted
# portable outside operation uses own and external resource entitlements to
# create 4d(1-d) extra outside value. Ordinary returns/fees stay fixed.
# Already-sustained ordinary-policy margin m=1/8. Dependence is still d,
# read from own capacity BEFORE incentives; it is not defined by a verdict.
outside_margin = S.factor(S.Rational(1, 8)+2*d-4*d*(1-d))
outside_roots = S.solve(outside_margin, d)
assert outside_margin.subs(d, 0) > 0
assert outside_margin.subs(d, S.Rational(1, 4)) == -S.Rational(1, 8)
assert outside_margin.subs(d, 1) > 0

def encode(x):
    if isinstance(x, S.Basic): return str(x)
    if isinstance(x, dict): return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [encode(v) for v in x]
    return x

data = {'tag': '[B: lab]', 'grade': 'computed exact', 'simulations': 0,
        'E1': {'survival_phase_matrix': list(T), 'weights': weights,
          'differences': differences, 'pre_margin_general': pre_margin, 'post_margin_general': post_margin,
          'beta': S.Rational(3, 4), 'pre_margin': pre_at_beta, 'post_margin': post_at_beta,
          'pre_passing_pi': '[0,1/3] union [2/3,1]', 'weight_derivatives': weight_derivatives,
          'refutation': {'pi_0': pre_at_beta.subs(pi, 0), 'pi_half': pre_at_beta.subs(pi, S.Rational(1, 2))},
          'positive_grim_pre': grim_pre, 'positive_grim_post': grim_post,
          'full_cycle_cases': full_cycle_cases,
          'subjective_prior_margin': prior_margin, 'true_pi_half_margin': -S.Rational(1, 36)},
        'E2': {'service_margin': service_margin, 'entry_exit_margin': membership_margin,
          'provider_margin': provider_margin, 'buyer_threshold': S.Rational(3, 4),
          'outside_production_margin': outside_margin, 'outside_roots': outside_roots,
          'scope': 'buyer monotonicity under fixed outside operations; refuted after the explicitly declared outside production extension'}}
(ROOT/'extension_results.json').write_text(json.dumps(encode(data), indent=2)+'\n')
print('PASS E1: improved continuation weights, but incentive-region inclusion refuted')
print('PASS E1: grim positive family and Bayesian mismatch; E2: threshold and disconnected control')
