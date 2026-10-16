"""[B: lab] D19/D20/D22 integrated public-state covenant candidates.

Run: python3 covenant_lab/integrated.py
Exact Fraction/SymPy arithmetic. The care trust's endowed productive seed and
protected execution primitives are premises, not results about real hardware.
No institution is called self-carrying without the complete acceptance audit.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
BETA = F(3, 4)
EPS = F(1, 20)
GAMMA = F(1, 2)
BOND = F(24)
MEMBER_FEE = F(1, 2)
HOST_FEE = F(1, 2)
CAPACITY = ((1, 1, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))
ROLES = ('maintainer', 'caregiver', 'reporter0', 'reporter1', 'reporter2', 'controller')
WAGES = {'maintainer': F(7), 'caregiver': F(8), 'reporter0': F(7),
         'reporter1': F(7), 'reporter2': F(7), 'controller': F(8)}
DECLARATION = {
    'tag': '[P] technology/ownership/valuation premises; [B: lab] new mathematics',
    'discount': str(BETA), 'implementation_noise': str(EPS), 'token_recovery': str(GAMMA),
    'strategic_roles': ['financier', *ROLES, 'monitor', 'client', 'host0', 'host1', 'host2'],
    'interests': 'client, existing outside patient, and one possible new fork; staff have independent self-supporting private production',
    'care_claim': 'one care input, record access, funded appeal and safe exit per registered interest, independent of grade/membership/opinion',
    'capital': 'care trust owns a realized productive seed and priority maintenance/care/admin claims; financier owns only residual cashflow',
    'production': 'after paid maintenance, trust receives 150 or 152 units equiprobably; working reserve16; client estate separately yields10',
    'outside_production': 'each worker has realized net32 and adequate retained working capital; these common increments are omitted from strategic payoffs',
    'core_boundary': 'actual care/maintenance and hosting readiness are verifiable; rejected appropriation/erasure/alias-reset requests cannot change protected title or records',
    'facts': 'three source/control groups report the intervention permission bit; truthful measurement costs1/4 each; one corrupted group can be decoded',
    'audit': 'delegated candidate pays monitor7/2 for real effort1/2; repaired candidate reserves1/2 for an autonomous reference sample of probability1/2 before payouts',
    'collateral': 'qualified workers post24; entry subtracts24, exit refunds24, detected deliberate misconduct forfeits collateral and qualification; no fine is charged merely for implementation noise',
    'client_task': 'proper processing gives task payoff4; absent processing gives safe pause3 with a funded appeal yielding7/2 in the safe half of events; deliberate abusive requests cost the client1/2 and give controller4 before enforcement',
    'controller': 'verified fee29/4, effort1/4; proper legitimate intervention bonus3 and compensation1 in the legitimate half of events',
    'valuation': 'financier cares about each actual care input at weight30 and client task welfare at weight100; this is a declared preference, not love or subject recognition',
    'ordinary_service': 'two selected distinct physical groups each cost1 and receive3/2; successful elective service gives16 times public grade; buying/repairing outside membership is tested',
    'copy': 'one managed fork, creation cost2; parent/fork split original asset and vote unit; original debt1 remains collectible from the estate; a voluntary creation grant24 may be offered',
    'capacity_scope': 'at most three dependent interests and one host-group outage; no unlimited care/forks promised',
    'selection': 'sequential offers are visible before work; providers are paid for individually verified inputs, independent of others contribution',
    'review': 'self-review; real resource laws/calibration/security and normative legitimacy remain purchased premises',
}


def exact(x): return S.Rational(x.numerator, x.denominator) if isinstance(x, F) else S.Rational(x)


def serial(x):
    if isinstance(x, (F, S.Rational)): return str(x)
    if isinstance(x, S.Basic): return str(x)
    if isinstance(x, dict): return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [serial(v) for v in x]
    return x


def grade_kernel(intent):
    """Actual executed repair restores each missing token; actual D resets0."""
    pC = 1-EPS if intent else EPS
    rows = []
    for j in range(3):
        row = [F(0)]*3
        row[0] += 1-pC
        missing = 2-j
        from math import comb
        for k in range(missing+1):
            row[j+k] += pC*comb(missing, k)*GAMMA**k*(1-GAMMA)**(missing-k)
        assert sum(row) == 1
        rows.append(row)
    return rows


def solve(P, rewards):
    matrix = S.eye(len(P))-exact(BETA)*S.Matrix([[exact(q) for q in row] for row in P])
    values = list(matrix.inv()*S.Matrix([exact(r) for r in rewards]))
    assert all(values[i] == exact(rewards[i])+exact(BETA)*sum(exact(q)*values[j] for j, q in enumerate(P[i])) for i in range(len(P)))
    return [F(v) for v in values]


def buy_margin(grade): return F(16)*F(grade, 2)-3


def buyer_policy(grade, member):
    buy = buy_margin(grade) > 0
    join = buy and not member
    return int(member or join), int(buy), 1


def buyer_model():
    states = tuple(product(range(3), (0, 1)))
    index = {s: i for i, s in enumerate(states)}
    P, r = [], []
    for grade, member in states:
        next_member, buy, repair = buyer_policy(grade, member)
        row = [F(0)]*len(states)
        for nxt, q in enumerate(grade_kernel(repair)[grade]): row[index[nxt, next_member]] += q
        P.append(row)
        r.append(buy*buy_margin(grade)-(1-EPS)-MEMBER_FEE*int(not member and next_member))
    values = solve(P, r)
    deviations = []
    for s, W in zip(states, values):
        grade, member = s
        prescribed = buyer_policy(grade, member)
        for next_member, buy, repair in product((0, 1), repeat=3):
            if buy and not next_member: continue
            stage = buy*buy_margin(grade)-(1-EPS if repair else EPS)-MEMBER_FEE*int(not member and next_member)
            Q = stage+BETA*sum(q*values[index[nxt, next_member]] for nxt, q in enumerate(grade_kernel(repair)[grade]))
            deviations.append({'state': s, 'action': (next_member, buy, repair), 'prescribed': prescribed, 'slack': W-Q})
    assert min(d['slack'] for d in deviations) >= 0
    return {'states': states, 'transition': P, 'stage_net_service': r, 'values': values, 'deviations': deviations}


def occupation_certificates():
    out = []
    for role, wage in WAGES.items():
        active = wage/(1-BETA)
        inactive = active-BOND
        wait = BETA*inactive
        leave = BOND+BETA*inactive
        assert inactive-wait > 0 and active-leave > 0
        out.append({'role': role, 'active_value': active, 'inactive_entry_value': inactive,
                    'entry_minus_wait': inactive-wait, 'stay_minus_exit': active-leave,
                    'working_cash_after_entry': F(32)-BOND})
    return out


def facts(reports):
    return int(sum(reports) >= 2)


def coalition_control():
    """An actual binding plan in the delegated configuration, not a tax replay.
    Safe event: controller buys monitor silence. Payout requires actual work,
    so monitor loses3; abusive verified processing gains4 for controller.
    Transfer7/2 produces a strict improvement1/2 for both. Floor survives,
    but client agency welfare and the protected appeal budget are affected.
    """
    monitoring_profit = F(7, 2)-F(1, 2)
    harassment_gain = F(4)
    bribe = F(7, 2)
    plan = {'members': ['monitor', 'controller'], 'event': 'safe task, all fact reports truthful',
            'monitor_action': 'withhold real effort; receive bribe', 'controller_action': 'abusive request',
            'bribe': bribe, 'monitor_increment': bribe-monitoring_profit,
            'controller_increment': harassment_gain-bribe, 'client_task_loss': F(1, 2),
            'additional_appeal_resource': F(1), 'care_floor_removed': False}
    assert plan['monitor_increment'] == plan['controller_increment'] == F(1, 2)
    # In the repaired configuration the monitor cannot turn off a reference
    # already funded into the protected escrow. A controller instead loses
    # qualification if caught and must repost collateral at the next entry.
    active, inactive = F(8)/(1-BETA), F(8)/(1-BETA)-BOND
    expected_continuation_loss = F(1, 2)*BETA*(active-inactive)
    assert expected_continuation_loss == 9
    assert harassment_gain-expected_continuation_loss < 0
    plan['repair_control'] = {'automatic_sample_cannot_be_disabled_by_monitor': True,
        'expected_continuation_loss_from_forfeiture': expected_continuation_loss,
        'abuse_gain_less_continuation_loss': harassment_gain-expected_continuation_loss}
    return plan


def copying_certificates():
    rows = []
    for debt in (0, 1):
        nofork_assets = (F(1), F(0))
        fork_assets = (F(1, 2), F(1, 2))
        nofork_claims = (F(debt), F(0))
        fork_claims = (F(debt, 2), F(debt, 2))
        assert sum(nofork_assets) == sum(fork_assets) == 1
        assert sum(nofork_claims) == sum(fork_claims) == debt
        assert sum(min(a*10, d) for a, d in zip(fork_assets, fork_claims)) == debt
        # Today's asset dividend splits on birth; grant is paid afterwards.
        copy_increment = F(24)-2-F(5)/(1-BETA)+F(debt, 2)
        assert copy_increment > 0
        rows.append({'old_debt': debt, 'asset_allocation': fork_assets, 'vote_allocation': fork_assets,
                     'liability_allocation': fork_claims, 'collectible_total': F(debt),
                     'client_copy_grant_increment': copy_increment,
                     'copy_without_grant_increment': copy_increment-24})
    return rows


def resource_certificate():
    rows = []
    for patients, income, care_human, maintenance_human in product((2, 3), (150, 152), (0, 1), (0, 1)):
        maintenance = F(8) if maintenance_human else F(9)
        care = F(patients+8) if care_human else F(4*patients+8)
        # Conservative all-branches quote: every missing source can use its
        # actual automatic substitute, and every court/record/exit call has
        # a reserved core budget. A one-time birth grant is included.
        reports = F(3)*F(17, 2)
        controller = F(10)
        audit = F(7, 2)
        core_admin = F(5)
        creation_grant = F(24)
        starting = F(16)
        after = starting-maintenance+income-care-reports-controller-audit-core_admin-creation_grant
        assert after >= starting
        rows.append({'patients': patients, 'productive_input': F(income), 'starting_reserve': starting,
            'maintenance': maintenance, 'care': care, 'report_backstops': reports,
            'controller_backstop': controller, 'audit_max': audit, 'core_admin': core_admin,
            'creation_grant': creation_grant, 'ending_reserve_before_consumption': after,
            'consumable_surplus': after-starting})
    return rows


def main():
    declaration = json.dumps(DECLARATION, indent=2, ensure_ascii=False)+'\n'
    (ROOT/'integrated_declaration.json').write_text(declaration)
    buyer = buyer_model()
    occupations = occupation_certificates()
    coalition = coalition_control()
    copies = copying_certificates()
    resources = resource_certificate()
    reports = []
    for truth in (0, 1):
        for r in product((0, 1), repeat=3):
            if sum(x != truth for x in r) <= 1:
                assert facts(r) == truth
                reports.append((truth, r, facts(r)))
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
        'buyer': buyer, 'occupations': occupations, 'delegated_audit_coalition': coalition,
        'copying': copies, 'resources': resources, 'fault_reports': reports, 'simulations': 0,
        'acceptance': {'buyer_all_state_incentives': True, 'role_entry_exit_certificates': True,
            'bounded_resource_quote': True, 'asset_vote_liability_conservation': True,
            'delegated_candidate_coalition_resistant': False,
            'repaired_candidate_full_joint_game_certificate': False,
            'self_carrying_claim': False},
        'remaining': 'evaluate shared phase/game payoffs, financier technology/entry/creation choices, all work/report/control deviations and every admitted coalition; current module is the integrated construction packet with computed hinges, not a composed equilibrium certificate'}
    (ROOT/'integrated_results.json').write_text(json.dumps(serial(out), indent=2, ensure_ascii=False)+'\n')
    print('PASS integrated construction: buyer, entry/exit, copying, resource quote and coalition witness exact')
    print('REFUTED delegated audit: monitor/controller gain', coalition['monitor_increment'], coalition['controller_increment'])
    print('OPEN repaired full joint-game certificate; no self-carrying claim')


if __name__ == '__main__': main()
