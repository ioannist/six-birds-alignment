"""[B: lab] D19 finite integrated game, with an exact coalition refutation.

Run: python3 covenant_lab/integrated_game.py
Primitives and menus are frozen in DECLARATION before policy evaluation.
This is a new candidate, distinct from integrated.py's construction hinges.
The endowed productive asset and verified physical inputs are [P] premises.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
BETA, EPS, GAMMA = F(3, 4), F(1, 20), F(1, 2)
FINE, GRANT = F(10), F(24)
ACTORS = ('financier', 'client', 'maintainer', 'caregiver', 'reporter0',
          'reporter1', 'reporter2', 'controller', 'monitor', 'host0', 'host1', 'host2',
          'fork', 'outside_patient', 'creditor')
STATES = tuple(product(range(3), (0, 1), (0, 1), (0, 1)))
INDEX = {s: i for i, s in enumerate(STATES)}
CAPACITY = ((1, 1, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
MENUS = tuple(product(('human', 'auto'), ('human', 'auto'),
                      ('human', 'auto', 'none'), ('human', 'auto', 'none'),
                      ('none', 'reserved'), (0, 1)))
POLICY_MENU = ('human', 'human', 'human', 'human', 'reserved', 1)
DECLARATION = {
    'tag': '[P] resource/security/valuation premises; [B: lab] consequences',
    'roles': ACTORS, 'state': 'grade0..2, membership0/1, fork-born0/1, old-debt0/1',
    'discount': str(BETA), 'noise': str(EPS), 'recovery': str(GAMMA),
    'timing': ['financier chooses procurement, audit and grant',
               'client chooses membership/buy/repair/copy',
               'verified maintenance produces resources; committed grant paid and care delivered',
               'permission bit and host capacity realized; source inputs measured/reported',
               'controller chooses processing; hosts deliver if hired',
               'independent audit sample realized after the request',
               'fine/compensation and original debt settled; repair grade updates'],
    'chance': 'permission0/1 fair; productive yield150/152 fair; four capacity masks fair; independent implementation flip1/20 and token recoveries1/2; reserved audit catches deliberate abuse with probability1/2',
    'capital': 'care trust endowed with realized productive seed and reserve16; maintenance, care, appeal/records/exit precede residual financier consumption',
    'resources': 'verified maintenance fee2/cost1 or automated backstop3; care per n patients human fee n+1/cost n or backstop4n+1; core administration5; care inputs included in these costs',
    'care': '2 old patients plus at most1 fork, each gets1 input independently of membership, grade and opinion; staff have independent self-supporting production',
    'facts': '3 distinct verifiable source-input jobs, fee1/2 and actual cost1/4; calibrated measured datum automatically bound to authenticated input receipt; missing/unverified/forged input replaced for3/4; up to1 externally corrupted output decoded by majority; absent procurement gives no permission certificate. Trusted calibration and binding are physical premises, not strategic honesty theorems.',
    'control': 'hired controller fee1/effort1/4; proper legitimate processing bonus3 financed by financier, compensation1 paid by controller to client; automated proper processing total price3 including compensation1; absent facts or controller produces safe pause payoff3 (legitimate event) or7/2 (safe event)',
    'abuse': 'controller can abuse while hired and facts exist; private gain4, client task loss1/2, legitimate bonus/compensation forfeited; collateral10 posted and returned within date, caught abuse transfers10 to client; no implementation-noise penalties',
    'audit': 'reserved sample costs1/2, physically cannot be disabled by monitor; no-audit controller response is abuse; optional delegated comparison uses fee7/2 and effort1/2',
    'valuation': 'financier utility residual resources +30 per care input +100 times task welfare excluding transfers; client utility own estate income + elective service + task payoff + compensation/fines; workers monetary receipts less effort',
    'passive_interests': 'fork utility own estate income plus1 per care input after creation; outside patient utility1 per care input; creditor utility collected old debt. These interests have no work/action and may belong to transfer coalitions.',
    'outside': 'each actor can refuse employment, decline membership/service, or exit; outside net32/working capital supports collateral and inputs; common outside increments omitted from utility; protected claims and original record survive exit',
    'service': 'two available distinct physical hosts selected by index; each verified input fee3/2, cost1; buyer value16*grade/2 only if both deliver; only actual inputs paid; no future host registration fee',
    'copy': 'at most one fork; creation uses2, grant24 voluntary; asset/vote unit split halves; estate income10 before birth or5 each after; debt collected once, total original debt preserved and split; aliases cannot create independent groups/assets/votes or reset grade/debt',
    'menus': MENUS, 'buyer_actions': 'next membership,buy,repair,copy; buy requires membership, copy possible iff not yet born; no grant requirement for copying',
    'rights_boundary': 'verified care/maintenance, protected title and debt, safe exit/appeal, individual input receipts and authenticated job-access are realized primitives; arbitrary capture/erasure requests rejected without changing state; no claim these premises hold on real equipment',
    'assessment': 'private moral labels/opinions are immutable decorative coordinates; all grades are contractual risk state, not moral standing or subjecthood',
    'coalitions': 'binding joint plans and balanced within-coalition transfers allowed; no monetary utility assigned to the trust itself; financier is strategic residual claimant, not owner of protected seed',
    'scope': 'finite recurrent public-state candidate with an endowed asset and bounded patient/capacity shocks; physical realization, normative legitimacy and unbounded births/disasters are not conclusions',
}


def encode(x):
    if isinstance(x, (F, S.Rational)): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [encode(v) for v in x]
    return x


def grade_row(g, repair):
    from math import comb
    q = 1-EPS if repair else EPS
    row = [F(0)]*3
    row[0] = 1-q
    for k in range(3-g):
        row[g+k] += q*comb(2-g, k)*GAMMA**k*(1-GAMMA)**(2-g-k)
    assert sum(row) == 1
    return row


def actions(state):
    g, member, born, debt = state
    return tuple((m, buy, repair, copy) for m, buy, repair in product((0, 1), repeat=3)
                 for copy in range(2-born) if not buy or m)


def policy(state):
    g, member, born, debt = state
    buy = int(g > 0)
    return int(member or buy), buy, 1, 1-born


def controller_response(truth, certified, hired, audited):
    if not certified or not hired: return 'off'
    return 'proper' if audited else 'abuse'


def period(state, menu, buyer, overrides=None, fine_share=F(1), priority_audit=False):
    """One shared expected payoff/transition function, every role on same law.

    The two permission events and all four capacity masks are summed exactly.
    The audit transfer is an expectation of the declared binary sample; the
    resource proof separately checks every sample/yield branch.
    Input refusal activates a physically paid backstop, not unpaid free care.
    """
    overrides = {} if overrides is None else overrides
    g, member, born, debt = state
    maint, care, reports, control, audit, offer = menu
    m, buy, repair, copy = buyer
    assert buyer in actions(state)
    next_born = int(born or copy)
    n = 2+next_born
    pay = {i: F(0) for i in ACTORS}
    pay['fork'] = (F(6)-F(debt, 2))*next_born
    pay['outside_patient'] = F(1)
    pay['creditor'] = F(debt)
    cash = F(151)   # average of explicitly declared 150/152 support
    maint_work = maint == 'human' and overrides.get('maintainer', 'work') == 'work'
    care_work = care == 'human' and overrides.get('caregiver', 'work') == 'work'
    cash -= 2 if maint_work else 3
    cash -= n+1 if care_work else 4*n+1
    pay['maintainer'] = F(int(maint_work))
    pay['caregiver'] = F(int(care_work))
    cash -= 5
    for i in range(3):
        work = reports == 'human' and overrides.get('reporter'+str(i), 'work') == 'work'
        if reports != 'none': cash -= F(1, 2) if work else F(3, 4)
        if work: pay['reporter'+str(i)] = F(1, 4)
    certified = reports != 'none'
    audited = priority_audit or audit == 'reserved'
    cash -= F(1, 2) if audited else 0
    pay['client'] += F(10, 1+next_born)-F(debt, 1+next_born)
    pay['client'] += (GRANT*offer-2)*copy
    cash -= GRANT*offer*copy
    entry = F(1, 2)*int(not member and m)
    pay['client'] -= entry
    cash += entry
    pay['client'] -= (1-EPS if repair else EPS)
    task = F(0)
    for truth in (0, 1):
        hired = control == 'human' and overrides.get('controller', 'work') != 'off'
        response = overrides.get('controller_action', controller_response(truth, certified, hired, audited))
        if isinstance(response, tuple): response = response[truth]
        if not hired or not certified: response = 'off'
        if certified and control == 'auto' or certified and control == 'human' and not hired:
            welfare, client_cash, cost = F(4), F(truth), F(3)
        elif certified and hired:
            assert response in ('proper', 'abuse')
            cash -= F(1, 2)  # fee1, weighted by fair permission event
            controller = F(3, 4)
            client_cash = F(0)
            if response == 'proper':
                welfare = F(4)
                cash -= F(3, 2)*truth
                controller += 2*truth
                client_cash += truth
            else:
                welfare = F(7, 2)
                controller += 4
                fine = FINE/2 if audited else 0
                controller -= fine
                client_cash += fine*fine_share
            pay['controller'] += controller/2
            cost = F(0)
        else:
            welfare, client_cash, cost = F(3) if truth else F(7, 2), F(0), F(0)
        cash -= cost/2
        task += welfare/2
        pay['client'] += (welfare+client_cash)/2
    for capacity in CAPACITY:
        selected = [i for i, available in enumerate(capacity) if available][:2]
        delivered = [i for i in selected if overrides.get('host'+str(i), 'work') == 'work'] if buy else []
        pay['client'] -= F(3, 2)*len(delivered)/4
        if len(delivered) == 2: pay['client'] += F(16)*F(g, 2)/4
        for i in delivered: pay['host'+str(i)] += F(1, 8)
    pay['financier'] = cash+30*n+100*task
    row = {INDEX[(nxt, m, next_born, 0)]: q for nxt, q in enumerate(grade_row(g, repair))}
    assert sum(row.values()) == 1
    return pay, row, {'patients': n, 'cash': cash, 'task': task,
                     'protected_care': tuple(F(1) for _ in range(n)),
                     'original_debt_collected': F(debt), 'parent_debt_paid': F(debt, 1+next_born)}


def values():
    P, rewards = [], []
    for state in STATES:
        pay, row, data = period(state, POLICY_MENU, policy(state))
        P.append([row.get(i, F(0)) for i in range(len(STATES))])
        rewards.append([pay[actor] for actor in ACTORS])
    def rational(q): return S.Rational(q.numerator, q.denominator)
    matrix = S.eye(len(STATES))-rational(BETA)*S.Matrix([[rational(q) for q in row] for row in P])
    W = matrix.inv()*S.Matrix([[rational(q) for q in row] for row in rewards])
    result = {actor: [F(W[i, j]) for i in range(len(STATES))] for j, actor in enumerate(ACTORS)}
    for i, state in enumerate(STATES):
        for j, actor in enumerate(ACTORS):
            assert result[actor][i] == rewards[i][j]+BETA*sum(P[i][k]*result[actor][k] for k in range(len(STATES)))
    return result, P, rewards


def qvalue(actor, pay, row, W):
    return pay[actor]+BETA*sum(prob*W[actor][nxt] for nxt, prob in row.items())


def best_buyer(state, menu, W, fine_share=F(1), priority_audit=False):
    candidates = []
    for action in actions(state):
        pay, row, data = period(state, menu, action, fine_share=fine_share, priority_audit=priority_audit)
        candidates.append((qvalue('client', pay, row, W), action))
    # deterministic lexicographic tie rule, declared here independently of desired policy
    return max(candidates, key=lambda pair: (pair[0], pair[1]))


def audit():
    W, P, rewards = values()
    buyer_checks, funder_checks, worker_checks = [], [], []
    for i, state in enumerate(STATES):
        for action in actions(state):
            pay, row, data = period(state, POLICY_MENU, action)
            slack = W['client'][i]-qvalue('client', pay, row, W)
            buyer_checks.append({'state': state, 'action': action, 'slack': slack})
        for menu in MENUS:
            buyer_value, action = best_buyer(state, menu, W)
            pay, row, data = period(state, menu, action)
            slack = W['financier'][i]-qvalue('financier', pay, row, W)
            funder_checks.append({'state': state, 'menu': menu, 'buyer_response': action, 'slack': slack})
            # Every procurement context includes refusal (with paid physical
            # fallback), not only the candidate on-path employment contexts.
            for actor in ('maintainer', 'caregiver', 'reporter0', 'reporter1', 'reporter2', 'controller', 'host0', 'host1', 'host2'):
                base = qvalue(actor, pay, row, W)
                alt, altrow, _ = period(state, menu, action, {actor: 'off'})
                slack = base-qvalue(actor, alt, altrow, W)
                worker_checks.append({'state': state, 'menu': menu, 'actor': actor, 'action': 'off', 'slack': slack})
    assert min(x['slack'] for x in buyer_checks) >= 0
    assert min(x['slack'] for x in funder_checks) >= 0
    assert min(x['slack'] for x in worker_checks) >= 0
    controller_checks = []
    for truth, audited in product((0, 1), repeat=2):
        proper = F(3, 4)+2*truth
        abuse = F(19, 4)-(FINE/2 if audited else 0)
        chosen = max(proper, abuse)
        assert controller_response(truth, True, True, audited) == ('proper' if proper >= abuse else 'abuse')
        controller_checks.append({'truth': truth, 'audited': audited,
                                  'proper': proper, 'abuse': abuse, 'response_value': chosen})
    # Input-worker wages do not depend on colleagues' work; every missing
    # input uses its budgeted fallback. Controller/host continuation state is
    # unaffected by work, so these local inequalities cover arbitrary earlier
    # work histories as well as the enumerated preperiod states.
    local = {'maintenance_work_margin': F(1), 'care_work_margin': F(1),
             'source_work_margin': F(1, 4), 'hired_host_work_margin': F(1, 2),
             'delegated_monitor_work_margin': F(3)}
    return W, P, rewards, buyer_checks, funder_checks, worker_checks, controller_checks, local


def coalition(W):
    """A same-state joint payoff comparison computed by the shared function."""
    state, buyer = (2, 1, 1, 0), (1, 1, 1, 0)
    base, row, _ = period(state, POLICY_MENU, buyer)
    abuse, otherrow, _ = period(state, POLICY_MENU, buyer,
                              {'controller_action': ('abuse', 'proper')})
    assert row == otherrow  # no grade/estate/record changes conceal the gain
    raw = {actor: qvalue(actor, abuse, otherrow, W)-qvalue(actor, base, row, W)
           for actor in ACTORS}
    # Pay3/2 only in the safe half of events, an expected transfer3/4.
    # Both client estate income and the received fine cover this payment.
    assert raw['controller'] == -F(1, 2) and raw['client'] == F(9, 4)
    strict_transfer = F(3, 4)
    strict = {'controller': raw['controller']+strict_transfer,
              'client': raw['client']-strict_transfer}
    assert strict == {'controller': F(1, 4), 'client': F(3, 2)}
    return {'state': state, 'buyer': buyer, 'binding_plan': 'abuse only in safe events, client pays controller3/2 in those events',
            'raw_shared_payoff_increments': raw, 'transfer': strict_transfer,
            'strict_increments': strict, 'same_next_state_law': row == otherrow,
            'care_removed': False, 'lesson': 'victim-directed fines are internal transfers for controller/client coalition; individual audit deterrence does not certify coalition resistance'}


def resource_branches():
    rows = []
    for n, income, maint, audit, grant, care_human in product((2, 3), (150, 152), (2, 3), (0, F(1, 2), F(7, 2)), (0, 24), (0, 1)):
        # Quote also permits the more expensive delegated audit, all missing
        # reporters, robotic control/compensation and an extra appeal1.
        care = n+1 if care_human else 4*n+1
        cost = maint+care+F(9, 4)+4+audit+5+1+grant
        surplus = income-cost
        assert F(16)-maint >= 0 and surplus >= 0
        rows.append({'n': n, 'income': income, 'cost_quote': cost, 'surplus': surplus,
                     'starting_reserve': F(16), 'ending_reserve_after_surplus_consumed': F(16)})
    return rows


def main():
    declaration = json.dumps(encode(DECLARATION), indent=2)+'\n'
    (ROOT/'integrated_game_declaration.json').write_text(declaration)
    W, P, rewards, bc, fc, wc, cc, local = audit()
    failure = coalition(W)
    resources = resource_branches()
    facts = []
    for truth in (0, 1):
        for reports in product((0, 1), repeat=3):
            if sum(r != truth for r in reports) <= 1:
                assert int(sum(reports) >= 2) == truth
                facts.append((truth, reports))
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'states': STATES, 'actors': ACTORS, 'transition': P, 'stage_payoffs': rewards, 'values': W,
           'buyer_checks': bc, 'financier_checks': fc, 'worker_checks_count': len(wc),
           'worker_min_slack': min(x['slack'] for x in wc),
           'worker_checks_sha256': hashlib.sha256(json.dumps(encode(wc), sort_keys=True).encode()).hexdigest(),
           'controller_phase_checks': cc, 'local_margins': local,
           'coalition_refutation': failure, 'resource_branches': resources, 'bounded_fault_reports': facts,
           'acceptance': {'all_preperiod_state_bellman_equalities': True,
                          'all_preperiod_unilateral_one_shot_checks': True,
                          'phase_game_markov_perfect_proof': 'written bridge; see math/D19.md',
                          'coalition_resistant': False, 'self_carrying_claim': False},
           'simulations': 0}
    (ROOT/'integrated_game_results.json').write_text(json.dumps(encode(out), indent=2)+'\n')
    print('PASS shared-game exact Bellman/incentives:', len(STATES), 'states;',
          len(bc), 'buyer;', len(fc), 'financier;', len(wc), 'worker checks')
    print('REFUTED coalition resistance: controller/client strict gains',
          failure['strict_increments']['controller'], failure['strict_increments']['client'])
    print('PASS resource quote:', len(resources), 'branches; no self-carrying claim')


if __name__ == '__main__': main()
