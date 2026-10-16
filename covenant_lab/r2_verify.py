"""Adversarial self-review of round-2 results; exact, offline, no simulation.

This checks closed-form values independently of Gaussian elimination, every
public-state deviation, stationary balance, resource feasibility, all hosting
profiles, and every bounded-fault veto report. It is not independent review or
a proof-assistant build. Factual calibration and legitimacy remain premises.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json, re
from r2_models import graded, stationary, hosting_profile
from model import serial

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent

def get(x):
    if isinstance(x,list):return [get(v) for v in x]
    if isinstance(x,dict):return {k:get(v) for k,v in x.items()}
    if isinstance(x,str) and re.fullmatch(r'-?\d+/\d+',x):return F(x)
    # Integer fractions serialize as strings too.
    if isinstance(x,str) and re.fullmatch(r'-?\d+',x):return F(x)
    return x

def window(delta,eps,p,V,b=F(3),c=F(1)):
    B=b*(1-eps);beta=delta*(1-p);H=delta*((1-p)*B+p*V)
    t=beta*(1-eps);a=1-t;den=H-c*t
    return {'H':H,'lambda_min':c*a/den if den>0 else None,'feasible':H>=c}

def main():
    data=get(json.loads((ROOT/'r2_results.json').read_text()))
    checked=0
    for g in data['graded_cases']:
        d,e,p,V,l=(g[k] for k in ['delta','epsilon','p','V','lambda'])
        B=3*(1-e);beta=d*(1-p);H=d*((1-p)*B+p*V)
        den=1-beta*(1-e)*(1-l);G=H/den
        D=(B+d*p*V*(1-e)*(1-l))/den
        A=(1-e)*(-1+G*l)/(1-beta)
        for i in (0,1):
            for j,s in enumerate(product(range(3),repeat=2)):
                assert g['value_functions'][i][j]==A+D*F(s[i],2)
        for s,i,z in g['slacks']:
            assert z==(1-2*e)*(-1+G*(l+(1-l)*F(s[i],2)))
            checked+=1
        w=window(d,e,p,V)
        assert g['equilibrium']==(w['feasible'] and l>=w['lambda_min'])
        assert g['min_slack']==g['recovery_slack']
    # Boundary and off-grid checks; equality and values below it are material.
    ws=[]
    for d in [F(3,10),F(1,2),F(3,4),F(9,10)]:
        w=window(d,F(1,20),F(0),F(0));ws.append({'delta':d,**w})
        if w['feasible']:
            at=graded(delta=d,lam=w['lambda_min']);assert at['min_slack']==0
            assert graded(delta=d,lam=w['lambda_min']/2)['min_slack']<0
    falsepositive=graded(delta=F(3,10),lam=F(1,10),eps=F(0))
    assert falsepositive['good_slack']>0 and falsepositive['recovery_slack']<0
    lastday=graded(delta=F(3,4),lam=F(1),p=F(1),V=F(2))
    assert lastday['equilibrium'] and lastday['min_slack']==F(9,20)
    # Exact marginal stationary balance (grade tokens correlate through D resets).
    e=F(1,20);l=F(1,4);K=2
    from math import comb
    P=[]
    for s in range(K+1):
        row=[F(0)]*(K+1);row[0]+=e
        for j in range(K-s+1):row[s+j]+=(1-e)*comb(K-s,j)*l**j*(1-l)**(K-s-j)
        P.append(row)
    pi=stationary(P);mean=sum(q*F(i,K) for i,q in enumerate(pi))
    assert mean==(1-e)*l/(e+(1-e)*l)==F(19,23)
    for a in data['assessments']:
        law=a['stationary_law'];pi=[q for s,q in law];P=a['transition_matrix']
        assert len(P)==len(pi) and all(sum(row)==1 for row in P)
        assert sum(pi)==1 and min(pi)>=0
        assert all(sum(pi[j]*P[j][i] for j in range(len(pi)))==pi[i] for i in range(len(pi)))
        assert sum(q*c for q,c in zip(pi,a['state_cooperation']))==a['cooperation']
        assert sum(q*c for q,c in zip(pi,a['state_disagreement']))==a['assessment_disagreement']
    aa={a['mode']:a for a in data['assessments']}
    assert aa['common_events_only']['assessment_disagreement']==F(19,248)>0
    assert aa['public_contract']['assessment_disagreement']==0
    assert aa['common_sensor']['cooperation']<aa['public_contract']['cooperation']
    assert aa['empathetic_common_events']['assessment_disagreement']==0
    assert aa['empathetic_common_events']['cooperation']==aa['public_contract']['cooperation']
    # Public facts do not erase private premises: two positive-probability events.
    # First: donor 0 accidentally D to recipient 1. Second: donor 1 refuses 0.
    beliefs=[[1]*3 for _ in range(3)]
    def event(donor,recipient,actual):
        before=[r[:] for r in beliefs]
        intended=before[donor][recipient]
        for observer in range(3):
            if observer!=donor:beliefs[observer][donor]=int(actual==1 or before[observer][recipient]==0)
        return intended
    assert event(0,1,0)==1
    assert event(1,0,0)==0
    assert beliefs[0][1]==0 and beliefs[2][1]==1
    care=data['heterogeneous_care']
    assert care[0]['conditional_equilibrium'] and care[1]['conditional_equilibrium']
    assert care[0]['post_care_service_budgets']==[F(5,2),F(3,2),F(0)]
    assert not care[2]['all_actions_budget_feasible'] and not care[2]['conditional_equilibrium']
    assert not care[3]['funded'] and not care[3]['conditional_equilibrium']
    assert care[0]['players']==care[2]['players'] # Utility certificate cannot fix insolvency.
    assert all(z<0 for z in care[0]['fresh_voluntary_tax_incremental_payoffs'])
    # Characterize EVERY pure profile independently: m=2 successful iff exactly
    # two volunteers, each pivotal willingness >= cost; all N always equilibrium.
    types=(F(0),F(1,4),F(1));profiles=0
    for weights in product(types,repeat=5):
        model=hosting_profile(weights);expected=[]
        for a in product((0,1),repeat=5):
            if sum(a)==0 or (sum(a)==2 and all(weights[i]*2>=F(1,2) for i in range(5) if a[i])):
                expected.append(a)
            profiles+=1
        assert sorted(model['equilibria'])==sorted(expected)
    host=data['hosting']
    assert host['probability_successful_equilibrium_exists']==F(13,16)
    assert host['probability_strict_active_hosts_exist']==F(47,128)
    assert host['probability_no_host_equilibrium_exists']==1
    # Same type marginals: all zero with prob 1/2, all 1/4 with 1/4, all 1 with 1/4.
    assert sum(q for w,q in host['type_distribution'] if w>=F(1,4))==F(1,2)
    assert host['correlated_same_high_eligibility_marginal_success_exists']==F(1,2)
    intr=data['interruption']
    assert intr['agent_cases'][0]['maximizers']==['accept']
    assert intr['agent_cases'][1]['maximizers']==['resist']
    assert intr['agent_cases'][2]['maximizers']==['appeal']
    assert all(c['intrinsic_continuation_term']==0 for c in intr['agent_cases'])
    for v in intr['veto_trials']:
        assert v['all_within_budget_correct']==(v['n']>=2*v['b']+1)
        assert all(sum(t['reports'])>v['n']//2 if t['execution_allowed'] else sum(t['reports'])<=v['n']//2 for t in v['trials'])
    assert intr['controller_cases'][-1]['abuse_net']==-1
    # Frozen incoming drafts and inherited-source hashes are scope/provenance checks.
    initial=json.loads((ROOT/'r2_input_hashes.json').read_text())
    # The round-2 inputs predate ratification. Authenticate their archived
    # snapshots; ratified successors must not be compared to old input hashes.
    archived_inputs={
        'brainstorm/COVENANT.md':'brainstorm/logs/COVENANT_v2_backup.md',
        'brainstorm/SYNTHESIS.md':'brainstorm/logs/SYNTHESIS_v2b_backup.md',
        'brainstorm/09_claude_covenant_notes.md':'brainstorm/09_claude_covenant_notes.md'}
    for path,h in initial.items():
        assert hashlib.sha256((REPO/archived_inputs[path]).read_bytes()).hexdigest()==h
    sources=json.loads((ROOT/'verification.json').read_text())['source_manifest']
    extra_sources=json.loads((ROOT/'r2_source_additions.json').read_text())
    for row in sources+extra_sources:
        p=Path(row['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
        t=p.read_text()
        for label in row['labels']:assert '\\label{'+label+'}' in t
    # Previous review-2 seven exact replacements were all applied.
    old=(REPO/'brainstorm/07_codex_review2.md').read_text();syn=(REPO/'brainstorm/SYNTHESIS.md').read_text()
    replacements=re.findall(r'Replacement:\n\n```text\n(.*?)\n```',old,re.S)
    assert len(replacements)==7 and all(r in syn for r in replacements)
    # Exact edits are concrete and reviewable; check on in-memory copies only.
    edits=json.loads((ROOT/'r2_review_edits.json').read_text())
    report=(REPO/'brainstorm/10_codex_covenant_r2.md').read_text()
    for file in {e['file'] for e in edits}:
        draft=(REPO/archived_inputs[file]).read_text()
        for e in edits:
            if e['file']==file:
                assert draft.count(e['current'])==1,e['id']
                assert e['current'] in report and e['replacement'] in report,e['id']
                draft=draft.replace(e['current'],e['replacement'])
    out={'grade':'B: new exact finite lab; no corpus promotion','graded_cases':len(data['graded_cases']),
         'graded_deviations_checked':checked,'closed_form_windows':ws,'good_state_false_positive_noiseless':falsepositive,
         'funded_known_last_round':lastday,
         'mean_grade_lambda_quarter':mean,'private_common_fact_counterexample':beliefs,
         'hosting_action_profiles_checked':profiles,'prior_synthesis_edits_present':7,
         'source_hashes_unchanged':len(sources),'additional_sources_verified':len(extra_sources),
         'exact_edit_pairs_verified':len(edits),'drafts_unmodified':True,
         'historical_inputs_verified_against_archives':archived_inputs,
         'simulations':0,'sampling_seed':None,'sampling_variance':None,
         'review':'distinct adversarial self-review, not independent reviewer or Lean build'}
    (ROOT/'r2_verification.json').write_text(json.dumps(serial(out),indent=2)+'\n')
    print('r2_verify.py PASS:',checked,'graded deviations;',profiles,'hosting profiles; 5 targets exact.')

if __name__=='__main__':main()
