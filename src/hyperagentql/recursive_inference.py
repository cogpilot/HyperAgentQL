"""
Recursive Inference Engine with 3 Nested Recursions

This module implements the core inference engine with three levels of nested
recursion that operate at different scales and time horizons, creating a
sophisticated multi-level reasoning system.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Callable, Tuple
import torch
import torch.nn as nn
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class RecursionLevel(Enum):
    """Enumeration of the three recursion levels."""
    MICRO = 1    # Fast, local, pattern-level recursion
    MACRO = 2    # Medium, structural, concept-level recursion  
    META = 3     # Slow, global, meta-cognitive recursion


@dataclass
class InferenceState:
    """Represents the state at a particular recursion level."""
    level: RecursionLevel
    state_vector: np.ndarray
    confidence: float
    timestamp: float
    metadata: Dict[str, Any]


class RecursiveInferenceLayer(ABC):
    """Abstract base class for recursive inference layers."""
    
    @abstractmethod
    def forward(self, input_state: InferenceState, 
                context: Optional[Dict[str, Any]] = None) -> InferenceState:
        """Forward pass through the recursive layer."""
        pass
    
    @abstractmethod
    def backward(self, gradient: np.ndarray) -> np.ndarray:
        """Backward pass for learning."""
        pass
    
    @abstractmethod
    def get_recursion_depth(self) -> int:
        """Get the current recursion depth."""
        pass


class MicroRecursion(RecursiveInferenceLayer):
    """
    Micro-level recursion: Fast, pattern-based inference.
    
    Operates on immediate sensory/data patterns with high frequency
    and low latency. Handles local feature detection and basic
    pattern recognition.
    """
    
    def __init__(self, input_dim: int = 64, hidden_dim: int = 128, 
                 max_depth: int = 5):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.max_depth = max_depth
        self.current_depth = 0
        
        # Neural components for pattern processing
        self.pattern_encoder = self._create_pattern_encoder()
        self.recursive_unit = self._create_recursive_unit()
        self.output_decoder = self._create_output_decoder()
        
        # Micro-scale memory
        self.micro_memory = []
        self.pattern_cache = {}
        
    def _create_pattern_encoder(self) -> nn.Module:
        """Create the pattern encoding network."""
        return nn.Sequential(
            nn.Linear(self.input_dim, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.Tanh()
        )
    
    def _create_recursive_unit(self) -> nn.Module:
        """Create the recursive processing unit."""
        return nn.GRUCell(self.hidden_dim, self.hidden_dim)
    
    def _create_output_decoder(self) -> nn.Module:
        """Create the output decoding network."""
        return nn.Sequential(
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.input_dim),  # Changed to input_dim
            nn.Sigmoid()
        )
    
    def forward(self, input_state: InferenceState, 
                context: Optional[Dict[str, Any]] = None) -> InferenceState:
        """Forward pass through micro recursion."""
        if self.current_depth >= self.max_depth:
            # Base case: return processed state
            return self._process_base_case(input_state)
        
        # Recursive case
        self.current_depth += 1
        
        # Ensure input matches expected dimensions
        input_vector = input_state.state_vector[:self.input_dim]
        if len(input_vector) < self.input_dim:
            input_vector = np.pad(input_vector, (0, self.input_dim - len(input_vector)))
        
        # Encode input pattern
        encoded = self.pattern_encoder(torch.tensor(input_vector, dtype=torch.float32))
        
        # Apply recursive processing
        if len(self.micro_memory) > 0:
            prev_hidden = torch.tensor(self.micro_memory[-1], dtype=torch.float32)
        else:
            prev_hidden = torch.zeros(self.hidden_dim)
        
        hidden_state = self.recursive_unit(encoded, prev_hidden)
        self.micro_memory.append(hidden_state.detach().numpy())
        
        # Create intermediate state for recursion
        intermediate_state = InferenceState(
            level=RecursionLevel.MICRO,
            state_vector=hidden_state.detach().numpy(),
            confidence=input_state.confidence * 0.95,  # Slight confidence decay
            timestamp=input_state.timestamp,
            metadata={**input_state.metadata, 'micro_depth': self.current_depth}
        )
        
        # Recursive call
        recursive_result = self.forward(intermediate_state, context)
        
        # Decode and combine results
        result_vector = recursive_result.state_vector[:self.hidden_dim]
        if len(result_vector) < self.hidden_dim:
            result_vector = np.pad(result_vector, (0, self.hidden_dim - len(result_vector)))
        
        decoded = self.output_decoder(torch.tensor(result_vector, dtype=torch.float32))
        
        self.current_depth -= 1
        
        return InferenceState(
            level=RecursionLevel.MICRO,
            state_vector=decoded.detach().numpy(),
            confidence=recursive_result.confidence,
            timestamp=recursive_result.timestamp,
            metadata=recursive_result.metadata
        )
    
    def _process_base_case(self, state: InferenceState) -> InferenceState:
        """Process the base case when max depth is reached."""
        # Simple pattern completion
        processed_vector = np.tanh(state.state_vector * 1.1)
        
        return InferenceState(
            level=RecursionLevel.MICRO,
            state_vector=processed_vector,
            confidence=state.confidence * 0.9,
            timestamp=state.timestamp,
            metadata={**state.metadata, 'base_case': True}
        )
    
    def backward(self, gradient: np.ndarray) -> np.ndarray:
        """Implement backward pass for learning."""
        # Simplified gradient computation
        return gradient * 0.1  # Learning rate
    
    def get_recursion_depth(self) -> int:
        return self.current_depth


class MacroRecursion(RecursiveInferenceLayer):
    """
    Macro-level recursion: Structural, concept-based inference.
    
    Operates on higher-level concepts and structural relationships.
    Handles compositional reasoning and hierarchical understanding.
    """
    
    def __init__(self, concept_dim: int = 256, structure_dim: int = 512,
                 max_depth: int = 3):
        self.concept_dim = concept_dim
        self.structure_dim = structure_dim
        self.max_depth = max_depth
        self.current_depth = 0
        
        # Structural processing components
        self.concept_extractor = self._create_concept_extractor()
        self.structure_builder = self._create_structure_builder()
        self.composition_network = self._create_composition_network()
        
        # Macro-scale knowledge graph
        self.concept_graph = {}
        self.structural_memory = []
        
    def _create_concept_extractor(self) -> nn.Module:
        """Create concept extraction network."""
        return nn.Sequential(
            nn.Linear(self.concept_dim, self.structure_dim),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(self.structure_dim, self.concept_dim),
            nn.LayerNorm(self.concept_dim)
        )
    
    def _create_structure_builder(self) -> nn.Module:
        """Create structural relationship builder."""
        return nn.TransformerEncoderLayer(
            d_model=self.concept_dim,
            nhead=8,
            dim_feedforward=self.structure_dim,
            dropout=0.1
        )
    
    def _create_composition_network(self) -> nn.Module:
        """Create compositional reasoning network."""
        return nn.Sequential(
            nn.Linear(self.concept_dim * 2, self.structure_dim),
            nn.GELU(),
            nn.Linear(self.structure_dim, self.concept_dim),
            nn.Tanh()
        )
    
    def forward(self, input_state: InferenceState,
                context: Optional[Dict[str, Any]] = None) -> InferenceState:
        """Forward pass through macro recursion."""
        if self.current_depth >= self.max_depth:
            return self._process_structural_base_case(input_state)
        
        self.current_depth += 1
        
        # Extract concepts from input - ensure proper dimensions
        input_vector = input_state.state_vector[:self.concept_dim]
        if len(input_vector) < self.concept_dim:
            input_vector = np.pad(input_vector, (0, self.concept_dim - len(input_vector)))
        
        state_tensor = torch.tensor(input_vector, dtype=torch.float32)
        concepts = self.concept_extractor(state_tensor)
        
        # Build structural relationships
        struct_input = concepts.unsqueeze(0)  # Add batch dimension
        structural_rep = self.structure_builder(struct_input).squeeze(0)
        
        # Store in structural memory
        self.structural_memory.append(structural_rep.detach().numpy())
        
        # Create state for recursion
        recursive_state = InferenceState(
            level=RecursionLevel.MACRO,
            state_vector=structural_rep.detach().numpy(),
            confidence=input_state.confidence * 0.92,
            timestamp=input_state.timestamp,
            metadata={**input_state.metadata, 'macro_depth': self.current_depth}
        )
        
        # Recursive call
        recursive_result = self.forward(recursive_state, context)
        
        # Compositional reasoning
        if len(self.structural_memory) > 1:
            prev_struct = torch.tensor(self.structural_memory[-2], dtype=torch.float32)
            curr_struct = torch.tensor(recursive_result.state_vector, dtype=torch.float32)
            
            # Ensure tensors are the same size
            min_size = min(len(prev_struct), len(curr_struct))
            composition_input = torch.cat([prev_struct[:min_size], curr_struct[:min_size]])
            
            composed = self.composition_network(composition_input)
        else:
            composed = torch.tensor(recursive_result.state_vector, dtype=torch.float32)
        
        self.current_depth -= 1
        
        return InferenceState(
            level=RecursionLevel.MACRO,
            state_vector=composed.detach().numpy(),
            confidence=recursive_result.confidence,
            timestamp=recursive_result.timestamp,
            metadata=recursive_result.metadata
        )
    
    def _process_structural_base_case(self, state: InferenceState) -> InferenceState:
        """Process base case for structural reasoning."""
        # Structural stabilization
        processed = state.state_vector / (1 + np.abs(state.state_vector))
        
        return InferenceState(
            level=RecursionLevel.MACRO,
            state_vector=processed,
            confidence=state.confidence * 0.95,
            timestamp=state.timestamp,
            metadata={**state.metadata, 'structural_base': True}
        )
    
    def backward(self, gradient: np.ndarray) -> np.ndarray:
        return gradient * 0.05  # Slower learning for structural components
    
    def get_recursion_depth(self) -> int:
        return self.current_depth


class MetaRecursion(RecursiveInferenceLayer):
    """
    Meta-level recursion: Global, meta-cognitive inference.
    
    Operates on meta-cognitive strategies and global reasoning patterns.
    Handles self-reflection, strategy selection, and adaptive control.
    """
    
    def __init__(self, meta_dim: int = 512, strategy_dim: int = 256,
                 max_depth: int = 2):
        self.meta_dim = meta_dim
        self.strategy_dim = strategy_dim
        self.max_depth = max_depth
        self.current_depth = 0
        
        # Meta-level memory and strategies (initialize first)
        self.meta_memory = []
        self.strategy_repertoire = self._initialize_strategies()
        self.global_context = {}
        
        # Meta-cognitive components (initialize after strategy_repertoire)
        self.meta_analyzer = self._create_meta_analyzer()
        self.strategy_selector = self._create_strategy_selector()
        self.adaptation_network = self._create_adaptation_network()
        
    def _create_meta_analyzer(self) -> nn.Module:
        """Create meta-cognitive analysis network."""
        return nn.Sequential(
            nn.Linear(self.meta_dim, self.strategy_dim),
            nn.SELU(),
            nn.Linear(self.strategy_dim, self.strategy_dim),
            nn.BatchNorm1d(self.strategy_dim),
            nn.SELU(),
            nn.Linear(self.strategy_dim, self.meta_dim)
        )
    
    def _create_strategy_selector(self) -> nn.Module:
        """Create strategy selection network."""
        return nn.Sequential(
            nn.Linear(self.meta_dim, len(self.strategy_repertoire)),
            nn.Softmax(dim=0)
        )
    
    def _create_adaptation_network(self) -> nn.Module:
        """Create adaptation mechanism."""
        return nn.Sequential(
            nn.Linear(self.meta_dim + self.strategy_dim, self.meta_dim),
            nn.SiLU(),  # SiLU is equivalent to Swish
            nn.Linear(self.meta_dim, self.meta_dim),
            nn.Tanh()
        )
    
    def _initialize_strategies(self) -> List[Dict[str, Any]]:
        """Initialize meta-cognitive strategies."""
        return [
            {'name': 'analytical', 'bias': np.array([1, 0, 0]), 'weight': 0.3},
            {'name': 'intuitive', 'bias': np.array([0, 1, 0]), 'weight': 0.4},
            {'name': 'creative', 'bias': np.array([0, 0, 1]), 'weight': 0.2},
            {'name': 'integrative', 'bias': np.array([1, 1, 1]), 'weight': 0.1}
        ]
    
    def forward(self, input_state: InferenceState,
                context: Optional[Dict[str, Any]] = None) -> InferenceState:
        """Forward pass through meta recursion."""
        if self.current_depth >= self.max_depth:
            return self._process_meta_base_case(input_state)
        
        self.current_depth += 1
        
        # Meta-cognitive analysis - ensure proper dimensions
        input_vector = input_state.state_vector[:self.meta_dim]
        if len(input_vector) < self.meta_dim:
            input_vector = np.pad(input_vector, (0, self.meta_dim - len(input_vector)))
        
        state_tensor = torch.tensor(input_vector, dtype=torch.float32)
        meta_analysis = self.meta_analyzer(state_tensor.unsqueeze(0)).squeeze(0)
        
        # Strategy selection
        strategy_probs = self.strategy_selector(meta_analysis)
        selected_strategy_idx = torch.argmax(strategy_probs).item()
        selected_strategy = self.strategy_repertoire[selected_strategy_idx]
        
        # Update global context
        self.global_context.update({
            'selected_strategy': selected_strategy['name'],
            'strategy_confidence': strategy_probs[selected_strategy_idx].item(),
            'meta_depth': self.current_depth
        })
        
        # Apply strategy bias
        strategy_bias = torch.tensor(
            np.tile(selected_strategy['bias'], self.meta_dim // 3 + 1)[:self.meta_dim],
            dtype=torch.float32
        )
        biased_analysis = meta_analysis + strategy_bias * selected_strategy['weight']
        
        # Store in meta memory
        self.meta_memory.append(biased_analysis.detach().numpy())
        
        # Create recursive state
        recursive_state = InferenceState(
            level=RecursionLevel.META,
            state_vector=biased_analysis.detach().numpy(),
            confidence=input_state.confidence * 0.88,
            timestamp=input_state.timestamp,
            metadata={**input_state.metadata, 'meta_depth': self.current_depth,
                     'strategy': selected_strategy['name']}
        )
        
        # Recursive call
        recursive_result = self.forward(recursive_state, context)
        
        # Adaptation based on recursive result
        if len(self.meta_memory) > 1:
            prev_meta = torch.tensor(self.meta_memory[-2], dtype=torch.float32)
            curr_meta = torch.tensor(recursive_result.state_vector, dtype=torch.float32)
            
            # Pad shorter tensor
            max_len = max(len(prev_meta), len(curr_meta))
            if len(prev_meta) < max_len:
                prev_meta = torch.cat([prev_meta, torch.zeros(max_len - len(prev_meta))])
            if len(curr_meta) < max_len:
                curr_meta = torch.cat([curr_meta, torch.zeros(max_len - len(curr_meta))])
            
            adaptation_input = torch.cat([prev_meta[:self.meta_dim], curr_meta[:self.strategy_dim]])
            adapted = self.adaptation_network(adaptation_input)
        else:
            adapted = torch.tensor(recursive_result.state_vector, dtype=torch.float32)
        
        self.current_depth -= 1
        
        return InferenceState(
            level=RecursionLevel.META,
            state_vector=adapted.detach().numpy(),
            confidence=recursive_result.confidence,
            timestamp=recursive_result.timestamp,
            metadata={**recursive_result.metadata, 'global_context': self.global_context}
        )
    
    def _process_meta_base_case(self, state: InferenceState) -> InferenceState:
        """Process base case for meta-cognitive reasoning."""
        # Meta-cognitive stabilization with self-reflection
        reflection_gain = 1 + 0.1 * np.sin(np.sum(state.state_vector))
        processed = state.state_vector * reflection_gain
        processed = np.tanh(processed)  # Bounded output
        
        return InferenceState(
            level=RecursionLevel.META,
            state_vector=processed,
            confidence=state.confidence * 0.93,
            timestamp=state.timestamp,
            metadata={**state.metadata, 'meta_base': True, 'reflection_gain': reflection_gain}
        )
    
    def backward(self, gradient: np.ndarray) -> np.ndarray:
        return gradient * 0.01  # Very slow learning for meta-level
    
    def get_recursion_depth(self) -> int:
        return self.current_depth


class RecursiveInference:
    """
    Main recursive inference engine coordinating all three recursion levels.
    
    Orchestrates the interaction between micro, macro, and meta recursions
    to create a comprehensive multi-level reasoning system.
    """
    
    def __init__(self, input_dim: int = 128):
        self.input_dim = input_dim
        
        # Initialize the three recursion levels
        self.micro_recursion = MicroRecursion(input_dim=input_dim)
        self.macro_recursion = MacroRecursion(concept_dim=min(256, input_dim * 2))
        self.meta_recursion = MetaRecursion(meta_dim=min(512, input_dim * 4))
        
        # Cross-level communication networks
        self.micro_to_macro = self._create_level_bridge(input_dim, 256)
        self.macro_to_meta = self._create_level_bridge(256, 512)
        self.meta_to_macro = self._create_level_bridge(512, 256)
        self.macro_to_micro = self._create_level_bridge(256, input_dim)
        
        # Global inference state
        self.global_state = None
        self.inference_history = []
        
    def _create_level_bridge(self, input_dim: int, output_dim: int) -> nn.Module:
        """Create bridge network between recursion levels."""
        return nn.Sequential(
            nn.Linear(input_dim, max(input_dim, output_dim)),
            nn.ReLU(),
            nn.Linear(max(input_dim, output_dim), output_dim),
            nn.LayerNorm(output_dim)
        )
    
    def infer(self, input_data: np.ndarray, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform inference using all three recursion levels."""
        timestamp = len(self.inference_history)
        
        # Create initial inference state
        initial_state = InferenceState(
            level=RecursionLevel.MICRO,
            state_vector=input_data[:self.input_dim],
            confidence=1.0,
            timestamp=timestamp,
            metadata={'input_shape': input_data.shape}
        )
        
        # Level 1: Micro recursion
        micro_result = self.micro_recursion.forward(initial_state, context)
        
        # Bridge micro to macro
        micro_tensor = torch.tensor(micro_result.state_vector, dtype=torch.float32)
        macro_input = self.micro_to_macro(micro_tensor)
        
        macro_state = InferenceState(
            level=RecursionLevel.MACRO,
            state_vector=macro_input.detach().numpy(),
            confidence=micro_result.confidence,
            timestamp=timestamp,
            metadata=micro_result.metadata
        )
        
        # Level 2: Macro recursion
        macro_result = self.macro_recursion.forward(macro_state, context)
        
        # Bridge macro to meta
        macro_tensor = torch.tensor(macro_result.state_vector, dtype=torch.float32)
        meta_input = self.macro_to_meta(macro_tensor)
        
        meta_state = InferenceState(
            level=RecursionLevel.META,
            state_vector=meta_input.detach().numpy(),
            confidence=macro_result.confidence,
            timestamp=timestamp,
            metadata=macro_result.metadata
        )
        
        # Level 3: Meta recursion
        meta_result = self.meta_recursion.forward(meta_state, context)
        
        # Top-down influence: Meta back to Macro
        meta_tensor = torch.tensor(meta_result.state_vector, dtype=torch.float32)
        meta_to_macro_influence = self.meta_to_macro(meta_tensor)
        
        # Combine macro result with meta influence
        enhanced_macro = macro_result.state_vector + 0.3 * meta_to_macro_influence.detach().numpy()[:len(macro_result.state_vector)]
        
        # Macro back to Micro
        enhanced_macro_tensor = torch.tensor(enhanced_macro, dtype=torch.float32)
        macro_to_micro_influence = self.macro_to_micro(enhanced_macro_tensor)
        
        # Final integration
        final_result = micro_result.state_vector + 0.2 * macro_to_micro_influence.detach().numpy()[:len(micro_result.state_vector)]
        
        # Compile inference results
        inference_result = {
            'final_output': final_result,
            'micro_result': micro_result,
            'macro_result': macro_result,
            'meta_result': meta_result,
            'confidence': meta_result.confidence,
            'recursion_depths': {
                'micro': self.micro_recursion.get_recursion_depth(),
                'macro': self.macro_recursion.get_recursion_depth(),
                'meta': self.meta_recursion.get_recursion_depth()
            },
            'global_context': getattr(self.meta_recursion, 'global_context', {}),
            'timestamp': timestamp
        }
        
        # Store in history
        self.inference_history.append(inference_result)
        self.global_state = inference_result
        
        return inference_result
    
    def reset_recursions(self):
        """Reset all recursion levels to initial state."""
        self.micro_recursion.current_depth = 0
        self.micro_recursion.micro_memory = []
        
        self.macro_recursion.current_depth = 0
        self.macro_recursion.structural_memory = []
        
        self.meta_recursion.current_depth = 0
        self.meta_recursion.meta_memory = []
        self.meta_recursion.global_context = {}
    
    def get_inference_summary(self) -> Dict[str, Any]:
        """Get summary of inference capabilities and current state."""
        return {
            'total_inferences': len(self.inference_history),
            'current_global_state': self.global_state,
            'micro_config': {
                'max_depth': self.micro_recursion.max_depth,
                'hidden_dim': self.micro_recursion.hidden_dim
            },
            'macro_config': {
                'max_depth': self.macro_recursion.max_depth,
                'concept_dim': self.macro_recursion.concept_dim
            },
            'meta_config': {
                'max_depth': self.meta_recursion.max_depth,
                'strategy_count': len(self.meta_recursion.strategy_repertoire)
            }
        }