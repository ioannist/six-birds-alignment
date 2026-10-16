"""Integrity checks for this research packet, not tests of a duplicate model.
Run: python3 math/validate_delivery.py
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent.parent
audit = json.loads((ROOT/'covenant_lab/audit_results.json').read_text())
for name, digest in audit['provenance']['current_ratified_drafts'].items():
    assert hashlib.sha256((ROOT/'brainstorm'/name).read_bytes()).hexdigest() == digest
for name, digest in audit['provenance']['lab_source_hashes'].items():
    assert hashlib.sha256((ROOT/'covenant_lab'/name).read_bytes()).hexdigest() == digest
for row in json.loads((ROOT/'math/proposed_edits.json').read_text()):
    # After the owner-approved application (2026-10-08) each edit is applied: its replacement
    # is present; before application its current text occurs exactly once.
    text = (ROOT/row['file']).read_text()
    assert text.count(row['replacement']) >= 1 or text.count(row['current']) == 1
    if row['current'].startswith('|'):
        old, new = row['current'].split('|'), row['replacement'].split('|')
        assert len(old) == len(new)
        if row['file'] == 'brainstorm/CATALOGUE.md':
            identifier = old[1].strip()
            allowed = 2 if identifier.startswith(('C', 'E')) else 4 if identifier.startswith(('A', 'B')) else 3
            assert all(old[i] == new[i] for i in range(len(old)) if i != allowed)
for prefix, maximum in [('C', 15), ('D', 23), ('E', 7)]:
    for i in range(1, maximum+1):
        assert (ROOT/f'math/{prefix}{i}.md').exists()

trust = (ROOT/'lean/trust_base.txt').read_text()
axioms = {}
for name, receipt in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", trust):
    axioms[name] = [] if not receipt.strip() else re.split(r',\s*', receipt.strip())
for name in re.findall(r"'([^']+)' does not depend on any axioms", trust):
    axioms[name] = []
assert not ({a for aa in axioms.values() for a in aa} - {'propext', 'Classical.choice', 'Quot.sound'})
modules = {'Recovery': ['D7', 'E3', 'D18'], 'Decoding': ['D5', 'D18'],
           'Horizon': ['D3', 'E5', 'D18'], 'Discounted': ['D18'], 'Carrier': ['C13'],
           'Behavioral': ['D18'], 'StochasticGame': ['D18'], 'CertificationControls': ['D18'],
           'Coalitions': ['D15', 'D19'], 'Assessment': ['D8'], 'RolePrivacy': ['C2'],
           'ControlGroups': ['D16', 'D22'], 'Evidence': ['D23'], 'Adoption': ['D14'],
           'Dependence': ['E2', 'D13']}
rows = []
for source in sorted((ROOT/'lean/Alignment').glob('*.lean')):
    text = source.read_text()
    assert not re.search(r'\bsorry\b|^axiom ', text, re.M)
    compiled = ROOT/'lean/.lake/build/lib/lean/Alignment'/source.with_suffix('.olean').name
    assert compiled.is_file() and compiled.stat().st_mtime_ns >= source.stat().st_mtime_ns, source
    namespace = re.search(r'^namespace ([\w.]+)', text, re.M)[1]
    for short in re.findall(r'^theorem (\w+)', text, re.M):
        name = namespace+'.'+short
        assert name in axioms, name
        ids = (['D1', 'D18'] if short == 'threshold_endpoint_signs' else
               ['D11', 'D18'] if short in ('interruption_iff', 'deterrence_iff', 'strict_deterrence_iff') else
               ['D10', 'D18']) if source.stem == 'Payoffs' else modules[source.stem]
        rows.append({'declaration': name, 'catalogue_ids': ids, 'grade': 'kernel-checked',
                     'source': str(source.relative_to(ROOT/'lean')), 'axioms': axioms[name],
                     'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
assert len(rows) == len(axioms) and len(rows) >= 27
required_certification = {
    'Alignment.Decoding.majority_correct',
    'Alignment.Decoding.decoder_exists_iff',
    'Alignment.Behavioral.truncated_cauchy',
    'Alignment.Behavioral.payoff_tendsto',
    'Alignment.Behavioral.one_shot_certifies_best_response',
    'Alignment.StochasticGame.one_shot_deviation_implies_markov_perfect',
    'Alignment.StochasticGame.one_shot_deviation_implies_legal_markov_perfect',
    'Alignment.StochasticGame.supported_joint_action_legal',
    'Alignment.CertificationControls.bad_profile_not_markov_perfect',
    'Alignment.CertificationControls.good_profile_not_legal_markov_perfect',
    'Alignment.Coalitions.coalition_sum_le_forced_upper',
    'Alignment.Coalitions.forced_upper_attained',
    'Alignment.Coalitions.balanced_transfers_preserve_sum',
    'Alignment.Coalitions.no_pareto_improvement',
    'Alignment.Coalitions.atomic_stage_cap',
    'Alignment.Assessment.affine_bellman',
    'Alignment.Assessment.public_gap_iff',
    'Alignment.Assessment.public_root_endpoint_signs',
    'Alignment.RolePrivacy.fiber_private_iff_action_factor',
    'Alignment.RolePrivacy.no_original_package_with_accountability',
    'Alignment.RolePrivacy.future_injective',
    'Alignment.ControlGroups.added_alias_no_capacity_gain',
    'Alignment.ControlGroups.floor_feasible_iff',
    'Alignment.Evidence.posterior_separation_identity',
    'Alignment.Evidence.exact_summary_must_be_injective',
    'Alignment.Evidence.odds_cross_bound',
    'Alignment.Evidence.unobserved_prediction',
    'Alignment.Adoption.entry_improves_potential',
    'Alignment.Adoption.exit_improves_potential',
    'Alignment.Adoption.detailed_balance_stationary',
    'Alignment.Dependence.outside_passing_region',
    'Alignment.Dependence.binding_gain_strict'}
assert required_certification <= set(axioms)
(ROOT/'lean/theorem_inventory.json').write_text(json.dumps({'toolchain': 'leanprover/lean4:v4.28.0',
    'mathlib_revision': '8f9d9cff6bd728b17a24e163c9402775d9e6a365', 'theorems': rows}, indent=2)+'\n')
assert audit['review']['checks'] == 12007
assert audit['review']['imports_existing_lab_code'] is False
assert audit['review']['simulations'] == 0
assert 'Build completed successfully (375 jobs).' in (ROOT/'math/B4_build_receipt.txt').read_text()
assert json.loads((ROOT/'math/B4_results.json').read_text())['nonstandard_axioms'] == []
gates = json.loads((ROOT/'covenant_lab/gate_results.json').read_text())
assert gates['source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/gates.py').read_bytes()).hexdigest()
assert gates['declaration_sha256'] == hashlib.sha256((ROOT/'covenant_lab/gate_declaration.json').read_bytes()).hexdigest()
assert gates['whole_world_states'] == 8192 and gates['macros_per_date'] == 169
assert [set(int(i) for i, passed in row['gates'].items() if not passed) for row in gates['models']] == [
    set(), {1}, {3}, {4}, {5}, {6, 7}, {7}, {2, 8}]
for stem, declaration in [('integrated', 'integrated_declaration'),
                          ('integrated_game', 'integrated_game_declaration'),
                          ('integrated_coalition', 'integrated_coalition_declaration'),
                          ('integrated_priority', 'integrated_priority_declaration')]:
    source = 'integrated_coalitions' if stem == 'integrated_coalition' else stem
    receipt = json.loads((ROOT/f'covenant_lab/{stem}_results.json').read_text())
    assert receipt['source_sha256'] == hashlib.sha256((ROOT/f'covenant_lab/{source}.py').read_bytes()).hexdigest()
    assert receipt['declaration_sha256'] == hashlib.sha256((ROOT/f'covenant_lab/{declaration}.json').read_bytes()).hexdigest()
    assert receipt['simulations'] == 0 and receipt['acceptance']['self_carrying_claim'] is False
game = json.loads((ROOT/'covenant_lab/integrated_game_results.json').read_text())
assert len(game['states']) == 24 and len(game['actors']) == 15
assert len(game['buyer_checks']) == 216 and len(game['financier_checks']) == 3456
assert game['worker_checks_count'] == 31104
coal = json.loads((ROOT/'covenant_lab/integrated_coalition_results.json').read_text())
assert coal['game_source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/integrated_game.py').read_bytes()).hexdigest()
assert coal['joint_plans_checked'] == 51840 and coal['max_coalition_increment'] == '1/2'
assert coal['acceptance']['period_boundary_coalition_resistant'] is False
priority = json.loads((ROOT/'covenant_lab/integrated_priority_results.json').read_text())
assert priority['game_source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/integrated_game.py').read_bytes()).hexdigest()
assert priority['coalition_source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/integrated_coalitions.py').read_bytes()).hexdigest()
assert priority['boundary_audit']['joint_plans_checked'] == 51840
assert priority['boundary_audit']['max_coalition_increment'] == '0'
assert priority['acceptance']['every_phase_coalition_resistance'] is False
atomic = json.loads((ROOT/'covenant_lab/atomic_service_results.json').read_text())
assert atomic['source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/atomic_service.py').read_bytes()).hexdigest()
assert atomic['declaration_sha256'] == hashlib.sha256((ROOT/'covenant_lab/atomic_service_declaration.json').read_bytes()).hexdigest()
assert atomic['stage_cap'] == ['627/400', '627/400']
assert atomic['family_profiles_checked'] == 6561 and atomic['simulations'] == 0
assert atomic['pure_stage_equilibria'] == [['exit', 'exit'], ['C', 'C']]
contract = json.loads((ROOT/'covenant_lab/contract_game_results.json').read_text())
assert contract['source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/contract_game.py').read_bytes()).hexdigest()
assert contract['inherited_source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/integrated_game.py').read_bytes()).hexdigest()
assert contract['declaration_sha256'] == hashlib.sha256((ROOT/'covenant_lab/contract_game_declaration.json').read_bytes()).hexdigest()
assert {k: v['joint_choices_checked'] for k, v in contract['phase_checks'].items()} == {
    'procurement': 3456, 'birth_escrow': 13824, 'inputs': 165888,
    'controller': 31104, 'subject': 93312, 'market_escrow': 2688}
assert all(v['largest_aggregate']['aggregate_bound'] == '0' for v in contract['phase_checks'].values())
assert contract['standing_corrigibility_negative_control']['refusal_gain'] == '1'
assert contract['enrollment']['priced_bootstrap']['outlay'] == '24'
assert contract['enrollment']['gains']['financier'] == '190931/502'
assert contract['simulations'] == 0
assert contract['acceptance']['physical_realization'] is False
assert contract['acceptance']['self_carrying_claim'] is False
assessment = json.loads((ROOT/'covenant_lab/assessment_game_results.json').read_text())
assert assessment['source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/assessment_games.py').read_bytes()).hexdigest()
assert assessment['declaration_sha256'] == hashlib.sha256((ROOT/'covenant_lab/assessment_game_declaration.json').read_bytes()).hexdigest()
assert assessment['original_transition_sha256'] == hashlib.sha256((ROOT/'covenant_lab/r2_results.json').read_bytes()).hexdigest()
arows = {row['mode']: row for row in assessment['results']}
assert {m: len(r['states']) for m, r in arows.items()} == {
    'private_noisy': 63, 'common_events_only': 51, 'public_contract': 7,
    'common_sensor': 7, 'empathetic_common_events': 7}
assert sum(len(r['all_selected_donor_slacks']) for r in arows.values()) == 810
assert all(arows[m]['markov_perfect_at_discount'] for m in ('public_contract', 'common_sensor', 'empathetic_common_events'))
assert arows['common_events_only']['markov_perfect_at_discount'] is False
assert F(arows['common_events_only']['public_initial_nash_refutation']['triggered_initial_gain']) > 0
assert arows['private_noisy']['private_nash_refuted_by_feasible_policy'] is True
assert arows['private_noisy']['full_state_slacks_are_private_equilibrium_verdict'] is False
for name in ('public_contract', 'common_sensor', 'empathetic_common_events'):
    interval = [F(v) for v in arows[name]['symbolic_formula']['threshold_isolation']]
    assert 0 < interval[0] < interval[1] < 1 and interval[1]-interval[0] < F(1, 10**13)
    assert arows[name]['symbolic_bellman_identities_checked'] == 21
c15 = json.loads((ROOT/'math/C15_source_results.json').read_text())
assert c15['script_sha256'] == hashlib.sha256((ROOT/'math/c15_sources.py').read_bytes()).hexdigest()
assert len(c15['source_records']) == 27 and len(c15['targets']) == 17
for record in c15['source_records']:
    text = Path(record['path']).read_text()
    assert record['source_sha256'] == hashlib.sha256(Path(record['path']).read_bytes()).hexdigest()
    assert record['statement'] in text and len(record['grade_as_recorded_in_ratified_index']) == 1
    assert record['source_grade_promoted'] is False
    assert record['has_own_statement_label'] is True
    assert '\\label{'+record['exact_anchor']+'}' in record['statement']
assert all(row['named_deployment_outcome'] == 'missing mapping' for row in c15['targets'])
assert c15['lab_examples']['factual_quorum']['target_distance'] == 3
assert len(c15['lab_examples']['factual_quorum']['reports']) == 8
assert c15['lab_examples']['public_grade_hiddenness']['nonconstant_public_readout_factors_through_predictive_class'] is True
for stem, declaration in [('role_privacy', 'role_privacy_declaration'), ('control_group', 'control_group_declaration')]:
    source = 'control_groups' if stem == 'control_group' else stem
    receipt = json.loads((ROOT/f'covenant_lab/{stem}_results.json').read_text())
    assert receipt['source_sha256'] == hashlib.sha256((ROOT/f'covenant_lab/{source}.py').read_bytes()).hexdigest()
    assert receipt['declaration_sha256'] == hashlib.sha256((ROOT/f'covenant_lab/{declaration}.json').read_bytes()).hexdigest()
    assert receipt['simulations'] == 0
role = json.loads((ROOT/'covenant_lab/role_privacy_results.json').read_text())
assert role['cases']['base']['C4prime'] and role['cases']['base']['action_accountable']
assert role['cases']['base']['original_C4'] is False
assert len(role['all_binary_current_channels']) == 16
assert role['action_based_guess_success'] == '3/4'
groups = json.loads((ROOT/'covenant_lab/control_group_results.json').read_text())
assert len(groups['capacity_rows']) == 1458 and groups['cartel_cases_checked'] == 27216
assert len(groups['protected_care']['all_coalition_checks']) == 54
assert groups['paid_input']['binding_payer_operator_failure']['strict_gains'] == {'payer': '3/4', 'provider4': '1/4'}
assert groups['alias_controls']['true_distinct_units'] == groups['alias_controls']['actual_fact_group_count'] == 1
assert all(r['grade'] == 0 and r['unpaid_debt'] == '1' for r in groups['alias_controls']['origin_linked_service_records'].values())
assert groups['protected_care']['captured_backstop_control']['floor_passes'] is False
assert groups['protected_care']['unmanaged_fourth_interest_failure']['full_floor_possible'] is False
evidence = json.loads((ROOT/'covenant_lab/type_evidence_results.json').read_text())
assert evidence['source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/type_evidence.py').read_bytes()).hexdigest()
assert evidence['declaration_sha256'] == hashlib.sha256((ROOT/'covenant_lab/type_evidence_declaration.json').read_bytes()).hexdigest()
assert evidence['latent_path_comparisons'] == 254 and len(evidence['uninformative_grade_paths']) == 144
assert evidence['grade_mean'] == '19/21'
precision = evidence['precision_repair']
assert len(precision['indices']) == 257 and len(precision['transition_table']) == 514
assert precision['exact_word_reconstructions_and_quantized_checks'] == 8190
assert precision['posterior_error_bound'] == '41/841' and precision['next_type_error_bound'] == '123/3364'
assert precision['strict_history_merger']['exact_posterior0'] != precision['strict_history_merger']['exact_posterior1']
assert precision['MAP_last_record_summary']['current_MAP_error'] == '1/20'
assert precision['MAP_last_record_summary']['next_MAP_error'] == '13/80'
assert evidence['simulations'] == 0 and evidence['patienthood_or_good_intent_inference'] is False
adoption = json.loads((ROOT/'covenant_lab/adoption_population_results.json').read_text())
assert adoption['source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/adoption_population.py').read_bytes()).hexdigest()
assert adoption['declaration_sha256'] == hashlib.sha256((ROOT/'covenant_lab/adoption_population_declaration.json').read_bytes()).hexdigest()
assert len(adoption['families']) == 495 and adoption['micro_actor_matching_checks'] == 768
assert adoption['plain']['probabilities'][3][1] == '1/2'
assert adoption['plain']['expected_updates'][3] == '10'
assert adoption['subsidy_half']['probabilities'][2][1] == '2/3'
assert adoption['high_entry_hysteresis']['absorbing'] == [0, 4, 6]
assert adoption['founder_license_revoked']['expected_updates'][6] == '147/10'
assert adoption['temporary_subsidy'][-1]['eventual_all_adopt_probability'] == '85/128'
assert adoption['simulations'] == 0 and adoption['forward_looking_population_equilibrium_claim'] is False
corridor = json.loads((ROOT/'covenant_lab/corridor_game_results.json').read_text())
assert corridor['source_sha256'] == hashlib.sha256((ROOT/'covenant_lab/corridor_game.py').read_bytes()).hexdigest()
assert corridor['declaration_sha256'] == hashlib.sha256((ROOT/'covenant_lab/corridor_game_declaration.json').read_bytes()).hexdigest()
assert len(corridor['samples']) == 16 and sum(r['phase_comparisons'] for r in corridor['samples']) == 554816
for row in corridor['samples']:
    d, K = F(row['dependence']), row['K']
    assert F(row['minimum_unilateral']['unilateral_margin']) == min(F(0),2*d-K*d*(1-d))
    assert row['individual_policy_passes'] == (K == 0 or d == 0 or d >= F(3,4))
    assert row['binding_policy_passes'] is False
    assert all(F(x) > 0 for x in row['binding_strict_witness']['strict_gains'].values())
assert corridor['false_report_controller_alias_attack']['ledger']['verified_claim'] == 0
assert corridor['false_report_controller_alias_attack']['ledger']['consumed_external_quantity'] == '0'
assert corridor['worst_resource_branch']['protected_cash_remaining'] == '11/4'
assert corridor['simulations'] == 0 and corridor['care_or_exit_withholding'] is False
print('PASS: ratified/source hashes, exact edit cells, all target files,', len(rows), 'theorem mappings/axiom receipts')
