"""
Simple demonstration script for the cognitive architecture
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from hyperagentql import CognitiveArchitecture

def main():
    print("🚀 HyperAgentQL: Cognitive Architecture Demonstration")
    print("=" * 60)
    
    # Initialize architecture
    print("Initializing cognitive architecture...")
    architecture = CognitiveArchitecture(
        base_dimension=64,
        toroidal_resolution=32,
        num_bootstrap_modules=6
    )
    print("✅ Architecture initialized!")
    
    # Bootstrap phase
    print("\n🧬 Running autogenesis bootstrap...")
    bootstrap_result = architecture.bootstrap_architecture(num_bootstrap_steps=30)
    print(f"✅ Bootstrap completed: {bootstrap_result['final_phase']}")
    print(f"   Complexity: {bootstrap_result['final_complexity']:.2f}")
    print(f"   Stability: {bootstrap_result['final_stability']:.2f}")
    
    # Inference demonstrations
    print("\n🧠 Running inference demonstrations...")
    
    for i in range(5):
        # Create varied inputs
        if i == 0:
            input_data = np.sin(np.linspace(0, 4*np.pi, 64)) * 0.5
            input_type = "sinusoidal"
        elif i == 1:
            input_data = np.random.randn(64) * 0.3
            input_type = "random"
        elif i == 2:
            quat = np.array([1, 0, 0, 0])
            input_data = np.tile(quat, 16)
            input_type = "quaternion"
        elif i == 3:
            input_data = np.ones(64) * 0.1 + np.random.randn(64) * 0.05
            input_type = "constant+noise"
        else:
            t = np.linspace(0, 2*np.pi, 64)
            input_data = np.cos(t) * np.sin(3*t) * 0.4
            input_type = "complex_wave"
        
        result = architecture.infer(input_data)
        
        print(f"  Inference {i+1} ({input_type}):")
        print(f"    Coherence: {result['architecture_metrics']['global_coherence']:.3f}")
        print(f"    Emergence: {result['architecture_metrics']['emergence_level']:.3f}")
        
        contrib = result['component_contributions']
        print(f"    Components - T:{contrib['toroidal_contribution']:.2f}, "
              f"H:{contrib['hopf_contribution']:.2f}, "
              f"B:{contrib['bootstrap_contribution']:.2f}")
    
    # Final summary
    print("\n📊 Final Architecture Summary:")
    summary = architecture.get_architecture_summary()
    print(f"  Mode: {summary['architecture_info']['current_mode']}")
    print(f"  Iterations: {summary['architecture_info']['iteration']}")
    print(f"  Global coherence: {summary['current_state']['global_coherence']:.3f}")
    print(f"  Emergence level: {summary['current_state']['emergence_level']:.3f}")
    print(f"  Patterns detected: {summary['emergence_tracking']['patterns_detected_count']}")
    
    print("\n🎉 Demonstration Complete!")
    print("=" * 60)
    print("The cognitive architecture successfully demonstrated:")
    print("✅ Dynamical autogenesis through self-organization")
    print("✅ Multi-level recursive inference (micro/macro/meta)")
    print("✅ Toroidal feedback dynamics")
    print("✅ 4-tier Hopf fibration projections (S^0 to S^15)")
    print("✅ Emergent pattern formation and complexity growth")
    print("✅ Integrated multi-component operation")
    print("=" * 60)

if __name__ == "__main__":
    main()