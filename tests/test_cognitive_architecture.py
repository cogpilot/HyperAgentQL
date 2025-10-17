"""
Test suite for HyperAgentQL Cognitive Architecture
"""

import pytest
import numpy as np
from typing import Dict, Any

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hyperagentql.cognitive_architecture import CognitiveArchitecture, ArchitectureMode
from hyperagentql.hopf_fibrations import HopfFibrations
from hyperagentql.toroidal_core import ToroidalCore
from hyperagentql.recursive_inference import RecursiveInference, RecursionLevel
from hyperagentql.autogenesis import AutogenesisBootstrapper, BootstrapPhase


class TestHopfFibrations:
    """Test the Hopf fibrations implementation."""
    
    def test_initialization(self):
        """Test that Hopf fibrations initialize correctly."""
        hopf = HopfFibrations()
        
        assert len(hopf.tiers) == 4
        assert 1 in hopf.tiers
        assert 4 in hopf.tiers
        
        # Check tier dimensions
        assert hopf.tiers[1]['dimensions'] == [0, 1, 2, 3]
        assert hopf.tiers[4]['dimensions'] == [12, 13, 14, 15]
    
    def test_coordinate_generation(self):
        """Test coordinate generation for different spheres."""
        hopf = HopfFibrations()
        
        # Test S^3 coordinates
        s3_params = np.array([0.5, 1.0, 1.5])
        s3_coords = hopf._s3_coordinates(s3_params)
        assert len(s3_coords) == 4
        assert abs(np.linalg.norm(s3_coords) - 1.0) < 1e-10  # Unit sphere
        
        # Test S^7 coordinates
        s7_params = np.random.rand(7) * 2 * np.pi
        s7_coords = hopf._s7_coordinates(s7_params)
        assert len(s7_coords) == 8
        assert abs(np.linalg.norm(s7_coords) - 1.0) < 1e-10
    
    def test_fibration_maps(self):
        """Test the fibration maps between tiers."""
        hopf = HopfFibrations()
        
        # Create a unit S^3 point
        s3_point = np.array([1, 0, 0, 0])
        
        # Test projection through tiers
        s7_point = hopf.project_through_tiers(s3_point, 2)
        assert len(s7_point) == 8
        assert abs(np.linalg.norm(s7_point) - 1.0) < 1e-10
        
        s15_point = hopf.project_through_tiers(s3_point, 4)
        assert len(s15_point) == 16
        assert abs(np.linalg.norm(s15_point) - 1.0) < 1e-10
    
    def test_curvature_computation(self):
        """Test curvature computation."""
        hopf = HopfFibrations()
        
        point = np.random.randn(8)
        curvature = hopf.compute_curvature(2, point)
        
        assert isinstance(curvature, float)
        assert curvature > 0


class TestToroidalCore:
    """Test the toroidal core implementation."""
    
    def test_initialization(self):
        """Test toroidal core initialization."""
        torus = ToroidalCore(major_radius=2.0, minor_radius=1.0, resolution=32)
        
        assert torus.major_radius == 2.0
        assert torus.minor_radius == 1.0
        assert torus.resolution == 32
        
        # Check coordinate system
        assert 'x' in torus.coordinate_system
        assert 'y' in torus.coordinate_system
        assert 'z' in torus.coordinate_system
        
        # Check dimensions
        assert torus.coordinate_system['x'].shape == (32, 32)
    
    def test_topology_graph(self):
        """Test topology graph creation."""
        torus = ToroidalCore(resolution=8)
        
        assert torus.topology_graph.number_of_nodes() == 64  # 8x8
        assert torus.topology_graph.number_of_edges() > 0
        
        # Check toroidal connectivity
        for node in torus.topology_graph.nodes():
            neighbors = list(torus.topology_graph.neighbors(node))
            assert len(neighbors) >= 2  # At least u and v direction neighbors
    
    def test_flow_field(self):
        """Test flow field initialization."""
        torus = ToroidalCore(resolution=16)
        
        assert 'u_component' in torus.flow_field
        assert 'v_component' in torus.flow_field
        assert 'magnitude' in torus.flow_field
        
        # Check dimensions
        assert torus.flow_field['u_component'].shape == (16, 16)
        assert torus.flow_field['magnitude'].shape == (16, 16)
    
    def test_information_flow(self):
        """Test information flow computation."""
        torus = ToroidalCore(resolution=16)
        
        # Create test state
        state = np.random.randn(16, 16) * 0.5
        
        info_flow = torus.compute_information_flow(state)
        
        assert 'flow_u' in info_flow
        assert 'flow_v' in info_flow
        assert 'divergence' in info_flow
        assert 'curl' in info_flow
        
        # Check dimensions
        assert info_flow['flow_u'].shape == (16, 16)
        assert info_flow['divergence'].shape == (16, 16)


class TestRecursiveInference:
    """Test the recursive inference engine."""
    
    def test_initialization(self):
        """Test recursive inference initialization."""
        inference = RecursiveInference(input_dim=64)
        
        assert inference.input_dim == 64
        assert hasattr(inference, 'micro_recursion')
        assert hasattr(inference, 'macro_recursion')
        assert hasattr(inference, 'meta_recursion')
    
    def test_inference_execution(self):
        """Test inference execution."""
        inference = RecursiveInference(input_dim=32)
        
        # Create test input
        input_data = np.random.randn(32) * 0.5
        
        # Run inference
        result = inference.infer(input_data)
        
        assert 'final_output' in result
        assert 'micro_result' in result
        assert 'macro_result' in result
        assert 'meta_result' in result
        assert 'confidence' in result
        assert 'recursion_depths' in result
        
        # Check output dimensions
        assert len(result['final_output']) == 32
        assert isinstance(result['confidence'], float)
    
    def test_recursion_depth_tracking(self):
        """Test that recursion depths are tracked correctly."""
        inference = RecursiveInference(input_dim=16)
        
        input_data = np.random.randn(16) * 0.3
        result = inference.infer(input_data)
        
        depths = result['recursion_depths']
        assert 'micro' in depths
        assert 'macro' in depths
        assert 'meta' in depths
        
        # All depths should be non-negative
        for depth in depths.values():
            assert depth >= 0
    
    def test_inference_summary(self):
        """Test inference summary generation."""
        inference = RecursiveInference(input_dim=24)
        
        # Run a few inferences
        for _ in range(3):
            input_data = np.random.randn(24) * 0.4
            inference.infer(input_data)
        
        summary = inference.get_inference_summary()
        
        assert 'total_inferences' in summary
        assert summary['total_inferences'] == 3
        assert 'micro_config' in summary
        assert 'macro_config' in summary
        assert 'meta_config' in summary


class TestAutogenesisBootstrapper:
    """Test the autogenesis bootstrapper."""
    
    def test_initialization(self):
        """Test bootstrapper initialization."""
        bootstrapper = AutogenesisBootstrapper(num_modules=4, base_dim=32)
        
        assert bootstrapper.num_modules == 4
        assert bootstrapper.base_dim == 32
        assert len(bootstrapper.modules) == 4
        assert bootstrapper.current_state.phase == BootstrapPhase.INITIALIZATION
    
    def test_bootstrap_step(self):
        """Test single bootstrap step."""
        bootstrapper = AutogenesisBootstrapper(num_modules=3, base_dim=16)
        
        # Create test input
        input_signal = np.random.randn(16) * 0.5
        
        # Run bootstrap step
        state = bootstrapper.bootstrap_step(input_signal)
        
        assert state.iteration == 1
        assert isinstance(state.complexity, float)
        assert isinstance(state.stability, float)
        assert isinstance(state.energy, float)
        assert state.complexity >= 0
        assert 0 <= state.stability <= 1
    
    def test_bootstrap_progression(self):
        """Test that bootstrap progresses through phases."""
        bootstrapper = AutogenesisBootstrapper(num_modules=3, base_dim=16)
        
        initial_phase = bootstrapper.current_state.phase
        
        # Run multiple steps
        for _ in range(20):
            input_signal = np.random.randn(16) * 0.3
            bootstrapper.bootstrap_step(input_signal)
        
        # Should have made some progress
        assert bootstrapper.current_state.iteration == 20
        final_complexity = bootstrapper.current_state.complexity
        assert final_complexity >= 0
    
    def test_bootstrap_summary(self):
        """Test bootstrap summary generation."""
        bootstrapper = AutogenesisBootstrapper(num_modules=2, base_dim=12)
        
        # Run a few steps
        for _ in range(5):
            input_signal = np.random.randn(12) * 0.2
            bootstrapper.bootstrap_step(input_signal)
        
        summary = bootstrapper.get_bootstrap_summary()
        
        assert 'current_phase' in summary
        assert 'iterations' in summary
        assert 'complexity' in summary
        assert 'stability' in summary
        assert summary['iterations'] == 5


class TestCognitiveArchitecture:
    """Test the main cognitive architecture."""
    
    def test_initialization(self):
        """Test cognitive architecture initialization."""
        arch = CognitiveArchitecture(
            base_dimension=32,
            toroidal_resolution=16,
            num_bootstrap_modules=3
        )
        
        assert arch.base_dimension == 32
        assert arch.toroidal_resolution == 16
        assert arch.num_bootstrap_modules == 3
        
        assert hasattr(arch, 'toroidal_core')
        assert hasattr(arch, 'hopf_fibrations')
        assert hasattr(arch, 'recursive_inference')
        assert hasattr(arch, 'autogenesis_bootstrapper')
        
        assert arch.current_state.mode == ArchitectureMode.BOOTSTRAP
    
    def test_bootstrap_architecture(self):
        """Test architecture bootstrapping."""
        arch = CognitiveArchitecture(
            base_dimension=16,
            toroidal_resolution=8,
            num_bootstrap_modules=2
        )
        
        # Run bootstrap
        result = arch.bootstrap_architecture(num_bootstrap_steps=10)
        
        assert 'bootstrap_completed' in result
        assert result['bootstrap_completed'] is True
        assert 'final_phase' in result
        assert 'steps_completed' in result
        assert 'final_complexity' in result
        assert 'final_stability' in result
        
        # Architecture should now be in inference mode
        assert arch.current_state.mode == ArchitectureMode.INFERENCE
    
    def test_inference_execution(self):
        """Test inference execution."""
        arch = CognitiveArchitecture(
            base_dimension=24,
            toroidal_resolution=8,
            num_bootstrap_modules=2
        )
        
        # Quick bootstrap
        arch.bootstrap_architecture(num_bootstrap_steps=5)
        
        # Create test input
        input_data = np.random.randn(24) * 0.4
        
        # Run inference
        result = arch.infer(input_data)
        
        assert 'primary_output' in result
        assert 'inference_details' in result
        assert 'toroidal_state' in result
        assert 'hopf_projections' in result
        assert 'architecture_metrics' in result
        assert 'component_contributions' in result
        
        # Check output dimensions
        assert len(result['primary_output']) == 24
        
        # Check metrics
        metrics = result['architecture_metrics']
        assert 'global_coherence' in metrics
        assert 'emergence_level' in metrics
        assert 'mode' in metrics
    
    def test_architecture_summary(self):
        """Test architecture summary generation."""
        arch = CognitiveArchitecture(
            base_dimension=20,
            toroidal_resolution=8,
            num_bootstrap_modules=2
        )
        
        summary = arch.get_architecture_summary()
        
        assert 'architecture_info' in summary
        assert 'current_state' in summary
        assert 'component_status' in summary
        assert 'performance_metrics' in summary
        assert 'emergence_tracking' in summary
        assert 'integration_weights' in summary
        
        # Check architecture info
        arch_info = summary['architecture_info']
        assert arch_info['base_dimension'] == 20
        assert arch_info['toroidal_resolution'] == 8
        assert arch_info['num_bootstrap_modules'] == 2
    
    def test_architecture_reset(self):
        """Test architecture reset functionality."""
        arch = CognitiveArchitecture(
            base_dimension=16,
            toroidal_resolution=8,
            num_bootstrap_modules=2
        )
        
        # Run some operations
        arch.bootstrap_architecture(num_bootstrap_steps=5)
        input_data = np.random.randn(16) * 0.3
        arch.infer(input_data)
        
        # Check that history exists
        assert len(arch.state_history) > 0
        
        # Reset
        arch.reset_architecture()
        
        # Check reset state
        assert arch.current_state.mode == ArchitectureMode.BOOTSTRAP
        assert arch.current_state.iteration == 0
        assert len(arch.state_history) == 0
        assert len(arch.emergence_tracking['patterns_detected']) == 0


class TestIntegration:
    """Test integration between components."""
    
    def test_component_interaction(self):
        """Test that components interact properly."""
        arch = CognitiveArchitecture(
            base_dimension=32,
            toroidal_resolution=8,
            num_bootstrap_modules=3
        )
        
        # Bootstrap
        bootstrap_result = arch.bootstrap_architecture(num_bootstrap_steps=10)
        assert bootstrap_result['bootstrap_completed']
        
        # Run inference with all components
        input_data = np.random.randn(32) * 0.5
        result = arch.infer(
            input_data,
            use_toroidal_modulation=True,
            use_hopf_projection=True
        )
        
        # Check that all components contributed
        contrib = result['component_contributions']
        assert contrib['toroidal_contribution'] >= 0
        assert contrib['hopf_contribution'] >= 0
        assert contrib['bootstrap_contribution'] >= 0
        
        # Check that toroidal state evolved
        assert np.any(arch.current_state.toroidal_state != 0)
        
        # Check that Hopf projections exist
        assert len(arch.current_state.hopf_projections) > 0
    
    def test_emergence_tracking(self):
        """Test that emergence is tracked across components."""
        arch = CognitiveArchitecture(
            base_dimension=24,
            toroidal_resolution=8,
            num_bootstrap_modules=2
        )
        
        # Bootstrap and run multiple inferences
        arch.bootstrap_architecture(num_bootstrap_steps=20)
        
        for i in range(5):
            input_data = np.random.randn(24) * 0.3
            result = arch.infer(input_data)
        
        # Check emergence tracking
        assert len(arch.emergence_tracking['coherence_history']) > 0
        assert len(arch.emergence_tracking['complexity_evolution']) > 0
        
        # Check that metrics are reasonable
        final_coherence = arch.current_state.global_coherence
        final_emergence = arch.current_state.emergence_level
        
        assert 0 <= final_coherence <= 1
        assert final_emergence >= 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])