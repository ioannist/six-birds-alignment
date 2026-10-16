"""Exact symbolic Bellman/deviation certificates; real-root isolation, no simulations."""
import json
import sympy as S
from model import carrier, policy, F, ROOT, serial, evaluate

x,z,d=S.symbols('x z delta',real=True)
def rat(v):return S.Rational(v.numerator,v.denominator)

def formulas(k,mode='reset'):
    ss,P,r,outcome=carrier(k=k,mode=mode)
    P=S.Matrix([[rat(a) for a in row] for row in P])
    w=(S.eye(len(ss))-x*P).inv()*(S.Matrix(list(map(rat,r[0])))+z*P*S.Matrix([int(s==(0,0)) for s in ss]))
    answer=[]
    for j,s in enumerate(ss):
        a=[policy(s,i,mode) for i in range(2)];a[0]=1-a[0]
        dev=0
        for pr,t,u in outcome(s,a):
            dev+=rat(pr)*(rat(u[0])+z*int(t==(0,0))+x*w[ss.index(t)])
        answer.append((s,S.factor(w[j]-dev)))
    return answer

def bernstein(poly,lo=0,hi=1):
    # Exact certificate of positivity on [lo,hi]; sufficient, not necessary.
    if poly == 0: return [S.Rational(0)]
    t=S.symbols('t');p=S.Poly(S.expand(poly.subs(x,lo+(hi-lo)*t)),t)
    n=p.degree();a=[p.nth(i) for i in range(n+1)]
    return [S.factor(sum(a[j]*S.binomial(i,j)/S.binomial(n,j) for j in range(i+1))) for i in range(n+1)]

def main():
    result={'symbolic_convention':'x=delta*(1-p), z=delta*p*max(0,V-h)', 'cases':[],'bonus_monotonicity':[]}
    text=[]
    for k in (1,2):
        fs=formulas(k)
        text.append('k='+str(k))
        for state,f in fs:
            text.append(str(state)+' : '+str(f))
            derivative=S.factor(S.diff(f,z));num,den=S.fraction(derivative)
            bc=bernstein(num);dc=bernstein(den)
            # A polynomial may be represented with negative common sign.
            ok=all(v>=0 for v in bc) and all(v>0 for v in dc)
            if not ok:
                ok=all(v<=0 for v in bc) and all(v<0 for v in dc)
            result['bonus_monotonicity'].append({'k':k,'state':state,'derivative':str(derivative),
                'numerator_bernstein':list(map(str,bc)),'denominator_bernstein':list(map(str,dc)),
                'certified_nonnegative':ok})
        for p,V in [(F(0),F(0)),(F(1,20),F(0)),(F(1,20),F(2)),(F(1,20),F(10)),(F(1,5),F(0)),(F(1,5),F(5,2)),(F(1,5),F(10))]:
            R=max(F(0),V-F(1,2)); rows=[];roots=[]
            for state,f in fs:
                f=S.factor(f.subs({x:d*(1-rat(p)),z:d*rat(p*R)}));num,den=S.fraction(f)
                intervals=S.Poly(num,d).intervals(eps=S.Rational(1,10**12)) if num!=0 else []
                relevant=[(ab,m) for ab,m in intervals if 0<ab[1] and ab[0]<1]
                for (a,b),m in relevant:roots.append((a,b,state))
                rows.append({'state':state,'slack':str(f),'root_intervals':[(str(a),str(b),m) for (a,b),m in relevant]})
            roots.sort(key=lambda q:q[0]);hi=max([b for a,b,_ in roots]+[S.Rational(0)])
            # Above every zero the signs are constant. One exact sample certifies
            # the complete upper interval; interval denominators are also
            # root-checked below, avoiding pole-related sign mistakes.
            sample=(hi+1)/2
            assert all(S.factor(f.subs({x:sample*(1-rat(p)),z:sample*rat(p*R)}))>0 for _,f in fs)
            for _,f in fs:
                den=S.fraction(S.factor(f.subs({x:d*(1-rat(p)),z:d*rat(p*R)})))[1]
                assert not any(a<1 and b>0 for (a,b),_ in S.Poly(den,d).intervals())
            last=max(roots,key=lambda q:q[1]) if roots else (S.Rational(0),S.Rational(0),None)
            binding_row=next(row for row in rows if row['state']==last[2])
            assert len(binding_row['root_intervals'])==1
            # The binding inequality is negative at delta=0 and has only
            # one interior zero. This also excludes isolated lower equilibria
            # hidden inside root-isolation intervals of other inequalities.
            binding_f=next(f for state,f in fs if state==last[2])
            assert binding_f.subs({x:0,z:0})<0
            below=max(S.Rational(0),last[0]-S.Rational(1,1000000))
            # All root gaps are sampled exactly: establish the entire feasible
            # set, rather than assuming only one incentive threshold exists.
            cut=[(S.Rational(0),S.Rational(0))]+[(a,b) for a,b,_ in roots]+[(S.Rational(1),S.Rational(1))]
            feasible_cells=[]
            for left,right in zip(cut,cut[1:]):
                if left[1]>=right[0]:continue
                mid=(left[1]+right[0])/2
                feasible=all(f.subs({x:mid*(1-rat(p)),z:mid*rat(p*R)})>=0 for _,f in fs)
                feasible_cells.append({'from':str(left[1]),'to':str(right[0]),'feasible':bool(feasible)})
            result['cases'].append({'k':k,'p':str(p),'V':str(V),'threshold_interval':[str(last[0]),str(last[1])],
               'approximate_threshold':float((last[0]+last[1])/2),'binding_state':last[2],
               'above_threshold_exact_sample':str(sample),'below_sample_fails':not evaluate(F(below),p,V,k=k)['equilibrium'],
               'binding_has_unique_interior_zero':True,
               'slacks':rows,'root_gap_signs':feasible_cells})
    (ROOT/'symbolic_formulas.txt').write_text('\n'.join(text)+'\n')
    (ROOT/'symbolic_results.json').write_text(json.dumps(serial(result),indent=2)+'\n')
    for c in result['cases']:print(c['k'],c['p'],c['V'],c['approximate_threshold'],c['binding_state'])
    print('Bonus derivative certificates:',sum(r['certified_nonnegative'] for r in result['bonus_monotonicity']),len(result['bonus_monotonicity']))

if __name__=='__main__':main()
