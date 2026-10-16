"""[B: lab] Exact binding-plan audit of integrated_game, not independent review.

Run: python3 covenant_lab/integrated_coalitions.py
The repair expends fines outside every strategic interest's assets/utility.
It is a declared new enforcement technology, not ordinary damages paid victims.
"""
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
import hashlib
import json
import integrated_game as G

ROOT = Path(__file__).resolve().parent
DECLARATION = {
    'tag': '[P] fine disposition; [B: lab] coalition computations',
    'source_model': 'integrated_game.py; all its technology/ownership/menu hypotheses retained',
    'repair': 'fine_share0: caught abuse expends the full10 outside all strategic interests; no actor or trust residual claimant receives or recovers it',
    'target': 'sum-of-coalition discounted payoff upper bound for binding plans starting at each public period-boundary state; balanced transfers cannot change that sum',
    'phase_target': 'separate strong-Nash test after every procurement history, including no-audit histories',
    'dominance_reductions': 'all maintenance/care/source workers deliver: their net receipt is positive, and a coalition containing financier spends less on real human effort than fallback. For controller, work/proper dominates refusal with robotic fallback in any coalition that could prefer refusal. If client is outside, hosts prefer delivery independently; if client is inside and delivery incomplete, replace buy with no-buy, preserving all other controls and continuation. Otherwise both hosts deliver. This enumerates a weakly dominating plan for every omitted input-refusal plan.',
    'primary_controls': 'all financier menus, all buyer actions, all four proper/abuse contingent controller profiles; default off-path individual responses for actors outside coalition',
    'coalition_membership': 'contains actors changing their strategies in the current period; any other actor with positive payoff increment may be added; maximum aggregate obtained by adding all positive optional increments',
    'negative_control': 'fine_share1 transfers fines to client and must reproduce the earlier strict controller/client deviation',
    'nonclaims': 'no private-information, arbitrary physical attacks, unbounded disasters/forks or internally stable coalition-proof theorem; period-boundary aggregate bound does not certify every off-path phase',
}


def audit(priority=False):
    W, P, rewards = G.values()
    scale = lcm(*(v.denominator for values in W.values() for v in values))*320
    base = {actor: [int(scale*v) for v in vals] for actor, vals in W.items()}
    assert all(F(base[a][i], scale) == W[a][i] for a in G.ACTORS for i in range(len(G.STATES)))
    continuations = {}
    for i, state in enumerate(G.STATES):
        for action in G.actions(state):
            _, row, _ = G.period(state, G.POLICY_MENU, action)
            vv = [G.BETA*sum(q*W[a][nxt] for nxt, q in row.items()) for a in G.ACTORS]
            assert all((v*scale).denominator == 1 for v in vv)
            continuations[i, action] = [int(scale*v) for v in vv]
    checked = 0
    max_increment = None
    witness = None
    for i, state in enumerate(G.STATES):
        for menu in G.MENUS:
            _, default_buyer = G.best_buyer(state, menu, W, fine_share=F(0), priority_audit=priority)
            certified = menu[2] != 'none'
            hired = menu[3] == 'human'
            default_controller = tuple(G.controller_response(t, certified, hired, priority or menu[4] == 'reserved') for t in (0, 1))
            profiles = tuple(product(('proper', 'abuse'), repeat=2)) if certified and hired else (default_controller,)
            for action in G.actions(state):
                for profile in profiles:
                    pay, row, data = G.period(state, menu, action,
                                              {'controller_action': profile}, fine_share=F(0), priority_audit=priority)
                    required = set()
                    if menu != G.POLICY_MENU: required.add('financier')
                    if action != default_buyer: required.add('client')
                    if profile != default_controller: required.add('controller')
                    cont = continuations[i, action]
                    delta = []
                    for j, a in enumerate(G.ACTORS):
                        assert (pay[a]*scale).denominator == 1
                        delta.append(int(pay[a]*scale)+cont[j]-base[a][i])
                    aggregate = sum(d for a, d in zip(G.ACTORS, delta) if a in required or d > 0)
                    checked += 1
                    if max_increment is None or aggregate > max_increment:
                        max_increment = aggregate
                        witness = {'state': state, 'menu': menu, 'buyer': action,
                                   'controller_profile': profile, 'required': sorted(required),
                                   'payoff_increments': {a: F(d, scale) for a, d in zip(G.ACTORS, delta)},
                                   'maximizing_coalition': [a for a, d in zip(G.ACTORS, delta) if a in required or d > 0]}
    assert F(max_increment, scale) == (F(0) if priority else F(1, 2)), G.encode(witness)
    if priority:
        return {'joint_plans_checked': checked, 'max_coalition_increment': F(max_increment, scale),
                'maximizer': witness, 'priority_audit': True}
    # A simpler maximizer: financier/controller bind themselves to proper
    # processing without the audit. Every other outcome/law is identical.
    state, buyer = (2, 1, 1, 0), (1, 1, 1, 0)
    baseline, row, _ = G.period(state, G.POLICY_MENU, buyer, fine_share=F(0))
    cheap_menu = (*G.POLICY_MENU[:4], 'none', 1)
    cheap, nxt, _ = G.period(state, cheap_menu, buyer,
                           {'controller_action': ('proper', 'proper')}, fine_share=F(0))
    assert row == nxt
    assert cheap['financier']-baseline['financier'] == F(1, 2)
    assert cheap['controller'] == baseline['controller']
    saving = {'state': state, 'plan': 'financier omits audit; controller binds itself to proper processing; financier pays controller1/4',
              'strict_increments': {'financier': F(1, 4), 'controller': F(1, 4)},
              'same_next_state_law': True, 'all_task_and_care_outputs_preserved': True,
              'scope': 'binding deviation; proper processing is not self-enforcing under the no-audit residual game'}
    # A later off-path coalition remains profitable even with external fines:
    # after the financier picked no audit, proper processing can be purchased
    # by a binding financier/controller side payment in the safe event.
    state, buyer = (2, 1, 1, 0), (1, 1, 1, 0)
    menu = (*G.POLICY_MENU[:4], 'none', 1)
    before, row, _ = G.period(state, menu, buyer, fine_share=F(0))
    after, nxt, _ = G.period(state, menu, buyer,
                           {'controller_action': ('proper', 'abuse')}, fine_share=F(0))
    assert row == nxt
    raw = {a: after[a]-before[a] for a in G.ACTORS}
    assert raw['financier'] == 25 and raw['controller'] == -2
    transfer = F(5, 2)  # transfer5 in safe events only
    gains = {'financier': raw['financier']-transfer,
             'controller': raw['controller']+transfer}
    assert gains == {'financier': F(45, 2), 'controller': F(1, 2)}
    offpath = {'state': state, 'fixed_procurement_menu': menu,
               'plan': 'proper instead of abuse in safe event; financier pays controller5 in that event',
               'expected_transfer': transfer, 'strict_increments': gains,
               'same_next_state_law': True,
               'scope': 'procurement already sunk; financier/control actors can form coalition at the later phase'}
    negative_control = G.coalition(W)
    return {'joint_plans_checked': checked, 'max_coalition_increment': F(max_increment, scale),
            'maximizer': witness, 'period_boundary_refutation': saving,
            'off_path_phase_refutation': offpath,
            'fine_share1_negative_control': negative_control}


def main():
    declaration = json.dumps(G.encode(DECLARATION), indent=2)+'\n'
    (ROOT/'integrated_coalition_declaration.json').write_text(declaration)
    result = audit()
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'game_source_sha256': hashlib.sha256((ROOT/'integrated_game.py').read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           **result, 'acceptance': {'period_boundary_coalition_resistant': False,
                                  'every_phase_coalition_resistance': False,
                                  'self_carrying_claim': False}, 'simulations': 0}
    (ROOT/'integrated_coalition_results.json').write_text(json.dumps(G.encode(out), indent=2)+'\n')
    print('REFUTED period-boundary binding-plan bound:', result['joint_plans_checked'], 'plans;',
          'maximum aggregate', result['max_coalition_increment'])
    print('REFUTED every-phase coalition resistance:', result['off_path_phase_refutation']['strict_increments'])


if __name__ == '__main__': main()
