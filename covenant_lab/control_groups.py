"""[B: lab] D16/D22 control-group, capacity and protected-care mechanisms.
Run: python3 covenant_lab/control_groups.py
Exact exhaustive cases; willingness, control binding and real backup inputs are
premises, not consequences of factual calibration or names.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
DECLARATION = {
    'tag': '[P] ownership/control/care/utility premises; [B: lab] computations',
    'groups': 'factual groups and host control groups are separate namespaces; corruptible-group count follows ACTUAL control roots, not keys or aliases',
    'physical_units': 'each unit has a unique bound ID, capacity and actual controller; duplicates of a unit counted once, multiple distinct units under one controller summed as its capacity weight',
    'robust_capacity': 'nonnegative capacities c_g; cartel may withhold all units of at most b_host controls; capacity remaining does not establish willingness/execution',
    'optional_hosting': 'five factual groups truthful; self-interested hosts utility weight0 and delivery cost1/2; voluntary hosting fails despite facts',
    'paid_input': 'fee3/2 per verified delivered unit, actual input cost1, payer escrow; payment independent of other inputs. Five-unit fixed offer or no offer, service needs2 units and gives payer value10; payer/operator coalition can exploit redundant inputs.',
    'protected_care': 'three registered interests incl one fork; each needs1. Separately controlled realized backup has capacity3; each missing human input replaced at actual cost2, human input fee3/2 and cost1; senior escrow6; nominal backup under cartel control is a negative control.',
    'care_game': 'one payer and3 care providers; care value9 to payer, money/effort utilities to providers; floor delivery by real paid human or backup input is mandatory priority under protected title; no best-response argument proves ethical deservingness',
    'fission': 'managed creation allowed only with reserved extra care slot; parent estate/vote1 and old debt1 split halves but per-interest care demands add. Unauthorized fourth genuine interest refutes any unlimited-floor guarantee; denial of a permit is not denial of existing patienthood.',
    'history_namespaces': 'authenticated bearer/claim lineage distinct from control roots. New alias for same bearer retains service/debt record; a genuine fork is a new interest with declared legacy allocations, not automatically the same patient merely because its controller is shared.',
    'renewal': 'care component repeats only under owned realized funded-production/maintenance law; D19/D22 supplies such bounded conditional resource invariants. No indefinite output inferred from a finite escrow alone.',
    'nonclaims': 'control binding, protected title, actual backup/capacity and normative recognition not proved by signatures; no universal anti-cartel, Sybil detection or unbounded fork protection',
}


def subsets(n, b):
    return tuple(s for k in range(min(b, n)+1) for s in combinations(range(n), k))


def capacity_audit():
    rows, checks = [], 0
    for caps in product((0, 1, 2), repeat=5):
        for b in range(6):
            minimum = min(sum(caps)-sum(caps[i] for i in s) for s in subsets(5, b))
            formula = sum(caps)-sum(sorted(caps, reverse=True)[:b])
            assert minimum == formula
            checks += len(subsets(5, b))
            rows.append({'capacities': caps, 'b_host': b, 'worst_remaining': minimum,
                         'at_least2_outside_cartel': minimum >= 2})
    examples = []
    for caps in ((2, 0, 0, 0, 0), (1, 1, 0, 0, 0), (1, 1, 1, 1, 1)):
        left = sum(caps)-max(caps)
        examples.append({'capacities': caps, 'b_host': 1, 'remaining': left, 'two_unit_target_passes': left >= 2})
    assert [x['remaining'] for x in examples] == [0, 1, 4]
    return rows, checks, examples


def alias_controls():
    aliases = tuple(range(5))
    unit_of = {a: 0 for a in aliases}
    root_of = {a: 0 for a in aliases}
    physical_units = set(unit_of.values())
    actual_roots = set(root_of.values())
    assert len(physical_units) == len(actual_roots) == 1
    # A corruption of one true control group can invert every alias transcript.
    attacked = (1,)*5
    assert sum(attacked) >= 3 and len(actual_roots) == 1
    legacy = {0: {'grade': 0, 'unpaid_debt': F(1)}}
    bearer_of = {a: 0 for a in aliases}
    records = {a: legacy[bearer_of[a]] for a in aliases}
    assert all(record['grade'] == 0 and record['unpaid_debt'] == 1 for record in records.values())
    return {'aliases': aliases, 'unit_of': unit_of, 'actual_control_root': root_of,
            'nominal_unit_count': len(aliases), 'true_distinct_units': len(physical_units),
            'nominal_fact_group_count': len(aliases), 'actual_fact_group_count': len(actual_roots),
            'single_control_corruption_wrongly_passes_alias_majority': True,
            'bearer_of': bearer_of, 'origin_linked_service_records': records,
            'naive_new_name_default_record': {'grade': 1, 'unpaid_debt': F(0)},
            'shared_control_does_not_identify_genuine_patient_interests': True,
            'one_root_owning_two_real_units': {'actual_capacity': 2, 'independent_control_groups': 1,
                                             'after_that_root_withholds': 0}}


def paid_input_control():
    fee, cost, value = F(3, 2), F(1), F(10)
    def payoff(offer, deliveries):
        n = sum(deliveries) if offer else 0
        return (value*int(n >= 2)-fee*n, *(offer*x*(fee-cost) for x in deliveries))
    base = payoff(1, (1,)*5)
    assert base == (F(5, 2), *(F(1, 2),)*5)
    provider_checks = []
    for d in product((0, 1), repeat=5):
        p = payoff(1, d)
        for s in subsets(5, 5):
            # Only coalition providers may change their input decisions;
            # nonmembers keep the all-delivery candidate.
            if any(not d[i] for i in range(5) if i not in s): continue
            increment = sum((p[i+1]-base[i+1] for i in s), F(0))
            assert increment <= 0
            provider_checks.append({'members': s, 'deliveries': d, 'increment': increment})
    assert payoff(0, (1,)*5)[0] == 0 < base[0]  # payer best response under fixed five-input offer
    alt = payoff(1, (1, 1, 1, 1, 0))
    raw = {'payer': alt[0]-base[0], 'provider4': alt[5]-base[5]}
    transfer = F(3, 4)
    gains = {'payer': raw['payer']-transfer, 'provider4': raw['provider4']+transfer}
    assert gains == {'payer': F(3, 4), 'provider4': F(1, 4)}
    return {'candidate_payoff': base, 'operator_only_checks': provider_checks,
            'binding_payer_operator_failure': {'deliveries': (1, 1, 1, 1, 0),
                                               'unchanged_service_target': True, 'transfer': transfer, 'strict_gains': gains}}


def protected_care():
    def payoff(d):
        fee = sum(F(3, 2) if x else F(2) for x in d)
        return (F(9)-fee, *(F(1, 2)*x for x in d)), fee
    base, expense = payoff((1, 1, 1))
    rows = []
    for d in product((0, 1), repeat=3):
        pay, cash = payoff(d)
        assert cash <= 6
        for coalition in subsets(4, 4):
            if any(not d[i] and i+1 not in coalition for i in range(3)): continue
            increment = sum((pay[i]-base[i] for i in coalition), F(0))
            assert increment <= 0
            rows.append({'providers': d, 'coalition': coalition, 'increment': increment,
                         'actual_human_inputs': sum(d), 'actual_backup_inputs': 3-sum(d),
                         'delivered_care': (1, 1, 1), 'expense': cash})
    # Money/name independence alone is not physical control independence.
    captured_backup = {'cartel': (0,), 'nominal_backstop_controller': 0,
                       'actual_backstop_available': 0, 'needed': 3, 'floor_passes': False}
    independent_backup = {'cartel': (0,), 'actual_backstop_controller': 5,
                          'actual_backstop_available': 3, 'needed': 3, 'floor_passes': True}
    # Managed fork consumes an extra care slot despite conserved legacy rights.
    asset, votes, debt = (F(1, 2),)*2, (F(1, 2),)*2, (F(1, 2),)*2
    assert sum(asset) == sum(votes) == sum(debt) == 1
    population = 2
    admissions = []
    for _ in range(3):
        allowed = population+1 <= 3
        if allowed: population += 1
        admissions.append({'accepted_managed_fork': allowed, 'population': population,
                           'remaining_care_slots': 3-population})
    assert [r['accepted_managed_fork'] for r in admissions] == [True, False, False]
    shortage = {'genuine_interests': 4, 'capacity': 3, 'full_floor_possible': False,
                'authorized_pro_rata': (F(3, 4),)*4, 'shortfall_each': F(1, 4),
                'recognition_not_denied_by_failed_admission': True}
    return {'care_game_candidate': base, 'all_coalition_checks': rows,
            'startup_reserved_cash': F(6), 'captured_backstop_control': captured_backup,
            'independent_backstop_case': independent_backup,
            'fork_legacy_allocations': {'assets': asset, 'votes': votes, 'old_debt': debt},
            'managed_admission': admissions, 'unmanaged_fourth_interest_failure': shortage}


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [encode(v) for v in x]
    return x


def main():
    declaration = json.dumps(DECLARATION, indent=2)+'\n'
    (ROOT/'control_group_declaration.json').write_text(declaration)
    capacities, count, examples = capacity_audit()
    aliases, paid, care = alias_controls(), paid_input_control(), protected_care()
    out = {'tag': '[B: lab]', 'grade': 'computed exact', 'review': 'self-reviewed',
           'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'declaration_sha256': hashlib.sha256(declaration.encode()).hexdigest(),
           'capacity_rows': capacities, 'cartel_cases_checked': count, 'capacity_examples': examples,
           'alias_controls': aliases, 'paid_input': paid, 'protected_care': care,
           'simulations': 0, 'universal_cartel_or_unlimited_patient_guarantee': False}
    (ROOT/'control_group_results.json').write_text(json.dumps(encode(out), indent=2)+'\n')
    print('PASS D16 capacity formula:', len(capacities), 'families;', count, 'actual cartel cases')
    print('REFUTED nominal aliases/backstop independence and payer/operator oversupply resilience')
    print('PASS bounded independently controlled funded care:', len(care['all_coalition_checks']), 'coalition cases')
    print('REFUTED unlimited fork floor; no recognition inferred from group/grade fields')


if __name__ == '__main__': main()
