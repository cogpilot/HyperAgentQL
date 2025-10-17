"""
Example usage of HyperAgentQL Cognitive Architecture

This script demonstrates how to use the cognitive architecture for
dynamical autogenesis and advanced inference capabilities.
"""

import numpy as np
import time
from typing import Dict, List, Any

# Import the cognitive architecture
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hyperagentql import CognitiveArchitecture, ArchitectureMode


def create_complex_input_sequence(length: int, dimension: int) -> List[np.ndarray]:
    """Create a complex input sequence for testing."""
    sequence = []
    
    for i in range(length):
        t = i * 0.1
        
        # Multi-scale temporal patterns
        base_signal = np.sin(np.arange(dimension) * t * 0.1)
        harmonic = 0.5 * np.sin(np.arange(dimension) * t * 0.3)
        noise = 0.1 * np.random.randn(dimension)
        
        # Quaternion-inspired component
        if dimension >= 4:
            quat_component = np.zeros(dimension)
            quat_component[:4] = [np.cos(t), np.sin(t), np.cos(2*t), np.sin(2*t)]
            if dimension > 4:
                quat_component[4:] = np.tile(quat_component[:4], (dimension-4)//4 + 1)[:(dimension-4)]
        else:
            quat_component = np.zeros(dimension)
        
        # Combine components
        combined_input = base_signal + harmonic + noise + 0.2 * quat_component
        sequence.append(combined_input)
    
    return sequence


def main():
    """Main example execution."""
    print("=" * 60)
    print("HyperAgentQL Cognitive Architecture Example")
    print("=" * 60)
    
    # Initialize architecture
    print("Initializing cognitive architecture...")
    architecture = CognitiveArchitecture(
        base_dimension=64,
        toroidal_resolution=32,
        num_bootstrap_modules=6
    )
    print(f"Architecture initialized with {architecture.base_dimension}D base space")
    
    # Create input sequences
    print("\nGenerating input sequences...")
    bootstrap_sequence = create_complex_input_sequence(50, architecture.base_dimension)
    test_sequence = create_complex_input_sequence(10, architecture.base_dimension)
    print(f"Created bootstrap sequence: {len(bootstrap_sequence)} inputs")
    print(f"Created test sequence: {len(test_sequence)} inputs")
    
    # Run bootstrap analysis
    print("\nStarting bootstrap analysis...")
    bootstrap_result = architecture.bootstrap_architecture(
        num_bootstrap_steps=len(bootstrap_sequence),
        external_inputs=bootstrap_sequence
    )
    
    print(f"Bootstrap completed: {bootstrap_result['bootstrap_completed']}")
    print(f"Final phase: {bootstrap_result['final_phase']}")
    print(f"Final complexity: {bootstrap_result['final_complexity']:.3f}")
    print(f"Final stability: {bootstrap_result['final_stability']:.3f}")
    
    # Run inference analysis
    print("\nStarting inference analysis...")
    
    for i, input_data in enumerate(test_sequence):
        context = {
            'test_id': i,
            'input_type': 'complex_sequence',
            'timestamp': time.time()
        }
        
        result = architecture.infer(
            input_data,
            context=context,
            use_toroidal_modulation=True,
            use_hopf_projection=True
        )
        
        print(f"  Inference {i+1}/{len(test_sequence)}: "
              f"coherence={result['architecture_metrics']['global_coherence']:.3f}, "
              f"emergence={result['architecture_metrics']['emergence_level']:.3f}")
    
    # Final architecture summary
    print("\n" + "=" * 60)
    print("FINAL ARCHITECTURE SUMMARY")
    print("=" * 60)
    
    final_summary = architecture.get_architecture_summary()
    
    print(f"Architecture Mode: {final_summary['architecture_info']['current_mode']}")
    print(f"Total Iterations: {final_summary['architecture_info']['iteration']}")
    print(f"Global Coherence: {final_summary['current_state']['global_coherence']:.3f}")
    print(f"Emergence Level: {final_summary['current_state']['emergence_level']:.3f}")
    
    print(f"\nComponent Status:")
    print(f"  Toroidal Core: {final_summary['component_status']['toroidal_core']['num_feedback_channels']} feedback channels")
    print(f"  Hopf Fibrations: {final_summary['component_status']['hopf_fibrations']['num_tiers']} tiers")
    print(f"  Recursive Inference: {final_summary['component_status']['recursive_inference']['total_inferences']} inferences")
    
    if final_summary['component_status']['autogenesis_bootstrapper']:
        bootstrap_status = final_summary['component_status']['autogenesis_bootstrapper']
        print(f"  Autogenesis Bootstrap: {bootstrap_status['global_patterns']} patterns, {bootstrap_status['feedback_loops']} feedback loops")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("The cognitive architecture has demonstrated:")
    print("- Self-organization through autogenesis")
    print("- Multi-level recursive inference")
    print("- Toroidal feedback dynamics")
    print("- 4-tier Hopf fibration projections")
    print("- Emergent pattern formation")
    print("=" * 60)


if __name__ == "__main__":
    main()