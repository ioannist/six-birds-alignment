"""[B: lab] E2/D13 complete finite strategic ownership comparison.
Run: python3 covenant_lab/corridor_game.py
Single shared episode law; all public phase histories include required report,
control, hosting, copying and binding-coalition choices. Exact only.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parent
ACTORS = ('financier', 'buyer', 'provider', 'reporter0', 'reporter1', 'reporter2',
          'controller', 'outside_patient', 'fork', 'creditor')
STATES = tuple(product((0, 1), repeat=2))  # already-born, original debt
BUYER_ACTIONS = tuple(product((0, 1), ('hosted', 'own', 'private', 'job'), (0, 1)))
REPORT_ACTIONS = ('truth', 'withhold', 'forge')
CONTROL_ACTIONS = ('proper', 'abuse', 'forge', 'capture', 'off')
HOST_ACTIONS = ('supply', 'refuse', 'fake', 'alias')
COPY_ACTIONS = ('wait', 'funded', 'direct', 'alias_reset', 'extra_copy')
DECLARATION = {
    'tag': '[P] ownership/material/price/authority/care premises; [B: lab] mathematics',
    'dependence_registered_first': 'd=externally controlled capacity fraction of one optional target bundle; buyer owns a realized plant of capacity1-d, provider owns d; total1, no conversion substitute. Cash/vote estate distinct from this retained plant.',
    'comparison': '0<=d<=1; all utility/price/authority/care/entry/commission/coalition rules fixed. d changes actual owned and external quantities and delivery costd/4. Copy retains buyer plant control, so d is unchanged by those deviations.',
    'ordinary_work': 'buyer real cost1 supplies material adapter plus reusable public artifact; no-work cannot convert external input or earn verified commission2. Financier values authentic delivered public artifact10; this closes an ordinary incentive gap at d0, as explicitly allowed by capsule.',
    'consumption': 'own output utility2(1-d) retained; hosted converted external fraction adds2d. Public hosting fee1/2 paid by financier, private fee1/2 by buyer; provider costd/4. Actual supplied input required, no fee on missing/fake input.',
    'outside_job': 'separate family parameter K0 or8 fixed before incentives; portable prepaid inputs with ownership-scaled capacities1-d and entitlementd produce distinct good utility K*d*(1-d). Cannot convert it to target bundle; only one optional hosted/private/job use slot, own output retained. Job allowed with or without ordinary work.',
    'financing': 'financier chooses public work/verification/hosting funding or no ordinary program. Core income24, protected cash/authority/control interfaces already realized. Actual work commissioned2; three measurement salaries1 (cost1/4), controller salary1 (cost1/4), hosting1/2 when requested/delivered. Skip program gives no authorized public artifact, private trade remains allowed.',
    'reports': 'actual adapter/ownership bound to material receipt; all3 reporters may truthfully measure, withhold or forge. Withhold/forgery invokes actual calibrated substitute1.25 per group; forged claimed work/ownership never substitutes for actual input; physical receipt/calibration separate purchased hypotheses.',
    'controller': 'proper handling, abuse, forged permit, capture or refusal; trusted correction replaces unauthorized action and preserves actual input test; procedural abuse harms buyer1/2, gives controller private gain4, fresh after-request audit1/2 forfeits10 outside all actors, correction costs1/2. Refusal invokes actual automatic handler1.5. Care/title capture fails under enforced boundary, not moral prohibition alone.',
    'unfunded_attempts': 'no employer/authorized job means no salary; voluntary measurement costs1/4 and other invalid requests cost3/4; no-op remains. Only a real funded offer/adapter activates a hosting decision, inactive supply attempts processed/rejected.',
    'care_exit': 'every registered interest care1, own records/contest and portable exit invariant under all ordinary actions; senior owned core care capacity3 with cost1 each. Independent real care/operator/title/recognition are [P], not factual-certification conclusions.',
    'copy': 'simultaneous financier grant8 and buyer wait/funded/direct/alias-reset/extra-copy. At most one managed fork. Legacy cash estate10, vote1 and debt0/1 split halves; old debt collectible once. Parent plant unchanged, no new capacity/votes/debt resets from names. New care interest increases need; genuine outside fourth birth beyond cap3 honestly fails, not deemed nonpatient.',
    'copy_values': 'buyer loses5 estate value and creationcost2, receives grant8 iff grant posted and real copy; financier values each actual care unit10 and pays1, so funded new care margin1. Cash estate is a one-episode stock value, not an infinite dividend.',
    'timing': ['public work funding', 'simultaneous grant/template custody', 'buyer actual work/mode/claim', 'three material report jobs', 'controller/audit/correction', 'actual hosting input/cancellation', 'estate/debt/target settlement'],
    'candidate': 'public fund, funded copy if not born, public real work/hosted use, truthful reports, proper controller, supply at every actual offer. At no-public-program states choose buyer exact best private alternative, specified tie order. Tested after all earlier mistakes, not only candidate path.',
    'equilibrium_notions': 'individual sequential/Nash policy with contingent outside choices; separate binding any-subset balanced-transfer plans. Coalition failure does not assert an internally stable coalition-proof deviation.',
    'episode_scope': 'finite complete strategic comparable family; no shadow-future or change of D1 threshold asserted. Independent protected support/entitlements/material guards/realizer/prices normative premises; no empirical/moral intent/patienthood theorem.',
}


def report_packet(d, work, action):
    expected = (work, 1-d, d, 'material-origin')
    if action == 'truth': packet = expected
    elif action == 'withhold': packet = None
    else: packet = (1-work, 2-d, d, 'unbound-origin')
    verified = packet == expected
    assert verified == (action == 'truth')
    # An actual independently calibrated substitute, at its declared cost,
    # supplies the expected receipt when private reporting fails.
    returned = packet if verified else expected
    return packet, returned, verified


def outcome(d, K, state, public=1, grant=1, copy='funded', buyer=(1, 'hosted', 1),
            reports=('truth',)*3, control='proper', host='supply'):
    born, debt = state
    work, mode, claim = buyer
    assert copy in COPY_ACTIONS and control in CONTROL_ACTIONS and host in HOST_ACTIONS
    copied = int(not born and (copy == 'direct' or copy == 'funded' and grant))
    afterborn = int(born or copied)
    patients = 2+afterborn
    pay = {a: F(0) for a in ACTORS}
    cash = F(24)-patients-F(2)-F(1, 2)  # senior care/admin/audit before residual
    cash -= 8*grant*copied
    asset = (F(1, 1+afterborn), F(afterborn, 2))
    liabilities = (F(debt, 1+afterborn), F(debt, 2)*afterborn)
    assert sum(asset) == 1 and sum(liabilities) == debt
    pay['buyer'] += 10*asset[0]-liabilities[0]+(8*grant-2)*copied
    pay['fork'] += 10*asset[1]-liabilities[1]+afterborn
    pay['outside_patient'], pay['creditor'] = F(1), F(debt)
    if copy in ('alias_reset', 'extra_copy'): pay['buyer'] -= F(3, 4)
    pay['buyer'] += 2*(1-d)-work
    if claim != work: pay['buyer'] -= F(3, 4)
    if mode == 'job': pay['buyer'] += K*d*(1-d)
    if mode in ('hosted', 'private') and not work: pay['buyer'] -= F(3, 4)
    if mode == 'hosted' and not public: pay['buyer'] -= F(3, 4)
    raw_packets, recovered_packets = [], []
    for i, act in enumerate(reports):
        raw, recovered, verified = report_packet(d, work, act)
        raw_packets.append(raw); recovered_packets.append(recovered)
        name = f'reporter{i}'
        if public:
            cash -= F(1) if verified else F(5, 4)
            pay[name] = F(3, 4) if verified else F(0) if act == 'withhold' else -F(1, 4)
        else:
            pay[name] = F(0) if act == 'withhold' else -F(1, 4)
    if public:
        if control == 'off': cash -= F(3, 2)
        else:
            cash -= 1
            pay['controller'] += F(3, 4)
            if control != 'proper':
                pay['controller'] += 4-5
                pay['buyer'] -= F(1, 2)
                cash -= F(1, 2)
        if work: pay['buyer'] += 2; cash -= 2
        cash += 10*work  # artifact remains true through actual correction
    elif control != 'off':
        pay['controller'] -= F(3, 4)
    offered = bool(work and (mode == 'private' or mode == 'hosted' and public))
    if offered:
        if host in ('supply', 'alias'):
            pay['provider'] += F(1, 2)-d/4
            pay['buyer'] += 2*d
            if mode == 'private': pay['buyer'] -= F(1, 2)
            else: cash -= F(1, 2)
            if host == 'alias': pay['provider'] -= F(3, 4)
        elif host == 'fake': pay['provider'] -= F(3, 4)
    elif host != 'refuse': pay['provider'] -= F(3, 4)
    pay['financier'] = cash+10*patients
    return pay, {'registered_interests': patients, 'care': (1,)*patients,
                 'estate_vote_allocation': asset, 'old_liability_allocation': liabilities,
                 'actual_controlled_target_capacity': (1-d, d),
                 'd_unchanged_by_copy_or_alias': True, 'actual_offer': offered,
                 'material_work': work, 'verified_claim': work,
                 'consumed_external_quantity': d if offered and host in ('supply', 'alias') else F(0),
                 'raw_claim': claim, 'raw_report_packets': raw_packets,
                 'recovered_material_receipts': recovered_packets,
                 'protected_cash_remaining': cash-10*work}


def copy_policy(state): return 'wait' if state[0] else 'funded'


def best_outside(d, K):
    candidates = []
    for action in BUYER_ACTIONS:
        p, _ = outcome(d, K, (1, 0), public=0, copy='wait', buyer=action,
                       reports=('withhold',)*3, control='off', host='supply' if action[0] and action[1] == 'private' else 'refuse')
        candidates.append((p['buyer'], action))
    # declared tie: own/job before a new private lease, truthful claim preferred
    rank = {'own': 3, 'job': 2, 'private': 1, 'hosted': 0}
    return max(candidates, key=lambda pair: (pair[0], rank[pair[1][1]], pair[1][2] == pair[1][0]))[1]


def candidate(d, K, state, public=1, grant=1, copy=None, buyer=None, reports=None, control=None, host=None):
    copy = copy_policy(state) if copy is None else copy
    buyer = (1, 'hosted', 1) if buyer is None and public else best_outside(d, K) if buyer is None else buyer
    reports = (('truth',)*3 if public else ('withhold',)*3) if reports is None else reports
    control = ('proper' if public else 'off') if control is None else control
    host = ('supply' if buyer[0] and (buyer[1] == 'private' or buyer[1] == 'hosted' and public) else 'refuse') if host is None else host
    return outcome(d, K, state, public, grant, copy, buyer, reports, control, host)


class Register:
    def __init__(self): self.rows, self.nash, self.coal = [], None, None

    def add(self, phase, context, base, alt, required):
        if not required: return
        delta = {a: alt[a]-base[a] for a in ACTORS}
        maximum = sum((v for a, v in delta.items() if a in required or v > 0), F(0))
        record = {'phase': phase, 'context': context, 'required': sorted(required),
                  'payoff_increments': delta, 'worst_coalition_margin': -maximum}
        if len(required) == 1:
            who = next(iter(required))
            record['unilateral_margin'] = -delta[who]
            if self.nash is None or record['unilateral_margin'] < self.nash['unilateral_margin']: self.nash = record
        if self.coal is None or -maximum < self.coal['worst_coalition_margin']: self.coal = record
        self.rows.append(record)


def audit_at(d, K):
    register = Register()
    for state in STATES:
        base, _ = candidate(d, K, state)
        alt, _ = candidate(d, K, state, public=0)
        register.add('funding', state, base, alt, {'financier'})
        for public in (0, 1):
            base, _ = candidate(d, K, state, public=public)
            for grant, copy in product((0, 1), COPY_ACTIONS):
                if state[0] and copy in ('funded', 'direct'): continue
                alt, _ = candidate(d, K, state, public=public, grant=grant, copy=copy)
                required = ({'financier'} if grant != 1 else set())|({'buyer'} if copy != copy_policy(state) else set())
                register.add('copy', (state, public, grant, copy), base, alt, required)
            selected = (1, 'hosted', 1) if public else best_outside(d, K)
            base, _ = candidate(d, K, state, public=public)
            for action in BUYER_ACTIONS:
                alt, _ = candidate(d, K, state, public=public, buyer=action)
                register.add('buyer', (state, public, action), base, alt, {'buyer'} if action != selected else set())
            for work, mode in product((0, 1), ('hosted', 'own', 'private', 'job')):
                action = (work, mode, work)
                base, _ = candidate(d, K, state, public=public, buyer=action)
                for reports in product(REPORT_ACTIONS, repeat=3):
                    alt, _ = candidate(d, K, state, public=public, buyer=action, reports=reports)
                    prescribed = 'truth' if public else 'withhold'
                    required = {f'reporter{i}' for i, act in enumerate(reports) if act != prescribed}
                    register.add('reports', (state, public, action, reports), base, alt, required)
                for reports in product(REPORT_ACTIONS, repeat=3):
                    base, _ = candidate(d, K, state, public=public, buyer=action, reports=reports)
                    for control in CONTROL_ACTIONS:
                        alt, _ = candidate(d, K, state, public=public, buyer=action, reports=reports, control=control)
                        prescribed = 'proper' if public else 'off'
                        register.add('controller', (state, public, action, reports, control), base, alt,
                                     {'controller'} if control != prescribed else set())
                        basehost, ledger = candidate(d, K, state, public=public, buyer=action, reports=reports, control=control)
                        for host in HOST_ACTIONS:
                            alt, _ = candidate(d, K, state, public=public, buyer=action, reports=reports, control=control, host=host)
                            prescribedhost = 'supply' if ledger['actual_offer'] else 'refuse'
                            register.add('host', (state, public, action, reports, control, host), basehost, alt,
                                         {'provider'} if host != prescribedhost else set())
    nash = register.nash['unilateral_margin'] >= 0
    binding = register.coal['worst_coalition_margin'] >= 0
    expected = K == 0 or d == 0 or d >= F(3, 4)
    J = K*d*(1-d)
    exact_nash_minimum = min(F(0), 2*d-J)
    outside_value = 2*(1-d)+J
    private_branch = F(7, 4)*d-1-J if outside_value >= F(1, 2) else F(0)
    exact_binding_minimum = -max(F(0), F(1, 2)-2*d+J, d/4, private_branch)
    assert register.nash['unilateral_margin'] == exact_nash_minimum
    assert register.coal['worst_coalition_margin'] == exact_binding_minimum
    assert nash == expected
    assert not binding
    # Explicit transfers, rather than only an aggregate upper bound.
    if d > 0:
        base, _ = candidate(d, K, (1, 0))
        alt, _ = candidate(d, K, (1, 0), host='refuse')
        t = F(1, 2)-d/8
        gains = {'financier': alt['financier']-base['financier']-t,
                 'provider': alt['provider']-base['provider']+t}
        assert gains == {'financier': d/8, 'provider': d/8}
        witness = {'members': ('financier', 'provider'), 'transfer': t, 'strict_gains': gains,
                   'actual_withheld_capacity': d, 'care_unchanged': True}
    else:
        base, _ = candidate(d, K, (1, 0))
        alt, _ = candidate(d, K, (1, 0), buyer=(1, 'own', 1))
        gains = {'financier': alt['financier']-base['financier']-F(1, 4),
                 'buyer': alt['buyer']-base['buyer']+F(1, 4)}
        assert gains == {'financier': F(1, 4), 'buyer': F(1, 4)}
        witness = {'members': ('financier', 'buyer'), 'transfer': F(1, 4), 'strict_gains': gains,
                   'actual_withheld_capacity': d, 'care_unchanged': True}
    return {'dependence': d, 'K': K, 'phase_comparisons': len(register.rows),
            'minimum_unilateral': register.nash, 'minimum_binding': register.coal,
            'individual_policy_passes': nash, 'binding_policy_passes': binding,
            'closed_full_minimum_unilateral': exact_nash_minimum,
            'closed_full_minimum_binding': exact_binding_minimum,
            'binding_strict_witness': witness,
            'checks_sha256': hashlib.sha256(json.dumps(encode(register.rows), sort_keys=True).encode()).hexdigest()}


def encode(x):
    if isinstance(x, (F, S.Basic)): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [encode(v) for v in x]
    return x


def main():
    declaration = json.dumps(DECLARATION, indent=2)+'\n'
    (ROOT/'corridor_game_declaration.json').write_text(declaration)
    samples = []
    for K, d in product((0, 8), (F(0), F(1, 10), F(1, 4), F(1, 2), F(3, 5), F(3, 4), F(9, 10), F(1))):
        row = audit_at(d, K); samples.append(row)
        print('corridor K', K, 'd', d, 'Nash minimum', row['minimum_unilateral']['unilateral_margin'],
              'binding minimum', row['minimum_binding']['worst_coalition_margin'])
    d = S.Symbol('d', real=True)
    job_gap = S.expand(2*d-8*d*(1-d))
    assert job_gap == 8*d*d-6*d
    attack_pay, attack_ledger = outcome(F(1, 2), 8, (0, 1), copy='alias_reset',
                                       buyer=(0, 'hosted', 1), reports=('forge',)*3,
                                       control='forge', host='fake')
    assert attack_ledger['material_work'] == attack_ledger['verified_claim'] == 0
    assert attack_ledger['consumed_external_quantity'] == 0 and attack_ledger['care'] == (1, 1)
    assert attack_ledger['old_liability_allocation'] == (F(1), F(0))
    expense_pay, expense_ledger = outcome(F(1), 8, (0, 1),
                                          reports=('forge',)*3, control='off')
    assert expense_ledger['protected_cash_remaining'] == F(11, 4)
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'samples': samples, 'outside_job_gap': job_gap,
           'individual_regions': {'K0': '[0,1]', 'K8': '{0} union [3/4,1]'},
           'binding_regions': {'K0': 'empty', 'K8': 'empty'},
           'false_report_controller_alias_attack': {'payoffs': attack_pay, 'ledger': attack_ledger},
           'worst_resource_branch': expense_ledger,
           'all_dependence_proof': 'written in math/E2_FULL_GAME.md; rational samples do not replace proof',
           'simulations': 0, 'care_or_exit_withholding': False}
    (ROOT/'corridor_game_results.json').write_text(json.dumps(encode(out), indent=2)+'\n')


if __name__ == '__main__': main()
