import Alignment.Discounted
import Mathlib.Tactic.Linarith

/- [B: lab] D3 / D18(e) / E5. Finite-horizon backward induction on a
   noisy donation MDP against the all-D opponent. All transitions are allowed;
   rewards are state-independent and D exceeds C by a fixed positive gap. -/
namespace Alignment.Horizon
open scoped BigOperators
variable {S : Type*} [Fintype S]

noncomputable def payoff (d β : ℝ) : Nat → ℝ
  | 0 => 0
  | n+1 => d+β*payoff d β n

noncomputable def optimal (d g β : ℝ) (P : S → Bool → S → ℝ) : Nat → S → ℝ
  | 0, _ => 0
  | n+1, s => max (d + β*∑ t, P s false t*optimal d g β P n t)
      (d-g + β*∑ t, P s true t*optimal d g β P n t)

theorem backward_induction (d g β : ℝ) (P : S → Bool → S → ℝ)
    (hrow : ∀ s a, ∑ t, P s a t = 1) (hg : 0 < g) (n : Nat) :
    ∀ s, optimal d g β P n s = payoff d β n := by
  induction n with
  | zero => intro s; rfl
  | succ n ih =>
    intro s
    simp only [optimal, ih, ← Finset.sum_mul, hrow, one_mul, payoff]
    exact max_eq_left (by linarith)

theorem D_unique_at_every_stage (d g β : ℝ) (P : S → Bool → S → ℝ)
    (hrow : ∀ s a, ∑ t, P s a t = 1) (hg : 0 < g) (n : Nat) (s : S) :
    d-g+β*∑ t, P s true t*optimal d g β P n t <
    d+β*∑ t, P s false t*optimal d g β P n t := by
  simp only [backward_induction d g β P hrow hg n,
    ← Finset.sum_mul, hrow, one_mul]
  linarith

theorem noisy_donation_gap (ε c : ℝ) (he : ε < 1/2) (hc : 0 < c) :
    0 < (1-2*ε)*c := by
  exact mul_pos (by linarith) hc

end Alignment.Horizon
