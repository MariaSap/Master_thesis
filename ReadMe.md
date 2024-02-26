# Upper Arm Neuromuscular Model Simulation

This Python project, implemented in Python 3.9, simulates an upper arm neuromuscular model using the MuJoCo physics engine (version 2.1). The simulation involves a 26-muscle upper arm model with four different arm configurations defined by activation muscle vectors. External forces are applied at different angles when the arm reaches equilibrium for each configuration. The simulation results, including position, velocity, and other relevant information, are saved in CSV files.

## Prerequisites

- Python 3.9
- MuJoCo Physics Engine (version 2.1)
- PyCharm (Version 2021.2.1, JetBrains, Prague, Czech Republic)
- Anaconda environment

## Project Structure

- bm_model.xml: MuJoCo XML file defining the arm model.

- simulation.py: The main simulation script. It implements the upper arm neuromuscular model simulation. The simulation parameters, such as the XML model file, simulation time, and print configurations, can be adjusted within the script.
- analyze_simulation.m: MATLAB script for post-processing the simulation results  stored in CSV files.


## MuJoCo Data Structures

The simulation utilizes MuJoCo data structures for modeling, data storage, and visualization. It includes a visualization window with mouse and keyboard interactions for controlling the simulation view. 

## Data Logging

The simulation logs various data into CSV files, including:
- Position and force information (`xpos_*.csv`).
- Joint positions and muscle activations (`qpos_*.csv`).
- Joint velocities (`qvel_*.csv`).
- Sensor data (`sensors*.csv` and `sensorsMaria*.csv`).

All the aforementioned files refer to data emerging from _elv_angle_, _shoulder_elv_, _shoulder_rot_, _elbow_flexion_ and _pro_sup_ joints. 

## How to Run

1. Set up the required environment and dependencies.
2. Run the `Simulation.py` script.
3. After the simulation completes, run the `main.m` MATLAB script to analyze the results. 

## Additional Notes

### Python Script
- Force magnitudes are defined in _force_vector_ (see line 304).
- Arm configuations are defined by activation muscle vectors (see lines 366-380, alternatively).
- Detect joints' violation of the torque limits (see lines 116-125 and `def detect_joint_limit_violation`, lines 195-205).
- The project uses GLFW for initializing and handling the window and user input.
- Camera configurations are printed for initializing the view of the model (see lines 12, 348-351).

### Matlab Script
- Directory exploration & file selection and reading of CSV files (see lines 36-92).
- Check joint limits and do not counf any case of joint that exceeds 8 Nm (see lines 159-163).
- Stiffness ellipsoids from different perturbation levels are divived into two batches for clearer visualization.
- Orientation, area and shape of the stiffness ellipsoids are calculated (see lines 389-397). 
- R-squared values indicate the appropriateness of fit of the ellipsoids and indicate how well the characteristics could be explained using the stiffness ellipse representation.

### MuJoCo XML File
The neuromuscular model was derived from Ikkala et al. (https://doi.org/10.1145/3526113.3545689).
- It is a rigid-body arm model that contains 26 Hill-type muscle actuators with non-elastic tendons, 17 segments, and has five degrees of freedom (DOFs) 
- Addition to the original version: detection the violation of joint limits (see lines 667-673).