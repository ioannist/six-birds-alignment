import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/- [B: lab] D8. Three-person public simple-standing donation algebra.
   Transition/payoff instantiation and hidden-information scope are separate. -/
namespace Alignment.Assessment
variable {R : Type*} [Field R] [LinearOrder R] [IsStrictOrderedRing R]

theorem affine_bellman (a x y r0 rg rk d η g k : R)
    (ha : a = r0+d*(a+x/3+2*y/3))
    (hx : x = rg+d*(2*x/3-η*y/3))
    (hy : y = rk+d*(-η*x/6+(2/3-η/6)*y)) :
    a+x*g+y*k = r0+rg*g+rk*k+
      d*(a+x*(2*g/3+1/3-η*k/6)+y*(2/3+(2/3-η/6)*k-η*g/3)) := by
  have hxg := congrArg (fun v : R => v*g) hx
  have hyk := congrArg (fun v : R => v*k) hy
  nlinarith [ha, hxg, hyk]

def determinant (d η : R) : R := (1-d*(2-η)/3)*(1-d*(4+η)/6)

theorem determinant_pos (d η : R) (hd : 0 ≤ d) (hd1 : d < 1)
    (hη : 0 ≤ η) (hη1 : η ≤ 1) : 0 < determinant d η := by
  have hprod : 0 ≤ d*η := mul_nonneg hd hη
  have hupper : 0 ≤ d*(1-η) := mul_nonneg hd (by linarith)
  have h1 : 0 < 1-d*(2-η)/3 := by nlinarith
  have h2 : 0 < 1-d*(4+η)/6 := by nlinarith
  exact mul_pos h1 h2

def publicDenominator (d : R) : R := (13*d-20)*(27*d-40)
def publicPolynomial (d : R) : R := -823*d^2+1780*d-800
def publicSlope (d : R) : R := (720-472*d)/publicDenominator d

theorem public_denominator_pos (d : R) (hd1 : d ≤ 1) :
    0 < publicDenominator d := by
  have h1 : 13*d-20 < 0 := by linarith
  have h2 : 27*d-40 < 0 := by linarith
  exact mul_pos_of_neg_of_neg h1 h2

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem public_gap_identity (d : R) (h : publicDenominator d ≠ 0) :
    d*publicSlope d-1 = publicPolynomial d/publicDenominator d := by
  have hm : publicSlope d*publicDenominator d = 720-472*d := div_mul_cancel₀ _ h
  apply (eq_div_iff h).mpr
  calc
    (d*publicSlope d-1)*publicDenominator d =
        d*(publicSlope d*publicDenominator d)-publicDenominator d := by ring
    _ = d*(720-472*d)-publicDenominator d := by rw [hm]
    _ = publicPolynomial d := by unfold publicPolynomial publicDenominator; ring

theorem public_gap_iff (d : R) (hd1 : d ≤ 1) :
    0 ≤ d*publicSlope d-1 ↔ 0 ≤ publicPolynomial d := by
  have hp := public_denominator_pos d hd1
  rw [public_gap_identity d (ne_of_gt hp)]
  constructor
  · intro h
    simpa using (le_div_iff₀ hp).mp h
  · intro h
    apply (le_div_iff₀ hp).mpr
    simpa using h

theorem public_polynomial_strict (x y : R) (hxy : x < y) (hy : y ≤ 1) :
    publicPolynomial x < publicPolynomial y := by
  have hf : 0 < 1780-823*(x+y) := by linarith
  have hm := mul_pos (sub_pos.mpr hxy) hf
  have he : publicPolynomial y-publicPolynomial x = (y-x)*(1780-823*(x+y)) := by
    unfold publicPolynomial
    ring
  linarith

theorem public_root_endpoint_signs :
    publicPolynomial (5019074/7877751 : ℚ) < 0 ∧
    0 < publicPolynomial (1047883/1644718 : ℚ) := by
  norm_num [publicPolynomial]

end Alignment.Assessment
