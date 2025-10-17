"""
Toroidal Core Implementation for the Cognitive Architecture

The toroidal core serves as the geometric foundation for the feedback loops
and recursive inference mechanisms. It provides the topological structure
where information flows in cycles while maintaining stability.
"""

import numpy as np
from typing import List, Tuple, Dict, Any, Optional
import networkx as nx
from scipy.integrate import solve_ivp
import torch


class ToroidalCore:
    """
    Toroidal core structure that provides the geometric foundation for
    the cognitive architecture's feedback loops and recursive processing.
    """
    
    def __init__(self, major_radius: float = 2.0, minor_radius: float = 1.0, 
                 resolution: int = 64):
        self.major_radius = major_radius  # R - distance from center of tube to center of torus
        self.minor_radius = minor_radius  # r - radius of the tube
        self.resolution = resolution
        
        # Toroidal coordinates and topology
        self.coordinate_system = self._initialize_coordinates()
        self.topology_graph = self._create_topology_graph()
        self.flow_field = self._initialize_flow_field()
        
        # Feedback loop structures
        self.feedback_channels = self._create_feedback_channels()
        self.resonance_modes = self._compute_resonance_modes()
        
    def _initialize_coordinates(self) -> Dict[str, np.ndarray]:
        """Initialize toroidal coordinate system (u, v) -> (x, y, z)."""
        u = np.linspace(0, 2*np.pi, self.resolution)  # Major circle parameter
        v = np.linspace(0, 2*np.pi, self.resolution)  # Minor circle parameter
        
        U, V = np.meshgrid(u, v)
        
        # Toroidal coordinates
        x = (self.major_radius + self.minor_radius * np.cos(V)) * np.cos(U)
        y = (self.major_radius + self.minor_radius * np.cos(V)) * np.sin(U)
        z = self.minor_radius * np.sin(V)
        
        return {
            'u': U,
            'v': V, 
            'x': x,
            'y': y,
            'z': z,
            'u_vals': u,
            'v_vals': v
        }
    
    def _create_topology_graph(self) -> nx.Graph:
        """Create a graph representing the toroidal topology."""
        G = nx.Graph()
        
        # Add nodes for each coordinate point
        for i in range(self.resolution):
            for j in range(self.resolution):
                node_id = i * self.resolution + j
                u_idx, v_idx = i, j
                
                # Add node with position and toroidal coordinates
                G.add_node(node_id, 
                          u_idx=u_idx, 
                          v_idx=v_idx,
                          pos=(self.coordinate_system['x'][i,j], 
                               self.coordinate_system['y'][i,j], 
                               self.coordinate_system['z'][i,j]))
        
        # Add edges for toroidal connectivity
        for i in range(self.resolution):
            for j in range(self.resolution):
                current = i * self.resolution + j
                
                # Connect to neighbors with toroidal wrapping
                next_u = ((i + 1) % self.resolution) * self.resolution + j
                next_v = i * self.resolution + ((j + 1) % self.resolution)
                
                G.add_edge(current, next_u, weight=1.0, edge_type='u_direction')
                G.add_edge(current, next_v, weight=1.0, edge_type='v_direction')
        
        return G
    
    def _initialize_flow_field(self) -> Dict[str, np.ndarray]:
        """Initialize the flow field on the torus for information circulation."""
        u_flow = np.zeros((self.resolution, self.resolution))
        v_flow = np.zeros((self.resolution, self.resolution))
        
        # Create spiral flow patterns for information circulation
        for i in range(self.resolution):
            for j in range(self.resolution):
                u_norm = self.coordinate_system['u_vals'][i] / (2*np.pi)
                v_norm = self.coordinate_system['v_vals'][j] / (2*np.pi)
                
                # Spiral flow with phase coupling
                u_flow[i, j] = np.sin(2*np.pi*u_norm + np.pi*v_norm) * 0.5
                v_flow[i, j] = np.cos(2*np.pi*v_norm + np.pi*u_norm) * 0.5
        
        return {
            'u_component': u_flow,
            'v_component': v_flow,
            'magnitude': np.sqrt(u_flow**2 + v_flow**2)
        }
    
    def _create_feedback_channels(self) -> List[Dict[str, Any]]:
        """Create multiple feedback channels with different characteristics."""
        channels = []
        
        # Channel 1: Fast local feedback
        channels.append({
            'name': 'local_fast',
            'time_scale': 0.1,
            'spatial_scale': 'local',
            'coupling_strength': 0.8,
            'nonlinearity': lambda x: np.tanh(x)
        })
        
        # Channel 2: Medium-range coupling
        channels.append({
            'name': 'medium_coupling', 
            'time_scale': 1.0,
            'spatial_scale': 'medium',
            'coupling_strength': 0.5,
            'nonlinearity': lambda x: x / (1 + x**2)
        })
        
        # Channel 3: Global slow feedback
        channels.append({
            'name': 'global_slow',
            'time_scale': 10.0,
            'spatial_scale': 'global',
            'coupling_strength': 0.3,
            'nonlinearity': lambda x: np.sin(x)
        })
        
        # Channel 4: Cross-dimensional feedback
        channels.append({
            'name': 'cross_dimensional',
            'time_scale': 5.0,
            'spatial_scale': 'cross',
            'coupling_strength': 0.6,
            'nonlinearity': lambda x: x**3 - x
        })
        
        return channels
    
    def _compute_resonance_modes(self) -> Dict[str, np.ndarray]:
        """Compute resonance modes of the toroidal structure."""
        modes = {}
        
        # Fundamental toroidal modes (m, n) where m = poloidal, n = toroidal
        for m in range(1, 4):  # poloidal mode number
            for n in range(1, 4):  # toroidal mode number
                mode_name = f"mode_{m}_{n}"
                
                # Compute mode shape
                mode_shape = np.zeros((self.resolution, self.resolution))
                for i in range(self.resolution):
                    for j in range(self.resolution):
                        u = self.coordinate_system['u_vals'][i]
                        v = self.coordinate_system['v_vals'][j]
                        
                        mode_shape[i, j] = np.cos(m * u) * np.cos(n * v)
                
                modes[mode_name] = mode_shape
        
        return modes
    
    def evolve_state(self, initial_state: np.ndarray, time_span: Tuple[float, float], 
                    feedback_params: Optional[Dict[str, float]] = None) -> np.ndarray:
        """Evolve a state on the torus through the feedback dynamics."""
        if feedback_params is None:
            feedback_params = {'coupling': 1.0, 'damping': 0.1}
        
        def torus_dynamics(t: float, state: np.ndarray) -> np.ndarray:
            """Dynamics function for the toroidal system."""
            # Reshape state to 2D grid
            state_2d = state.reshape((self.resolution, self.resolution))
            
            # Compute spatial derivatives with periodic boundary conditions
            du_state = np.roll(state_2d, -1, axis=0) - np.roll(state_2d, 1, axis=0)
            dv_state = np.roll(state_2d, -1, axis=1) - np.roll(state_2d, 1, axis=1)
            
            # Apply flow field
            flow_term = (self.flow_field['u_component'] * du_state + 
                        self.flow_field['v_component'] * dv_state)
            
            # Feedback terms from different channels
            feedback_sum = np.zeros_like(state_2d)
            for channel in self.feedback_channels:
                coupling = feedback_params.get('coupling', 1.0) * channel['coupling_strength']
                nonlin = channel['nonlinearity']
                scale = channel['time_scale']
                
                feedback_sum += coupling * nonlin(state_2d) / scale
            
            # Damping term
            damping = feedback_params.get('damping', 0.1)
            
            # Complete dynamics
            dstate_dt = flow_term + feedback_sum - damping * state_2d
            
            return dstate_dt.flatten()
        
        # Solve the ODE
        sol = solve_ivp(torus_dynamics, time_span, initial_state.flatten(), 
                       method='RK45', dense_output=True)
        
        return sol.y.reshape((self.resolution, self.resolution, -1))
    
    def compute_information_flow(self, state: np.ndarray) -> Dict[str, np.ndarray]:
        """Compute information flow patterns on the torus."""
        # Gradient of the state (information density gradient)
        grad_u = np.gradient(state, axis=0)
        grad_v = np.gradient(state, axis=1)
        
        # Information flow follows negative gradient (flows toward higher information)
        info_flow_u = -grad_u * self.flow_field['u_component']
        info_flow_v = -grad_v * self.flow_field['v_component']
        
        # Compute divergence (information sources/sinks)
        div_u = np.gradient(info_flow_u, axis=0)
        div_v = np.gradient(info_flow_v, axis=1)
        divergence = div_u + div_v
        
        # Compute curl (rotational information flow)
        curl = np.gradient(info_flow_v, axis=0) - np.gradient(info_flow_u, axis=1)
        
        return {
            'flow_u': info_flow_u,
            'flow_v': info_flow_v,
            'divergence': divergence,
            'curl': curl,
            'magnitude': np.sqrt(info_flow_u**2 + info_flow_v**2)
        }
    
    def project_to_resonance_mode(self, state: np.ndarray, mode_name: str) -> float:
        """Project state onto a specific resonance mode."""
        if mode_name not in self.resonance_modes:
            raise ValueError(f"Unknown resonance mode: {mode_name}")
        
        mode = self.resonance_modes[mode_name]
        
        # Compute projection (inner product)
        projection = np.sum(state * mode) / np.sum(mode * mode)
        
        return projection
    
    def get_toroidal_distance(self, point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
        """Compute distance between two points on the torus."""
        i1, j1 = point1
        i2, j2 = point2
        
        # Get 3D coordinates
        x1 = self.coordinate_system['x'][i1, j1]
        y1 = self.coordinate_system['y'][i1, j1]
        z1 = self.coordinate_system['z'][i1, j1]
        
        x2 = self.coordinate_system['x'][i2, j2]
        y2 = self.coordinate_system['y'][i2, j2]
        z2 = self.coordinate_system['z'][i2, j2]
        
        # Euclidean distance in 3D
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
        
        return distance
    
    def create_feedback_loop(self, source_region: List[Tuple[int, int]], 
                           target_region: List[Tuple[int, int]], 
                           delay: float = 0.0) -> Dict[str, Any]:
        """Create a specific feedback loop between regions."""
        loop = {
            'source_region': source_region,
            'target_region': target_region,
            'delay': delay,
            'connection_weights': []
        }
        
        # Compute connection weights based on toroidal distances
        for src in source_region:
            for tgt in target_region:
                distance = self.get_toroidal_distance(src, tgt)
                weight = np.exp(-distance / self.minor_radius)  # Exponential decay
                loop['connection_weights'].append((src, tgt, weight))
        
        return loop
    
    def visualize_torus_state(self, state: np.ndarray) -> Dict[str, np.ndarray]:
        """Prepare data for visualizing the state on the torus."""
        return {
            'x': self.coordinate_system['x'],
            'y': self.coordinate_system['y'], 
            'z': self.coordinate_system['z'],
            'state': state,
            'u': self.coordinate_system['u'],
            'v': self.coordinate_system['v']
        }