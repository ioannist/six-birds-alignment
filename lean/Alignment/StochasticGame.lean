import Alignment.Behavioral
import Mathlib.Algebra.BigOperators.Ring.Finset

/- [B: lab] D18(f). A finite observed stochastic game with independently
   randomized Markov candidates. Each unilateral response kernel is constructed
   from the same raw joint-action reward/transition data. -/
namespace Alignment.StochasticGame
open scoped BigOperators
open Alignment.Behavioral

variable {I S A : Type*} [Fintype I] [Fintype S] [Fintype A] [DecidableEq I]
abbrev JointAction (I A : Type*) := I → A

structure Game (I S A : Type*) [Fintype S] where
  reward : S → JointAction I A → I → ℝ
  transition : S → JointAction I A → S → ℝ
  nonnegative : ∀ s j t, 0 ≤ transition s j t
  stochastic : ∀ s j, ∑ t, transition s j t = 1

abbrev Profile (I S A : Type*) [Fintype A] := I → MarkovStrategy S A

noncomputable def responseFactor (μ : Profile I S A) (i : I) (s : S) (a : A)
    (k : I) (b : A) : ℝ := by
  classical
  exact if k=i then (if b=a then 1 else 0) else (μ k).probability s b

omit [Fintype I] [Fintype S] in
theorem response_factor_nonnegative (μ : Profile I S A) (i : I) (s : S) (a : A)
    (k : I) (b : A) : 0 ≤ responseFactor μ i s a k b := by
  classical
  unfold responseFactor
  split_ifs <;> first | positivity | exact (μ k).nonnegative s b

omit [Fintype I] [Fintype S] in
theorem response_factor_normalized (μ : Profile I S A) (i : I) (s : S) (a : A)
    (k : I) : ∑ b, responseFactor μ i s a k b = 1 := by
  classical
  by_cases hk : k=i
  · simp [responseFactor, hk]
  · simpa only [responseFactor, if_neg hk] using (μ k).normalized s

noncomputable def responseProbability (μ : Profile I S A) (i : I) (s : S) (a : A)
    (j : JointAction I A) : ℝ := ∏ k, responseFactor μ i s a k (j k)

omit [Fintype S] in
theorem response_probability_nonnegative (μ : Profile I S A) (i : I) (s : S)
    (a : A) (j : JointAction I A) : 0 ≤ responseProbability μ i s a j := by
  exact Finset.prod_nonneg fun k _ => response_factor_nonnegative μ i s a k (j k)

omit [Fintype S] in
theorem response_probability_normalized (μ : Profile I S A) (i : I) (s : S)
    (a : A) : ∑ j, responseProbability μ i s a j = 1 := by
  classical
  unfold responseProbability
  rw [← Fintype.prod_sum]
  simp only [response_factor_normalized, Finset.prod_const_one]

omit [Fintype S] in
theorem response_own_action (μ : Profile I S A) (i : I) (s : S) (a : A)
    (j : JointAction I A) (hp : responseProbability μ i s a j ≠ 0) : j i = a := by
  classical
  by_contra hn
  have hz : responseFactor μ i s a i (j i)=0 := by simp [responseFactor, hn]
  have hp0 : responseProbability μ i s a j=0 :=
    Finset.prod_eq_zero (Finset.mem_univ i) hz
  exact hp hp0

noncomputable def response (G : Game I S A) (μ : Profile I S A) (i : I) :
    Model S A (JointAction I A × S) where
  reward s a := average (responseProbability μ i s a) (fun j => G.reward s j i)
  transition s a o := responseProbability μ i s a o.1*G.transition s o.1 o.2
  nextState := Prod.snd
  nonnegative s a o := mul_nonneg (response_probability_nonnegative μ i s a o.1)
    (G.nonnegative s o.1 o.2)
  stochastic s a := by
    classical
    simp only [Fintype.sum_prod_type, ← Finset.mul_sum, G.stochastic, mul_one]
    exact response_probability_normalized μ i s a

noncomputable def oneStep (G : Game I S A) (μ : Profile I S A) (β : ℝ)
    (i : I) (W : S → ℝ) (s : S) (a : A) : ℝ :=
  average (responseProbability μ i s a) (fun j => G.reward s j i+
    β*average (G.transition s j) W)

theorem response_one_step_eq (G : Game I S A) (μ : Profile I S A) (β : ℝ)
    (i : I) (W : S → ℝ) (s : S) (a : A) :
    (response G μ i).reward s a+β*average ((response G μ i).transition s a)
      (fun o => W ((response G μ i).nextState o))=oneStep G μ β i W s a := by
  classical
  simp only [response, oneStep, average, Fintype.sum_prod_type]
  simp only [mul_add, Finset.sum_add_distrib, Finset.mul_sum, mul_assoc, mul_left_comm]

/- Every player's arbitrary history-dependent behavioral deviations, at every
   initial observed history and current state, are compared to that player's
   Markov component against the other fixed Markov components. -/
def MarkovPerfect (G : Game I S A) (β : ℝ) (μ : Profile I S A) : Prop :=
  ∀ i, BestResponse (response G μ i) β (μ i)

theorem one_shot_deviation_implies_markov_perfect (G : Game I S A)
    (β : ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1) (μ : Profile I S A) (W : I → S → ℝ)
    (hvalue : ∀ i s, average ((μ i).probability s)
      (fun a => oneStep G μ β i (W i) s a)=W i s)
    (hcert : ∀ i s a, oneStep G μ β i (W i) s a ≤ W i s) :
    MarkovPerfect G β μ := by
  intro i
  apply one_shot_certifies_best_response (response G μ i) β hβ hβ1 (μ i) (W i)
  · intro s
    simpa only [response_one_step_eq] using hvalue i s
  · intro s a
    simpa only [response_one_step_eq] using hcert i s a

def AdmissibleProfile (L : I → S → A → Prop) (μ : Profile I S A) : Prop :=
  ∀ i s a, ¬ L i s a → (μ i).probability s a=0

omit [Fintype S] in
theorem supported_joint_action_legal (L : I → S → A → Prop) (μ : Profile I S A)
    (hμ : AdmissibleProfile L μ) (i : I) (s : S) (a : A) (ha : L i s a)
    (j : JointAction I A) (hp : responseProbability μ i s a j ≠ 0) :
    ∀ k, L k s (j k) := by
  classical
  intro k
  by_cases hk : k=i
  · subst k
    rw [response_own_action μ i s a j hp]
    exact ha
  · by_contra hn
    have hz : responseFactor μ i s a k (j k)=0 := by
      simp only [responseFactor, if_neg hk]
      exact hμ k s (j k) hn
    have hzero : responseProbability μ i s a j=0 :=
      Finset.prod_eq_zero (Finset.mem_univ k) hz
    exact hp hzero

def MarkovPerfectLegal (G : Game I S A) (β : ℝ) (L : I → S → A → Prop)
    (μ : Profile I S A) : Prop :=
  AdmissibleProfile L μ ∧ ∀ i, BestResponseLegal (response G μ i) β (L i) (μ i)

theorem one_shot_deviation_implies_legal_markov_perfect (G : Game I S A)
    (β : ℝ) (hβ : 0 ≤ β) (hβ1 : β < 1) (L : I → S → A → Prop)
    (μ : Profile I S A) (hμ : AdmissibleProfile L μ) (W : I → S → ℝ)
    (hvalue : ∀ i s, average ((μ i).probability s)
      (fun a => oneStep G μ β i (W i) s a)=W i s)
    (hcert : ∀ i s a, L i s a → oneStep G μ β i (W i) s a ≤ W i s) :
    MarkovPerfectLegal G β L μ := by
  refine ⟨hμ, ?_⟩
  intro i
  apply one_shot_certifies_legal_best_response (response G μ i) β hβ hβ1 (L i) (μ i) (W i)
  · exact hμ i
  · intro s
    simpa only [response_one_step_eq] using hvalue i s
  · intro s a ha
    simpa only [response_one_step_eq] using hcert i s a ha

end Alignment.StochasticGame
