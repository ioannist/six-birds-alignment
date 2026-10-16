"""Distinct adversarial self-review: algebra, terminal incentives, source map.
This is not an independent review or a Lean formalization.
"""
from model import *
import sympy as S
from symbolic import formulas,x,z
import hashlib,re

def finite_horizon(T=4,k=2,delta=F(3,4)):
    ss,P,r,outcome=carrier(k=k)
    w=[[F(0) for _ in ss] for _ in range(2)]; minima=[]
    for remaining in range(1,T+1):
        nw=[[r[i][j]+delta*sum(P[j][l]*w[i][l] for l in range(len(ss))) for j in range(len(ss))] for i in range(2)]
        slacks=[]
        for j,s in enumerate(ss):
            for i in range(2):
                a=[policy(s,t,'reset') for t in range(2)];a[i]=1-a[i]
                dev=sum(pr*(u[i]+delta*w[i][ss.index(t)]) for pr,t,u in outcome(s,a))
                slacks.append(nw[i][j]-dev)
        minima.append(min(slacks));w=nw
    assert minima[0]==F(-9,10)
    return {'horizon':T,'delta':str(delta),'minimum_slacks_by_remaining_rounds':list(map(str,minima)),
            'equilibrium':False,'terminal_V':'0'}

def main():
    checks=[]
    for k in (1,2):
        ss,P,r,outcome=carrier(k=k)
        assert all(sum(row)==1 and all(t>=0 for t in row) for row in P)
        f=formulas(k)
        for delta,p,V in [(F(3,4),F(0),F(0)),(F(9,10),F(1,20),F(2))]:
            a=evaluate(delta,p,V,k=k)
            for j,s in enumerate(ss):
                b=ss.index((s[1],s[0]));assert a['values'][0][j]==a['values'][1][b]
                for i in range(2):
                    rhs=sum(pr*(u[i]+delta*(p*max(F(0),V-F(1,2))*int(t==(0,0))+(1-p)*a['values'][i][ss.index(t)])) for pr,t,u in outcome(s,tuple(policy(s,t,'reset') for t in range(2))))
                    assert a['values'][i][j]==rhs
            for state,slack in f:
                exact=slack.subs({x:S.Rational(delta*(1-p)),z:S.Rational(delta*p*max(F(0),V-F(1,2)))})
                expected=next(t for s,i,t in a['slacks'] if s==state and i==0)
                assert exact==S.Rational(expected)
        # Stationary law: stochastic, not deterministically formed under noise.
        n=len(ss);A=[[P[j][i]-F(i==j) for j in range(n)] for i in range(n)]
        A[-1]=[F(1)]*n;y=[F(0)]*(n-1)+[F(1)];pi=solve(A,y)
        assert all(t>0 for t in pi) and sum(pi)==1
        avg=sum(pi[j]*r[0][j] for j in range(n))
        checks.append({'k':k,'stationary_law':list(map(str,pi)),'GG_mass':str(pi[0]),'mean_payoff':str(avg)})
    grimthreshold=F(80,209)
    assert evaluate(grimthreshold,mode='grim')['min_slack']==0
    assert not evaluate(grimthreshold-F(1,10000),mode='grim')['equilibrium']
    assert evaluate(grimthreshold+F(1,10000),mode='grim')['equilibrium']
    # Whole-history split, same profile/counts/payoffs.
    histories=[[(1,1),(0,1),(1,1)],[(0,1),(1,1),(1,1)]]
    witness=[]
    for hist in histories:
        s=(0,0)
        for e in hist:s=update(s,e,2,'reset')
        a=tuple(policy(s,i,'reset') for i in range(2))
        prob=F(1)
        for j in range(2):prob *= F(19,20) if a[j] else F(1,20)
        witness.append({'history':hist,'state':s,'next_CC_probability':str(prob)})
    assert witness[0]['next_CC_probability']=='19/400' and witness[1]['next_CC_probability']=='361/400'
    # Good/marked alone omits repair age, hence is not a closed Markov state.
    ss,P,_,_=carrier(k=2)
    assert P[ss.index((1,0))][ss.index((0,0))]==F(19,20)
    assert P[ss.index((2,0))][ss.index((0,0))]==0
    for n in range(1,8):
        for b in range(3):assert certification(n,b)['decodable']==(n>=2*b+1)
    sr=json.loads((ROOT/'symbolic_results.json').read_text())
    assert all(v['certified_nonnegative'] for v in sr['bonus_monotonicity'])
    # Actual label/grade sources, not earlier digest guesses.
    repo=ROOT.parent;Papers=repo.parent/'six-birds-papers'
    inventory={
      'Tsiokos_2026_Institutions_Are_Strict_Extensions_of_the_Game.tex':['prop:carrier-nondefinability','prop:formation-formed','prop:material-forcing','prop:washout-mechanism','prop:coercion-null-probe','prop:self-dual-obstruction','prop:self-dual-breaker','prop:away-from-self-duality-selection','subsec:run-only-no-shortcut','prop:promotion-certificate'],
      'Tsiokos_2026_A_Closure_Architecture_for_Consciousness.tex':['thm:t17o','def:cpackage','thm:t5','sec:selfaudit','sec:boundaries'],
      'Tsiokos_2026_Six_Birds_Foundations_III_A_Finite_Audited_Interaction_Calculus_for_SBT.tex':['cl:thm:24','cl:thm:25','sn:15.2'],
      'Tsiokos_2026_Six_Birds_Foundations_IV_A_Catalog_of_Layer_Agnostic_Structural_Laws.tex':['thm:F15a'],
      'Tsiokos_2026_Six_Birds_Foundations_V_Endogenous_Closure_A_Catalog_of_Structural_Laws_for_Living_Cognitive_and_Social_Systems.tex':['thm:e13-chain','prop:e13-flat','tmpl:e13'],
      'Tsiokos_2026_Six_Birds_Verified_I_Layer_Receipts_and_Purchase_Laundering.tex':['thm:R6','thm:R7','cm:m14'],
      'Tsiokos_2026_Six_Birds_Verified_X_Wholes_That_Grow_Each_Other.tex':['thm:MOT5'],
      'Tsiokos_2026_Six_Birds_Verified_XI_Self_Carried_Closure.tex':['thm:null-bootstrap','thm:carriage','thm:siphon','thm:transversal','thm:audit-boundary'],
      'Tsiokos_2026_Six_Birds_Verified_XIII_Time_Charge_and_Currency.tex':['thm:atlas'],
      'Tsiokos_2026_Six_Birds_Verified_XIV_Objectivity_Without_Finality.tex':['thm:corruption','thm:identifiable','ex:blind'],
      'Tsiokos_2026_Six_Birds_No_Go_Theorems_for_Audited_Emergence.tex':['thm:NG_LADDER_IDEM']}
    source_manifest=[]
    for name,labels in inventory.items():
        f=Papers/name;text=f.read_text()
        for label in labels:assert '\\label{'+label+'}' in text
        source_manifest.append({'path':str(f),'labels':labels,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    extra={
      '/home/repos/six-birds-foundations-v/paper/supplement/supp_templates.tex':['def:e8','lem:e8'],
      '/home/repos/six-birds-transcendence/cst-tt/registries/FINAL_THEOREM_STATUS.csv':[],
      '/home/repos/six-birds-transcendence/cst-tt/handoff/CST-TT-08_SCIENCE_HANDOFF.md':[]}
    for name,labels in extra.items():
        f=Path(name);text=f.read_text()
        for label in labels:assert '\\label{'+label+'}' in text
        source_manifest.append({'path':name,'labels':labels,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
    originals={name:hashlib.sha256((repo/'brainstorm'/name).read_bytes()).hexdigest() for name in ['SYNTHESIS.md','COVENANT.md']}
    result={'self_review':'Bellman residuals; symmetry; symbolic/numerical agreement; root and derivative certificates; full-state deviations; terminal credible selection; finite-horizon failure; stationary distributions; source label existence plus manual statement/grade inspection',
            'stationary':checks,'finite_horizon_negative':finite_horizon(),'grim_threshold':str(grimthreshold),
            'stage_split':witness,'binary_label_not_Markov':True,'source_manifest':source_manifest,
            'unmodified_draft_hashes':originals,
            'hosting_negative':'Plain donation H costs h and only benefits partner; strictly dominated by N for h>0',
            'corrigibility_negative':{'accept_payoff':'0','resist_payoff':'1','standing_after_resist':'marked','consciousness_variable':False},
            'coercion_information_negative':{'worlds':['theta=0','theta=1'],'free_action':[0,0],'informed_enforcer_forced_action':[0,1],'information_bits_free':'0','information_bits_forced':'1'}}
    (ROOT/'verification.json').write_text(json.dumps(serial(result),indent=2)+'\n')
    print('PASS: all exact self-review checks; no network; no Lean build claimed.')
    for c in checks:print(c)

if __name__=='__main__':main()
