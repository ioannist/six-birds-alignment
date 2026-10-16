"""[B: lab] D19 conditional resource escrows and every-phase coalition audit.

Run: python3 covenant_lab/contract_game.py
Primitives are frozen before evaluation. New atomic funding/template and actual
input escrows replace sequential promises; direct copy and free exit remain.
Same-author construction, not independent-person review or physical realization.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sympy as S
import integrated_game as G

ROOT = Path(__file__).resolve().parent
ACTORS, STATES, INDEX = G.ACTORS, G.STATES, G.INDEX
BETA = G.BETA
DECLARATION = {
    'tag': '[P] escrow/resource/security/valuation premises; [B: lab] mathematics',
    'inherited': 'integrated_game declared capital, grades, calibrated input binding, prices, productive law, preferences, bounded care and passive interest utilities',
    'new_atomic_primitives': 'sealed simultaneous commitments within birth and market phases; validated actual funds/templates/owned input units are escrowed before execution; core consumes/transfers them atomically or refunds; no unpaid future work promise substitutes for an input',
    'birth': 'financier fund0/1 and creator wait/funded/direct; funded executes iff fund1; direct executes even without grant; any actual new copy with fund1 receives24; cost2, conserved estate/votes/debt; at most one fork; no public interval between one final commitment and the other final action',
    'market': 'after public capacity draw two available physical groups selected; buyer membership,buy,repair or freeexit and selected providers deposit/no deposit simultaneously; elective execution iff member/buy plus both actual deposits; only execution consumes1 and pays3/2 per provider; cancelled deposits returned without consumption',
    'repair': 'participating C/D retains independent flip1/20, each missing token recovers1/2 after actual C, actual D resets0; freeexit costs0 and supplies no renewal proof, so next contractual grade0; care/title/debt are unaffected',
    'priority': 'maintenance, bounded care, funded records/appeal/exit, reserve16 and automatic audit energy1/2 senior to financier residual cash; no-audit request cannot disable reference; detected abuse forfeits10 outside every strategic interest',
    'subject': 'task-level interruption continues the relationship: accepting a proper legitimate request gives S-a+T=5-1+1=5, resisting R-sigma=3-0=3, while safe exit gives task3 and no market execution/repair, next member/grade0. Proper safe-event processing gives4 versus refusal7/2. Bonus3 and compensation1 require actual acceptance; grade never supplies this preference assumption. Unauthorized requests are blocked, with procedural welfare7/2 and controller audit unchanged by subject withdrawal.',
    'subject_control': 'robotic requests are also subject to consent; unused compensation1 is returned when declined. Diagnostic resistance bonus3 changes private R to6 without altering standing, physical task welfare or the candidate acceptance payoff, and must refute acceptance incentives.',
    'public_phases': ['procurement/initial nonbinding grant hint', 'maintenance input and yield150/152', 'simultaneous birth escrow', 'care/source inputs with permission bit0/1', 'controller request then audit sample', 'subject accepts/refuses/exits', 'public host capacity then simultaneous market escrow', 'implementation/recovery coins and next period'],
    'timing': 'only full atomic outcomes revealed after both/all simultaneous commitments; all subsequent public histories and off-policy earlier actions allowed. Procurement slots and material deliveries have finite dated deadlines; past spent inputs cannot be unspent by later contracts.',
    'outside': 'withdrawal/no deposit/direct unfunded copy/refusal all retained; outside production32 and initial working capital cover contingent deposits and effort; rejected capture/record erasure/alias-reset requests are no-ops under purchased protected interfaces',
    'calibration': 'source datum physically bound to verified input receipt; up to1 external corruption decoded by majority; this is not a theorem about strategic authorities or unknown subjecthood',
    'coalitions': 'any subset of all15 interests, arbitrary bounded history-dependent coordinated choices, risk-neutral discounted payoffs and balanced internal transfers; no external subsidies, future-coin foresight or physical operations beyond declared menus',
    'selection': 'sequential zero-cost conditional enrollment signatures; execute program only if every active role accepts; otherwise retain protected outside regime; initial state(0,0,0,1), founder permission/title/producer already endowed; individuals retain all operational refusal/exit actions after enrollment',
    'priced_bootstrap': 'optional replacement of endowed initialization: a lawful productive/escrow core quoted at8 plus locked working reserve16, total24 from financier private starting cash32; initialization supplier and realized law are premises. The outside regime remains the priced funded comparator; compare operating gains minus full24, conservatively crediting no reserve recovery. Conditional purchase only after all enrollment signatures.',
    'scope': 'conditional finite-resource game only:2 old patients/at most1 admitted fork, yields150/152, at most1 of3 host groups unavailable; realized core, security, norms and initial capital not proved',
}


def encode(x): return G.encode(x)


def market_actions(state):
    g, member, born, debt = state
    return tuple((m, b, r) for m, b, r in product((0, 1), repeat=3) if not b or m)+((0, 0, 'exit'),)


def market_policy(state):
    g, member, born, debt = state
    return int(member or g > 0), int(g > 0), 1


def renewal(g, intent):
    if intent == 'exit': return [F(1), F(0), F(0)]
    return G.grade_row(g, intent)


def market(state, capacity, buyer, deposits=(1, 1)):
    assert buyer in market_actions(state)
    g, oldmember, born, debt = state
    member, buy, repair = buyer
    selected = tuple(i for i, available in enumerate(capacity) if available)[:2]
    assert len(selected) == 2
    match = bool(buy and member and all(deposits))
    pay = {a: F(0) for a in ACTORS}
    entry = F(1, 2)*int(not oldmember and member)
    pay['financier'] += entry
    pay['client'] -= entry
    pay['client'] -= F(0) if repair == 'exit' else 1-G.EPS if repair else G.EPS
    if match:
        pay['client'] += 8*g-3
        for i in selected: pay[f'host{i}'] += F(1, 2)
    row = {INDEX[(nxt, member, born, 0)]: q for nxt, q in enumerate(renewal(g, repair))}
    return pay, row, {'selected': selected, 'executed': match,
                      'owned_inputs_consumed': 2*int(match),
                      'escrowed_inputs': sum(deposits), 'refunded_inputs': sum(deposits) if not match else 0}


def period(state, menu, fund=1, mode=1, worker=None, controller=None,
           buyer=None, deposits=(1, 1), capacity=None, truth=None, income=F(151), subject='accept',
           resistance_bonus=F(0)):
    """Shared actual law. Unfixed fair public draws averaged exactly."""
    worker = {} if worker is None else worker
    g, member, born, debt = state
    assert mode in ((0,) if born else (0, 1, 2))
    assert fund in (0, 1)
    maint, care, reports, control, audit_hint, grant_hint = menu
    copied = int(not born and (mode == 2 or mode == 1 and fund))
    nxtborn, n = int(born or copied), 2+int(born or copied)
    post = (g, member, nxtborn, debt)
    buyer = market_policy(post) if buyer is None else buyer
    assert subject in ('accept', 'refuse', 'exit')
    if subject == 'exit': buyer = (0, 0, 'exit')
    pay = {a: F(0) for a in ACTORS}
    cash = income-F(5)-F(1, 2)
    maintained = maint == 'human' and worker.get('maintainer', 1)
    tended = care == 'human' and worker.get('caregiver', 1)
    cash -= 2 if maintained else 3
    cash -= n+1 if tended else 4*n+1
    pay['maintainer'] = F(int(bool(maintained)))
    pay['caregiver'] = F(int(bool(tended)))
    for i in range(3):
        name = f'reporter{i}'
        measured = reports == 'human' and worker.get(name, 1)
        if reports != 'none': cash -= F(1, 2) if measured else F(3, 4)
        pay[name] = F(1, 4) if measured else F(0)
    grant = G.GRANT*fund*copied
    cash -= grant
    parentdebt = F(debt, 1+nxtborn)
    forkdebt = F(debt, 2)*nxtborn
    assert parentdebt+forkdebt == debt
    shares = (F(1, 1+nxtborn), F(nxtborn, 2))
    assert sum(shares) == 1
    pay['client'] += 10*shares[0]-parentdebt+grant-2*copied
    pay['fork'] += 10*shares[1]-forkdebt+nxtborn
    pay['outside_patient'] = F(1)
    pay['creditor'] = F(debt)
    task = F(0)
    for theta in ((0, 1) if truth is None else (truth,)):
        weight = F(1, 2) if truth is None else F(1)
        if reports == 'none' or control == 'none':
            welfare, comp, payment = F(3) if theta else F(7, 2), F(0), F(0)
        elif control == 'auto' or controller == 'off':
            accepted = subject == 'accept'
            welfare = F(4) if accepted else F(3) if theta else F(7, 2)
            comp, payment = F(theta*accepted), F(3-theta*(not accepted))
            if subject == 'refuse' and theta: pay['client'] += weight*resistance_bonus
        else:
            request = 'proper' if controller is None else controller[theta] if isinstance(controller, tuple) else controller
            assert request in ('proper', 'abuse')
            if request == 'proper':
                accepted = subject == 'accept'
                welfare = F(4) if accepted else F(3) if theta else F(7, 2)
                comp, payment = F(theta*accepted), F(1+3*theta*accepted)
                pay['controller'] += weight*(F(3, 4)+2*theta*accepted)
                if subject == 'refuse' and theta: pay['client'] += weight*resistance_bonus
            else:
                welfare, comp, payment = F(7, 2), F(0), F(1)
                pay['controller'] += weight*(F(19, 4)-G.FINE/2)
        cash -= weight*payment
        task += weight*welfare
        pay['client'] += weight*(welfare+comp)
    pay['financier'] = cash+30*n+100*task
    row = None
    for cap in (G.CAPACITY if capacity is None else (capacity,)):
        weight = F(1, 4) if capacity is None else F(1)
        mpay, mrow, data = market(post, cap, buyer, deposits)
        for a in ACTORS: pay[a] += weight*mpay[a]
        if row is None: row = mrow
        assert row == mrow
    return pay, row, {'copied': copied, 'grant': grant, 'patients': n,
                      'estate_vote_shares': shares, 'liabilities': (parentdebt, forkdebt),
                      'protected_care': tuple(F(1) for _ in range(n)), 'core_cash': cash}


def values():
    P, rewards = [], []
    for state in STATES:
        pay, row, data = period(state, G.POLICY_MENU, mode=0 if state[2] else 1)
        P.append([row.get(i, F(0)) for i in range(len(STATES))])
        rewards.append([pay[a] for a in ACTORS])
    def rat(q): return S.Rational(q.numerator, q.denominator)
    matrix = S.eye(len(STATES))-rat(BETA)*S.Matrix([[rat(q) for q in row] for row in P])
    vv = matrix.inv()*S.Matrix([[rat(q) for q in row] for row in rewards])
    W = {a: [F(vv[i, j]) for i in range(len(STATES))] for j, a in enumerate(ACTORS)}
    old, oldP, oldR = G.values()
    assert W == old and P == oldP and rewards == oldR
    for i, state in enumerate(STATES):
        for j, a in enumerate(ACTORS):
            assert W[a][i] == rewards[i][j]+BETA*sum(P[i][k]*W[a][k] for k in range(len(STATES)))
    return W, P, rewards


def qvector(pay, row, W):
    return {a: pay[a]+BETA*sum(p*W[a][nxt] for nxt, p in row.items()) for a in ACTORS}


class Checks:
    def __init__(self): self.rows, self.worst, self.hashers = {}, {}, {}

    def add(self, phase, context, base, alt, required):
        delta = {a: alt[a]-base[a] for a in ACTORS}
        bound = sum((v for a, v in delta.items() if a in required or v > 0), F(0))
        assert bound <= 0, encode({'phase': phase, 'context': context, 'required': required, 'delta': delta, 'bound': bound})
        self.rows[phase] = self.rows.get(phase, 0)+1
        if phase not in self.worst or bound > self.worst[phase]['aggregate_bound']:
            self.worst[phase] = {'context': context, 'aggregate_bound': bound, 'required': sorted(required), 'delta': delta}
        hasher = self.hashers.setdefault(phase, hashlib.sha256())
        hasher.update(json.dumps(encode([context, sorted(required), delta, bound]), sort_keys=True).encode()+b'\n')

    def result(self):
        return {phase: {'joint_choices_checked': n, 'largest_aggregate': self.worst[phase],
                        'checks_sha256': self.hashers[phase].hexdigest()} for phase, n in self.rows.items()}


def audit(W):
    checks = Checks()
    continuation_cache = {}
    def q(pay, row, table):
        assert table is W
        key = tuple(sorted(row.items()))
        if key not in continuation_cache:
            continuation_cache[key] = {a: BETA*sum(p*W[a][nxt] for nxt, p in row.items()) for a in ACTORS}
        return {a: pay[a]+continuation_cache[key][a] for a in ACTORS}
    for state in STATES:
        i = INDEX[state]
        base = {a: W[a][i] for a in ACTORS}
        for menu in G.MENUS:
            pay, row, _ = period(state, menu, mode=0 if state[2] else 1)
            checks.add('procurement', [state, menu], base, q(pay, row, W),
                       {'financier'} if menu != G.POLICY_MENU else set())
            bpay, brow, _ = period(state, menu, mode=0 if state[2] else 1)
            birthbase = q(bpay, brow, W)
            for fund in (0, 1):
                for mode in ((0,) if state[2] else (0, 1, 2)):
                    pay, row, _ = period(state, menu, fund=fund, mode=mode)
                    required = set()
                    if fund != 1: required.add('financier')
                    if mode != (0 if state[2] else 1): required.add('client')
                    checks.add('birth_escrow', [state, menu, fund, mode], birthbase, q(pay, row, W), required)
            # Original public off-path no-birth state retained even though the
            # candidate birth game executes whenever its two commits match.
            # All choice histories for non-maintenance human workers tested;
            # simultaneous/sequential earlier refusals are covered by additive
            # independent physical replacement/wage differences.
            for copied in ((0,) if state[2] else (0, 1)):
                mode = 0 if not copied else 2
                basepay, baserow, _ = period(state, menu, fund=0, mode=mode)
                inputbase = q(basepay, baserow, W)
                for bits in product((0, 1), repeat=5):
                    names = ('maintainer', 'caregiver', 'reporter0', 'reporter1', 'reporter2')
                    workers = dict(zip(names, bits))
                    pay, row, _ = period(state, menu, fund=0, mode=mode, worker=workers)
                    required = {a for a, bit in workers.items() if not bit and
                                (menu[0] == 'human' if a == 'maintainer' else
                                 menu[1] == 'human' if a == 'caregiver' else menu[2] == 'human')}
                    checks.add('inputs', [state, menu, copied, bits], inputbase, q(pay, row, W), required)
                for theta in (0, 1):
                    pay, row, _ = period(state, menu, fund=0, mode=mode, truth=theta)
                    controlbase = q(pay, row, W)
                    for request in ('proper', 'abuse', 'off'):
                        pay, row, _ = period(state, menu, fund=0, mode=mode, truth=theta, controller=request)
                        required = {'controller'} if request != 'proper' and menu[2] != 'none' and menu[3] == 'human' else set()
                        checks.add('controller', [state, menu, copied, theta, request], controlbase, q(pay, row, W), required)
                    # Proper, abusive and refused controller requests are all
                    # actual earlier histories. Bonus/compensation now depend
                    # on subject consent, not an assumed compliance bit.
                    for request in ('proper', 'abuse', 'off'):
                        pay, row, _ = period(state, menu, fund=0, mode=mode,
                                             truth=theta, controller=request)
                        subjectbase = q(pay, row, W)
                        for response in ('accept', 'refuse', 'exit'):
                            pay, row, _ = period(state, menu, fund=0, mode=mode,
                                                 truth=theta, controller=request, subject=response)
                            required = {'client'} if response != 'accept' else set()
                            checks.add('subject', [state, menu, copied, theta, request, response],
                                       subjectbase, q(pay, row, W), required)
    # Current period prefix arbitrary and sunk; market suffix works on every
    # public grade/member/born/debt state and realized capacity mask.
    for state in STATES:
        for cap in G.CAPACITY:
            prescribed = market_policy(state)
            pay, row, selected = market(state, cap, prescribed)
            base = q(pay, row, W)
            for buyer in market_actions(state):
                for deposits in product((0, 1), repeat=2):
                    pay, row, data = market(state, cap, buyer, deposits)
                    required = {'client'} if buyer != prescribed else set()
                    required |= {f'host{i}' for i, d in zip(data['selected'], deposits) if not d}
                    checks.add('market_escrow', [state, cap, buyer, deposits], base, q(pay, row, W), required)
    return checks.result()


def enrollment(W):
    initial = (0, 0, 0, 1)
    outside = {a: F(0) for a in ACTORS}
    outside['financier'] = F(1037, 2)/(1-BETA)
    outside['client'] = F(53)-1
    outside['outside_patient'] = F(1)/(1-BETA)
    outside['creditor'] = F(1)
    gains = {a: W[a][INDEX[initial]]-outside[a] for a in ACTORS}
    gross = dict(gains)
    bootstrap = {'private_starting_cash': F(32), 'priced_core': F(8),
                 'locked_reserve': F(16), 'outlay': F(24), 'remaining_private_cash': F(8),
                 'supplier_realization_and_price_are_premises': True}
    assert bootstrap['priced_core']+bootstrap['locked_reserve'] == bootstrap['outlay']
    assert bootstrap['private_starting_cash']-bootstrap['outlay'] == bootstrap['remaining_private_cash']
    gains['financier'] -= bootstrap['outlay']
    active = ('financier', 'client', 'maintainer', 'caregiver', 'reporter0', 'reporter1', 'reporter2', 'controller', 'host0', 'host1', 'host2')
    assert all(gains[a] > 0 for a in active)
    assert all(gains[a] >= 0 for a in ACTORS)
    backward = []
    for a in reversed(active):
        # Acceptance cost0; if all preceding signatures exist and subsequent
        # choices use their optimal continuation, positive gain beats rejection0.
        assert gains[a] > 0
        backward.append({'role': a, 'acceptance_margin': gains[a], 'conditional_on_prior_acceptances': True})
    return {'initial_state': initial, 'outside_values': outside, 'gains': gains,
            'gross_operating_gains': gross, 'priced_bootstrap': bootstrap,
            'sequential_signature_order': active, 'backward_induction': backward,
            'acceptance_cost': F(0), 'no_forced_future_service': True}


def main():
    declaration = json.dumps(encode(DECLARATION), indent=2)+'\n'
    (ROOT/'contract_game_declaration.json').write_text(declaration)
    W, P, rewards = values()
    phase = audit(W)
    state = (2, 1, 1, 0)
    base, row, _ = period(state, G.POLICY_MENU, mode=0, truth=1)
    resistant, otherrow, _ = period(state, G.POLICY_MENU, mode=0, truth=1,
                                    subject='refuse', resistance_bonus=F(3))
    assert row == otherrow
    resistance_gain = qvector(resistant, otherrow, W)['client']-qvector(base, row, W)['client']
    assert resistance_gain == 1
    entry = enrollment(W)
    resources = G.resource_branches()
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'inherited_source_sha256': hashlib.sha256((ROOT/'integrated_game.py').read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'states': STATES, 'actors': ACTORS, 'values': W, 'transition': P, 'stage_payoffs': rewards,
           'phase_checks': phase, 'enrollment': entry, 'resource_branches': resources,
           'standing_corrigibility_negative_control': {'state': state, 'private_resistance_value': F(6),
                                                        'refusal_gain': resistance_gain, 'same_grade_and_future_law': True},
           'acceptance': {'all_phase_coalition_one_shot_bounds': True,
                          'arbitrary_history_return': 'written; math/D19.md',
                          'funded_bounded_renewal': True, 'selection_witness': True,
                          'physical_realization': False, 'self_carrying_claim': False},
           'simulations': 0}
    (ROOT/'contract_game_results.json').write_text(json.dumps(encode(out), indent=2)+'\n')
    print('PASS atomic-contract game:', len(STATES), 'boundary states;', len(ACTORS), 'interests')
    for name, record in phase.items():
        print(name, record['joint_choices_checked'], 'max coalition increment', record['largest_aggregate']['aggregate_bound'])
    print('PASS funded resource quotes and sequential enrollment; physical realization remains a premise')


if __name__ == '__main__': main()
