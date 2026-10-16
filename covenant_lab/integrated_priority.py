"""[B: lab] D19 protected-audit repair, with genuine off-path phase tests.
Run: python3 covenant_lab/integrated_priority.py
Same-author extension; no independent-person review is implied.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import integrated_game as G
import integrated_coalitions as C

ROOT = Path(__file__).resolve().parent
DECLARATION = {
    'tag': '[P] strengthened protected execution premise; [B: lab] computations',
    'repair': 'reference audit energy1/2 is a protected priority claim, paid before optional procurement; financier no-audit requests cannot disable it. Fines expended outside all strategic interests.',
    'retained': 'all other menus, timings, payoffs, birth/exit/resource/noise/calibration and binding-transfer hypotheses of integrated_game retained',
    'target1': 'every public period-boundary state and admitted binding joint plan',
    'target2': 'coalition behavior at every reachable public phase history, including earlier mistakes or off-policy procurement',
    'negative_controls': 'after no-grant procurement; after buyer requested zero-value service',
    'nonclaims': 'physical audit locking, source calibration, endowed productive title not proved; passing target1 cannot be promoted to target2 or self-carrying',
}


def main():
    declaration = json.dumps(DECLARATION, indent=2)+'\n'
    (ROOT/'integrated_priority_declaration.json').write_text(declaration)
    boundary = C.audit(priority=True)
    W, P, rewards = G.values()
    # No grant offered: buyer individually delays birth, anticipating the
    # candidate grant next period. Binding financier/client transfer restores
    # a worthwhile birth now. The exact shared continuation matters here.
    state = (2, 1, 0, 0)
    menu = (*G.POLICY_MENU[:5], 0)
    _, prescribed = G.best_buyer(state, menu, W, fine_share=F(0), priority_audit=True)
    assert prescribed == (1, 1, 1, 0)
    copied = (1, 1, 1, 1)
    before, row, _ = G.period(state, menu, prescribed, fine_share=F(0), priority_audit=True)
    after, nxt, _ = G.period(state, menu, copied, fine_share=F(0), priority_audit=True)
    raw = {a: G.qvalue(a, after, nxt, W)-G.qvalue(a, before, row, W) for a in G.ACTORS}
    assert raw['financier'] == 47 and raw['client'] == -F(47, 2)
    birth = {'state': state, 'fixed_menu': menu,
             'plan': 'after no-grant procurement, client copies; financier pays client24 by binding transfer',
             'raw_increments': raw, 'transfer': F(24),
             'strict_increments': {'financier': raw['financier']-24, 'client': raw['client']+24},
             'comparison_uses_actual_next_period_candidate_grant': True}
    assert birth['strict_increments'] == {'financier': F(23), 'client': F(1, 2)}
    # The buyer can make a mistaken zero-grade purchase. This is not excluded
    # from the game. Later hosts individually want fees, but a binding joint
    # cancellation avoids preparation for an elective bundle valued at zero.
    state, request = (0, 1, 1, 0), (1, 1, 1, 0)
    before, row, _ = G.period(state, G.POLICY_MENU, request, fine_share=F(0), priority_audit=True)
    after, nxt, _ = G.period(state, G.POLICY_MENU, request,
                           {f'host{i}': 'off' for i in range(3)}, fine_share=F(0), priority_audit=True)
    assert row == nxt
    raw = {a: after[a]-before[a] for a in G.ACTORS}
    transfers = {'host0': F(9, 16), 'host1': F(9, 16), 'host2': F(3, 8)}
    gains = {a: raw[a]+t for a, t in transfers.items()}
    gains['client'] = raw['client']-sum(transfers.values())
    assert gains == {'host0': F(3, 16), 'host1': F(3, 16), 'host2': F(1, 8), 'client': F(3, 2)}
    service = {'state': state, 'fixed_purchase': request,
               'plan': 'after zero-grade purchase, both selected hosts withhold; client pays each selected host3/4',
               'strict_increments': gains, 'same_next_state_law': True,
               'care_floor_removed': False, 'outside_host_capacity_masks': G.CAPACITY}
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'game_source_sha256': hashlib.sha256((ROOT/'integrated_game.py').read_bytes()).hexdigest(),
           'coalition_source_sha256': hashlib.sha256((ROOT/'integrated_coalitions.py').read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'boundary_audit': boundary, 'no_grant_phase_refutation': birth,
           'zero_value_service_phase_refutation': service,
           'acceptance': {'period_boundary_aggregate_bound': True,
                          'every_phase_coalition_resistance': False,
                          'self_carrying_claim': False}, 'simulations': 0}
    (ROOT/'integrated_priority_results.json').write_text(json.dumps(G.encode(out), indent=2)+'\n')
    print('PASS priority-audit boundary:', boundary['joint_plans_checked'], 'plans; maximum', boundary['max_coalition_increment'])
    print('REFUTED full-phase acceptance: no-grant gains', birth['strict_increments'])
    print('REFUTED zero-grade purchase phase:', gains)


if __name__ == '__main__': main()
