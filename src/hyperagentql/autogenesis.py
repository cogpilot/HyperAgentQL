"""
Autogenesis Bootstrapper for Self-Organizing Cognitive Architecture

This module implements the bootstrapping mechanism that enables the cognitive
architecture to self-organize and emerge complex behaviors from simple rules.
The autogenesis process creates self-reinforcing loops that generate increasingly
sophisticated cognitive patterns.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Callable, Tuple
import torch
import torch.nn as nn
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx
from scipy.optimize import minimize
import time


class BootstrapPhase(Enum):
    """Phases of the autogenesis bootstrapping process."""
    INITIALIZATION = 1  # Initial random organization
    EMERGENCE = 2       # Pattern emergence and self-organization
    STABILIZATION = 3   # Pattern stabilization and refinement
    COMPLEXIFICATION = 4 # Emergence of higher-order patterns
    INTEGRATION = 5     # Integration with recursive inference


@dataclass
class AutegenesisState:
    """State of the autogenesis process."""
    phase: BootstrapPhase
    iteration: int
    energy: float
    entropy: float
    complexity: float
    stability: float
    emergent_patterns: List[Dict[str, Any]] = field(default_factory=list)
    self_organization_score: float = 0.0
    bootstrap_metrics: Dict[str, float] = field(default_factory=dict)


class SelfOrganizingModule:
    """
    Self-organizing module that can adapt its structure and function
    through interaction with other modules.
    """
    
    def __init__(self, module_id: str, input_dim: int, output_dim: int):
        self.module_id = module_id
        self.input_dim = input_dim
        self.output_dim = output_dim
        
        # Adaptive neural network
        self.network = nn.Sequential(
            nn.Linear(input_dim, max(input_dim, output_dim)),
            nn.Tanh(),
            nn.Linear(max(input_dim, output_dim), output_dim)
        )
        
        # Self-organization parameters
        self.plasticity = 0.1
        self.activation_history = []
        self.connection_strengths = {}
        self.adaptation_rate = 0.01
        
        # Emergence tracking
        self.local_patterns = {}
        self.fitness_score = 0.0
        
    def process(self, input_signal: np.ndarray, context: Optional[Dict] = None) -> np.ndarray:
        """Process input and adapt based on self-organization principles."""
        input_tensor = torch.tensor(input_signal[:self.input_dim], dtype=torch.float32)
        
        # Forward pass
        output = self.network(input_tensor)
        output_np = output.detach().numpy()
        
        # Record activation
        self.activation_history.append({
            'input': input_signal,
            'output': output_np,
            'timestamp': time.time()
        })
        
        # Self-organization: adapt based on local patterns
        self._adapt_structure(input_signal, output_np)
        
        return output_np
    
    def _adapt_structure(self, input_signal: np.ndarray, output_signal: np.ndarray):
        """Adapt module structure based on input-output patterns."""
        # Compute local correlation patterns
        if len(self.activation_history) > 10:
            recent_inputs = np.array([h['input'][:self.input_dim] for h in self.activation_history[-10:]])
            recent_outputs = np.array([h['output'] for h in self.activation_history[-10:]])
            
            # Compute correlation matrix
            input_corr = np.corrcoef(recent_inputs.T)
            output_corr = np.corrcoef(recent_outputs.T)
            
            # Identify stable patterns
            stable_threshold = 0.7
            stable_input_pairs = np.where(np.abs(input_corr) > stable_threshold)
            stable_output_pairs = np.where(np.abs(output_corr) > stable_threshold)
            
            # Store patterns
            pattern_id = f"pattern_{len(self.local_patterns)}"
            self.local_patterns[pattern_id] = {
                'input_correlations': input_corr,
                'output_correlations': output_corr,
                'stability': np.mean(np.abs(input_corr)) + np.mean(np.abs(output_corr)),
                'timestamp': time.time()
            }
            
            # Adapt network weights based on patterns
            self._adapt_weights(input_corr, output_corr)
    
    def _adapt_weights(self, input_corr: np.ndarray, output_corr: np.ndarray):
        """Adapt network weights based on correlation patterns."""
        with torch.no_grad():
            for param in self.network.parameters():
                if param.dim() == 2:  # Weight matrices
                    # Apply correlation-based adaptation
                    adaptation = torch.randn_like(param) * self.adaptation_rate
                    param.add_(adaptation)
        
        # Update adaptation rate based on stability
        stability = np.mean(np.abs(input_corr)) * np.mean(np.abs(output_corr))
        self.adaptation_rate *= (1 - stability * 0.1)  # Reduce adaptation as stability increases
    
    def get_complexity_measure(self) -> float:
        """Compute module complexity based on patterns and connections."""
        if not self.local_patterns:
            return 0.0
        
        # Complexity as pattern diversity and connection strength
        pattern_diversity = len(self.local_patterns)
        connection_strength = sum(self.connection_strengths.values()) if self.connection_strengths else 0
        
        complexity = pattern_diversity + connection_strength * 0.1
        return complexity
    
    def connect_to(self, other_module: 'SelfOrganizingModule', strength: float = 1.0):
        """Create connection to another module."""
        self.connection_strengths[other_module.module_id] = strength
        other_module.connection_strengths[self.module_id] = strength


class AutogenesisBootstrapper:
    """
    Main bootstrapper for the autogenesis process.
    
    Coordinates self-organization across multiple modules and scales
    to create emergent cognitive capabilities.
    """
    
    def __init__(self, num_modules: int = 8, base_dim: int = 32):
        self.num_modules = num_modules
        self.base_dim = base_dim
        
        # Initialize self-organizing modules
        self.modules = self._create_modules()
        self.module_graph = self._create_module_graph()
        
        # Autogenesis state
        self.current_state = AutegenesisState(
            phase=BootstrapPhase.INITIALIZATION,
            iteration=0,
            energy=1.0,
            entropy=1.0,
            complexity=0.0,
            stability=0.0
        )
        
        # Bootstrap configuration
        self.config = {
            'max_iterations': 1000,
            'stability_threshold': 0.8,
            'complexity_target': 10.0,
            'energy_decay_rate': 0.001,
            'phase_transition_criteria': {
                BootstrapPhase.INITIALIZATION: {'min_iterations': 50, 'min_connections': 10},
                BootstrapPhase.EMERGENCE: {'min_complexity': 2.0, 'min_stability': 0.3},
                BootstrapPhase.STABILIZATION: {'min_stability': 0.6, 'complexity_growth_rate': 0.1},
                BootstrapPhase.COMPLEXIFICATION: {'min_complexity': 5.0, 'min_stability': 0.7},
                BootstrapPhase.INTEGRATION: {'min_complexity': 8.0, 'min_stability': 0.8}
            }
        }
        
        # Emergence tracking
        self.global_patterns = {}
        self.emergence_history = []
        self.feedback_loops = []
        
    def _create_modules(self) -> List[SelfOrganizingModule]:
        """Create the initial set of self-organizing modules."""
        modules = []
        
        for i in range(self.num_modules):
            # Use consistent dimensions to avoid mismatch
            input_dim = self.base_dim
            output_dim = self.base_dim
            
            module = SelfOrganizingModule(f"module_{i}", input_dim, output_dim)
            modules.append(module)
        
        return modules
    
    def _create_module_graph(self) -> nx.Graph:
        """Create initial connection graph between modules."""
        G = nx.Graph()
        
        # Add modules as nodes
        for i, module in enumerate(self.modules):
            G.add_node(i, module=module)
        
        # Create initial random connections
        num_connections = min(self.num_modules * 2, self.num_modules * (self.num_modules - 1) // 4)
        
        for _ in range(num_connections):
            i, j = np.random.choice(self.num_modules, 2, replace=False)
            if not G.has_edge(i, j):
                strength = np.random.uniform(0.1, 1.0)
                G.add_edge(i, j, weight=strength)
                self.modules[i].connect_to(self.modules[j], strength)
        
        return G
    
    def bootstrap_step(self, external_input: Optional[np.ndarray] = None) -> AutegenesisState:
        """Perform one step of the autogenesis bootstrapping process."""
        self.current_state.iteration += 1
        
        # Generate or use external input
        if external_input is None:
            external_input = self._generate_bootstrap_input()
        
        # Process through modules with self-organization
        module_outputs = self._process_through_modules(external_input)
        
        # Detect and reinforce emergent patterns
        emergent_patterns = self._detect_emergent_patterns(module_outputs)
        
        # Update global patterns and feedback loops
        self._update_global_patterns(emergent_patterns)
        self._update_feedback_loops(module_outputs)
        
        # Compute metrics
        self._compute_bootstrap_metrics()
        
        # Check for phase transitions
        self._check_phase_transition()
        
        # Evolve module connections
        self._evolve_connections()
        
        return self.current_state
    
    def _generate_bootstrap_input(self) -> np.ndarray:
        """Generate bootstrap input signal based on current phase."""
        if self.current_state.phase == BootstrapPhase.INITIALIZATION:
            # Random input to kickstart self-organization
            return np.random.randn(self.base_dim) * 0.5
        
        elif self.current_state.phase == BootstrapPhase.EMERGENCE:
            # Structured input to encourage pattern formation
            t = self.current_state.iteration * 0.1
            signal = np.sin(np.arange(self.base_dim) * t * 0.1)
            signal += np.random.randn(self.base_dim) * 0.1
            return signal
        
        elif self.current_state.phase == BootstrapPhase.STABILIZATION:
            # Input that reinforces existing patterns
            if self.global_patterns:
                pattern_key = list(self.global_patterns.keys())[0]
                base_pattern = self.global_patterns[pattern_key]['template']
                noise = np.random.randn(len(base_pattern)) * 0.05
                return base_pattern + noise
            else:
                return np.random.randn(self.base_dim) * 0.2
        
        elif self.current_state.phase == BootstrapPhase.COMPLEXIFICATION:
            # Complex multi-scale input
            scales = [0.1, 0.5, 1.0, 2.0]
            signal = np.zeros(self.base_dim)
            t = self.current_state.iteration * 0.1
            
            for scale in scales:
                component = np.sin(np.arange(self.base_dim) * t * scale)
                signal += component * (1.0 / scale)
            
            return signal / len(scales)
        
        else:  # INTEGRATION
            # Input that challenges the integrated system
            return np.random.randn(self.base_dim) * 0.3 + np.sin(self.current_state.iteration * 0.05)
    
    def _process_through_modules(self, input_signal: np.ndarray) -> Dict[str, np.ndarray]:
        """Process input through all modules with cross-module interactions."""
        module_outputs = {}
        
        # Initial processing
        for i, module in enumerate(self.modules):
            output = module.process(input_signal)
            module_outputs[f"module_{i}"] = output
        
        # Cross-module interaction (one iteration)
        for edge in self.module_graph.edges(data=True):
            i, j, data = edge
            weight = data['weight']
            
            # Module i influences module j
            influence = module_outputs[f"module_{i}"] * weight * 0.1
            
            # Ensure compatible dimensions
            target_dim = self.modules[j].input_dim
            if len(influence) != target_dim:
                if len(influence) > target_dim:
                    influence = influence[:target_dim]
                else:
                    influence = np.pad(influence, (0, target_dim - len(influence)))
            
            # Apply influence
            influenced_output = self.modules[j].process(influence)
            module_outputs[f"module_{j}"] += influenced_output * 0.1
        
        return module_outputs
    
    def _detect_emergent_patterns(self, module_outputs: Dict[str, np.ndarray]) -> List[Dict[str, Any]]:
        """Detect emergent patterns across module outputs."""
        patterns = []
        
        # Collect all outputs
        all_outputs = list(module_outputs.values())
        if not all_outputs:
            return patterns
        
        # Compute cross-module correlations
        min_length = min(len(output) for output in all_outputs)
        output_matrix = np.array([output[:min_length] for output in all_outputs])
        
        if output_matrix.shape[0] > 1:
            correlation_matrix = np.corrcoef(output_matrix)
            
            # Find strong correlations
            strong_correlation_threshold = 0.6
            strong_correlations = np.where(np.abs(correlation_matrix) > strong_correlation_threshold)
            
            for i, j in zip(strong_correlations[0], strong_correlations[1]):
                if i < j:  # Avoid duplicates
                    pattern = {
                        'type': 'cross_module_correlation',
                        'modules': [f"module_{i}", f"module_{j}"],
                        'correlation': correlation_matrix[i, j],
                        'pattern_vector': output_matrix[i] + output_matrix[j],
                        'strength': abs(correlation_matrix[i, j]),
                        'timestamp': self.current_state.iteration
                    }
                    patterns.append(pattern)
        
        # Detect oscillatory patterns
        for module_name, output in module_outputs.items():
            if len(output) > 4:
                # Simple oscillation detection
                diffs = np.diff(output)
                sign_changes = np.sum(np.diff(np.sign(diffs)) != 0)
                
                if sign_changes > len(output) * 0.3:  # At least 30% sign changes
                    pattern = {
                        'type': 'oscillatory',
                        'module': module_name,
                        'frequency_estimate': sign_changes / len(output),
                        'amplitude': np.std(output),
                        'pattern_vector': output,
                        'strength': sign_changes / len(output),
                        'timestamp': self.current_state.iteration
                    }
                    patterns.append(pattern)
        
        return patterns
    
    def _update_global_patterns(self, emergent_patterns: List[Dict[str, Any]]):
        """Update global pattern repository with emergent patterns."""
        for pattern in emergent_patterns:
            pattern_signature = self._compute_pattern_signature(pattern)
            
            if pattern_signature in self.global_patterns:
                # Reinforce existing pattern
                self.global_patterns[pattern_signature]['strength'] += 0.1
                self.global_patterns[pattern_signature]['occurrences'] += 1
                self.global_patterns[pattern_signature]['last_seen'] = self.current_state.iteration
            else:
                # Add new pattern
                self.global_patterns[pattern_signature] = {
                    'template': pattern['pattern_vector'],
                    'type': pattern['type'],
                    'strength': pattern['strength'],
                    'occurrences': 1,
                    'first_seen': self.current_state.iteration,
                    'last_seen': self.current_state.iteration,
                    'metadata': pattern
                }
        
        # Decay old patterns
        patterns_to_remove = []
        for sig, pattern in self.global_patterns.items():
            if self.current_state.iteration - pattern['last_seen'] > 100:
                pattern['strength'] *= 0.9
                if pattern['strength'] < 0.1:
                    patterns_to_remove.append(sig)
        
        for sig in patterns_to_remove:
            del self.global_patterns[sig]
    
    def _compute_pattern_signature(self, pattern: Dict[str, Any]) -> str:
        """Compute a signature for pattern matching."""
        if 'pattern_vector' in pattern:
            # Quantize pattern vector for signature
            quantized = np.round(pattern['pattern_vector'] * 10).astype(int)
            signature = f"{pattern['type']}_{hash(tuple(quantized))}"
        else:
            signature = f"{pattern['type']}_{pattern.get('modules', ['unknown'])}"
        
        return signature
    
    def _update_feedback_loops(self, module_outputs: Dict[str, np.ndarray]):
        """Identify and strengthen feedback loops."""
        # Simple feedback loop detection based on circular influences
        for i, module_i in enumerate(self.modules):
            for j, module_j in enumerate(self.modules):
                if i != j and self.module_graph.has_edge(i, j):
                    # Check if there's mutual influence
                    if self.module_graph.has_edge(j, i):
                        # Strengthen feedback loop
                        current_weight_ij = self.module_graph[i][j]['weight']
                        current_weight_ji = self.module_graph[j][i]['weight']
                        
                        # Increase weights slightly for stable feedback
                        new_weight_ij = min(2.0, current_weight_ij * 1.01)
                        new_weight_ji = min(2.0, current_weight_ji * 1.01)
                        
                        self.module_graph[i][j]['weight'] = new_weight_ij
                        self.module_graph[j][i]['weight'] = new_weight_ji
                        
                        # Record feedback loop
                        loop_id = f"loop_{min(i,j)}_{max(i,j)}"
                        if not any(loop['id'] == loop_id for loop in self.feedback_loops):
                            self.feedback_loops.append({
                                'id': loop_id,
                                'modules': [i, j],
                                'strength': (new_weight_ij + new_weight_ji) / 2,
                                'created': self.current_state.iteration
                            })
    
    def _compute_bootstrap_metrics(self):
        """Compute metrics for the current bootstrap state."""
        # Complexity: based on patterns and connections
        pattern_complexity = len(self.global_patterns) * 0.5
        connection_complexity = self.module_graph.number_of_edges() * 0.1
        module_complexity = sum(module.get_complexity_measure() for module in self.modules) * 0.1
        
        self.current_state.complexity = pattern_complexity + connection_complexity + module_complexity
        
        # Stability: based on pattern persistence and connection weights
        if self.global_patterns:
            pattern_stability = np.mean([p['strength'] for p in self.global_patterns.values()])
        else:
            pattern_stability = 0.0
        
        connection_stability = np.mean([data['weight'] for _, _, data in self.module_graph.edges(data=True)])
        self.current_state.stability = (pattern_stability + connection_stability) / 2
        
        # Energy: decreases over time but can be renewed by new patterns
        self.current_state.energy *= (1 - self.config['energy_decay_rate'])
        if len(self.current_state.emergent_patterns) > 0:
            self.current_state.energy = min(1.0, self.current_state.energy + 0.1)
        
        # Entropy: measure of pattern diversity
        if self.global_patterns:
            pattern_types = [p['type'] for p in self.global_patterns.values()]
            unique_types = len(set(pattern_types))
            self.current_state.entropy = unique_types / max(1, len(pattern_types))
        else:
            self.current_state.entropy = 1.0
        
        # Self-organization score
        self.current_state.self_organization_score = (
            self.current_state.complexity * 0.3 +
            self.current_state.stability * 0.4 +
            self.current_state.entropy * 0.2 +
            len(self.feedback_loops) * 0.1
        )
        
        # Update metrics
        self.current_state.bootstrap_metrics = {
            'num_patterns': len(self.global_patterns),
            'num_connections': self.module_graph.number_of_edges(),
            'num_feedback_loops': len(self.feedback_loops),
            'total_module_complexity': sum(module.get_complexity_measure() for module in self.modules),
            'average_connection_weight': connection_stability
        }
    
    def _check_phase_transition(self):
        """Check if criteria are met for transitioning to next phase."""
        current_phase = self.current_state.phase
        criteria = self.config['phase_transition_criteria'].get(current_phase, {})
        
        transition = True
        
        # Check all criteria
        if 'min_iterations' in criteria:
            transition &= self.current_state.iteration >= criteria['min_iterations']
        
        if 'min_connections' in criteria:
            transition &= self.module_graph.number_of_edges() >= criteria['min_connections']
        
        if 'min_complexity' in criteria:
            transition &= self.current_state.complexity >= criteria['min_complexity']
        
        if 'min_stability' in criteria:
            transition &= self.current_state.stability >= criteria['min_stability']
        
        if 'complexity_growth_rate' in criteria:
            if len(self.emergence_history) > 10:
                recent_complexity = [s.complexity for s in self.emergence_history[-10:]]
                growth_rate = (recent_complexity[-1] - recent_complexity[0]) / 10
                transition &= growth_rate >= criteria['complexity_growth_rate']
        
        # Transition to next phase
        if transition and current_phase != BootstrapPhase.INTEGRATION:
            next_phase_value = current_phase.value + 1
            self.current_state.phase = BootstrapPhase(next_phase_value)
            print(f"Phase transition: {current_phase.name} -> {self.current_state.phase.name}")
    
    def _evolve_connections(self):
        """Evolve module connections based on performance."""
        if self.current_state.iteration % 50 == 0:  # Every 50 iterations
            # Add new beneficial connections
            unconnected_pairs = []
            for i in range(self.num_modules):
                for j in range(i + 1, self.num_modules):
                    if not self.module_graph.has_edge(i, j):
                        unconnected_pairs.append((i, j))
            
            if unconnected_pairs and len(unconnected_pairs) > 0:
                # Add a few random connections
                num_new = min(2, len(unconnected_pairs))
                new_pairs = np.random.choice(len(unconnected_pairs), num_new, replace=False)
                
                for idx in new_pairs:
                    i, j = unconnected_pairs[idx]
                    weight = np.random.uniform(0.1, 0.5)
                    self.module_graph.add_edge(i, j, weight=weight)
                    self.modules[i].connect_to(self.modules[j], weight)
            
            # Remove weak connections
            weak_edges = []
            for i, j, data in self.module_graph.edges(data=True):
                if data['weight'] < 0.05:
                    weak_edges.append((i, j))
            
            for i, j in weak_edges:
                self.module_graph.remove_edge(i, j)
                if j in self.modules[i].connection_strengths:
                    del self.modules[i].connection_strengths[j]
                if i in self.modules[j].connection_strengths:
                    del self.modules[j].connection_strengths[i]
    
    def run_bootstrap(self, num_steps: int, external_inputs: Optional[List[np.ndarray]] = None) -> List[AutegenesisState]:
        """Run the complete bootstrap process."""
        history = []
        
        for step in range(num_steps):
            if external_inputs and step < len(external_inputs):
                input_signal = external_inputs[step]
            else:
                input_signal = None
            
            state = self.bootstrap_step(input_signal)
            history.append(state)
            self.emergence_history.append(state)
            
            # Early termination if fully integrated
            if state.phase == BootstrapPhase.INTEGRATION and state.stability > 0.9:
                print(f"Bootstrap completed early at step {step}")
                break
        
        return history
    
    def get_bootstrap_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of bootstrap process."""
        return {
            'current_phase': self.current_state.phase.name,
            'iterations': self.current_state.iteration,
            'complexity': self.current_state.complexity,
            'stability': self.current_state.stability,
            'self_organization_score': self.current_state.self_organization_score,
            'global_patterns': len(self.global_patterns),
            'feedback_loops': len(self.feedback_loops),
            'module_connections': self.module_graph.number_of_edges(),
            'emergence_history_length': len(self.emergence_history),
            'bootstrap_metrics': self.current_state.bootstrap_metrics
        }
    
    def integrate_with_recursive_inference(self, recursive_inference_engine) -> Dict[str, Any]:
        """Integrate the bootstrapped system with recursive inference."""
        # Extract learned patterns as input for recursive inference
        pattern_vectors = []
        for pattern in self.global_patterns.values():
            if 'template' in pattern:
                pattern_vectors.append(pattern['template'])
        
        if not pattern_vectors:
            return {'status': 'no_patterns_to_integrate'}
        
        # Use patterns as input to recursive inference
        integrated_results = []
        for pattern_vector in pattern_vectors[:5]:  # Use top 5 patterns
            result = recursive_inference_engine.infer(pattern_vector)
            integrated_results.append(result)
        
        return {
            'status': 'integrated',
            'patterns_used': len(pattern_vectors),
            'inference_results': integrated_results,
            'bootstrap_state': self.get_bootstrap_summary()
        }