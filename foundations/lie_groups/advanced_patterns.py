"""
Advanced Patterns for SE(3) Double-and-Scale Returns

Implements sophisticated patterns from Claude Opus analysis:
- Berry phase tracking (geometric phase accumulation)
- Hysteresis tracking (path-dependent enhancement)
- Return quality calibration
- Ornstein-Uhlenbeck stochastic processes on Lie groups

These patterns extend the basic double-and-scale mechanism with
physically realistic features for regenerative systems modeling.
"""

import numpy as np
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass
from scipy.spatial.transform import Rotation as R

from se3_double_scale import (
    SE3Pose,
    SE3Trajectory,
    compose_se3,
    compose_trajectory,
    frobenius_distance_to_identity
)


@dataclass
class BerryPhase:
    """
    Berry geometric phase accumulated during cyclic evolution [Opus insight]

    When a system traverses a closed loop in parameter space (double cycle),
    it acquires a geometric phase even if it returns to the same state.
    This phase IS the transformation factor.

    Physical interpretation: Why the "same" agricultural cycle produces
    different results each time - it's accumulating geometric phase.

    Mathematical basis:
        γ_Berry = ∮ ⟨ψ|i∇|ψ⟩ · dl

    For SE(3), we track holonomy (parallel transport around closed loop).
    """
    rotation_phase: np.ndarray  # 3D rotation phase (axis-angle)
    translation_phase: np.ndarray  # 3D translation phase
    loop_area: float  # Geometric area enclosed by loop

    def total_magnitude(self) -> float:
        """Total geometric phase magnitude"""
        return np.linalg.norm(self.rotation_phase) + np.linalg.norm(self.translation_phase)


def compute_berry_phase(trajectory: SE3Trajectory, closed_loop: bool = True) -> BerryPhase:
    """
    Compute Berry geometric phase for SE(3) trajectory [Opus insight]

    Tracks holonomy (parallel transport) around a closed loop in SE(3).
    The accumulated phase explains why repeated cycles create different outcomes.

    Args:
        trajectory: SE(3) trajectory (should form closed or nearly-closed loop)
        closed_loop: Whether to enforce closure (compose with inverse to close)

    Returns:
        BerryPhase object with rotation and translation phases
    """
    # Compose full trajectory
    total = compose_trajectory(trajectory)

    # If loop isn't closed, close it artificially
    if closed_loop:
        # Close the loop by composing with inverse
        # (This is the "return" operation)
        inverse_rotation = total.rotation.T
        inverse_translation = -inverse_rotation @ total.translation
        closing = SE3Pose(rotation=inverse_rotation, translation=inverse_translation)
        closed_total = compose_se3(total, closing)
    else:
        closed_total = total

    # Extract geometric phase from deviation from identity
    rotation_phase = R.from_matrix(closed_total.rotation).as_rotvec()
    translation_phase = closed_total.translation

    # Estimate loop area (using translation path length as proxy)
    loop_area = 0.0
    for i in range(len(trajectory) - 1):
        # Area contribution from each segment
        p1 = trajectory[i].translation
        p2 = trajectory[i+1].translation
        # Cross product magnitude (2x triangle area)
        loop_area += 0.5 * np.linalg.norm(np.cross(p1, p2))

    return BerryPhase(
        rotation_phase=rotation_phase,
        translation_phase=translation_phase,
        loop_area=loop_area
    )


class HysteresisTracker:
    """
    Track rotational hysteresis: path-dependent enhancement [Opus insight]

    Agricultural and ecological systems exhibit hysteresis - the path matters,
    not just the endpoints. Repeated cycles through the same state space
    create cumulative "work" that enhances return quality.

    Physical analogy: Soil structure improves cumulatively with each rotation,
    even if nutrient levels return to baseline.
    """

    def __init__(self, enhancement_rate: float = 0.1):
        """
        Initialize hysteresis tracker.

        Args:
            enhancement_rate: Rate at which path integral enhances returns
        """
        self.path_integral = 0.0
        self.enhancement_rate = enhancement_rate
        self.history: List[float] = []

    def update(self, pose: SE3Pose, previous: Optional[SE3Pose] = None):
        """
        Update path integral with new pose.

        Computes "rotational work" = change in rotation + translation.

        Args:
            pose: Current SE(3) pose
            previous: Previous pose (if available)
        """
        if previous is not None:
            # Relative transformation
            rel_rotation = previous.rotation.T @ pose.rotation
            rel_rotvec = R.from_matrix(rel_rotation).as_rotvec()

            rel_translation = pose.translation - previous.translation

            # Compute "work" (Frobenius-like)
            work = np.linalg.norm(rel_rotvec) + np.linalg.norm(rel_translation)

            self.path_integral += work
            self.history.append(self.path_integral)

    def get_enhancement_factor(self) -> float:
        """
        Get enhancement factor for return quality [Opus insight]

        Hysteresis creates a "higher level" return - each cycle doesn't just
        restore the original state, but lifts the system to an enhanced baseline.

        Returns:
            Enhancement factor ∈ [1, ∞) where 1 = no enhancement
        """
        # Tanh saturation prevents unbounded growth
        enhancement = 1.0 + self.enhancement_rate * np.tanh(self.path_integral)
        return enhancement

    def reset(self):
        """Reset hysteresis tracking (e.g., after major perturbation)"""
        self.path_integral = 0.0
        self.history = []


class OrnsteinUhlenbeckProcess:
    """
    Ornstein-Uhlenbeck process on Lie groups [5.1, Opus insight]

    Mean-reverting stochastic process for SE(3):
        dX_t = -θ(X_t - μ)dt + σ dW_t

    Where:
    - θ: Mean reversion strength (return tendency)
    - μ: Target state (equilibrium / enhanced baseline)
    - σ: Noise amplitude (weather, pests, market volatility)

    Creates natural "basin of attraction" for regenerative returns.
    """

    def __init__(
        self,
        target: SE3Pose,
        reversion_strength: float = 0.5,
        noise_amplitude: float = 0.1,
        dt: float = 0.01
    ):
        """
        Initialize OU process.

        Args:
            target: Equilibrium state (μ in equation)
            reversion_strength: Mean reversion rate θ
            noise_amplitude: Noise strength σ
            dt: Time step for integration
        """
        self.target = target
        self.theta = reversion_strength
        self.sigma = noise_amplitude
        self.dt = dt
        self.current = SE3Pose.identity()

    def step(self) -> SE3Pose:
        """
        Take one step of OU process on SE(3).

        Returns:
            New SE(3) state after stochastic evolution
        """
        # Compute relative transformation to target (logarithmic map)
        rel_rotation = self.current.rotation.T @ self.target.rotation
        rel_rotvec = R.from_matrix(rel_rotation).as_rotvec()

        rel_translation = self.target.translation - self.current.translation

        # Mean reversion force (deterministic)
        rot_drift = self.theta * rel_rotvec
        trans_drift = self.theta * rel_translation

        # Stochastic noise (Brownian motion)
        rot_noise = np.random.normal(0, self.sigma, 3)
        trans_noise = np.random.normal(0, self.sigma, 3)

        # Update via Euler-Maruyama scheme [5.1]
        current_rotvec = self.current.to_rotation_vector()
        new_rotvec = current_rotvec + self.dt * rot_drift + np.sqrt(self.dt) * rot_noise
        new_rotation = R.from_rotvec(new_rotvec).as_matrix()

        new_translation = (
            self.current.translation +
            self.dt * trans_drift +
            np.sqrt(self.dt) * trans_noise
        )

        self.current = SE3Pose(rotation=new_rotation, translation=new_translation)
        return self.current

    def simulate_trajectory(self, T: int) -> SE3Trajectory:
        """
        Simulate full OU trajectory.

        Args:
            T: Number of time steps

        Returns:
            SE(3) trajectory showing mean-reverting behavior
        """
        poses = []
        for _ in range(T):
            pose = self.step()
            poses.append(SE3Pose(
                rotation=pose.rotation.copy(),
                translation=pose.translation.copy()
            ))

        return SE3Trajectory(poses, bounded=False)


class ReturnQualityCalibrator:
    """
    Calibrate scaling factor λ for target return quality [Opus insight]

    Uses binary search to find λ that achieves desired return quality,
    providing practical calibration for real-world regenerative systems.
    """

    def __init__(
        self,
        simulate_double_cycle: Callable[[SE3Trajectory, float], SE3Pose],
        target_quality: float = 0.95,
        max_iterations: int = 20
    ):
        """
        Initialize calibrator.

        Args:
            simulate_double_cycle: Function that simulates trajectory with scaling
            target_quality: Desired return quality ∈ [0, 1]
            max_iterations: Maximum binary search iterations
        """
        self.simulate = simulate_double_cycle
        self.target_quality = target_quality
        self.max_iterations = max_iterations

    def return_quality_metric(self, final_pose: SE3Pose) -> float:
        """
        Compute return quality ∈ [0, 1] where 1 = perfect return.

        Uses exponential decay: Q = exp(-error)

        Args:
            final_pose: Final pose after double-and-scale

        Returns:
            Quality metric ∈ [0, 1]
        """
        error = frobenius_distance_to_identity(final_pose)
        quality = np.exp(-error)
        return quality

    def is_overshooting(self, final_pose: SE3Pose, previous_error: float) -> bool:
        """
        Determine if current λ is overshooting target.

        Overshooting means λ is too large, causing system to
        "swing past" identity and move away.

        Args:
            final_pose: Current final pose
            previous_error: Error from previous iteration

        Returns:
            True if overshooting
        """
        current_error = frobenius_distance_to_identity(final_pose)
        # If error increased, we're overshooting
        return current_error > previous_error

    def calibrate(self, trajectory: SE3Trajectory) -> Tuple[float, Dict]:
        """
        Find optimal λ via binary search [Opus insight]

        Args:
            trajectory: SE(3) trajectory to calibrate

        Returns:
            (optimal_lambda, diagnostics_dict)
        """
        lambda_min, lambda_max = 0.1, 10.0
        best_lambda = None
        best_quality = 0.0
        iterations = []

        for iteration in range(self.max_iterations):
            lambda_test = (lambda_min + lambda_max) / 2

            # Simulate double cycle
            final_pose = self.simulate(trajectory, lambda_test)
            quality = self.return_quality_metric(final_pose)

            iterations.append({
                'iteration': iteration,
                'lambda': lambda_test,
                'quality': quality,
                'error': frobenius_distance_to_identity(final_pose)
            })

            if quality > best_quality:
                best_quality = quality
                best_lambda = lambda_test

            # Check convergence
            if quality >= self.target_quality:
                break

            # Binary search update
            if lambda_max - lambda_min < 0.01:
                break

            # Heuristic: if quality is low, try different direction
            if quality < 0.5:
                # Poor quality, need adjustment
                if iteration > 0:
                    prev_quality = iterations[-2]['quality']
                    if quality < prev_quality:
                        # Getting worse, reverse direction
                        lambda_min = lambda_test
                    else:
                        # Improving, continue
                        lambda_max = lambda_test
                else:
                    # First iteration, assume need to decrease λ
                    lambda_max = lambda_test
            else:
                # Good quality, fine-tune
                error = frobenius_distance_to_identity(final_pose)
                if error > 0:
                    lambda_min = lambda_test
                else:
                    lambda_max = lambda_test

        diagnostics = {
            'final_lambda': best_lambda if best_lambda else lambda_test,
            'final_quality': best_quality,
            'iterations': iterations,
            'converged': best_quality >= self.target_quality
        }

        return best_lambda if best_lambda else lambda_test, diagnostics


def campbell_baker_hausdorff_approximation(
    X: np.ndarray,
    Y: np.ndarray,
    order: int = 2
) -> np.ndarray:
    """
    Campbell-Baker-Hausdorff formula for composition [Opus insight]

    For small rotations, composition is approximately additive in Lie algebra:
        log(e^X e^Y) ≈ X + Y + (1/2)[X,Y] + (1/12)[X,[X,Y]] + ...

    This enables predictable composition for agricultural/ecological cycles.

    Practical rule: Keep individual rotations < π/4 for predictability.

    Args:
        X: First Lie algebra element (3x3 skew-symmetric for so(3))
        Y: Second Lie algebra element
        order: Approximation order (1=first-order, 2=second-order, etc.)

    Returns:
        Approximate log(e^X e^Y) as Lie algebra element
    """
    # First order: just sum
    result = X + Y

    if order >= 2:
        # Second order: add (1/2)[X,Y]
        commutator = X @ Y - Y @ X
        result += 0.5 * commutator

    if order >= 3:
        # Third order: add (1/12)([X,[X,Y]] + [Y,[Y,X]])
        comm_xx_y = X @ commutator - commutator @ X
        comm_yy_x = Y @ (-commutator) - (-commutator) @ Y
        result += (1.0/12.0) * (comm_xx_y + comm_yy_x)

    return result


def predict_composition_accuracy(
    pose1: SE3Pose,
    pose2: SE3Pose
) -> Dict[str, float]:
    """
    Predict accuracy of composition using CBH formula [Opus insight]

    Determines whether individual transformations are small enough
    for predictable composition via Campbell-Baker-Hausdorff.

    Args:
        pose1: First SE(3) transformation
        pose2: Second SE(3) transformation

    Returns:
        Dictionary with accuracy metrics and recommendations
    """
    # Extract rotation magnitudes
    rot1_angle = np.linalg.norm(pose1.to_rotation_vector())
    rot2_angle = np.linalg.norm(pose2.to_rotation_vector())

    # CBH works well for small rotations (< π/4 ≈ 0.785)
    threshold = np.pi / 4

    rot1_small = rot1_angle < threshold
    rot2_small = rot2_angle < threshold
    composition_predictable = rot1_small and rot2_small

    # Estimate commutator magnitude (interaction term)
    # For so(3), [X,Y] measures non-commutativity
    X = skew_symmetric(pose1.to_rotation_vector())
    Y = skew_symmetric(pose2.to_rotation_vector())
    commutator = X @ Y - Y @ X
    interaction_strength = np.linalg.norm(commutator, 'fro')

    return {
        'rot1_angle_rad': rot1_angle,
        'rot2_angle_rad': rot2_angle,
        'rot1_small': rot1_small,
        'rot2_small': rot2_small,
        'composition_predictable': composition_predictable,
        'interaction_strength': interaction_strength,
        'cbh_order_needed': 1 if interaction_strength < 0.01 else 2
    }


def skew_symmetric(v: np.ndarray) -> np.ndarray:
    """
    Convert 3D vector to skew-symmetric matrix (so(3) Lie algebra element).

    [v]× = [  0  -v3   v2 ]
           [ v3    0  -v1 ]
           [-v2   v1    0 ]

    Args:
        v: 3D vector

    Returns:
        3x3 skew-symmetric matrix
    """
    return np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])


def unskew_symmetric(M: np.ndarray) -> np.ndarray:
    """
    Convert skew-symmetric matrix to 3D vector.

    Args:
        M: 3x3 skew-symmetric matrix

    Returns:
        3D vector
    """
    return np.array([M[2, 1], M[0, 2], M[1, 0]])
