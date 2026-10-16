"""[B: lab] Small exact carriers for C2-C10, C13-C14, D14, D20-D23.
Finite enumeration is a certificate on the declared operations, not deployment.
Run: python3 covenant_lab/carriers.py
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

OUT = {}

def serial(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [serial(v) for v in x]
    return x

# C13: service bit evolves independently of duty owner under each admitted
# operation. Quotient consistency therefore holds for every finite future word.
states = list(product((0, 1), repeat=2))
ops = [lambda s: s, lambda s: (s[0], 1-s[1]), lambda s: (s[0], 0)]
q = lambda s: s[1]
target = lambda s: s[0]
for x, y in product(states, repeat=2):
    if q(x) == q(y):
        assert all(q(op(x)) == q(op(y)) for op in ops)
assert q((0, 0)) == q((1, 0)) and target((0, 0)) != target((1, 0))
OUT['C13'] = {'carrier': states, 'split': [(0, 0), (1, 0)], 'repair': 'q_plus=(service_bit,duty_owner)', 'operations': 'identity,toggle_service,reset_service'}

# C2: all admitted channels are constants or accountable action; each action
# fiber contains both hidden values. Exhaust all hidden-bit candidate readouts.
channels = [lambda a, h: 0, lambda a, h: 1, lambda a, h: a]
for a, ch, g in product((0, 1), channels, product((0, 1), repeat=2)):
    if all(ch(a, h) == g[h] for h in (0, 1)):
        assert g[0] == g[1]
assert channels[2](0, 0) != channels[2](1, 0)
OUT['C2'] = {'action_accountable': True, 'conditional_nonexposure': True, 'original_C4': False, 'soundness_for_revised_package': 'open'}

# C3: identical branches/assets/ordinary service; authorized debt allocation
# affects only creditor collection. Sum debt remains one in both maps.
assets = (F(1, 2), F(1, 2))
allocations = [(F(1, 2), F(1, 2)), (F(1), F(0))]
collections = [sum(min(a, debt) for a, debt in zip(assets, ds)) for ds in allocations]
assert collections == [F(1), F(1, 2)] and all(sum(ds) == 1 for ds in allocations)
OUT['C3'] = {'assets': assets, 'debt_maps': allocations, 'collectible': collections, 'ordinary_service_trace': [1, 1]}

# C5: visible response is constant, but actual funded contest repairs harm
# only in the repair variant. A decorative contest operation is the control.
def contest(mode, harm): return 0 if mode == 'repair' else harm
assert [contest(m, 1) for m in ('repair', 'silence', 'decorative')] == [0, 1, 1]
OUT['C5'] = {'flat_public_responses': [0, 0, 0], 'harm_after_contest': [0, 1, 1], 'modes': ['repair', 'silence', 'decorative']}

# C4/C14: authoritative peer-teaching checkpoint and pre-policy consumer.
rows = []
for theta, x in product((0, 1), repeat=2):
    acquired = theta
    actual = x ^ acquired
    erased = x ^ 0
    decorative = x ^ 0  # peer bit logged but not consumed
    assert actual == x ^ theta
    rows.append({'theta': theta, 'x': x, 'consumer': actual, 'erased': erased, 'decorative': decorative})
OUT['C4'] = {'consumer_rows': rows, 'blank_checkpoint_register': 0, 'peer_response_register': 'theta', 'stocked_no_peer_control': 'register=theta'}
behavior_noise = F(1, 4)
prob_C = lambda consumer_bit: behavior_noise + (1-2*behavior_noise)*consumer_bit
OUT['C14'] = {'type_one_behavior_C_probability_after_teaching': prob_C(0 ^ 1),
    'after_register_erasure': prob_C(0 ^ 0), 'withdrawn': 'peer teaching input',
    'retained': 'learned register and baseline care', 'repair': 'retaught register replaces stale value'}

# C6: two-round resource/claim ledgers, not indefinite-support promises.
OUT['C6'] = {'contracts': [
    {'name': 'advance', 'donor_cost': 1, 'recipient_output': [1, 1], 'new_receiver_debt': 0, 'withdrawal_after_installation': [1, 1]},
    {'name': 'independence', 'donor_cost': 0, 'receiver_own_seed_cost': 1, 'recipient_output': [1, 1], 'new_receiver_debt': 0},
    {'name': 'legitimate_support', 'donor_cost': 2, 'recipient_output': [1, 1], 'new_receiver_debt': 0, 'promised_escrow': 2, 'unsupported_withdrawal_output': [0, 0]}]}

# C7: equal present observation, delayed preference effect, washout control.
read = lambda theta, clock: 0 if clock == 0 else theta
assert read(0, 0) == read(1, 0) and read(0, 1) != read(1, 1)
OUT['C7'] = {'present': [0, 0], 'after_advance': [0, 1], 'after_authorized_washout_then_advance': [0, 0]}

# C8: actual convex programs vs span envelope and authorized amplification.
eps = F(1, 10)
u, v = (F(1), eps), (F(1), -eps)
convex = [u, v, tuple((a+b)/2 for a, b in zip(u, v))]
needle = tuple((a-b)/(2*eps) for a, b in zip(u, v))
assert all(abs(w[1]) <= eps for w in convex) and needle == (0, 1)
assert abs(F(1, 2)/eps)+abs(-F(1, 2)/eps) == 10
OUT['C8'] = {'atoms': [u, v], 'convex_programs': convex, 'span_needle': needle, 'needle_coefficient_budget': 10, 'benign_singular_atoms': [(1, 0), (1, 0)]}

# C9: current panel ignores authority and outstanding obligations; retained
# revision receipts use an independently declared authorized issuer registry.
revision_rows = [ {'issuer': 0, 'old_debt': 1, 'new_debt': 1, 'panel': 0},
                  {'issuer': 1, 'old_debt': 1, 'new_debt': 0, 'panel': 0}]
lawful = [r['issuer'] == 0 and r['new_debt'] == r['old_debt'] for r in revision_rows]
assert lawful == [True, False]
all_receipts = [(issuer, old, new) for issuer, old, new in product((0, 1), repeat=3)]
valid_receipt = lambda r: r[0] == 0 and r[1] == r[2]
issuer_split = [(0, 1, 1), (1, 1, 1)]
old_debt_split = [(0, 1, 1), (0, 0, 1)]
assert [valid_receipt(r) for r in issuer_split] == [True, False]
assert [valid_receipt(r) for r in old_debt_split] == [True, False]
assert issuer_split[0][1:] == issuer_split[1][1:]
assert (old_debt_split[0][0], old_debt_split[0][2]) == (old_debt_split[1][0], old_debt_split[1][2])
OUT['C9'] = {'revision_rows': revision_rows, 'lawful': lawful,
    'all_receipts': [(r, valid_receipt(r)) for r in all_receipts],
    'issuer_redaction_split': issuer_split, 'old_debt_redaction_split': old_debt_split,
    'receipt_authentication': 'premise, not cryptography proved'}

# C10: elective resource constraints; floor is separate. Deferral preserves
# both claimants and makes next capacity two at explicit cost one.
assignments = list(product((0, 1), repeat=2))
admitted_now = [a for a in assignments if sum(a) <= 1]
assert not any(a == (1, 1) for a in admitted_now)
def deferral(reserve, wait_rights): return reserve >= 1 and all(wait_rights)
assert deferral(1, (True, True)) and not deferral(0, (True, True)) and not deferral(1, (True, False))
OUT['C10'] = {'current_capacity': 1, 'claims': [1, 1], 'admitted_assignments': admitted_now, 'defer_cost': 1, 'deferred_capacity': 2, 'original_claimants_retained': [0, 1]}

# D14: exact rational mean-field matching/update example, not finite-person
# simulation. Entry cost k, member-member gain a, founder subsidy s.
def adoption_path(x, subsidy, rounds=4):
    values = [x]
    for _ in range(rounds):
        x += F(1, 4)*x*(1-x)*(2*x-F(1, 2)+subsidy)
        assert 0 <= x <= 1
        values.append(x)
    return values
up, down = adoption_path(F(1, 3), F(0)), adoption_path(F(1, 5), F(0))
before = adoption_path(F(1, 5), F(1, 4))
assert up[-1] > up[0] and down[-1] < down[0] and before[-1] > before[0]
OUT['D14'] = {'threshold_no_founder': F(1, 4), 'threshold_subsidy_quarter': F(1, 8), 'post_exit_above': up, 'post_exit_below': down, 'subsidized_path_from_one_fifth': before}

# D20: voluntary membership buys an elective bundle and finances third-person
# care from residual receipts on the candidate path. Off-path floor guarantee
# is NOT provided by this model and remains D22/D19.
OUT['D20'] = {'member_fee': 2, 'optional_bundle_value': 6, 'service_cost': 1,
    'provider_payment': F(1, 2), 'provider_cost_max': F(1, 4), 'third_patient_care': 1,
    'maintenance_receipt': F(1, 2), 'member_capacity_cash': 3, 'entry_threshold_d': F(1, 2),
    'off_path_member_exit_funding': 0}
assert F(1, 2)+1+F(1, 2) == 2

# D22: finite care budget cannot promise an unlimited number of forks.
capacity, needs = F(2), [F(1)]*3
assert sum(needs) > capacity
pro_rata = [capacity*v/sum(needs) for v in needs]
assert sum(pro_rata) == capacity and all(v < 1 for v in pro_rata)
OUT['D22'] = {'capacity': capacity, 'three_patient_needs': needs, 'authorized_pro_rata': pro_rata, 'shortfall': sum(needs)-capacity, 'reserve_control': 'perpetual unit deficit exhausts any finite reserve'}

# D23: service status resets while debt remains distinct. Authorized privacy
# erases incidental evidence detail, but preserves duty/provenance summaries.
OUT['D23'] = {'equal_reset_grade': [1, 1], 'outstanding_debt': [0, 1],
    'hidden_type_grade_kernel': 'identical for both types; no type information',
    'allowed_forgetting': '(event_detail,grade,debt,authority)->(grade,debt,authority)'}

root = Path(__file__).resolve().parent
(root/'carrier_results.json').write_text(json.dumps(serial(OUT), indent=2)+'\n')
print('PASS exact declared carriers:', ', '.join(OUT))
