"""
Cognitive Architecture for Dynamical Autogenesis

This is the main cognitive architecture that integrates all components:
- Toroidal Core for geometric foundation and feedback loops
- Hopf Fibrations for 4-tier mathematical structure (S^0 to S^15)
- Recursive Inference with 3 nested recursions
- Autogenesis Bootstrapper for self-organization

The architecture creates a powerful inference engine with self-organizing
capabilities and sophisticated mathematical foundations.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Union
import torch
import time
from dataclasses import dataclass
from enum import Enum

from .toroidal_core import ToroidalCore
from .hopf_fibrations import HopfFibrations
from .recursive_inference import RecursiveInference, InferenceState, RecursionLevel
from .autogenesis import AutogenesisBootstrapper, BootstrapPhase


class ArchitectureMode(Enum):
    """Operating modes of the cognitive architecture."""
    BOOTSTRAP = 1      # Bootstrapping and self-organization
    INFERENCE = 2      # Primary inference mode
    LEARNING = 3       # Learning and adaptation mode
    INTEGRATION = 4    # Integrated multi-modal operation


@dataclass
class CognitiveState:
    """Complete state of the cognitive architecture."""
    mode: ArchitectureMode
    toroidal_state: np.ndarray
    hopf_projections: Dict[int, np.ndarray]
    inference_result: Optional[Dict[str, Any]]
    bootstrap_state: Optional[Any]
    timestamp: float
    iteration: int
    global_coherence: float
    emergence_level: float


class CognitiveArchitecture:
    """
    Main cognitive architecture integrating all components for 
    dynamical autogenesis and advanced inference capabilities.
    """
    
    def __init__(self, 
                 base_dimension: int = 64,
                 toroidal_resolution: int = 32,
                 num_bootstrap_modules: int = 6):
        
        self.base_dimension = base_dimension
        self.toroidal_resolution = toroidal_resolution
        self.num_bootstrap_modules = num_bootstrap_modules
        
        # Initialize core components
        self.toroidal_core = ToroidalCore(
            major_radius=2.0, 
            minor_radius=1.0, 
            resolution=toroidal_resolution
        )
        
        self.hopf_fibrations = HopfFibrations()
        
        self.recursive_inference = RecursiveInference(input_dim=base_dimension)
        
        self.autogenesis_bootstrapper = AutogenesisBootstrapper(
            num_modules=num_bootstrap_modules,
            base_dim=base_dimension
        )
        
        # Architecture state
        self.current_state = CognitiveState(
            mode=ArchitectureMode.BOOTSTRAP,
            toroidal_state=np.random.randn(toroidal_resolution, toroidal_resolution) * 0.1,
            hopf_projections={},
            inference_result=None,
            bootstrap_state=None,
            timestamp=time.time(),
            iteration=0,
            global_coherence=0.0,
            emergence_level=0.0
        )
        
        # Integration parameters
        self.integration_weights = {
            'toroidal_influence': 0.3,
            'hopf_influence': 0.2,
            'recursive_influence': 0.4,
            'bootstrap_influence': 0.1
        }
        
        # History and tracking
        self.state_history = []
        self.performance_metrics = {}
        self.emergence_tracking = {
            'patterns_detected': [],
            'complexity_evolution': [],
            'coherence_history': []
        }
        
    def bootstrap_architecture(self, 
                             num_bootstrap_steps: int = 200,
                             external_inputs: Optional[List[np.ndarray]] = None) -> Dict[str, Any]:
        """
        Bootstrap the cognitive architecture through autogenesis.
        
        This is the first phase where the architecture self-organizes
        and develops its basic cognitive capabilities.
        """
        print("Starting cognitive architecture bootstrap...")
        
        self.current_state.mode = ArchitectureMode.BOOTSTRAP
        bootstrap_history = []
        
        for step in range(num_bootstrap_steps):
            self.current_state.iteration = step
            
            # Generate or use external input
            if external_inputs and step < len(external_inputs):
                input_signal = external_inputs[step]
            else:
                input_signal = self._generate_architecture_input()
            
            # Run bootstrap step with toroidal influence
            bootstrap_state = self.autogenesis_bootstrapper.bootstrap_step(input_signal)
            self.current_state.bootstrap_state = bootstrap_state
            
            # Evolve toroidal state based on bootstrap
            self._evolve_toroidal_state(input_signal, bootstrap_state)
            
            # Project through Hopf fibrations
            self._update_hopf_projections(input_signal)
            
            # Compute emergence metrics
            self._compute_emergence_metrics()
            
            # Store state
            bootstrap_history.append({
                'step': step,
                'bootstrap_phase': bootstrap_state.phase.name,
                'complexity': bootstrap_state.complexity,
                'stability': bootstrap_state.stability,
                'global_coherence': self.current_state.global_coherence,
                'emergence_level': self.current_state.emergence_level
            })
            
            # Progress indicators
            if step % 50 == 0:
                print(f"Bootstrap step {step}: Phase={bootstrap_state.phase.name}, "
                      f"Complexity={bootstrap_state.complexity:.3f}, "
                      f"Stability={bootstrap_state.stability:.3f}")
            
            # Check for bootstrap completion
            if (bootstrap_state.phase == BootstrapPhase.INTEGRATION and 
                bootstrap_state.stability > 0.8):
                print(f"Bootstrap completed at step {step}")
                break
        
        # Transition to inference mode
        self.current_state.mode = ArchitectureMode.INFERENCE
        
        return {
            'bootstrap_completed': True,
            'final_phase': self.current_state.bootstrap_state.phase.name,
            'steps_completed': len(bootstrap_history),
            'final_complexity': self.current_state.bootstrap_state.complexity,
            'final_stability': self.current_state.bootstrap_state.stability,
            'bootstrap_history': bootstrap_history
        }
    
    def infer(self, 
              input_data: np.ndarray, 
              context: Optional[Dict[str, Any]] = None,
              use_toroidal_modulation: bool = True,
              use_hopf_projection: bool = True) -> Dict[str, Any]:
        """
        Perform inference using the integrated cognitive architecture.
        
        This combines all components for sophisticated multi-level reasoning.
        """
        self.current_state.iteration += 1
        self.current_state.timestamp = time.time()
        
        # Ensure we're in inference mode
        if self.current_state.mode == ArchitectureMode.BOOTSTRAP:
            print("Warning: Architecture not bootstrapped. Running basic inference.")
        
        # Prepare input through various modalities
        processed_input = self._preprocess_input(input_data)
        
        # Toroidal modulation
        if use_toroidal_modulation:
            toroidal_influence = self._compute_toroidal_influence(processed_input)
            modulated_input = processed_input + toroidal_influence * self.integration_weights['toroidal_influence']
        else:
            modulated_input = processed_input
        
        # Hopf fibration projection
        if use_hopf_projection:
            hopf_enhanced_input = self._apply_hopf_enhancement(modulated_input)
        else:
            hopf_enhanced_input = modulated_input
        
        # Recursive inference
        inference_result = self.recursive_inference.infer(hopf_enhanced_input, context)
        self.current_state.inference_result = inference_result
        
        # Bootstrap influence (if available)
        if (self.current_state.bootstrap_state and 
            self.current_state.bootstrap_state.phase in [BootstrapPhase.INTEGRATION, BootstrapPhase.COMPLEXIFICATION]):
            bootstrap_influence = self._compute_bootstrap_influence(inference_result)
            enhanced_result = self._integrate_bootstrap_influence(inference_result, bootstrap_influence)
        else:
            enhanced_result = inference_result
        
        # Update architecture state
        self._update_architecture_state(enhanced_result)
        
        # Compute comprehensive result
        comprehensive_result = {
            'primary_output': enhanced_result['final_output'],
            'inference_details': enhanced_result,
            'toroidal_state': self.current_state.toroidal_state.copy(),
            'hopf_projections': self.current_state.hopf_projections.copy(),
            'architecture_metrics': {
                'global_coherence': self.current_state.global_coherence,
                'emergence_level': self.current_state.emergence_level,
                'mode': self.current_state.mode.name,
                'iteration': self.current_state.iteration
            },
            'component_contributions': {
                'toroidal_contribution': np.linalg.norm(toroidal_influence) if use_toroidal_modulation else 0,
                'hopf_contribution': self._compute_hopf_contribution(),
                'recursive_depth_used': enhanced_result.get('recursion_depths', {}),
                'bootstrap_contribution': self._compute_bootstrap_contribution() if self.current_state.bootstrap_state else 0
            }
        }
        
        # Store in history
        self.state_history.append(self.current_state)
        
        return comprehensive_result
    
    def _generate_architecture_input(self) -> np.ndarray:
        """Generate input for architecture during bootstrap."""
        # Multi-scale input that exercises different components
        base_signal = np.random.randn(self.base_dimension) * 0.5
        
        # Add structured components
        t = self.current_state.iteration * 0.1
        
        # Toroidal-inspired component
        toroidal_component = np.sin(np.arange(self.base_dimension) * t * 0.05)
        
        # Hopf-inspired component (quaternion-like)
        if self.base_dimension >= 4:
            hopf_component = np.zeros(self.base_dimension)
            hopf_component[:4] = [np.cos(t), np.sin(t), np.cos(2*t), np.sin(2*t)]
            hopf_component = np.tile(hopf_component[:4], self.base_dimension // 4 + 1)[:self.base_dimension]
        else:
            hopf_component = np.zeros(self.base_dimension)
        
        # Combine components
        combined = base_signal + 0.3 * toroidal_component + 0.2 * hopf_component
        
        return combined
    
    def _evolve_toroidal_state(self, input_signal: np.ndarray, bootstrap_state):
        """Evolve the toroidal state based on input and bootstrap state."""
        # Create input for toroidal evolution
        if len(input_signal) > self.toroidal_resolution * self.toroidal_resolution:
            toroidal_input = input_signal[:self.toroidal_resolution * self.toroidal_resolution].reshape(
                self.toroidal_resolution, self.toroidal_resolution)
        else:
            # Tile or pad input to match toroidal dimensions
            repeated = np.tile(input_signal, 
                             (self.toroidal_resolution * self.toroidal_resolution // len(input_signal)) + 1)
            toroidal_input = repeated[:self.toroidal_resolution * self.toroidal_resolution].reshape(
                self.toroidal_resolution, self.toroidal_resolution)
        
        # Evolve with bootstrap influence
        bootstrap_influence = bootstrap_state.complexity * 0.1 if bootstrap_state else 0
        
        # Simple evolution equation
        self.current_state.toroidal_state += (
            0.1 * toroidal_input + 
            0.05 * bootstrap_influence * np.sin(self.current_state.toroidal_state) +
            -0.02 * self.current_state.toroidal_state  # Damping
        )
        
        # Normalize to prevent explosion
        max_val = np.max(np.abs(self.current_state.toroidal_state))
        if max_val > 5.0:
            self.current_state.toroidal_state *= 5.0 / max_val
    
    def _update_hopf_projections(self, input_signal: np.ndarray):
        """Update projections through Hopf fibrations."""
        # Create S^3 point from input
        if len(input_signal) >= 4:
            s3_point = input_signal[:4]
        else:
            s3_point = np.pad(input_signal, (0, 4 - len(input_signal)))
        
        # Normalize to unit sphere
        s3_point = s3_point / (np.linalg.norm(s3_point) + 1e-8)
        
        # Project through all tiers
        for tier in range(1, 5):
            projected = self.hopf_fibrations.project_through_tiers(s3_point, tier)
            self.current_state.hopf_projections[tier] = projected
    
    def _compute_emergence_metrics(self):
        """Compute metrics for emergence and coherence."""
        # Global coherence: how well components work together
        coherence_factors = []
        
        # Toroidal coherence
        toroidal_variation = np.std(self.current_state.toroidal_state)
        toroidal_coherence = 1.0 / (1.0 + toroidal_variation)
        coherence_factors.append(toroidal_coherence)
        
        # Hopf coherence
        if self.current_state.hopf_projections:
            hopf_norms = [np.linalg.norm(proj) for proj in self.current_state.hopf_projections.values()]
            hopf_coherence = 1.0 - np.std(hopf_norms) / (np.mean(hopf_norms) + 1e-8)
            coherence_factors.append(hopf_coherence)
        
        # Bootstrap coherence
        if self.current_state.bootstrap_state:
            bootstrap_coherence = self.current_state.bootstrap_state.stability
            coherence_factors.append(bootstrap_coherence)
        
        self.current_state.global_coherence = np.mean(coherence_factors)
        
        # Emergence level: based on complexity and organization
        emergence_factors = []
        
        if self.current_state.bootstrap_state:
            emergence_factors.append(self.current_state.bootstrap_state.complexity / 10.0)
            emergence_factors.append(self.current_state.bootstrap_state.self_organization_score)
        
        if self.current_state.inference_result:
            inference_complexity = len(self.current_state.inference_result.get('recursion_depths', {}))
            emergence_factors.append(inference_complexity / 3.0)
        
        if emergence_factors:
            self.current_state.emergence_level = np.mean(emergence_factors)
        else:
            self.current_state.emergence_level = 0.0
        
        # Track emergence history
        self.emergence_tracking['coherence_history'].append(self.current_state.global_coherence)
        self.emergence_tracking['complexity_evolution'].append(self.current_state.emergence_level)
    
    def _preprocess_input(self, input_data: np.ndarray) -> np.ndarray:
        """Preprocess input for the architecture."""
        # Ensure consistent dimensions
        if len(input_data) > self.base_dimension:
            processed = input_data[:self.base_dimension]
        else:
            processed = np.pad(input_data, (0, self.base_dimension - len(input_data)))
        
        # Normalize
        norm = np.linalg.norm(processed)
        if norm > 0:
            processed = processed / norm
        
        return processed
    
    def _compute_toroidal_influence(self, input_data: np.ndarray) -> np.ndarray:
        """Compute influence from toroidal core."""
        # Project toroidal state to input dimensions
        flattened_toroidal = self.current_state.toroidal_state.flatten()
        
        if len(flattened_toroidal) > len(input_data):
            toroidal_projection = flattened_toroidal[:len(input_data)]
        else:
            toroidal_projection = np.tile(flattened_toroidal, 
                                        len(input_data) // len(flattened_toroidal) + 1)[:len(input_data)]
        
        # Compute information flow influence
        info_flow = self.toroidal_core.compute_information_flow(self.current_state.toroidal_state)
        flow_magnitude = info_flow['magnitude'].flatten()
        
        if len(flow_magnitude) > len(input_data):
            flow_influence = flow_magnitude[:len(input_data)]
        else:
            flow_influence = np.tile(flow_magnitude, 
                                   len(input_data) // len(flow_magnitude) + 1)[:len(input_data)]
        
        # Combine influences
        combined_influence = 0.6 * toroidal_projection + 0.4 * flow_influence
        
        return combined_influence * 0.1  # Scale down influence
    
    def _apply_hopf_enhancement(self, input_data: np.ndarray) -> np.ndarray:
        """Apply Hopf fibration enhancement to input."""
        enhanced = input_data.copy()
        
        # Apply influences from each tier
        for tier, projection in self.current_state.hopf_projections.items():
            if len(projection) > 0:
                # Project Hopf fibration onto input space
                if len(projection) > len(input_data):
                    hopf_influence = projection[:len(input_data)]
                else:
                    hopf_influence = np.tile(projection, 
                                           len(input_data) // len(projection) + 1)[:len(input_data)]
                
                # Weight by tier (higher tiers have more influence)
                tier_weight = tier * 0.05
                enhanced += hopf_influence * tier_weight * self.integration_weights['hopf_influence']
        
        return enhanced
    
    def _compute_bootstrap_influence(self, inference_result: Dict[str, Any]) -> np.ndarray:
        """Compute influence from bootstrap patterns."""
        if not self.current_state.bootstrap_state:
            return np.zeros(len(inference_result['final_output']))
        
        # Use autogenesis patterns to modulate inference
        bootstrap_summary = self.autogenesis_bootstrapper.get_bootstrap_summary()
        
        # Create influence based on bootstrap complexity and patterns
        complexity_factor = min(1.0, bootstrap_summary['complexity'] / 10.0)
        stability_factor = bootstrap_summary['stability']
        
        # Generate influence signal
        influence = np.random.randn(len(inference_result['final_output'])) * complexity_factor * stability_factor * 0.1
        
        return influence
    
    def _integrate_bootstrap_influence(self, inference_result: Dict[str, Any], 
                                     bootstrap_influence: np.ndarray) -> Dict[str, Any]:
        """Integrate bootstrap influence with inference result."""
        enhanced_result = inference_result.copy()
        
        # Enhance final output
        enhanced_result['final_output'] = (
            inference_result['final_output'] + 
            bootstrap_influence * self.integration_weights['bootstrap_influence']
        )
        
        # Add bootstrap metadata
        enhanced_result['bootstrap_integration'] = {
            'influence_magnitude': np.linalg.norm(bootstrap_influence),
            'bootstrap_phase': self.current_state.bootstrap_state.phase.name,
            'bootstrap_complexity': self.current_state.bootstrap_state.complexity
        }
        
        return enhanced_result
    
    def _update_architecture_state(self, inference_result: Dict[str, Any]):
        """Update the architecture state based on inference result."""
        # Update performance metrics
        self.performance_metrics['last_inference_confidence'] = inference_result.get('confidence', 0.0)
        self.performance_metrics['recursion_depth_usage'] = inference_result.get('recursion_depths', {})
        
        # Check for pattern emergence
        if 'global_context' in inference_result:
            context = inference_result['global_context']
            if context not in self.emergence_tracking['patterns_detected']:
                self.emergence_tracking['patterns_detected'].append(context)
    
    def _compute_hopf_contribution(self) -> float:
        """Compute the contribution of Hopf fibrations."""
        if not self.current_state.hopf_projections:
            return 0.0
        
        total_norm = sum(np.linalg.norm(proj) for proj in self.current_state.hopf_projections.values())
        return total_norm / len(self.current_state.hopf_projections)
    
    def _compute_bootstrap_contribution(self) -> float:
        """Compute the contribution of bootstrap process."""
        if not self.current_state.bootstrap_state:
            return 0.0
        
        return (self.current_state.bootstrap_state.complexity + 
                self.current_state.bootstrap_state.stability +
                self.current_state.bootstrap_state.self_organization_score) / 3.0
    
    def get_architecture_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of the cognitive architecture."""
        return {
            'architecture_info': {
                'base_dimension': self.base_dimension,
                'toroidal_resolution': self.toroidal_resolution,
                'num_bootstrap_modules': self.num_bootstrap_modules,
                'current_mode': self.current_state.mode.name,
                'iteration': self.current_state.iteration
            },
            'current_state': {
                'global_coherence': self.current_state.global_coherence,
                'emergence_level': self.current_state.emergence_level,
                'toroidal_state_energy': np.sum(self.current_state.toroidal_state**2),
                'num_hopf_projections': len(self.current_state.hopf_projections)
            },
            'component_status': {
                'toroidal_core': {
                    'resolution': self.toroidal_core.resolution,
                    'num_feedback_channels': len(self.toroidal_core.feedback_channels),
                    'num_resonance_modes': len(self.toroidal_core.resonance_modes)
                },
                'hopf_fibrations': {
                    'num_tiers': len(self.hopf_fibrations.tiers),
                    'tier_dimensions': {tier: info['dimensions'] for tier, info in self.hopf_fibrations.tiers.items()}
                },
                'recursive_inference': self.recursive_inference.get_inference_summary(),
                'autogenesis_bootstrapper': self.autogenesis_bootstrapper.get_bootstrap_summary() if hasattr(self.autogenesis_bootstrapper, 'get_bootstrap_summary') else None
            },
            'performance_metrics': self.performance_metrics,
            'emergence_tracking': {
                'patterns_detected_count': len(self.emergence_tracking['patterns_detected']),
                'coherence_trend': self.emergence_tracking['coherence_history'][-10:] if self.emergence_tracking['coherence_history'] else [],
                'complexity_trend': self.emergence_tracking['complexity_evolution'][-10:] if self.emergence_tracking['complexity_evolution'] else []
            },
            'integration_weights': self.integration_weights
        }
    
    def visualize_architecture_state(self) -> Dict[str, Any]:
        """Prepare data for visualizing the current architecture state."""
        visualization_data = {
            'toroidal_visualization': self.toroidal_core.visualize_torus_state(self.current_state.toroidal_state),
            'hopf_projections': self.current_state.hopf_projections,
            'architecture_metrics': {
                'coherence_history': self.emergence_tracking['coherence_history'],
                'complexity_evolution': self.emergence_tracking['complexity_evolution'],
                'current_coherence': self.current_state.global_coherence,
                'current_emergence': self.current_state.emergence_level
            }
        }
        
        if self.current_state.bootstrap_state:
            visualization_data['bootstrap_metrics'] = {
                'phase': self.current_state.bootstrap_state.phase.name,
                'complexity': self.current_state.bootstrap_state.complexity,
                'stability': self.current_state.bootstrap_state.stability,
                'energy': self.current_state.bootstrap_state.energy
            }
        
        return visualization_data
    
    def reset_architecture(self):
        """Reset the architecture to initial state."""
        self.current_state = CognitiveState(
            mode=ArchitectureMode.BOOTSTRAP,
            toroidal_state=np.random.randn(self.toroidal_resolution, self.toroidal_resolution) * 0.1,
            hopf_projections={},
            inference_result=None,
            bootstrap_state=None,
            timestamp=time.time(),
            iteration=0,
            global_coherence=0.0,
            emergence_level=0.0
        )
        
        # Reset components
        self.recursive_inference.reset_recursions()
        self.autogenesis_bootstrapper = AutogenesisBootstrapper(
            num_modules=self.num_bootstrap_modules,
            base_dim=self.base_dimension
        )
        
        # Clear history
        self.state_history = []
        self.emergence_tracking = {
            'patterns_detected': [],
            'complexity_evolution': [],
            'coherence_history': []
        }