"""
Command Line Interface for HyperAgentQL Cognitive Architecture

Provides interactive access to the cognitive architecture for 
dynamical autogenesis and inference operations.
"""

import argparse
import numpy as np
import sys
import json
import time
from typing import Optional, Dict, Any

from .cognitive_architecture import CognitiveArchitecture, ArchitectureMode
from .recursive_inference import RecursionLevel
from .autogenesis import BootstrapPhase


def create_demo_input(input_type: str = "random", size: int = 64) -> np.ndarray:
    """Create demo input for testing the architecture."""
    if input_type == "random":
        return np.random.randn(size) * 0.5
    
    elif input_type == "structured":
        # Create structured input with patterns
        x = np.linspace(0, 4*np.pi, size)
        signal = np.sin(x) + 0.5*np.sin(3*x) + 0.25*np.sin(5*x)
        return signal + np.random.randn(size) * 0.1
    
    elif input_type == "quaternion":
        # Quaternion-inspired input
        if size >= 4:
            quat = np.array([1, 0, 0, 0])  # Identity quaternion
            result = np.tile(quat, size // 4 + 1)[:size]
            return result + np.random.randn(size) * 0.05
        else:
            return np.ones(size)
    
    elif input_type == "toroidal":
        # Toroidal-inspired input
        u = np.linspace(0, 2*np.pi, size)
        torus_signal = np.sin(u) * np.cos(2*u)
        return torus_signal + np.random.randn(size) * 0.1
    
    else:
        return np.random.randn(size) * 0.5


def run_bootstrap_demo(architecture: CognitiveArchitecture, 
                      num_steps: int = 100,
                      input_type: str = "structured") -> Dict[str, Any]:
    """Run a bootstrap demonstration."""
    print(f"\\n=== Bootstrap Demo ({num_steps} steps) ===")
    print(f"Input type: {input_type}")
    print(f"Architecture dimensions: {architecture.base_dimension}")
    
    # Generate external inputs for bootstrap
    external_inputs = []
    for i in range(num_steps):
        input_signal = create_demo_input(input_type, architecture.base_dimension)
        # Add some variation
        input_signal += np.sin(i * 0.1) * 0.1
        external_inputs.append(input_signal)
    
    # Run bootstrap
    start_time = time.time()
    bootstrap_result = architecture.bootstrap_architecture(
        num_bootstrap_steps=num_steps,
        external_inputs=external_inputs
    )
    end_time = time.time()
    
    print(f"\\nBootstrap completed in {end_time - start_time:.2f} seconds")
    print(f"Final phase: {bootstrap_result['final_phase']}")
    print(f"Final complexity: {bootstrap_result['final_complexity']:.3f}")
    print(f"Final stability: {bootstrap_result['final_stability']:.3f}")
    print(f"Steps completed: {bootstrap_result['steps_completed']}")
    
    return bootstrap_result


def run_inference_demo(architecture: CognitiveArchitecture,
                      num_inferences: int = 10,
                      input_type: str = "structured") -> List[Dict[str, Any]]:
    """Run inference demonstrations."""
    print(f"\\n=== Inference Demo ({num_inferences} inferences) ===")
    print(f"Input type: {input_type}")
    
    results = []
    
    for i in range(num_inferences):
        print(f"\\nInference {i+1}/{num_inferences}")
        
        # Create test input
        input_data = create_demo_input(input_type, architecture.base_dimension)
        
        # Add context
        context = {
            'inference_id': i,
            'timestamp': time.time(),
            'input_type': input_type
        }
        
        # Perform inference
        start_time = time.time()
        result = architecture.infer(
            input_data, 
            context=context,
            use_toroidal_modulation=True,
            use_hopf_projection=True
        )
        end_time = time.time()
        
        # Display results
        print(f"  Inference time: {end_time - start_time:.4f}s")
        print(f"  Global coherence: {result['architecture_metrics']['global_coherence']:.3f}")
        print(f"  Emergence level: {result['architecture_metrics']['emergence_level']:.3f}")
        print(f"  Output norm: {np.linalg.norm(result['primary_output']):.3f}")
        
        # Show component contributions
        contrib = result['component_contributions']
        print(f"  Contributions - Toroidal: {contrib['toroidal_contribution']:.3f}, "
              f"Hopf: {contrib['hopf_contribution']:.3f}, "
              f"Bootstrap: {contrib['bootstrap_contribution']:.3f}")
        
        results.append(result)
    
    return results


def run_integrated_demo(architecture: CognitiveArchitecture) -> Dict[str, Any]:
    """Run a complete integrated demonstration."""
    print("\\n=== Integrated Cognitive Architecture Demo ===")
    
    # Phase 1: Bootstrap
    print("\\nPhase 1: Bootstrapping the architecture...")
    bootstrap_result = run_bootstrap_demo(architecture, num_steps=150, input_type="structured")
    
    # Phase 2: Inference demonstrations
    print("\\nPhase 2: Running inference demonstrations...")
    inference_results = []
    
    # Test different input types
    input_types = ["structured", "quaternion", "toroidal", "random"]
    
    for input_type in input_types:
        print(f"\\nTesting with {input_type} input...")
        results = run_inference_demo(architecture, num_inferences=3, input_type=input_type)
        inference_results.extend(results)
    
    # Phase 3: Architecture analysis
    print("\\nPhase 3: Architecture analysis...")
    summary = architecture.get_architecture_summary()
    
    print(f"\\nArchitecture Summary:")
    print(f"  Current mode: {summary['architecture_info']['current_mode']}")
    print(f"  Total iterations: {summary['architecture_info']['iteration']}")
    print(f"  Global coherence: {summary['current_state']['global_coherence']:.3f}")
    print(f"  Emergence level: {summary['current_state']['emergence_level']:.3f}")
    print(f"  Patterns detected: {summary['emergence_tracking']['patterns_detected_count']}")
    
    # Component status
    print(f"\\nComponent Status:")
    print(f"  Toroidal feedback channels: {summary['component_status']['toroidal_core']['num_feedback_channels']}")
    print(f"  Hopf fibration tiers: {summary['component_status']['hopf_fibrations']['num_tiers']}")
    print(f"  Recursive inference history: {summary['component_status']['recursive_inference']['total_inferences']}")
    
    if summary['component_status']['autogenesis_bootstrapper']:
        bootstrap_status = summary['component_status']['autogenesis_bootstrapper']
        print(f"  Bootstrap patterns: {bootstrap_status['global_patterns']}")
        print(f"  Bootstrap feedback loops: {bootstrap_status['feedback_loops']}")
    
    return {
        'bootstrap_result': bootstrap_result,
        'inference_results': inference_results,
        'architecture_summary': summary
    }


def save_results(results: Dict[str, Any], filename: str = "hyperagentql_results.json"):
    """Save demo results to file."""
    # Convert numpy arrays to lists for JSON serialization
    def convert_numpy(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_numpy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy(item) for item in obj]
        else:
            return obj
    
    converted_results = convert_numpy(results)
    
    with open(filename, 'w') as f:
        json.dump(converted_results, f, indent=2, default=str)
    
    print(f"\\nResults saved to {filename}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="HyperAgentQL Cognitive Architecture CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Run full integrated demo
  hyperagentql --demo integrated
  
  # Run bootstrap only
  hyperagentql --demo bootstrap --steps 200
  
  # Run inference only (requires bootstrapped architecture)
  hyperagentql --demo inference --num-inferences 5
  
  # Custom architecture dimensions
  hyperagentql --demo integrated --base-dim 128 --toroidal-res 64
  
  # Save results to file
  hyperagentql --demo integrated --output results.json
        '''
    )
    
    parser.add_argument('--demo', choices=['bootstrap', 'inference', 'integrated'],
                       default='integrated', help='Type of demo to run')
    
    parser.add_argument('--base-dim', type=int, default=64,
                       help='Base dimension for the architecture')
    
    parser.add_argument('--toroidal-res', type=int, default=32,
                       help='Resolution for toroidal core')
    
    parser.add_argument('--bootstrap-modules', type=int, default=6,
                       help='Number of bootstrap modules')
    
    parser.add_argument('--steps', type=int, default=100,
                       help='Number of bootstrap steps')
    
    parser.add_argument('--num-inferences', type=int, default=5,
                       help='Number of inference demonstrations')
    
    parser.add_argument('--input-type', choices=['random', 'structured', 'quaternion', 'toroidal'],
                       default='structured', help='Type of input to use')
    
    parser.add_argument('--output', type=str, help='Output file for results')
    
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 60)
    print("HyperAgentQL: Cognitive Architecture for Dynamical Autogenesis")
    print("=" * 60)
    print(f"Base dimension: {args.base_dim}")
    print(f"Toroidal resolution: {args.toroidal_res}")
    print(f"Bootstrap modules: {args.bootstrap_modules}")
    
    # Initialize architecture
    print("\\nInitializing cognitive architecture...")
    try:
        architecture = CognitiveArchitecture(
            base_dimension=args.base_dim,
            toroidal_resolution=args.toroidal_res,
            num_bootstrap_modules=args.bootstrap_modules
        )
        print("Architecture initialized successfully!")
    except Exception as e:
        print(f"Error initializing architecture: {e}")
        sys.exit(1)
    
    # Run requested demo
    try:
        if args.demo == 'bootstrap':
            results = run_bootstrap_demo(architecture, args.steps, args.input_type)
        
        elif args.demo == 'inference':
            # For inference-only demo, do a quick bootstrap first
            print("\\nPerforming quick bootstrap for inference demo...")
            architecture.bootstrap_architecture(num_bootstrap_steps=50)
            results = run_inference_demo(architecture, args.num_inferences, args.input_type)
        
        elif args.demo == 'integrated':
            results = run_integrated_demo(architecture)
        
        else:
            print(f"Unknown demo type: {args.demo}")
            sys.exit(1)
        
        # Save results if requested
        if args.output:
            save_results(results, args.output)
        
        print("\\n" + "=" * 60)
        print("Demo completed successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\\n\\nDemo interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\\nError during demo: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()