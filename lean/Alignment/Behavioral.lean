import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/- [B: lab] D18(f). Expected finite-horizon returns for arbitrary behavioral
   strategies. Chance outcomes are retained in the observed history. Convergence
   is derived from finite reward bounds, not supplied as a certificate field. -/
namespace Alignment.Behavioral
open scoped BigOperators
open Filter

noncomputable def average {X : Type*} [Fintype X] (p f : X → ℝ) : ℝ :=
  ∑ x, p x * f x

theorem average_const {X : Type*} [Fintype X] (p : X → ℝ)
    (hp : ∑ x, p x = 1) (c : ℝ) : average p (fun _ => c) = c := by
  simp only [average, ← Finset.sum_mul, hp, one_mul]

theorem average_sub {X : Type*} [Fintype X] (p f g : X → ℝ) :
    average p (fun x => f x-g x) = average p f-average p g := by
  simp only [average, mul_sub, Finset.sum_sub_distrib]

theorem average_mono {X : Type*} [Fintype X] (p f g : X → ℝ)
    (hp : ∀ x, 0 ≤ p x) (hfg : ∀ x, f x ≤ g x) : average p f ≤ average p g := by
  exact Finset.sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (hfg x) (hp x)

theorem average_le_const {X : Type*} [Fintype X] (p f : X → ℝ)
    (hp : ∀ x, 0 ≤ p x) (hrow : ∑ x, p x = 1) (c : ℝ)
    (hf : ∀ x, f x ≤ c) : average p f ≤ c := by
  simpa only [average_const p hrow c] using average_mono p f (fun _ => c) hp hf

theorem average_le_on_support {X : Type*} [Fintype X] (p f : X → ℝ)
    (hp : ∀ x, 0 ≤ p x) (hrow : ∑ x, p x = 1) (c : ℝ)
    (hf : ∀ x, p x ≠ 0 → f x ≤ c) : average p f ≤ c := by
  have he : average p f ≤ average p (fun _ => c) := by
    apply Finset.sum_le_sum
    intro x hx
    by_cases hz : p x=0
    · simp [hz]
    · exact mul_le_mul_of_nonneg_left (hf x hz) (hp x)
  simpa only [average_const p hrow c] using he

theorem abs_average_le {X : Type*} [Fintype X] (p f : X → ℝ)
    (hp : ∀ x, 0 ≤ p x) (hrow : ∑ x, p x = 1) (c : ℝ)
    (hf : ∀ x, |f x| ≤ c) : |average p f| ≤ c := by
  calc
    |average p f| ≤ ∑ x, |p x*f x| := Finset.abs_sum_le_sum_abs _ _
    _ = average p (fun x => |f x|) := by
      simp only [average, abs_mul, abs_of_nonneg (hp _)]
    _ ≤ c := average_le_const p (fun x => |f x|) hp hrow c hf

variable {S A O : Type*} [Fintype S] [Fintype A] [Fintype O]

abbrev History (S A O : Type*) := List (S × A × O)

structure Model (S A O : Type*) [Fintype O] where
  reward : S → A → ℝ
  transition : S → A → O → ℝ
  nextState : O → S
  nonnegative : ∀ s a o, 0 ≤ transition s a o
  stochastic : ∀ s a, ∑ o, transition s a o = 1

structure Strategy (S A O : Type*) [Fintype A] where
  probability : History S A O → S → A → ℝ
  nonnegative : ∀ h s a, 0 ≤ probability h s a
  normalized : ∀ h s, ∑ a, probability h s a = 1

structure MarkovStrategy (S A : Type*) [Fintype A] where
  probability : S → A → ℝ
  nonnegative : ∀ s a, 0 ≤ probability s a
  normalized : ∀ s, ∑ a, probability s a = 1

def MarkovStrategy.behavioral (μ : MarkovStrategy S A) : Strategy S A O :=
  ⟨fun _ => μ.probability, fun _ => μ.nonnegative, fun _ => μ.normalized⟩

noncomputable def pure (π : S → A) : MarkovStrategy S A := by
  classical
  exact ⟨fun s a => if a=π s then 1 else 0,
    fun s a => by dsimp; split_ifs <;> positivity, fun s => by simp⟩

noncomputable def step (M : Model S A O) (β : ℝ) (σ : Strategy S A O)
    (V : History S A O → S → ℝ) (h : History S A O) (s : S) : ℝ :=
  average (σ.probability h s) (fun a => M.reward s a +
    β*average (M.transition s a) (fun o => V ((s,a,o)::h) (M.nextState o)))

noncomputable def truncated (M : Model S A O) (β : ℝ) (σ : Strategy S A O) :
    Nat → History S A O → S → ℝ
  | 0, _, _ => 0
  | n+1, h, s => step M β σ (truncated M β σ n) h s

noncomputable def rewardBound (M : Model S A O) : ℝ := ∑ s, ∑ a, |M.reward s a|

theorem reward_abs_le (M : Model S A O) (s : S) (a : A) :
    |M.reward s a| ≤ rewardBound M := by
  have h1 : |M.reward s a| ≤ ∑ b, |M.reward s b| :=
    Finset.single_le_sum (f := fun b : A => |M.reward s b|)
      (fun b _ => abs_nonneg _) (Finset.mem_univ a)
  have h2 : (∑ b, |M.reward s b|) ≤ rewardBound M :=
    Finset.single_le_sum (f := fun t : S => ∑ b : A, |M.reward t b|)
      (fun t _ => Finset.sum_nonneg fun b _ => abs_nonneg _)
      (Finset.mem_univ s)
  exact h1.trans h2

omit [Fintype S] in
theorem step_lipschitz (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β)
    (σ : Strategy S A O) (V W : History S A O → S → ℝ) (C : ℝ)
    (hVW : ∀ h s, |V h s-W h s| ≤ C) (h : History S A O) (s : S) :
    |step M β σ V h s-step M β σ W h s| ≤ β*C := by
  unfold step
  rw [← average_sub]
  apply abs_average_le _ _ (σ.nonnegative h s) (σ.normalized h s) (β*C)
  intro a
  have hi := abs_average_le (M.transition s a)
    (fun o => V ((s,a,o)::h) (M.nextState o)-W ((s,a,o)::h) (M.nextState o))
    (M.nonnegative s a) (M.stochastic s a) C (fun o => hVW _ _)
  have he : M.reward s a+β*average (M.transition s a)
      (fun o => V ((s,a,o)::h) (M.nextState o)) -
      (M.reward s a+β*average (M.transition s a)
      (fun o => W ((s,a,o)::h) (M.nextState o))) =
      β*average (M.transition s a)
      (fun o => V ((s,a,o)::h) (M.nextState o)-W ((s,a,o)::h) (M.nextState o)) := by
    rw [average_sub]
    ring
  rw [he, abs_mul, abs_of_nonneg hβ]
  exact mul_le_mul_of_nonneg_left hi hβ

theorem increment_bound (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β)
    (σ : Strategy S A O) (n : Nat) :
    ∀ h s, |truncated M β σ (n+1) h s-truncated M β σ n h s| ≤
      rewardBound M*β^n := by
  induction n with
  | zero =>
    intro h s
    simp only [truncated, step, average, mul_zero, Finset.sum_const_zero,
      add_zero, sub_zero, pow_zero, mul_one]
    exact abs_average_le _ _ (σ.nonnegative h s) (σ.normalized h s)
      (rewardBound M) (reward_abs_le M s)
  | succ n ih =>
    intro h s
    change |step M β σ (truncated M β σ (n+1)) h s-
      step M β σ (truncated M β σ n) h s| ≤ rewardBound M*β^(n+1)
    calc
      _ ≤ β*(rewardBound M*β^n) := step_lipschitz M β hβ σ _ _ _ ih h s
      _ = rewardBound M*β^(n+1) := by rw [pow_succ]; ring

theorem truncated_cauchy (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1)
    (σ : Strategy S A O) (h : History S A O) (s : S) :
    CauchySeq (fun n => truncated M β σ n h s) := by
  apply cauchySeq_of_le_geometric β (rewardBound M) hβ1
  intro n
  simpa only [Real.dist_eq, abs_sub_comm] using increment_bound M β hβ σ n h s

noncomputable def payoff (M : Model S A O) (β : ℝ) (σ : Strategy S A O)
    (h : History S A O) (s : S) : ℝ :=
  limUnder atTop (fun n => truncated M β σ n h s)

theorem payoff_tendsto (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1)
    (σ : Strategy S A O) (h : History S A O) (s : S) :
    Tendsto (fun n => truncated M β σ n h s) atTop (nhds (payoff M β σ h s)) :=
  (truncated_cauchy M β hβ hβ1 σ h s).tendsto_limUnder

theorem payoff_error_bound (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1)
    (σ : Strategy S A O) (h : History S A O) (s : S) (n : Nat) :
    |truncated M β σ n h s-payoff M β σ h s| ≤ rewardBound M*β^n/(1-β) := by
  apply dist_le_of_le_geometric_of_tendsto β (rewardBound M) hβ1
    (fun k => by simpa only [Real.dist_eq, abs_sub_comm] using increment_bound M β hβ σ k h s)
    (payoff_tendsto M β hβ hβ1 σ h s) n

omit [Fintype S] in
theorem truncated_upper (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β)
    (W : S → ℝ) (C : ℝ) (hW : ∀ s, -C ≤ W s)
    (hcert : ∀ s a, M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)) ≤ W s)
    (σ : Strategy S A O) (n : Nat) :
    ∀ h s, truncated M β σ n h s ≤ W s+β^n*C := by
  induction n with
  | zero => intro h s; simp only [truncated, pow_zero, one_mul]; linarith [hW s]
  | succ n ih =>
    intro h s
    change average (σ.probability h s) _ ≤ W s+β^(n+1)*C
    apply average_le_const _ _ (σ.nonnegative h s) (σ.normalized h s)
    intro a
    have hb := average_mono (M.transition s a)
      (fun o => truncated M β σ n ((s,a,o)::h) (M.nextState o))
      (fun o => W (M.nextState o)+β^n*C) (M.nonnegative s a) (fun o => ih _ _)
    have he : average (M.transition s a) (fun o => W (M.nextState o)+β^n*C) =
        average (M.transition s a) (fun o => W (M.nextState o))+β^n*C := by
      simp only [average, mul_add, Finset.sum_add_distrib, ← Finset.sum_mul,
        M.stochastic, one_mul]
    rw [he] at hb
    have hm := mul_le_mul_of_nonneg_left hb hβ
    have hc := hcert s a
    have hp : β^(n+1)*C=β*(β^n*C) := by rw [pow_succ]; ring
    rw [hp]
    linarith

theorem payoff_upper (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1)
    (W : S → ℝ)
    (hcert : ∀ s a, M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)) ≤ W s)
    (σ : Strategy S A O) (h : History S A O) (s : S) : payoff M β σ h s ≤ W s := by
  let C : ℝ := ∑ t, |W t|
  have hW : ∀ t, -C ≤ W t := by
    intro t
    have hb : |W t| ≤ C := Finset.single_le_sum (f := fun u : S => |W u|)
      (fun u _ => abs_nonneg _) (Finset.mem_univ t)
    linarith [neg_abs_le (W t)]
  have ht : Tendsto (fun n : Nat => W s+β^n*C) atTop (nhds (W s)) := by
    simpa using tendsto_const_nhds.add
      ((tendsto_pow_atTop_nhds_zero_of_lt_one hβ hβ1).mul_const C)
  exact le_of_tendsto_of_tendsto' (payoff_tendsto M β hβ hβ1 σ h s) ht
    (fun n => truncated_upper M β hβ W C hW hcert σ n h s)

omit [Fintype S] in
theorem markov_value_error (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β)
    (μ : MarkovStrategy S A) (W : S → ℝ) (C : ℝ) (hW : ∀ s, |W s| ≤ C)
    (hvalue : ∀ s, average (μ.probability s)
      (fun a => M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)))=W s)
    (n : Nat) : ∀ h s, |truncated M β μ.behavioral n h s-W s| ≤ β^n*C := by
  induction n with
  | zero => intro h s; simpa only [truncated, zero_sub, abs_neg, pow_zero, one_mul] using hW s
  | succ n ih =>
    intro h s
    have he : step M β μ.behavioral (fun _ s => W s) h s = W s := hvalue s
    change |step M β μ.behavioral (truncated M β μ.behavioral n) h s-W s| ≤ β^(n+1)*C
    rw [← he]
    calc
      _ ≤ β*(β^n*C) := step_lipschitz M β hβ μ.behavioral _ _ _ ih h s
      _ = β^(n+1)*C := by rw [pow_succ]; ring

theorem markov_payoff_eq (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1)
    (μ : MarkovStrategy S A) (W : S → ℝ)
    (hvalue : ∀ s, average (μ.probability s)
      (fun a => M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)))=W s)
    (h : History S A O) (s : S) : payoff M β μ.behavioral h s = W s := by
  let C : ℝ := ∑ t, |W t|
  have hW : ∀ t, |W t| ≤ C := fun t =>
    Finset.single_le_sum (f := fun u : S => |W u|)
      (fun u _ => abs_nonneg _) (Finset.mem_univ t)
  have ht : Tendsto (fun n : Nat => β^n*C) atTop (nhds (0 : ℝ)) := by
    simpa using (tendsto_pow_atTop_nhds_zero_of_lt_one hβ hβ1).mul_const C
  have ha : Tendsto (fun n => |truncated M β μ.behavioral n h s-W s|) atTop
      (nhds |payoff M β μ.behavioral h s-W s|) :=
    ((payoff_tendsto M β hβ hβ1 μ.behavioral h s).sub tendsto_const_nhds).abs
  have hb := le_of_tendsto_of_tendsto' ha ht
    (fun n => markov_value_error M β hβ μ W C hW hvalue n h s)
  exact sub_eq_zero.mp (abs_eq_zero.mp (le_antisymm hb (abs_nonneg _)))

def BestResponse (M : Model S A O) (β : ℝ) (μ : MarkovStrategy S A) : Prop :=
  ∀ σ : Strategy S A O, ∀ h s, payoff M β σ h s ≤ payoff M β μ.behavioral h s

theorem one_shot_certifies_best_response (M : Model S A O) (β : ℝ)
    (hβ : 0 ≤ β) (hβ1 : β < 1) (μ : MarkovStrategy S A) (W : S → ℝ)
    (hvalue : ∀ s, average (μ.probability s)
      (fun a => M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)))=W s)
    (hcert : ∀ s a, M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)) ≤ W s) :
    BestResponse M β μ := by
  intro σ h s
  rw [markov_payoff_eq M β hβ hβ1 μ W hvalue h s]
  exact payoff_upper M β hβ hβ1 W hcert σ h s

def Admissible (L : S → A → Prop) (σ : Strategy S A O) : Prop :=
  ∀ h s a, ¬ L s a → σ.probability h s a=0

def BestResponseLegal (M : Model S A O) (β : ℝ) (L : S → A → Prop)
    (μ : MarkovStrategy S A) : Prop :=
  Admissible L (μ.behavioral : Strategy S A O) ∧ ∀ σ : Strategy S A O, Admissible L σ →
    ∀ h s, payoff M β σ h s ≤ payoff M β μ.behavioral h s

omit [Fintype S] in
theorem truncated_upper_legal (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β)
    (L : S → A → Prop) (W : S → ℝ) (C : ℝ) (hW : ∀ s, -C ≤ W s)
    (hcert : ∀ s a, L s a →
      M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)) ≤ W s)
    (σ : Strategy S A O) (hσ : Admissible L σ) (n : Nat) :
    ∀ h s, truncated M β σ n h s ≤ W s+β^n*C := by
  induction n with
  | zero => intro h s; simp only [truncated, pow_zero, one_mul]; linarith [hW s]
  | succ n ih =>
    intro h s
    change average (σ.probability h s) _ ≤ W s+β^(n+1)*C
    apply average_le_on_support _ _ (σ.nonnegative h s) (σ.normalized h s)
    intro a hpa
    have hla : L s a := by
      by_contra hn
      exact hpa (hσ h s a hn)
    have hb := average_mono (M.transition s a)
      (fun o => truncated M β σ n ((s,a,o)::h) (M.nextState o))
      (fun o => W (M.nextState o)+β^n*C) (M.nonnegative s a) (fun o => ih _ _)
    have he : average (M.transition s a) (fun o => W (M.nextState o)+β^n*C) =
        average (M.transition s a) (fun o => W (M.nextState o))+β^n*C := by
      simp only [average, mul_add, Finset.sum_add_distrib, ← Finset.sum_mul,
        M.stochastic, one_mul]
    rw [he] at hb
    have hm := mul_le_mul_of_nonneg_left hb hβ
    have hc := hcert s a hla
    have hp : β^(n+1)*C=β*(β^n*C) := by rw [pow_succ]; ring
    rw [hp]
    linarith

theorem payoff_upper_legal (M : Model S A O) (β : ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1)
    (L : S → A → Prop) (W : S → ℝ)
    (hcert : ∀ s a, L s a →
      M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)) ≤ W s)
    (σ : Strategy S A O) (hσ : Admissible L σ) (h : History S A O) (s : S) :
    payoff M β σ h s ≤ W s := by
  let C : ℝ := ∑ t, |W t|
  have hW : ∀ t, -C ≤ W t := by
    intro t
    have hb : |W t| ≤ C := Finset.single_le_sum (f := fun u : S => |W u|)
      (fun u _ => abs_nonneg _) (Finset.mem_univ t)
    linarith [neg_abs_le (W t)]
  have ht : Tendsto (fun n : Nat => W s+β^n*C) atTop (nhds (W s)) := by
    simpa using tendsto_const_nhds.add
      ((tendsto_pow_atTop_nhds_zero_of_lt_one hβ hβ1).mul_const C)
  exact le_of_tendsto_of_tendsto' (payoff_tendsto M β hβ hβ1 σ h s) ht
    (fun n => truncated_upper_legal M β hβ L W C hW hcert σ hσ n h s)

theorem one_shot_certifies_legal_best_response (M : Model S A O) (β : ℝ)
    (hβ : 0 ≤ β) (hβ1 : β < 1) (L : S → A → Prop)
    (μ : MarkovStrategy S A) (W : S → ℝ)
    (hμ : ∀ s a, ¬ L s a → μ.probability s a=0)
    (hvalue : ∀ s, average (μ.probability s)
      (fun a => M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)))=W s)
    (hcert : ∀ s a, L s a →
      M.reward s a+β*average (M.transition s a) (fun o => W (M.nextState o)) ≤ W s) :
    BestResponseLegal M β L μ := by
  refine ⟨fun _ s a hn => hμ s a hn, ?_⟩
  intro σ hσ h s
  rw [markov_payoff_eq M β hβ hβ1 μ W hvalue h s]
  exact payoff_upper_legal M β hβ hβ1 L W hcert σ hσ h s

end Alignment.Behavioral
