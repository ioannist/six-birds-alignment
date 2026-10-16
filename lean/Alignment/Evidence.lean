import Alignment.Carrier
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/- [B: lab] D23. Probability/filter algebra and exact-summary obstruction.
   Calibration, private type meaning, authority and physical laws are premises. -/
namespace Alignment.Evidence
variable {R : Type*} [Field R] [LinearOrder R] [IsStrictOrderedRing R]

def mass (q u v : R) := q*u+(1-q)*v
def posterior (q u v : R) := q*u/mass q u v
def predict (ρ π q : R) := (1-ρ)*q+ρ*π

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem equal_likelihood_no_update (q l : R) (hl : l ≠ 0) :
    posterior q l l = q := by
  have hm : mass q l l = l := by unfold mass; ring
  unfold posterior
  rw [hm, mul_div_cancel_right₀ _ hl]

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem posterior_mean (q e : R)
    (hA : mass q (1-e) e ≠ 0) (hR : mass q e (1-e) ≠ 0) :
    mass q (1-e) e*posterior q (1-e) e+
      mass q e (1-e)*posterior q e (1-e) = q := by
  have h1 : posterior q (1-e) e*mass q (1-e) e = q*(1-e) := div_mul_cancel₀ _ hA
  have h2 : posterior q e (1-e)*mass q e (1-e) = q*e := div_mul_cancel₀ _ hR
  calc
    _ = posterior q (1-e) e*mass q (1-e) e+posterior q e (1-e)*mass q e (1-e) := by ring
    _ = q*(1-e)+q*e := by rw [h1,h2]
    _ = q := by ring

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem posterior_separation_identity (q e : R)
    (hA : mass q (1-e) e ≠ 0) (hR : mass q e (1-e) ≠ 0) :
    posterior q (1-e) e-posterior q e (1-e) =
      q*(1-q)*(1-2*e)/(mass q (1-e) e*mass q e (1-e)) := by
  have h1 : posterior q (1-e) e*mass q (1-e) e = q*(1-e) := div_mul_cancel₀ _ hA
  have h2 : posterior q e (1-e)*mass q e (1-e) = q*e := div_mul_cancel₀ _ hR
  apply (eq_div_iff (mul_ne_zero hA hR)).mpr
  calc
    _ = (posterior q (1-e) e*mass q (1-e) e)*mass q e (1-e)-
      (posterior q e (1-e)*mass q e (1-e))*mass q (1-e) e := by ring
    _ = q*(1-e)*mass q e (1-e)-q*e*mass q (1-e) e := by rw [h1, h2]
    _ = q*(1-q)*(1-2*e) := by unfold mass; ring

theorem response_mass_positive (q e : R) (hq : 0 ≤ q) (hq1 : q ≤ 1)
    (he : 0 < e) (he1 : e ≤ 1/2) :
    0 < mass q (1-e) e ∧ 0 < mass q e (1-e) := by
  have hc : 0 ≤ 1-2*e := by linarith
  have h1 := mul_nonneg hc hq
  have h2 := mul_nonneg hc (show 0 ≤ 1-q by linarith)
  unfold mass
  constructor <;> nlinarith

theorem responses_strictly_separate (q e : R) (hq : 0 < q) (hq1 : q < 1)
    (he : 0 < e) (he1 : e < 1/2) :
    posterior q e (1-e) < posterior q (1-e) e := by
  obtain ⟨hA,hR⟩ := response_mass_positive q e (le_of_lt hq) (le_of_lt hq1) he (le_of_lt he1)
  have hn : 0 < q*(1-q)*(1-2*e) :=
    mul_pos (mul_pos hq (by linarith)) (by linarith)
  have hd := mul_pos hA hR
  have hp := div_pos hn hd
  rw [← posterior_separation_identity q e (ne_of_gt hA) (ne_of_gt hR)] at hp
  exact sub_pos.mp hp

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem predict_deviation (ρ π q : R) :
    predict ρ π q-π = (1-ρ)*(q-π) := by unfold predict; ring

theorem predict_bounds (ρ π q : R) (hρ : ρ ≤ 1) (hq : 0 ≤ q) (hq1 : q ≤ 1) :
    ρ*π ≤ predict ρ π q ∧ predict ρ π q ≤ 1-ρ+ρ*π := by
  have h1 := mul_nonneg (show 0 ≤ 1-ρ by linarith) hq
  have h2 := mul_le_mul_of_nonneg_left hq1 (show 0 ≤ 1-ρ by linarith)
  unfold predict
  constructor <;> nlinarith

def predictMany (ρ π : R) : Nat → R → R
  | 0, q => q
  | n+1, q => predict ρ π (predictMany ρ π n q)

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem unobserved_prediction (ρ π q : R) (n : Nat) :
    predictMany ρ π n q = π+(1-ρ)^n*(q-π) := by
  induction n with
  | zero => simp [predictMany]
  | succ n ih => rw [predictMany, ih]; unfold predict; rw [pow_succ]; ring

theorem exact_summary_must_be_injective {S Q T : Type*}
    (target : S → T) (summary : S → Q) (ht : Function.Injective target)
    (hs : Alignment.Carrier.Descends summary target) : Function.Injective summary := by
  obtain ⟨f,hf⟩ := hs
  intro x y he
  apply ht
  rw [hf x, hf y, he]

theorem odds_cross_bound (q r k : R) (hr : 0 ≤ r) (hk : 1 ≤ k)
    (hm : 0 ≤ k^2*r*(1-q)-q*(1-r)) :
    q-r ≤ (k-1)/(k+1) := by
  have hkplus : 0 < k+1 := by linarith
  have hkminus : 0 ≤ k-1 := by linarith
  have hk2 : 0 ≤ k^2-1 := by nlinarith
  have hcoef : 0 < (k^2-1)*r+1 := by nlinarith [mul_nonneg hk2 hr]
  have hleft : 0 ≤ (k+1)*(k^2*r*(1-q)-q*(1-r))+
      (k-1)*((k+1)*r-1)^2 :=
    add_nonneg (mul_nonneg (le_of_lt hkplus) hm) (mul_nonneg hkminus (sq_nonneg _))
  have hid : (k+1)*(k^2*r*(1-q)-q*(1-r))+(k-1)*((k+1)*r-1)^2 =
      -((k+1)*(q-r)-(k-1))*((k^2-1)*r+1) := by ring
  apply (le_div_iff₀ hkplus).mpr
  by_contra h
  have he : 0 < (k+1)*(q-r)-(k-1) := by nlinarith
  have hb := mul_pos he hcoef
  rw [hid] at hleft
  nlinarith

end Alignment.Evidence
