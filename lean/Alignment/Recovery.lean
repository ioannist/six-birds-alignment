import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/- [B: lab] Catalogue D7 / D18(a) / E3. Ordered-field algebra.
   Stochastic-game semantics and bounded-payoff hypotheses are in math/D7.md. -/
namespace Alignment.Recovery
variable {R : Type*} [Field R] [LinearOrder R] [IsStrictOrderedRing R]

def denominator (β q γ : R) := 1 - β*q*(1-γ)
def slope (B z β q γ : R) := (B + z*q*(1-γ)) / denominator β q γ
def gain (B z β q γ : R) := (β*B+z) / denominator β q γ
def intercept (B z β q γ c : R) := q*(-c + gain B z β q γ*γ)/(1-β)

omit [LinearOrder R] [IsStrictOrderedRing R] in
theorem gain_identity (B z β q γ : R) (hd : denominator β q γ ≠ 0) :
    gain B z β q γ = β*slope B z β q γ + z := by
  unfold gain slope denominator at *
  field_simp [hd]
  ring

theorem bellman_affine (B z β q γ c s : R)
    (hd : denominator β q γ ≠ 0) (hb : 1-β ≠ 0) :
    intercept B z β q γ c + slope B z β q γ*s =
    B*s-c*q + z*(q*(γ+(1-γ)*s)) +
    β*(intercept B z β q γ c + slope B z β q γ*(q*(γ+(1-γ)*s))) := by
  have hD : slope B z β q γ * denominator β q γ = B+z*q*(1-γ) := by
    exact div_mul_cancel₀ _ hd
  have hA : intercept B z β q γ c * (1-β) = q*(-c+gain B z β q γ*γ) := by
    exact div_mul_cancel₀ _ hb
  rw [gain_identity B z β q γ hd] at hA
  have hDs := congrArg (fun v : R => v*s) hD
  unfold denominator at hDs
  nlinarith [hA, hDs]

theorem denominator_pos (t γ : R) (ht : 0 ≤ t) (ht1 : t < 1)
    (hg : 0 ≤ γ) (_hg1 : γ ≤ 1) : 0 < 1-t*(1-γ) := by
  have h := mul_le_mul_of_nonneg_left (show 1-γ ≤ 1 by linarith) ht
  linarith

theorem recovery_iff (H c t γ : R) (hd : 0 < 1-t*(1-γ)) :
    0 ≤ -c + (H/(1-t*(1-γ)))*γ ↔ γ*(H-c*t) ≥ c*(1-t) := by
  have he : (H/(1-t*(1-γ)))*γ = H*γ/(1-t*(1-γ)) := by ring
  rw [he]
  constructor
  · intro h
    have h' : c ≤ H*γ/(1-t*(1-γ)) := by linarith
    have hm := (le_div_iff₀ hd).mp h'
    nlinarith
  · intro h
    have hm : c*(1-t*(1-γ)) ≤ H*γ := by nlinarith
    have h' := (le_div_iff₀ hd).mpr hm
    linarith

theorem recovery_feasible (H c t : R) (hc : 0 < c) (ht1 : t < 1) :
    (∃ γ : R, 0 ≤ γ ∧ γ ≤ 1 ∧ γ*(H-c*t) ≥ c*(1-t)) ↔ c ≤ H := by
  constructor
  · rintro ⟨γ, hg, hg1, h⟩
    have hr : 0 < c*(1-t) := mul_pos hc (by linarith)
    have hd : 0 < H-c*t := by
      by_contra hn
      have hp := mul_nonpos_of_nonneg_of_nonpos hg (le_of_not_gt hn)
      linarith
    have hp := mul_le_mul_of_nonneg_right hg1 (le_of_lt hd)
    nlinarith
  · intro h
    refine ⟨1, by positivity, le_rfl, ?_⟩
    nlinarith

theorem recovery_window (H c t γ : R) (hc : 0 < c) (ht1 : t < 1)
    (hH : c ≤ H) :
    γ*(H-c*t) ≥ c*(1-t) ↔ c*(1-t)/(H-c*t) ≤ γ := by
  have hd : 0 < H-c*t := by nlinarith
  rw [div_le_iff₀ hd]

theorem all_grades_iff (c G γ : R) (hG : 0 ≤ G) (hg1 : γ ≤ 1) :
    (∀ s : R, 0 ≤ s → s ≤ 1 → 0 ≤ -c+G*(γ+(1-γ)*s)) ↔
    0 ≤ -c+G*γ := by
  constructor
  · intro h
    simpa using h 0 le_rfl (by positivity)
  · intro h s hs hs1
    have hp : 0 ≤ G*((1-γ)*s) := mul_nonneg hG (mul_nonneg (by linarith) hs)
    nlinarith

theorem coverage_iff (q ε γ η : R) (hd : 0 < ε+q*γ)
    (hq : 0 < q) (he : η < 1) :
    η ≤ q*γ/(ε+q*γ) ↔ η*ε/(q*(1-η)) ≤ γ := by
  have hd2 : 0 < q*(1-η) := mul_pos hq (by linarith)
  rw [le_div_iff₀ hd, div_le_iff₀ hd2]
  constructor <;> intro h <;> nlinarith

end Alignment.Recovery
