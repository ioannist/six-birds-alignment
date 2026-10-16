import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/- [B: lab] D18(f). Finite observed MDP obtained by fixing opponents.
   History-dependent pure deviations; mixed deviations are convex combinations
   at each information set (written bridge in math/D18.md). -/
namespace Alignment.Discounted
open scoped BigOperators
open Filter
variable {S A : Type*} [Fintype S]

noncomputable def value (r : S → A → ℝ) (P : S → A → S → ℝ) (β : ℝ)
    (σ : List (S × A) → S → A) (hist : List (S × A)) (s : S) : Nat → ℝ
  | 0 => 0
  | n+1 => r s (σ hist s) + β * ∑ t, P s (σ hist s) t *
      value r P β σ ((s, σ hist s)::hist) t n

theorem truncation_bound (r : S → A → ℝ) (P : S → A → S → ℝ)
    (β C : ℝ) (W : S → ℝ) (hβ : 0 ≤ β)
    (hP : ∀ s a t, 0 ≤ P s a t) (hrow : ∀ s a, ∑ t, P s a t = 1)
    (hW : ∀ s, -C ≤ W s)
    (hcert : ∀ s a, r s a + β*∑ t, P s a t*W t ≤ W s)
    (σ : List (S × A) → S → A) (n : Nat) :
    ∀ hist s, value r P β σ hist s n ≤ W s + β^n*C := by
  induction n with
  | zero => intro hist s; simp only [value, pow_zero, one_mul]; linarith [hW s]
  | succ n ih =>
    intro hist s
    have hs : (∑ t, P s (σ hist s) t *
        value r P β σ ((s, σ hist s)::hist) t n) ≤
        ∑ t, P s (σ hist s) t * (W t + β^n*C) := by
      exact Finset.sum_le_sum fun t ht =>
        mul_le_mul_of_nonneg_left (ih _ t) (hP _ _ t)
    calc
      value r P β σ hist s (n+1) ≤
          r s (σ hist s) + β*∑ t, P s (σ hist s) t*(W t+β^n*C) := by
        simpa only [value, add_comm] using
          add_le_add_left (mul_le_mul_of_nonneg_left hs hβ) (r s (σ hist s))
      _ = (r s (σ hist s)+β*∑ t, P s (σ hist s) t*W t) + β^(n+1)*C := by
        simp only [mul_add, Finset.sum_add_distrib, ← Finset.sum_mul, hrow, one_mul]
        ring
      _ ≤ W s + β^(n+1)*C := by
        simpa only [add_comm] using
          add_le_add_right (hcert s (σ hist s)) (β^(n+1)*C)

theorem deviation_limit_le (r : S → A → ℝ) (P : S → A → S → ℝ)
    (β C : ℝ) (W : S → ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1)
    (hP : ∀ s a t, 0 ≤ P s a t) (hrow : ∀ s a, ∑ t, P s a t = 1)
    (hW : ∀ s, -C ≤ W s)
    (hcert : ∀ s a, r s a + β*∑ t, P s a t*W t ≤ W s)
    (σ : List (S × A) → S → A) (hist : List (S × A)) (s : S)
    (U : ℝ) (hU : Tendsto (fun n => value r P β σ hist s n) atTop (nhds U)) :
    U ≤ W s := by
  have ht : Tendsto (fun n : Nat => W s + β^n*C) atTop (nhds (W s)) := by
    simpa using tendsto_const_nhds.add
      ((tendsto_pow_atTop_nhds_zero_of_lt_one hβ hβ1).mul_const C)
  exact le_of_tendsto_of_tendsto' hU ht
    (fun n => truncation_bound r P β C W hβ hP hrow hW hcert σ n hist s)

end Alignment.Discounted
