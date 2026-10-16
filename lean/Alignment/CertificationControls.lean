import Alignment.StochasticGame
import Mathlib.Tactic.NormNum

/- [B: lab] D18(f): inhabited finite-game controls. A state is absorbing;
   choosing true earns one, choosing false earns zero. The bad candidate plays
   true in the true state, false in the false state. Its reachable true path
   passes while its off-path false state has a profitable deviation. -/
namespace Alignment.CertificationControls
open scoped BigOperators
open Alignment.Behavioral Alignment.StochasticGame

noncomputable def controlGame : Game Unit Bool Bool where
  reward _ j _ := if j () then 1 else 0
  transition s _ t := if t=s then 1 else 0
  nonnegative s j t := by split_ifs <;> norm_num
  stochastic s j := by
    classical
    simp

noncomputable def goodProfile : Profile Unit Bool Bool := fun _ => Behavioral.pure (fun _ => true)
noncomputable def badProfile : Profile Unit Bool Bool := fun _ => Behavioral.pure (fun s => s)
def badValue (_ : Unit) (s : Bool) : ℝ := if s then 2 else 0

theorem control_one_step (μ : Profile Unit Bool Bool) (β : ℝ) (W : Bool → ℝ) (s a : Bool) :
    oneStep controlGame μ β () W s a=(if a then 1 else 0)+β*W s := by
  classical
  unfold oneStep
  have hc : ∀ j : JointAction Unit Bool,
      average (controlGame.transition s j) W=W s := by
    intro j
    simp [average, controlGame, ite_mul]
  simp_rw [hc]
  change (∑ j : JointAction Unit Bool, responseProbability μ () s a j*
    ((if j () then 1 else 0)+β*W s))=_
  have he : (∑ j : JointAction Unit Bool, responseProbability μ () s a j*
      ((if j () then 1 else 0)+β*W s))=
      average (responseProbability μ () s a) (fun _ => (if a then 1 else 0)+β*W s) := by
    apply Finset.sum_congr rfl
    intro j hj
    by_cases hz : responseProbability μ () s a j=0
    · simp [hz]
    · rw [response_own_action μ () s a j hz]
  rw [he, average_const _ (response_probability_normalized μ () s a)]

theorem good_value_equation : ∀ i s,
    average ((goodProfile i).probability s)
      (fun a => oneStep controlGame goodProfile (1/2) i (fun _ => 2) s a)=2 := by
  intro i s
  cases i
  norm_num [goodProfile, Behavioral.pure, average, control_one_step]

theorem good_all_state_certificate : ∀ i s a,
    oneStep controlGame goodProfile (1/2) i (fun _ => 2) s a ≤ 2 := by
  intro i s a
  cases i
  rw [control_one_step]
  cases a <;> norm_num

theorem good_markov_perfect : MarkovPerfect controlGame (1/2) goodProfile := by
  exact one_shot_deviation_implies_markov_perfect controlGame (1/2)
    (by norm_num) (by norm_num) goodProfile (fun _ _ => 2)
    good_value_equation good_all_state_certificate

theorem bad_value_equation : ∀ i s,
    average ((badProfile i).probability s)
      (fun a => oneStep controlGame badProfile (1/2) i (badValue i) s a)=badValue i s := by
  intro i s
  cases i
  cases s <;> norm_num [badProfile, Behavioral.pure, average, control_one_step, badValue]

theorem reachable_state_passes : ∀ a,
    oneStep controlGame badProfile (1/2) () (badValue ()) true a ≤ badValue () true := by
  intro a
  rw [control_one_step]
  cases a <;> norm_num [badValue]

theorem off_path_state_fails :
    badValue () false < oneStep controlGame badProfile (1/2) () (badValue ()) false true := by
  rw [control_one_step]
  norm_num [badValue]

theorem bad_global_certificate_false : ¬ (∀ i s a,
    oneStep controlGame badProfile (1/2) i (badValue i) s a ≤ badValue i s) := by
  intro h
  exact (not_le_of_gt off_path_state_fails) (h () false true)

theorem bad_profile_deviation_payoffs
    (h : History Bool Bool (JointAction Unit Bool × Bool)) :
    payoff (response controlGame badProfile ()) (1/2) (goodProfile ()).behavioral h false=2 ∧
    payoff (response controlGame badProfile ()) (1/2) (badProfile ()).behavioral h false=0 := by
  constructor
  · apply markov_payoff_eq (response controlGame badProfile ()) (1/2)
      (by norm_num) (by norm_num) (goodProfile ()) (fun _ => 2)
    intro s
    simp_rw [response_one_step_eq controlGame badProfile (1/2) () (fun _ => 2)]
    norm_num [goodProfile, Behavioral.pure, average, control_one_step]
  · convert markov_payoff_eq (response controlGame badProfile ()) (1/2)
      (by norm_num) (by norm_num) (badProfile ()) (badValue ())
      (fun s => by simpa only [response_one_step_eq] using bad_value_equation () s) h false using 1

theorem bad_profile_not_markov_perfect : ¬ MarkovPerfect controlGame (1/2) badProfile := by
  intro h
  have hd := h () (goodProfile ()).behavioral [] false
  have hp := bad_profile_deviation_payoffs []
  rw [hp.1, hp.2] at hd
  norm_num at hd

def controlMenu (_ : Unit) (s a : Bool) : Prop := s=true ∨ a=false

theorem bad_profile_admissible : AdmissibleProfile controlMenu badProfile := by
  intro i s a hn
  cases i
  cases s <;> cases a <;> norm_num [controlMenu, badProfile, Behavioral.pure] at *

theorem bad_legal_all_state_certificate : ∀ i s a, controlMenu i s a →
    oneStep controlGame badProfile (1/2) i (badValue i) s a ≤ badValue i s := by
  intro i s a hlegal
  cases i
  rw [control_one_step]
  cases s <;> cases a <;> norm_num [controlMenu, badValue] at *

theorem bad_profile_legal_markov_perfect :
    MarkovPerfectLegal controlGame (1/2) controlMenu badProfile := by
  exact one_shot_deviation_implies_legal_markov_perfect controlGame (1/2)
    (by norm_num) (by norm_num) controlMenu badProfile bad_profile_admissible
    badValue bad_value_equation bad_legal_all_state_certificate

theorem good_profile_inadmissible : ¬ AdmissibleProfile controlMenu goodProfile := by
  intro h
  have hz := h () false true (by simp [controlMenu])
  norm_num [goodProfile, Behavioral.pure] at hz

theorem good_profile_not_legal_markov_perfect :
    ¬ MarkovPerfectLegal controlGame (1/2) controlMenu goodProfile := by
  intro h
  exact good_profile_inadmissible h.1

end Alignment.CertificationControls
