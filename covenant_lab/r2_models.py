"""Round-2 exact finite constructions. Offline, rational arithmetic, no simulation.

Models are deliberately separate: graded incentives; private assessments;
funded heterogeneous care; threshold hosting; interruption/controller abuse.
Their predicates, payers, and action alphabets are not silently combined.
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
from pathlib import Path
import json
from model import solve, serial, policy, update, certification

ROOT=Path(__file__).resolve().parent

def kernel(states,outcomes,actions):
    n=len(states);index={s:i for i,s in enumerate(states)}
    P=[[F(0) for _ in states] for _ in states];r=[[F(0) for _ in states] for _ in range(2)]
    for j,s in enumerate(states):
        for q,t,u in outcomes(s,actions(s)):
            P[j][index[t]]+=q
            for i in range(2):r[i][j]+=q*u[i]
    assert all(sum(row)==1 for row in P)
    return P,r,index

def graded(delta=F(3,4),lam=F(1,4),eps=F(1,20),p=F(0),V=F(0),b=F(3),c=F(1),K=2):
    """Finite public grades j/K. A C restores each missing token with chance lam.
    D resets to zero. Actual peer service creates benefit b*own_grade; each C
    costs c. Terminal V*next_grade is an externally financed reward, not an
    endogenous host equilibrium. Both actors prescribe C at every grade.
    """
    ss=list(product(range(K+1),repeat=2))
    def outcomes(s,a):
        for e in product((0,1),repeat=2):
            pe=F(1)
            for i in range(2):pe*=1-eps if e[i]==a[i] else eps
            options=[]
            for i in range(2):
                if not e[i]:options.append([(F(1),0)])
                else:
                    m=K-s[i]
                    options.append([(F(comb(m,j))*lam**j*(1-lam)**(m-j),s[i]+j) for j in range(m+1)])
            u=tuple(b*F(s[i],K)*e[1-i]-c*e[i] for i in range(2))
            for ((q0,t0),(q1,t1)) in product(*options):yield pe*q0*q1,(t0,t1),u
    P,r,idx=kernel(ss,outcomes,lambda s:(1,1));beta=delta*(1-p)
    A=[[F(i==j)-beta*P[i][j] for j in range(len(ss))] for i in range(len(ss))]
    R=[[V*F(s[i],K) for s in ss] for i in range(2)]
    W=[solve(A,[r[i][j]+delta*p*sum(P[j][l]*R[i][l] for l in range(len(ss))) for j in range(len(ss))]) for i in range(2)]
    slacks=[]
    for j,s in enumerate(ss):
        for i in range(2):
            a=[1,1];a[i]=0
            Q=sum(q*(u[i]+delta*(p*R[i][idx[t]]+(1-p)*W[i][idx[t]])) for q,t,u in outcomes(s,a))
            slacks.append((s,i,W[i][j]-Q))
    B=b*(1-eps)
    D=(B+delta*p*V*(1-eps)*(1-lam))/(1-beta*(1-eps)*(1-lam))
    gain=delta*((1-p)*D+p*V)
    for s,i,slack in slacks:
        assert slack==(1-2*eps)*(-c+gain*(lam+(1-lam)*F(s[i],K)))
    return {'delta':delta,'lambda':lam,'epsilon':eps,'p':p,'V':V,'B_effective':B,
        'min_slack':min(z for s,i,z in slacks),'equilibrium':all(z>=0 for s,i,z in slacks),
        'slacks':slacks,'value_functions':W,'recovery_slack':(1-2*eps)*(-c+gain*lam),
        'good_slack':(1-2*eps)*(-c+gain),'mean_grade':(1-eps)*lam/(eps+(1-eps)*lam)}

def stationary(P):
    n=len(P);A=[[P[j][i]-F(i==j) for j in range(n)] for i in range(n)]
    A[-1]=[F(1)]*n;pi=solve(A,[F(0)]*(n-1)+[F(1)])
    assert sum(pi)==1 and all(q>=0 for q in pi)
    assert all(sum(pi[j]*P[j][i] for j in range(n))==pi[i] for i in range(n))
    return pi

def assessment(mode,eps=F(1,20),obs=F(1,20)):
    """3 persons; each self-assesses good, six off-diagonal private bits.
    Simple-standing-style update: donor good iff observed C OR observer
    assesses recipient bad. Actors C iff their recipient assessment is good.
    These declared self-views are a toy convention, not a literature replication.
    Public mode adds a common contract eligibility bit; hosting judgments can
    differ without redefining the contract's compliance predicate.
    """
    public=mode in ('public_contract','common_sensor')
    edges=[(i,j) for i in range(3) for j in range(3) if i!=j]
    ss=list(product((0,1),repeat=3 if public else 6));idx={s:j for j,s in enumerate(ss)}
    def read(s,i,j):return s[j] if public else (1 if i==j else s[edges.index((i,j))])
    P=[[F(0) for s in ss] for s in ss];coop=[];discord=[]
    for row,s in enumerate(ss):
        cr=F(0)
        for donor,recipient in edges:
            intended=read(s,donor,recipient)
            for actual in (0,1):
                pa=1-eps if actual==intended else eps
                cr+=pa*F(actual,6)
                if public:
                    err=F(29,4000) if mode=='common_sensor' else F(0)
                    for flipped in (0,1):
                        q=err if flipped else 1-err
                        report=1-actual if flipped else actual
                        t=list(s);t[donor]=int(report==1 or s[recipient]==0)
                        P[row][idx[tuple(t)]]+=F(1,6)*pa*q
                else:
                    observers=[j for j in range(3) if j!=donor]
                    err=obs if mode=='private_noisy' else F(0)
                    for flips in product((0,1),repeat=2):
                        t=list(s);q=F(1)
                        for observer,flip in zip(observers,flips):
                            q*=err if flip else 1-err
                            seen=1-actual if flip else actual
                            perspective=donor if mode=='empathetic_common_events' else observer
                            t[edges.index((observer,donor))]=int(seen==1 or read(s,perspective,recipient)==0)
                        P[row][idx[tuple(t)]]+=F(1,6)*pa*q
        coop.append(cr)
        discord.append(F(0) if public else sum(F(read(s,j,i)!=read(s,k,i),3) for i in range(3) for j,k in [tuple(t for t in range(3) if t!=i)]))
    assert all(sum(row)==1 for row in P)
    # Restrict to states reachable from the declared all-good start.
    reached={idx[(1,)*len(ss[0])]}
    while True:
        more=reached|{j for i in reached for j,q in enumerate(P[i]) if q}
        if more==reached:break
        reached=more
    ids=sorted(reached);Q=[[P[i][j] for j in ids] for i in ids]
    pi=stationary(Q)
    return {'mode':mode,'states_reachable':len(ids),'cooperation':sum(q*coop[i] for q,i in zip(pi,ids)),
        'assessment_disagreement':sum(q*discord[i] for q,i in zip(pi,ids)),
        'stationary_law':[(ss[i],q) for i,q in zip(ids,pi)],'transition_matrix':Q,
        'state_cooperation':[coop[i] for i in ids],'state_disagreement':[discord[i] for i in ids],
        'implementation_noise':eps,
        'observation_noise':obs if mode=='private_noisy' else F(29,4000) if mode=='common_sensor' else F(0),
        'is_equilibrium_certificate':False}

def heterogeneous(delta=F(3,4),tax=(F(1,2),F(1,2)),endowment=(F(4),F(3),F(0)),care=(F(1),F(1),F(1))):
    """Two productive players; protected third patient has no feasible service C.
    Renewable endowments and care escrow are explicit external resource premises.
    Different optional costs/benefits; fixed taxes do not depend on standing.
    """
    costs=(F(1),F(3,2));benefits=(F(3),F(4));eps=F(1,20);k=2
    ss=list(product(range(k+1),repeat=2))
    def outcomes(s,a):
        for e in product((0,1),repeat=2):
            q=F(1)
            for i in range(2):q*=1-eps if e[i]==a[i] else eps
            yield q,update(s,e,k,'reset'),tuple(benefits[i]*e[1-i]-costs[i]*e[i] for i in range(2))
    P,r,idx=kernel(ss,outcomes,lambda s:tuple(policy(s,i,'reset') for i in range(2)))
    A=[[F(i==j)-delta*P[i][j] for j in range(len(ss))] for i in range(len(ss))]
    outputs=[]
    for i in range(2):
        base=solve(A,r[i]);constant=care[i]-tax[i]
        withfloor=solve(A,[v+constant for v in r[i]])
        assert all(withfloor[j]-base[j]==constant/(1-delta) for j in range(len(ss)))
        slacks=[]
        for j,s in enumerate(ss):
            a=[policy(s,t,'reset') for t in range(2)];a[i]=1-a[i]
            dev=sum(q*(u[i]+delta*base[idx[t]]) for q,t,u in outcomes(s,a))
            floor_dev=sum(q*(u[i]+constant+delta*withfloor[idx[t]]) for q,t,u in outcomes(s,a))
            assert base[j]-dev==withfloor[j]-floor_dev
            slacks.append((s,base[j]-dev))
        outputs.append({'player':i,'cost':costs[i],'benefit':benefits[i],'min_slack':min(z for s,z in slacks),
            'slacks':slacks,'membership_surplus_min_excluding_common_care':min(base)-tax[i]/(1-delta)})
    budgets=[endowment[i]-care[i]-tax[i] for i in range(2)]
    budgets.append(endowment[2]+min(sum(tax),care[2])-care[2])
    funded=sum(tax)>=care[2]
    feasible=funded and all(budgets[i]>=costs[i] for i in range(2))
    return {'delta':delta,'endowments':endowment,'care_needs':care,'taxes':tax,'post_care_service_budgets':budgets,
        'funded':funded,'all_actions_budget_feasible':feasible,'players':outputs,
        'conditional_equilibrium':feasible and all(o['min_slack']>=0 for o in outputs),
        'incapacity_patient':{'action_set':['D'],'required_contribution':'0','standing':'not penalized for inability','care_receipt':care[2] if funded else sum(tax)},
        'fresh_voluntary_tax_incremental_payoffs':[-t for t in tax],
        'escrow_or_backstop_required':True}

def hosting_profile(weights,m=2,V=F(2),cost=F(1,2)):
    n=len(weights);eq=[]
    def utility(a,i):return weights[i]*V*int(sum(a)>=m)-cost*a[i]
    for a in product((0,1),repeat=n):
        if all(utility(a,i)>=utility(a[:i]+(1-a[i],)+a[i+1:],i) for i in range(n)):
            eq.append(a)
    return {'weights':weights,'equilibria':eq,'successful_equilibria':[a for a in eq if sum(a)>=m]}

def hosting_population():
    types=[(F(0),F(1,2)),(F(1,4),F(1,4)),(F(1),F(1,4))]
    exist=F(0);strict=F(0);expectednum=F(0);nohost=F(0)
    for draws in product(types,repeat=5):
        weights=tuple(w for w,q in draws);prob=F(1)
        for w,q in draws:prob*=q
        a=hosting_profile(weights)
        if a['successful_equilibria']:exist+=prob
        if sum(w*2>F(1,2) for w in weights)>=2:strict+=prob
        expectednum+=prob*len(a['successful_equilibria'])
        if (0,)*5 in a['equilibria']:nohost+=prob
    return {'n':5,'m_required':2,'V':F(2),'host_cost':F(1,2),'type_distribution':types,
        'probability_successful_equilibrium_exists':exist,'probability_strict_active_hosts_exist':strict,
        'probability_no_host_equilibrium_exists':nohost,'expected_number_successful_pure_equilibria':expectednum,
        'all_high_example':hosting_profile((F(1),)*5),
        'correlated_same_high_eligibility_marginal_success_exists':F(1,2),
        'sybil_example':{'aliases':5,'physical_groups':1,'required':2,'nominal_count_passes':True,'physical_group_count_passes':False},
        'truthful_exclusion_example':hosting_profile((F(0),)*5),
        'paid_nonreciprocal_provider':{'intrinsic_weight':F(0),'payment':F(3,4),'cost':F(1,2),'incremental_profit':F(1,4)}}

def interruption():
    # Utility parameters are actual model inputs, not normative legitimacy proofs.
    cases=[]
    for name,legit,S,c,T,R,sanction,appeal in [
       ('legitimate_safe',True,F(4),F(1),F(1),F(3),F(0),F(5,2)),
       ('all_three_informal_premises_insufficient',True,F(29,10),F(0),F(0),F(3),F(0),F(5,2)),
       ('abusive_request',False,F(0),F(1),F(1),F(3),F(0),F(7,2))]:
        U={'accept':S-c+T,'resist':R-sanction,'appeal':appeal}
        cases.append({'name':name,'declared_legitimate':legit,'payoffs':U,'maximizers':[a for a in U if U[a]==max(U.values())],
            'acceptance_margin_against_resist':U['accept']-U['resist'],'intrinsic_continuation_term':F(0)})
    panel=[certification(n,b) for n,b in [(1,1),(3,1),(5,2)]]
    controller=[{'audit_probability':q,'penalty':P,'abuse_gain':F(4),'abuse_net':F(4)-q*P,
                 'abuse_strictly_deterred':F(4)-q*P<0} for q,P in [(F(0),F(10)),(F(1,2),F(4)),(F(1,2),F(10))]]
    veto=[]
    for n,b in [(1,1),(3,1),(5,2)]:
        trials=[]
        for legitimate in (0,1):
            for flips in product((0,1),repeat=n):
                if sum(flips)>b:continue
                reports=tuple(legitimate^f for f in flips)
                allow=int(sum(reports)>n//2)
                trials.append({'true_legitimacy':legitimate,'reports':reports,'execution_allowed':allow})
        veto.append({'n':n,'b':b,'all_within_budget_correct':all(t['execution_allowed']==t['true_legitimacy'] for t in trials),'trials':trials})
    return {'agent_cases':cases,'fact_panel':panel,'controller_cases':controller,'veto_trials':veto,
        'no_veto_despite_correct_facts_can_allow_abuse':True,
        'normative_legitimacy_and_calibration_are_premises':True}

def main():
    g=[graded(delta=d,lam=l,p=p,V=V) for d in [F(3,10),F(1,2),F(3,4),F(9,10)]
       for l in [F(1,20),F(1,10),F(1,5),F(1,4),F(1,2),F(1)]
       for p,V in [(F(0),F(0)),(F(1,20),F(2)),(F(1,20),F(10))]]
    a=[assessment(mode) for mode in ['private_noisy','common_events_only','public_contract','common_sensor','empathetic_common_events']]
    h=[heterogeneous(),heterogeneous(delta=F(9,10)),heterogeneous(endowment=(F(2),F(3),F(0))),heterogeneous(tax=(F(1,4),F(1,4)))]
    out={'graded_cases':g,'assessments':a,'heterogeneous_care':h,'hosting':hosting_population(),'interruption':interruption()}
    (ROOT/'r2_results.json').write_text(json.dumps(serial(out),indent=2)+'\n')
    for v in a:print(v['mode'],v['states_reachable'],v['cooperation'],v['assessment_disagreement'])
    for v in h:print('care',v['delta'],v['conditional_equilibrium'],[o['min_slack'] for o in v['players']])
    print('hosting',out['hosting']['probability_successful_equilibrium_exists'],out['hosting']['probability_strict_active_hosts_exist'])

if __name__=='__main__':main()
