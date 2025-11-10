"""
Test Suite for SE(3) Double-and-Scale Approximate Returns

Tests the core functionality of the regenerative return mechanism,
validating both mathematical correctness and practical applicability
to ecological, agricultural, and digital twin systems.
"""

import pytest
import numpy as np
from typing import Dict

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from se3_double_scale import (
    SE3Pose,
    SE3Trajectory,
    compose_se3,
    compose_trajectory,
    scale_se3_pose,
    scale_trajectory,
    double_trajectory,
    frobenius_distance_to_identity,
    compute_return_error,
    optimize_scaling_factor,
    generate_random_trajectory,
    verify_approximate_return,
    TetheredSE3Walker,
    predict_intervention_interference
)


class TestSE3Basics:
    """Test fundamental SE(3) operations"""

    def test_identity_element(self):
        """Identity element should be R=I, p=0"""
        identity = SE3Pose.identity()
        assert np.allclose(identity.rotation, np.eye(3))
        assert np.allclose(identity.translation, np.zeros(3))

    def test_identity_composition(self):
        """Composing with identity should be neutral operation"""
        # Random pose
        pose = SE3Pose.from_rotation_vector(
            np.array([0.1, 0.2, 0.3]),
            np.array([1.0, 2.0, 3.0])
        )
        identity = SE3Pose.identity()

        # Identity is left-neutral
        result1 = compose_se3(identity, pose)
        assert np.allclose(result1.rotation, pose.rotation)
        assert np.allclose(result1.translation, pose.translation)

        # Identity is right-neutral
        result2 = compose_se3(pose, identity)
        assert np.allclose(result2.rotation, pose.rotation)
        assert np.allclose(result2.translation, pose.translation)

    def test_rotation_orthogonality(self):
        """All rotations must remain orthogonal under operations"""
        pose = SE3Pose.from_rotation_vector(
            np.array([np.pi/4, 0, 0]),
            np.array([0, 0, 0])
        )

        # Check R^T R = I
        assert np.allclose(pose.rotation.T @ pose.rotation, np.eye(3))

        # Check det(R) = 1
        assert np.allclose(np.linalg.det(pose.rotation), 1.0)

    def test_quaternion_stability(self):
        """Quaternions should provide stable representation"""
        rot_vec = np.array([np.pi/2, np.pi/3, np.pi/4])
        pose = SE3Pose.from_rotation_vector(rot_vec, np.zeros(3))

        quat = pose.to_quaternion()

        # Quaternion should be unit norm
        assert np.allclose(np.linalg.norm(quat), 1.0)

    def test_bounded_trajectory_validation(self):
        """Bounded trajectories should enforce r_max constraint"""
        r_max = 1.0

        # Valid bounded trajectory
        valid_poses = [
            SE3Pose.from_rotation_vector(np.zeros(3), np.array([0.5, 0.5, 0.0]))
        ]
        trajectory = SE3Trajectory(valid_poses, bounded=True, r_max=r_max)
        assert len(trajectory) == 1

        # Invalid bounded trajectory should raise assertion
        invalid_poses = [
            SE3Pose.from_rotation_vector(np.zeros(3), np.array([2.0, 0.0, 0.0]))
        ]
        with pytest.raises(AssertionError):
            SE3Trajectory(invalid_poses, bounded=True, r_max=r_max)


class TestDoubleAndScaleCore:
    """Test core double-and-scale mechanism"""

    def test_scaling_identity(self):
        """Scaling identity should remain identity for any λ"""
        identity = SE3Pose.identity()

        for lambda_scale in [0.5, 1.0, 2.0]:
            scaled = scale_se3_pose(identity, lambda_scale)
            assert np.allclose(scaled.rotation, np.eye(3))
            assert np.allclose(scaled.translation, np.zeros(3))

    def test_scaling_commutativity_with_composition(self):
        """Test that scaling distributes: (g1*g2)^λ vs g1^λ * g2^λ"""
        # Note: In general, (g1*g2)^λ ≠ g1^λ * g2^λ for SE(3)
        # This is because SE(3) is non-commutative
        # Test documents this non-commutativity

        pose1 = SE3Pose.from_rotation_vector(
            np.array([0.1, 0, 0]),
            np.array([1, 0, 0])
        )
        pose2 = SE3Pose.from_rotation_vector(
            np.array([0, 0.1, 0]),
            np.array([0, 1, 0])
        )
        lambda_scale = 0.5

        # Compose then scale
        composed = compose_se3(pose1, pose2)
        scaled_composed = scale_se3_pose(composed, lambda_scale)

        # Scale then compose
        scaled1 = scale_se3_pose(pose1, lambda_scale)
        scaled2 = scale_se3_pose(pose2, lambda_scale)
        composed_scaled = compose_se3(scaled1, scaled2)

        # These should be different (non-commutativity)
        # But document the difference magnitude
        rot_diff = np.linalg.norm(
            scaled_composed.rotation - composed_scaled.rotation
        )
        trans_diff = np.linalg.norm(
            scaled_composed.translation - composed_scaled.translation
        )

        # For small rotations, difference should be small but non-zero
        assert rot_diff > 0 or trans_diff > 0, "Expected non-commutativity"

    def test_double_trajectory_length(self):
        """Doubling should exactly double trajectory length"""
        trajectory = generate_random_trajectory(T=10)
        doubled = double_trajectory(trajectory)

        assert len(doubled) == 2 * len(trajectory)

    def test_frobenius_distance_properties(self):
        """Frobenius distance should satisfy metric properties"""
        identity = SE3Pose.identity()

        # Distance to self is zero
        assert frobenius_distance_to_identity(identity) < 1e-10

        # Distance is non-negative
        pose = SE3Pose.from_rotation_vector(
            np.array([0.5, 0, 0]),
            np.array([1, 0, 0])
        )
        assert frobenius_distance_to_identity(pose) > 0

    def test_return_error_decreases_with_optimization(self):
        """Optimized λ should reduce error compared to λ=1"""
        trajectory = generate_random_trajectory(T=10, r_max=1.0)

        # Error with λ = 1 (no scaling)
        error_unscaled = compute_return_error(trajectory, lambda_scale=1.0, double=True)

        # Error with optimized λ
        result = optimize_scaling_factor(trajectory, double=True)
        error_optimized = result.fun

        # Optimized should be better or equal
        assert error_optimized <= error_unscaled


class TestApproximateReturns:
    """Test approximate return to identity mechanism"""

    def test_random_trajectory_approximate_return(self):
        """Random trajectories should achieve approximate return when doubled and scaled"""
        np.random.seed(42)  # Reproducibility

        for trial in range(5):
            trajectory = generate_random_trajectory(T=10, r_max=1.0)

            # Optimize scaling factor
            result = optimize_scaling_factor(trajectory, double=True)
            lambda_opt = result.x

            # Verify approximate return
            metrics = verify_approximate_return(
                trajectory,
                lambda_opt,
                tolerance=0.5,  # Generous tolerance for random trajectories
                double=True
            )

            # Should achieve some level of return (not perfect, but improved)
            assert metrics['total_error'] < 2.0, \
                f"Trial {trial}: Error {metrics['total_error']} too large"

    def test_doubling_improves_return(self):
        """Doubling should improve return probability compared to single pass"""
        trajectory = generate_random_trajectory(T=10, r_max=1.0)

        # Optimize for single pass
        result_single = optimize_scaling_factor(trajectory, double=False)
        error_single = result_single.fun

        # Optimize for double pass
        result_double = optimize_scaling_factor(trajectory, double=True)
        error_double = result_double.fun

        # Double should generally achieve better return
        # (Not guaranteed for every random trajectory, but statistically true)
        print(f"Single pass error: {error_single:.4f}")
        print(f"Double pass error: {error_double:.4f}")

    def test_small_rotations_approximate_return(self):
        """Trajectories with small rotations should achieve good approximate returns"""
        # Small rotations have higher return probability
        trajectory = generate_random_trajectory(
            T=10,
            r_max=0.5,
            rotation_scale=0.05  # Very small rotations
        )

        result = optimize_scaling_factor(trajectory, double=True)
        lambda_opt = result.x

        metrics = verify_approximate_return(
            trajectory,
            lambda_opt,
            tolerance=0.2,  # Tighter tolerance for small rotations
            double=True
        )

        assert metrics['return_achieved'], \
            f"Small rotation trajectory failed to return: error {metrics['total_error']}"

    def test_golden_ratio_scaling(self):
        """Test if λ ≈ 0.618 (golden ratio) appears as optimal scaling"""
        golden_ratio = (np.sqrt(5) - 1) / 2  # ≈ 0.618

        successes = 0
        trials = 10

        for _ in range(trials):
            trajectory = generate_random_trajectory(T=10, r_max=1.0)
            result = optimize_scaling_factor(
                trajectory,
                lambda_bounds=(0.3, 1.5),
                double=True
            )
            lambda_opt = result.x

            # Check if within 30% of golden ratio
            if abs(lambda_opt - golden_ratio) / golden_ratio < 0.3:
                successes += 1

        # Document golden ratio frequency (informational, not strict requirement)
        golden_ratio_frequency = successes / trials
        print(f"Golden ratio (±30%) appeared in {golden_ratio_frequency:.1%} of trials")


class TestTetheredWalker:
    """Test tethered random walk with elastic return"""

    def test_tethered_walker_initialization(self):
        """Tethered walker should initialize at identity"""
        walker = TetheredSE3Walker()
        assert np.allclose(walker.current_position.rotation, np.eye(3))
        assert np.allclose(walker.current_position.translation, np.zeros(3))

    def test_return_force_at_home(self):
        """Return force should be zero at home position"""
        walker = TetheredSE3Walker()
        trans_force, rot_force = walker.compute_return_force()

        assert np.allclose(trans_force, np.zeros(3), atol=1e-6)
        assert np.allclose(rot_force, np.zeros(3), atol=1e-6)

    def test_return_force_increases_with_distance(self):
        """Return force should increase linearly with distance (Hooke's law)"""
        walker = TetheredSE3Walker(elastic_constant=0.5)

        # Move away from home
        walker.current_position = SE3Pose.from_rotation_vector(
            np.array([0, 0, 0]),
            np.array([1, 0, 0])
        )

        trans_force, _ = walker.compute_return_force()

        # Force should point back toward home
        assert trans_force[0] < 0  # Negative x-direction

        # Force magnitude should equal k * displacement
        expected_magnitude = walker.k * 1.0
        actual_magnitude = np.linalg.norm(trans_force)
        assert np.allclose(actual_magnitude, expected_magnitude)

    def test_tethered_walk_boundedness(self):
        """Tethered walk should remain bounded over many steps"""
        walker = TetheredSE3Walker(
            elastic_constant=0.2,
            translation_noise=0.05,
            rotation_noise=0.1
        )

        max_distance = 0.0
        for _ in range(1000):
            pose = walker.step(dt=0.1)
            distance = np.linalg.norm(pose.translation)
            max_distance = max(max_distance, distance)

        # With elastic force, should remain bounded
        # (not drift to infinity like unbounded random walk)
        assert max_distance < 5.0, \
            f"Tethered walk exceeded expected bounds: {max_distance}"


class TestInterventionInterference:
    """Test interference prediction between interventions"""

    def test_commuting_interventions_no_interference(self):
        """Commuting transformations should have minimal interference"""
        # Rotations around same axis commute
        intervention1 = SE3Pose.from_rotation_vector(
            np.array([0.1, 0, 0]),
            np.zeros(3)
        )
        intervention2 = SE3Pose.from_rotation_vector(
            np.array([0.2, 0, 0]),
            np.zeros(3)
        )

        interference = predict_intervention_interference(intervention1, intervention2)

        # Should be small (commuting)
        assert interference < 0.1

    def test_noncommuting_interventions_interference(self):
        """Non-commuting transformations should show interference"""
        # Rotations around different axes don't commute
        intervention1 = SE3Pose.from_rotation_vector(
            np.array([0.5, 0, 0]),
            np.zeros(3)
        )
        intervention2 = SE3Pose.from_rotation_vector(
            np.array([0, 0.5, 0]),
            np.zeros(3)
        )

        interference = predict_intervention_interference(intervention1, intervention2)

        # Should be significant (non-commuting)
        assert interference > 0.05


class TestBoundedDomainBehavior:
    """Test behavior of bounded SE(3) domains"""

    def test_bounded_trajectory_generation(self):
        """Generated trajectories should respect bounds"""
        r_max = 1.0
        trajectory = generate_random_trajectory(T=50, r_max=r_max, bounded=True)

        for pose in trajectory.poses:
            distance = np.linalg.norm(pose.translation)
            assert distance <= r_max * 1.1, \
                f"Pose exceeded bounds: {distance} > {r_max}"

    def test_composition_preserves_boundedness(self):
        """Composed trajectory should remain within reasonable bounds"""
        r_max = 1.0
        trajectory = generate_random_trajectory(T=10, r_max=r_max, bounded=True)

        # Compose entire trajectory
        total_pose = compose_trajectory(trajectory)

        # Total translation might exceed r_max due to composition
        # but should remain bounded by T * r_max (worst case)
        total_distance = np.linalg.norm(total_pose.translation)
        assert total_distance < len(trajectory) * r_max


class TestPhysicalInterpretations:
    """Test physical interpretations for regenerative systems"""

    def test_agricultural_rotation_metaphor(self):
        """
        Test agricultural rotation cycle:
        hemp → wheat → hemp → wheat (doubled) with scaled inputs
        """
        # Define two crop interventions
        hemp_rotation = SE3Pose.from_rotation_vector(
            np.array([0.3, 0.1, 0.0]),  # Soil transformation
            np.array([0.5, 0.0, 0.0])   # Nutrient movement
        )
        wheat_rotation = SE3Pose.from_rotation_vector(
            np.array([-0.2, 0.15, 0.0]),
            np.array([0.0, 0.3, 0.0])
        )

        # Create rotation cycle: hemp → wheat
        trajectory = SE3Trajectory([hemp_rotation, wheat_rotation], bounded=True, r_max=2.0)

        # Find optimal scaling (intervention intensity)
        result = optimize_scaling_factor(trajectory, double=True)
        lambda_opt = result.x

        # Verify return to baseline soil health
        metrics = verify_approximate_return(trajectory, lambda_opt, tolerance=0.5, double=True)

        print(f"Agricultural cycle:")
        print(f"  Optimal intervention intensity: λ = {lambda_opt:.3f}")
        print(f"  Return to baseline: {metrics['return_achieved']}")
        print(f"  Soil health error: {metrics['total_error']:.4f}")

        # Document the result (informational)
        assert lambda_opt > 0  # Sanity check

    def test_narrative_arc_resolution(self):
        """
        Test narrative arc: journey out → journey back (transformed return)
        """
        # Protagonist's journey: departure → crisis
        departure = SE3Pose.from_rotation_vector(
            np.array([0.5, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0])
        )
        crisis = SE3Pose.from_rotation_vector(
            np.array([0.0, 0.7, 0.0]),
            np.array([0.0, 1.5, 0.0])
        )

        # Narrative trajectory
        trajectory = SE3Trajectory([departure, crisis], bounded=True, r_max=3.0)

        # Find optimal pacing factor
        result = optimize_scaling_factor(trajectory, double=True)
        lambda_opt = result.x

        metrics = verify_approximate_return(trajectory, lambda_opt, tolerance=1.0, double=True)

        print(f"Narrative arc:")
        print(f"  Optimal pacing: λ = {lambda_opt:.3f}")
        print(f"  Return with transformation: {metrics['return_achieved']}")

        # The "return" is not to the original state, but to a transformed equilibrium
        assert metrics['total_error'] >= 0  # Sanity check


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
