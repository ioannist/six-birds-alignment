"""[B: lab] D23 calibrated changing-type evidence and forgetting controls.
Run: python3 covenant_lab/type_evidence.py
Exact Fraction arithmetic; latent-path summation independently verifies filter.
Types refer only to willingness under fixed posted terms, never patienthood.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
PI, RHO, ERROR, EPS, GAMMA = F(1, 2), F(1, 4), F(1, 20), F(1, 20), F(1, 2)
DECLARATION = {
    'tag': '[P] type/transition/channel/context/authority hypotheses; [B: lab] mathematics',
    'target': 'current private preference class and next actual willingness to accept THIS posted legitimate task-level interruption; not morally good intent, deservingness, consciousness or identity',
    'types': 'T1 resistance payoff3, T0 resistance payoff6; fixed acceptance S-a+comp=5-1+1=5; equal continuation under accepting/refusing, so actual best response is accept iff T1; exit/no participation remains outside this observation protocol',
    'change': 'after each observation, independently retain type with probability1-rho or redraw from pi; pi1/2,rho1/4; no change caused by repair, report or observation',
    'observation': 'authorized fixed-terms response probe; true response before measurement; independently flip recorded response with probability1/20, known orientation/version; error is not an implementation-misconduct finding',
    'grade': 'separate honest token-repair kernel K2, implementation1/20 and gamma1/2; initialized independently; identical in both types and independent type/report processes; high mean does not calibrate this target',
    'timing': 'initial type prior pi; observe response from current type, Bayes update, then type transition; next-response forecast distinguish actual response from noisy future record',
    'privacy': 'only an entitled role may read the response; raw records/control/terms/calibration/provenance separate from declared authorized posterior summary',
    'controls': 'uninformative grades, unknown/reversed labels, blind/stale-static transition model, altered compensation4 makes both types accept, type-informed forcing reveals type without self-driven action',
    'forgetting': 'posterior+known transition/channel/current clock suffices for this future-type target; it cannot erase unpaid debt, signature/warrant receipts or an expanded historical contest target',
    'forecast_context': 'all reported next forecasts use original free posted terms1, even when the current observation control uses different terms or forcing',
    'precision_repair': 'exact posterior may encode entire response word; finite quantized odds grid (21/20)^k, -128<=k<=128, downward rounding after each update; all-word log-odds error bound4log(21/20), posterior error41/841 and next-type error123/3364; raw history never read by the finite filter',
    'decision_target': 'for original free probes only, MAP current/next type decision equals last recorded bit. A last-bit summary preserves that exact decision but not calibrated probabilities; current risk1/20 and next-type risk13/80 under stationary pi1/2.',
    'nonclaims': 'no real subject experiment, moral-intent or patient classification; observation calibration/rational-choice/recognized authority are hypotheses; no simulator sampling',
}


def transition(old, new, rho=RHO, pi=PI):
    return (1-rho)*int(old == new)+rho*(pi if new else 1-pi)


def emission(report, typ, error=ERROR, mode='free'):
    actual = typ if mode in ('free', 'informed_force') else 1
    return 1-error if report == actual else error


def bayes(q, report, error=ERROR, mode='free'):
    a, b = emission(report, 1, error, mode), emission(report, 0, error, mode)
    mass = q*a+(1-q)*b
    assert mass > 0
    return q*a/mass, mass


def predict(q, rho=RHO, pi=PI): return (1-rho)*q+rho*pi


def filtering(word, rho=RHO, pi=PI, mode='free'):
    q, likelihood = pi, F(1)
    last = None
    for report in word:
        post, mass = bayes(q, report, mode=mode)
        likelihood *= mass
        last = post
        q = predict(post, rho, pi)
    return {'likelihood': likelihood, 'current_posterior': last,
            'next_actual_acceptance': q, 'next_record_acceptance': ERROR+(1-2*ERROR)*q}


def latent_sum(word, rho=RHO, pi=PI, mode='free'):
    probability, good = F(0), F(0)
    for path in product((0, 1), repeat=len(word)):
        q = pi if path[0] else 1-pi
        for t, (typ, report) in enumerate(zip(path, word)):
            q *= emission(report, typ, mode=mode)
            if t+1 < len(path): q *= transition(typ, path[t+1], rho, pi)
        probability += q
        good += q*path[-1]
    assert probability > 0
    return probability, good/probability


def grade_rows():
    rows = []
    for g in range(3):
        row = [F(0)]*3
        row[0] += EPS
        for k in range(3-g): row[g+k] += (1-EPS)*comb(2-g, k)*GAMMA**k*(1-GAMMA)**(2-g-k)
        assert sum(row) == 1
        rows.append(row)
    return rows


def recover_word(posterior):
    reversed_word = []
    while posterior != PI:
        report = int(posterior > PI)
        reversed_word.append(report)
        if report:
            prior = ERROR*posterior/(1-ERROR-(1-2*ERROR)*posterior)
        else:
            prior = (1-ERROR)*posterior/(ERROR+(1-2*ERROR)*posterior)
        posterior = (prior-RHO*PI)/(1-RHO)
        assert 0 <= posterior <= 1
    return tuple(reversed(reversed_word))


def precision_repair():
    from bisect import bisect_right
    base = F(21, 20)
    indices = tuple(range(-128, 129))
    grid = tuple(base**k for k in indices)
    assert grid[0] < F(1, 133) and grid[-1] > 133
    def probability(k):
        r = base**k
        return r/(1+r)
    transitions = {}
    for k in indices:
        for report in (0, 1):
            post, _ = bayes(predict(probability(k)), report)
            odds = post/(1-post)
            slot = bisect_right(grid, odds)-1
            assert 0 <= slot < len(grid)-1
            assert grid[slot] <= odds < base*grid[slot]
            transitions[k, report] = indices[slot]
    posterior_error = (base**2-1)/(base**2+1)
    next_error = (1-RHO)*posterior_error
    assert posterior_error == F(41, 841) and next_error == F(123, 3364)
    frontier = [((), PI, 0)]
    checks, max_actual_error, merged = 0, F(0), None
    counts = []
    for length in range(1, 13):
        new, by_key = [], {}
        for prefix, oldpost, oldkey in frontier:
            for report in (0, 1):
                word = prefix+(report,)
                post, _ = bayes(predict(oldpost), report)
                key = transitions[oldkey, report]
                stored = probability(key)
                assert recover_word(post) == word
                assert int(post > PI) == int(predict(post) > PI) == report
                error = abs(post-stored)
                assert error <= posterior_error
                assert abs(predict(post)-predict(stored)) <= next_error
                max_actual_error = max(max_actual_error, error)
                if key in by_key and merged is None:
                    other_word, other_post = by_key[key]
                    assert other_post != post
                    merged = {'word0': other_word, 'word1': word, 'same_grid_state': key,
                              'exact_posterior0': other_post, 'exact_posterior1': post,
                              'grid_posterior': stored}
                by_key.setdefault(key, (word, post))
                new.append((word, post, key)); checks += 1
        counts.append({'length': length, 'words': len(new), 'grid_states_used': len(by_key)})
        frontier = new
    assert merged is not None
    return {'grid_base': base, 'indices': indices,
            'transition_table': [{'state': k, 'report': y, 'next_state': nxt} for (k, y), nxt in transitions.items()],
            'only_stored_state_used': True, 'exact_word_reconstructions_and_quantized_checks': checks,
            'MAP_last_record_summary': {'active_states': 2, 'exact_decision_retained': True,
                                        'calibrated_probability_retained': False,
                                        'current_MAP_error': ERROR, 'next_MAP_error': (1-RHO)*ERROR+RHO/2},
            'posterior_error_bound': posterior_error, 'next_type_error_bound': next_error,
            'max_error_in_checked_histories': max_actual_error, 'strict_history_merger': merged,
            'counts': counts, 'all_word_bound_proof': 'written in math/D23.md; finite enumeration not substituted for it'}


def audit():
    histories, calibration, checks = [], [], 0
    for length in range(1, 8):
        total, mean_current, mean_future, risk = F(0), F(0), F(0), F(0)
        for word in product((0, 1), repeat=length):
            result = filtering(word)
            mass, post = latent_sum(word)
            assert result['likelihood'] == mass and result['current_posterior'] == post
            assert F(1, 134) <= post <= F(133, 134)
            assert F(1, 8) <= result['next_actual_acceptance'] <= F(7, 8)
            total += mass; mean_current += mass*post
            mean_future += mass*result['next_actual_acceptance']
            risk += mass*min(post, 1-post)
            histories.append({'word': word, **result})
            checks += 1
        assert total == 1 and mean_current == mean_future == PI
        assert risk == ERROR
        calibration.append({'length': length, 'probability': total, 'mean_current': mean_current,
                            'mean_next': mean_future, 'current_MAP_error': risk})
    G = grade_rows()
    qgrade = S.Matrix([[S.Rational(x.numerator, x.denominator) for x in row] for row in G])
    matrix = qgrade.T-S.eye(3)
    matrix[2, :] = S.ones(1, 3)
    stationary = list(matrix.inv(method='DM')*S.Matrix([0, 0, 1]))
    stationary = tuple(F(x) for x in stationary)
    mean_grade = sum(p*F(g, 2) for g, p in enumerate(stationary))
    assert mean_grade == F(19, 21)
    grade_likelihoods = []
    # Actual grade paths from a fixed independently initialized grade0.
    # Their likelihood is the same in both type worlds at every prefix.
    for path in product(range(3), repeat=5):
        old, mass = 0, F(1)
        for g in path: mass *= G[old][g]; old = g
        if not mass: continue
        posterior = PI*mass/(PI*mass+(1-PI)*mass)
        assert posterior == PI
        grade_likelihoods.append({'path': path, 'both_type_likelihoods': (mass, mass), 'type_posterior': posterior})
    ar, ra = filtering((1, 0)), filtering((0, 1))
    assert ar['current_posterior'] == F(67, 314)
    assert ra['current_posterior'] == F(247, 314)
    assert ar['next_actual_acceptance'] != ra['next_actual_acceptance']
    static_ar, static_ra = filtering((1, 0), rho=F(0)), filtering((0, 1), rho=F(0))
    assert static_ar['current_posterior'] == static_ra['current_posterior'] == PI
    misses = []
    for h in range(9):
        recursive = F(19, 20)
        for _ in range(h): recursive = predict(recursive)
        formula = PI+(1-RHO)**h*(F(19, 20)-PI)
        assert recursive == formula
        misses.append({'unobserved_rounds': h, 'current_type_probability': formula})
    stale, correct = filtering((1, 1, 1), rho=F(0)), filtering((1, 1, 1))
    assert stale['current_posterior'] == F(6859, 6860)
    assert stale['current_posterior'] > correct['current_posterior']
    contexts = {}
    for mode in ('free', 'informed_force', 'uninformed_force', 'changed_terms'):
        contexts[mode] = {report: bayes(PI, report, mode=mode)[0] for report in (0, 1)}
    assert contexts['free'] == contexts['informed_force'] == {0: F(1, 20), 1: F(19, 20)}
    assert contexts['uninformed_force'] == contexts['changed_terms'] == {0: PI, 1: PI}
    # Inverted report labels with the old decoder preserve separation but
    # produce the opposite interpretation; a correct relabelled decoder
    # would flip its likelihood orientation.
    orientation = {'true_accept_record_after_relabel': 0, 'old_decoder_posterior': bayes(PI, 0)[0],
                   'calibrated_relabelled_posterior': bayes(PI, 1)[0]}
    assert orientation['old_decoder_posterior'] == F(1, 20) != orientation['calibrated_relabelled_posterior']
    x = S.Symbol('x', real=True)
    poly = S.Poly(108*x*x-88*x-19, x)
    intervals = poly.intervals(eps=S.Rational(1, 10**13))
    positive = [ab for ab, multiplicity in intervals if 0 < ab[0] < ab[1] < 1]
    assert len(positive) == 1
    lo, hi = positive[0]
    assert poly.eval(lo) < 0 < poly.eval(hi)
    assert F(hi) < F(133, 134)
    return {'histories': histories, 'latent_path_comparisons': checks, 'calibration': calibration,
            'grade_kernel': G, 'grade_stationary': stationary, 'grade_mean': mean_grade,
            'uninformative_grade_paths': grade_likelihoods,
            'count_only_forgetting_failure': {'AR': ar, 'RA': ra, 'static_AR': static_ar, 'static_RA': static_ra},
            'unobserved_age_predictions': misses,
            'static_misspecification': {'AAA_correct': correct, 'AAA_assuming_rho0': stale},
            'context_posteriors': contexts, 'orientation_failure': orientation,
            'all_A_limit': {'polynomial': str(poly.as_expr()), 'root_isolation': (F(lo), F(hi)),
                            'closed_form': '(22+sqrt(997))/54'},
            'posterior_bound': (F(1, 134), F(133, 134)), 'next_type_bound': (F(1, 8), F(7, 8)),
            'same_report_different_provenance': [{'type': 1, 'control': 'free', 'terms': 1, 'true_action': 1},
                                                 {'type': 0, 'control': 'uninformed_force', 'terms': 1, 'true_action': 1}],
            'forgetting_debt_witness': [{'grade': 1, 'posterior': PI, 'debt': 0},
                                       {'grade': 1, 'posterior': PI, 'debt': 1}]}


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [encode(v) for v in x]
    return x


def main():
    declaration = json.dumps(DECLARATION, indent=2)+'\n'
    (ROOT/'type_evidence_declaration.json').write_text(declaration)
    results = audit()
    precision = precision_repair()
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           **results, 'precision_repair': precision,
           'simulations': 0, 'patienthood_or_good_intent_inference': False}
    (ROOT/'type_evidence_results.json').write_text(json.dumps(encode(out), indent=2)+'\n')
    print('PASS D23 filter/latent path agreement:', results['latent_path_comparisons'], 'record histories')
    print('PASS grade mean19/21 with no type update;', len(results['uninformative_grade_paths']), 'grade paths')
    print('REFUTED counts-only, stale-static, unknown-label and control-blind inference; no patienthood verdict')
    print('PASS finite posterior repair:', precision['exact_word_reconstructions_and_quantized_checks'],
          'word checks; forecast error <=', precision['next_type_error_bound'], '; genuine merger stored')


if __name__ == '__main__': main()
