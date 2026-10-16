"""Offline finite covenant game. Exact Fraction arithmetic, including all deviations.

C=1, D=0. State is two repair counters (0=good). Generous-repair policy:
carry if own counter is positive OR partner is good; otherwise refuse optional
service. Executed C is clean; D is authorized only in state (good, marked).
An unauthorized executed D resets own counter to k; executed C reduces it.
Independent implementation flips have probability epsilon. Moral intention is
not observed. Standing concerns service risk, not blame or patient rights.

Opportunity hazard p terminates the relationship after a round. At the next
discounted date an atomic mutual-host contract can execute if both are good.
Both offering H yields V-h each; any N cancels without cost. Select HH only
when both good and V>=h, NN otherwise. Plain uncontracted altruistic hosting
is a separate negative control (H strictly dominated when h>0).
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def solve(A, y):
    a = [list(row) + [v] for row, v in zip(A, y)]
    n = len(a)
    for j in range(n):
        q = next(i for i in range(j,n) if a[i][j])
        a[j], a[q] = a[q], a[j]
        z = a[j][j]
        a[j] = [x/z for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                z = a[i][j]
                a[i] = [x-z*t for x,t in zip(a[i],a[j])]
    return [r[-1] for r in a]

def policy(s, i, mode):
    if mode == 'none': return 1
    if mode == 'grim': return int(s == (0,0))
    return int(s[i] > 0 or s[1-i] == 0)

def update(s, e, k, mode):
    if mode == 'none': return (0,0)
    if mode == 'grim':
        return tuple(int(s[i]>0 or e[i]==0) for i in range(2))
    out = []
    for i in range(2):
        if mode == 'permanent' and s[i]>0:
            out.append(1)
        elif e[i] == 0 and (s[i] > 0 or s[1-i] == 0):
            out.append(k)
        else:
            out.append(max(0,s[i]-1))
    return tuple(out)

def carrier(k=2, eps=F(1,20), b=F(3), c=F(1), mode='reset'):
    if mode in ('permanent','grim'): k=1
    states = list(product(range(k+1),repeat=2)) if mode != 'none' else [(0,0)]
    def outcome(s, a):
        for e in product((0,1),repeat=2):
            pr = F(1)
            for i in range(2): pr *= 1-eps if e[i]==a[i] else eps
            yield pr, update(s,e,k,mode), tuple(b*e[1-i]-c*e[i] for i in range(2))
    P = [[F(0) for _ in states] for _ in states]
    r = [[F(0) for _ in states] for _ in range(2)]
    for j,s in enumerate(states):
        a = tuple(policy(s,i,mode) for i in range(2))
        for pr,t,u in outcome(s,a):
            P[j][states.index(t)] += pr
            for i in range(2): r[i][j] += pr*u[i]
    return states, P, r, outcome

def evaluate(delta, p=F(0), V=F(0), h=F(1,2), k=2, mode='reset', eps=F(1,20)):
    ss,P,r,outcome=carrier(k=k,mode=mode,eps=eps)
    n=len(ss); beta=delta*(1-p)
    bonus=[max(F(0),V-h) if s==(0,0) else F(0) for s in ss]
    A=[[F(i==j)-beta*P[i][j] for j in range(n)] for i in range(n)]
    w=[solve(A,[r[i][j]+delta*p*sum(P[j][l]*bonus[l] for l in range(n)) for j in range(n)]) for i in range(2)]
    slacks=[]
    for j,s in enumerate(ss):
        for i in range(2):
            a=list(policy(s,t,mode) for t in range(2)); a[i]=1-a[i]
            dev=F(0)
            for pr,t,u in outcome(s,a):
                l=ss.index(t)
                dev+=pr*(u[i]+delta*(p*bonus[l]+(1-p)*w[i][l]))
            slacks.append((s,i,w[i][j]-dev))
    return {'delta':delta,'p':p,'V':V,'h':h,'k':max(s[0] for s in ss),'mode':mode,
            'equilibrium':all(z>=0 for _,_,z in slacks),
            'min_slack':min(z for _,_,z in slacks), 'slacks':slacks,
            'values':w,'states':ss}

def certification(n,b,blind=False):
    codes=[(0,)*n,(0,)*n if blind else (1,)*n]
    def ball(code):
        return {tuple(1-x if i in flip else x for i,x in enumerate(code))
                for j in range(min(b,n)+1) for flip in combinations(range(n),j)}
    overlap=ball(codes[0]) & ball(codes[1])
    return {'n':n,'b':b,'distance':sum(x!=y for x,y in zip(*codes)),
            'decodable':not overlap,'collision':min(overlap) if overlap else None}

def siphons():
    # Two disjoint realized two-capability cycles. Realizer is the premise.
    C=frozenset('abcd'); rules=[({'a'},'b'),({'b'},'a'),({'c'},'d'),({'d'},'c')]
    subs=[frozenset(v) for j in range(5) for v in combinations(sorted(C),j)]
    def reach(seed):
        r=set(seed)
        while True:
            t=r|{o for req,o in rules if req <= r}
            if t==r:return frozenset(r)
            r=t
    siph=[x for x in subs if all(o not in x or bool(req & x) for req,o in rules)]
    feasible=[B for B in subs if reach(B)==C]
    minimal=[B for B in feasible if not any(A<B for A in feasible)]
    assert all((reach(B)==C)==all(bool(X&B) for X in siph if X) for B in subs)
    return {'rules':[(sorted(a),b) for a,b in rules],'siphons':[sorted(x) for x in siph],
            'minimal_seeds':[sorted(x) for x in minimal], 'local_seed_reach':sorted(reach({'a'}))}

def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x

def main():
    cases=[]
    for k in (1,2):
        for p,V in [(F(0),F(0)),(F(1,20),F(0)),(F(1,20),F(2)),(F(1,20),F(10)),(F(1,5),F(0)),(F(1,5),F(5,2)),(F(1,5),F(10))]:
            for d in [F(1,2),F(3,4),F(9,10),F(19,20),F(99,100),F(999,1000)]:
                cases.append(evaluate(d,p,V,k=k))
    for mode in ('none','permanent','grim'):
        for d in [F(1,2),F(3,4),F(9,10),F(99,100)]:cases.append(evaluate(d,mode=mode))
    results={'parameters':{'b':'3','c':'1','epsilon':'1/20','hosting_cost':'1/2'},
             'cases':cases,'certification':[certification(n,b) for n in range(1,8) for b in range(3)],
             'blind_panel':certification(7,0,True),'siphon_lab':siphons()}
    (ROOT/'results.json').write_text(json.dumps(serial(results),indent=2)+'\n')
    for x in cases:
        print(x['mode'],x['k'],x['p'],x['V'],x['delta'],x['equilibrium'],float(x['min_slack']))

if __name__=='__main__':main()
