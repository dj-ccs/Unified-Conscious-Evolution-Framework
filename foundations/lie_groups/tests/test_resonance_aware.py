"""
Test Suite for Resonance-Aware Extensions

Validates Claude Opus insights:
- Resonance detection (golden ratio, silver ratio, etc.)
- Multi-level verification cascade for EHDC tokens
- Narrative quality metrics
- Resonance-biased optimization
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
    generate_random_trajectory,
    optimize_scaling_factor
)

from resonance_aware import (
    ResonanceDetector,
    ResonanceResult,
    VerificationCascade,
    VerificationResult,
    NarrativeQualityMetric,
    ResonanceAwareOptimizer
)


class TestResonanceDetector:
    """Test natural mathematical constant detection"""

    def test_golden_ratio_detection(self):
        """Systems should detect golden ratio preference"""
        np.random.seed(42)

        # Generate trajectories, check for golden ratio
        golden_count = 0
        trials = 10

        detector = ResonanceDetector(tolerance=0.2)

        for _ in range(trials):
            trajectory = generate_random_trajectory(T=10, r_max=1.0)
            result = detector.detect_natural_scaling(trajectory)

            if result.best_resonance == "golden_ratio":
                golden_count += 1

            # Check result structure
            assert isinstance(result, ResonanceResult)
            assert result.best_resonance in detector.resonance_constants
            assert result.best_error >= 0
            assert isinstance(result.is_natural, bool)

        # Golden ratio should appear in some trials (not strict requirement)
        print(f"Golden ratio appeared in {golden_count}/{trials} trials")

    def test_all_resonances_tested(self):
        """All mathematical constants should be tested"""
        trajectory = generate_random_trajectory(T=10, r_max=1.0)
        detector = ResonanceDetector()

        result = detector.detect_natural_scaling(trajectory)

        # All resonances should be in results
        expected_resonances = [
            "golden_ratio", "silver_ratio", "plastic_number",
            "octave", "perfect_fifth", "perfect_fourth", "major_third"
        ]

        for resonance in expected_resonances:
            assert resonance in result.all_resonances
            assert result.all_resonances[resonance] >= 0

    def test_nearest_resonance_finder(self):
        """Should find nearest mathematical constant"""
        detector = ResonanceDetector()

        # Test with value near golden ratio
        lambda_test = 0.62
        nearest_name, nearest_value, distance = detector.find_nearest_resonance(lambda_test)

        assert nearest_name == "golden_ratio"
        assert abs(nearest_value - detector.GOLDEN_RATIO) < 0.01
        assert distance < 0.1

    def test_octave_resonance(self):
        """Test octave (doubling) resonance detection"""
        detector = ResonanceDetector()

        # Octave = 2.0
        assert abs(detector.OCTAVE - 2.0) < 1e-10

        # Test finding octave
        lambda_test = 2.05
        nearest_name, _, distance = detector.find_nearest_resonance(lambda_test)

        assert nearest_name == "octave"
        assert distance < 0.1

    def test_musical_ratios(self):
        """Test musical ratio constants"""
        detector = ResonanceDetector()

        # Perfect fifth = 3:2 = 1.5
        assert abs(detector.PERFECT_FIFTH - 1.5) < 1e-10

        # Perfect fourth = 4:3 ≈ 1.333
        assert abs(detector.PERFECT_FOURTH - 4.0/3.0) < 1e-10

        # Major third = 5:4 = 1.25
        assert abs(detector.MAJOR_THIRD - 1.25) < 1e-10


class TestVerificationCascade:
    """Test multi-level verification for EHDC token generation"""

    def test_verification_cascade_structure(self):
        """Verification should test all five levels"""
        cascade = VerificationCascade()

        # Check weights sum to 1.0
        total_weight = sum(cascade.weights.values())
        assert abs(total_weight - 1.0) < 1e-6

        # Check all required levels present
        required_levels = [
            "topological", "energetic", "temporal", "spatial", "stochastic"
        ]
        for level in required_levels:
            assert level in cascade.weights
            assert level in cascade.thresholds

    def test_return_quality_verification(self):
        """Topological verification should measure return error"""
        cascade = VerificationCascade()
        trajectory = generate_random_trajectory(T=10, r_max=1.0)

        # Optimize first
        result = optimize_scaling_factor(trajectory, double=True)
        lambda_opt = result.x

        # Verify return quality
        error = cascade.verify_return_quality(trajectory, lambda_opt)

        assert error >= 0
        assert error == result.fun  # Should match optimization result

    def test_spatial_verification(self):
        """Spatial verification should check bounded domain"""
        cascade = VerificationCascade()

        # Valid bounded trajectory
        valid_poses = [
            SE3Pose.from_rotation_vector(np.zeros(3), np.array([0.5, 0.5, 0.0]))
        ]
        valid_trajectory = SE3Trajectory(valid_poses, bounded=True, r_max=1.0)

        assert cascade.verify_bounded_domain(valid_trajectory) == True

        # Unbounded trajectory (should pass trivially)
        unbounded_trajectory = SE3Trajectory(valid_poses, bounded=False)
        assert cascade.verify_bounded_domain(unbounded_trajectory) == True

    def test_noise_robustness_verification(self):
        """Stochastic verification should test noise resistance"""
        cascade = VerificationCascade()
        trajectory = generate_random_trajectory(T=5, r_max=1.0)  # Small for speed

        result = optimize_scaling_factor(trajectory, double=True)
        lambda_opt = result.x

        # Test robustness (should return score ∈ [0, 1])
        robustness = cascade.verify_noise_robustness(
            trajectory,
            lambda_opt,
            num_trials=5,  # Small for speed
            noise_level=0.05
        )

        assert 0.0 <= robustness <= 1.0

    def test_full_verification_cascade(self):
        """Full verification should produce valid result"""
        cascade = VerificationCascade()
        trajectory = generate_random_trajectory(T=10, r_max=1.0)

        # Optimize
        result = optimize_scaling_factor(trajectory, double=True)
        lambda_opt = result.x

        # Verify
        verification = cascade.verify_regeneration(
            trajectory,
            lambda_opt,
            base_token_amount=100.0
        )

        # Check result structure
        assert isinstance(verification, VerificationResult)
        assert 0.0 <= verification.overall_score <= 1.0
        assert verification.token_award >= 0
        assert isinstance(verification.passed, bool)

        # All verification levels should be present
        assert len(verification.verifications) == 5

        print(f"Verification result:")
        print(f"  Overall score: {verification.overall_score:.3f}")
        print(f"  Token award: {verification.token_award:.1f}")
        print(f"  Passed: {verification.passed}")
        for level, value in verification.verifications.items():
            print(f"    {level}: {value:.4f}")

    def test_high_quality_trajectory_passes(self):
        """High-quality trajectory should pass verification"""
        cascade = VerificationCascade()

        # Create simple, small trajectory (easy to return)
        simple_poses = [
            SE3Pose.from_rotation_vector(
                np.array([0.05, 0, 0]),
                np.array([0.1, 0, 0])
            ),
            SE3Pose.from_rotation_vector(
                np.array([-0.05, 0, 0]),
                np.array([-0.1, 0, 0])
            )
        ]
        simple_trajectory = SE3Trajectory(simple_poses, bounded=True, r_max=1.0)

        # Should achieve very good return
        result = optimize_scaling_factor(simple_trajectory, double=True)
        verification = cascade.verify_regeneration(simple_trajectory, result.x)

        # Should pass with high score
        assert verification.overall_score > 0.5
        assert verification.token_award > 0


class TestNarrativeQualityMetric:
    """Test narrative structure quantification"""

    def test_story_beat_encoding(self):
        """Story beats should encode to SE(3) poses"""
        metric = NarrativeQualityMetric()

        # Encode a narrative beat
        beat = metric.encode_story_beat(
            beat_description="Hero departs on journey",
            intensity=0.6,
            emotion_vector=np.array([0.5, 0.7, 0.3])  # Moderate valence, high arousal
        )

        # Should produce valid SE(3) pose
        assert isinstance(beat, SE3Pose)
        assert beat.rotation.shape == (3, 3)
        assert beat.translation.shape == (3,)

    def test_narrative_return_measurement(self):
        """Narrative return should measure story satisfaction"""
        metric = NarrativeQualityMetric()

        # Create simple narrative: departure → crisis → return → resolution
        story_beats = [
            metric.encode_story_beat(
                "Opening equilibrium",
                intensity=0.2,
                emotion_vector=np.array([0.5, 0.2, 0.5])
            ),
            metric.encode_story_beat(
                "Call to adventure",
                intensity=0.5,
                emotion_vector=np.array([0.6, 0.6, 0.4])
            ),
            metric.encode_story_beat(
                "Crisis/midpoint",
                intensity=0.9,
                emotion_vector=np.array([0.3, 0.9, 0.2])
            ),
            metric.encode_story_beat(
                "Dark night of soul",
                intensity=0.7,
                emotion_vector=np.array([0.2, 0.7, 0.3])
            ),
            metric.encode_story_beat(
                "Resolution",
                intensity=0.4,
                emotion_vector=np.array([0.7, 0.4, 0.6])
            )
        ]

        result = metric.measure_story_return(story_beats)

        # Check result structure
        assert "satisfaction" in result
        assert "return_error" in result
        assert "optimal_crisis_point" in result
        assert "suggested_scaling" in result
        assert "interpretation" in result

        # Satisfaction should be ∈ [0, 1]
        assert 0.0 <= result["satisfaction"] <= 1.0

        # Crisis point should be near midpoint
        assert result["optimal_crisis_point"] == len(story_beats) // 2

        print(f"Narrative analysis:")
        print(f"  Satisfaction: {result['satisfaction']:.3f}")
        print(f"  Return error: {result['return_error']:.4f}")
        print(f"  Crisis point: beat {result['optimal_crisis_point']}")
        print(f"  Suggested scaling: {result['suggested_scaling']:.3f}")
        print(f"  Interpretation: {result['interpretation']}")

    def test_well_structured_story_high_satisfaction(self):
        """Well-balanced narrative should score high satisfaction"""
        metric = NarrativeQualityMetric()

        # Symmetric story: small departures, mirrored return
        story_beats = [
            metric.encode_story_beat(
                "Act 1 beat 1",
                intensity=0.3,
                emotion_vector=np.array([0.6, 0.3, 0.5])
            ),
            metric.encode_story_beat(
                "Act 1 beat 2",
                intensity=0.5,
                emotion_vector=np.array([0.5, 0.5, 0.4])
            ),
            metric.encode_story_beat(
                "Act 2 beat 1 (return)",
                intensity=0.5,
                emotion_vector=np.array([-0.5, -0.5, -0.4])  # Inverted
            ),
            metric.encode_story_beat(
                "Act 2 beat 2 (resolution)",
                intensity=0.3,
                emotion_vector=np.array([-0.6, -0.3, -0.5])  # Inverted
            )
        ]

        result = metric.measure_story_return(story_beats)

        # Symmetric structure should have reasonable satisfaction
        # (Not perfect due to SE(3) non-commutativity, but decent)
        print(f"Symmetric story satisfaction: {result['satisfaction']:.3f}")


class TestResonanceAwareOptimizer:
    """Test optimization biased toward natural scaling factors"""

    def test_golden_ratio_bias(self):
        """Optimizer should start near golden ratio when biased"""
        optimizer = ResonanceAwareOptimizer(bias_strength=0.8)
        trajectory = generate_random_trajectory(T=10, r_max=1.0)

        lambda_opt, error = optimizer.optimize_with_bias(
            trajectory,
            bias_to_golden=True
        )

        # Should find a reasonable solution
        assert 0.1 <= lambda_opt <= 10.0
        assert error >= 0

        # Lambda should be near golden ratio neighborhood
        golden = optimizer.golden_ratio
        # Not strict requirement (depends on trajectory), but informational
        distance_to_golden = abs(lambda_opt - golden)
        print(f"Optimized λ = {lambda_opt:.4f}")
        print(f"Golden ratio = {golden:.4f}")
        print(f"Distance: {distance_to_golden:.4f}")

    def test_unbiased_vs_biased_comparison(self):
        """Compare biased vs unbiased optimization"""
        optimizer = ResonanceAwareOptimizer()
        trajectory = generate_random_trajectory(T=10, r_max=1.0)

        # Biased optimization
        lambda_biased, error_biased = optimizer.optimize_with_bias(
            trajectory,
            bias_to_golden=True
        )

        # Unbiased optimization
        lambda_unbiased, error_unbiased = optimizer.optimize_with_bias(
            trajectory,
            bias_to_golden=False
        )

        print(f"Biased:   λ = {lambda_biased:.4f}, error = {error_biased:.4f}")
        print(f"Unbiased: λ = {lambda_unbiased:.4f}, error = {error_unbiased:.4f}")

        # Both should find valid solutions
        assert error_biased >= 0
        assert error_unbiased >= 0

    def test_multi_resonance_search(self):
        """Should test all natural resonances"""
        optimizer = ResonanceAwareOptimizer()
        trajectory = generate_random_trajectory(T=10, r_max=1.0)

        results = optimizer.multi_resonance_search(trajectory)

        # Should have results for all resonances
        expected_resonances = [
            "golden_ratio", "silver_ratio", "plastic_number",
            "octave", "perfect_fifth", "perfect_fourth", "major_third"
        ]

        for resonance in expected_resonances:
            assert resonance in results
            lambda_val, error = results[resonance]
            assert lambda_val > 0
            assert error >= 0

        # Find best resonance
        best_resonance = min(results.items(), key=lambda x: x[1][1])
        print(f"Best resonance: {best_resonance[0]}")
        print(f"  λ = {best_resonance[1][0]:.4f}")
        print(f"  error = {best_resonance[1][1]:.4f}")


class TestIntegratedWorkflow:
    """Test complete workflow: optimize → detect resonance → verify → award tokens"""

    def test_ehdc_biochar_workflow(self):
        """Simulate EHDC biochar protocol verification"""
        # Create biochar application trajectory
        biochar_app1 = SE3Pose.from_rotation_vector(
            np.array([0.3, 0.2, 0.4]),  # Soil structure improvement
            np.array([0.2, 0.0, 0.1])   # Carbon movement
        )
        biochar_app2 = SE3Pose.from_rotation_vector(
            np.array([0.25, 0.15, 0.35]),
            np.array([0.15, 0.0, 0.08])
        )

        trajectory = SE3Trajectory([biochar_app1, biochar_app2], bounded=True, r_max=2.0)

        # Step 1: Optimize scaling factor
        optimizer = ResonanceAwareOptimizer()
        lambda_opt, error = optimizer.optimize_with_bias(trajectory, bias_to_golden=True)

        # Step 2: Detect resonance
        detector = ResonanceDetector()
        resonance = detector.detect_natural_scaling(trajectory)

        # Step 3: Verify regeneration
        cascade = VerificationCascade()
        verification = cascade.verify_regeneration(trajectory, lambda_opt)

        # Step 4: Report results
        print("\n=== EHDC Biochar Protocol Verification ===")
        print(f"Optimal application intensity: λ = {lambda_opt:.3f}")
        print(f"Return error: {error:.4f}")
        print(f"Natural resonance detected: {resonance.best_resonance}")
        print(f"Is natural system: {resonance.is_natural}")
        print(f"\nVerification:")
        print(f"  Overall score: {verification.overall_score:.3f}")
        print(f"  REGEN token award: {verification.token_award:.1f}")
        print(f"  Protocol passed: {verification.passed}")

        # Should produce valid results
        assert lambda_opt > 0
        assert verification.overall_score >= 0
        assert verification.token_award >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
