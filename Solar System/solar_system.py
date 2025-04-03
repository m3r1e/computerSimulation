from typing import List
import json
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
import tqdm

# Load in the data from the data file as a dictionary (?)

with open("Solar System/parameters_solar.json", "r") as f:
    config = json.load(f)


# Set the constant used throughout by reading from config

G = config['grav_const']  
SUN_MASS = config['bodies'][0]['mass']
dt = config["timestep"]  
num_steps = config["num_iterations"]
total_time = int(num_steps * dt)

class Planet:
    '''
    Defines a planet and has methods for computing acceleration, updating position and velocity, and checking the orbital radius.
    '''
    def __init__(self, name, mass, orbital_radius, colour, integration_method):
        self.name = name
        self.mass = mass
        self.orbital_radius = orbital_radius  
        self.colour = colour
        self.pos = np.array([self.orbital_radius, 0], dtype=np.float64) # Store position as an array
        # Set initial velocity with an if statement to avoid division by zero
        if name != 'sun': 
            self.v = np.array([0, math.sqrt(G * (SUN_MASS) / self.orbital_radius)], dtype=np.float64)
        else:
            self.v = np.array([0,0], dtype=np.float64)
        # For storing the previous two accelerations and velocities, for use in integration implemenatation
        self.prev_as = np.array([[0,0],[0,0]], dtype=np.float64)
        self.prev_vs = np.array([[0,0],[0,0]], dtype=np.float64)

        self.orbital_period = None
        self.positions = [self.pos] # Store all positions
        self.integration_method = integration_method # To determine the method to execute, for experiment 2
        self.planetary_alignments = [] # To store time instances of planetary alignment
    
    def compute_acceleration(self, bodies):
        '''
        Takes the planets and their attributes as a lsit, and returns the total acceleration on one planet
        '''
        masses = np.array([other.mass for other in bodies if other is not self]) # Masses of all planets except itself
        other_matrix = np.stack([other.pos for other in bodies if other is not self]) # Creating a matrix of the planet positions 
        diff_vector = other_matrix - self.pos
        distances = np.linalg.norm(diff_vector, axis=-1)
        accelerations = G * masses / distances**3 # Acceleration on the planet due to every other planet 
        total_acceleration = np.sum(diff_vector*np.expand_dims(accelerations, -1), axis=0) # Sum these individual accelerations for the total acceleration vector
        return total_acceleration     

    def update_position(self):  
        '''
        Updates the position of a planet for either Beeman or Direct Euler
        '''
        if self.integration_method == 'beeman':
            new_pos = self.pos + self.v*dt + 1/6 * dt**2 * (4 * self.prev_as[1] - self.prev_as[0]) # Applying Beeman
            self.positions.append(new_pos) # Appending to the array of all positions
            self.pos = new_pos # Redefine current position
        elif self.integration_method == 'direct-euler':
            new_pos = self.pos + self.v * dt # Applying Direct Euler
            self.positions.append(new_pos)
            self.pos = new_pos
        else:
            pass

    def update_position_euler_cromer(self, new_v): #self.v instead of new.v
        '''
        Updates the position of a planet for the Euler Cromer Integration Method
        '''
        new_pos = self.pos + new_v * dt
        self.positions.append(new_pos)
        self.pos = new_pos

    def update_velocity(self, new_a):
        '''
        Updates the velocity of the planet 
        '''
        # Update according to each integration method
        if self.integration_method == 'beeman':
            self.v += 1/6 * dt * (2 * new_a + 5 * self.prev_as[1] - self.prev_as[0])
        elif self.integration_method == 'euler-cromer':
            self.v += new_a * dt
        elif self.integration_method == 'direct-euler':
            self.v += new_a * dt
        return self.v
    
    # Experiment 1 - Orbital Periods

    def check_orbital_period(self, sun):
        rotation = 0 #  Initialise the rotation about the sun
        for i in range(1, num_steps):
            # Reposition the position vectors to account for sun movement
            repositioned_prev = self.positions[i-1] - sun.positions[i-1]
            repositioned_curr = self.positions[i] - sun.positions[i]
            # Calculate the angle travelled in a timestep
            angle = np.arccos((np.dot(repositioned_curr, repositioned_prev)) / (np.linalg.norm(repositioned_curr) * np.linalg.norm(repositioned_prev)))
            rotation += angle # Add this angle to the total rotation
            if rotation >= 2 * np.pi:       
                self.orbital_period = i * dt # Record the first time at which we pass 2pi
                break
        
class Simulation:
    def __init__(self, dt, total_time, num_steps, bodies: List[Planet]):
        self.dt = dt  # Time step in seconds
        self.total_time = total_time  # Total simulation time
        self.num_steps = num_steps
        self.bodies = bodies
        self.energy_log = [] # To record the system energies
        self.planetary_alignments = [] # To store occurrences of planetary alignment

    def compute_total_energy(self): 
        '''
        Compute the total energy of the system for some time instance
        '''
        # KE = 1/2 * mass * velocity^2
        kinetic_energy = sum(0.5 * p.mass * (np.dot(p.v, p.v)) for p in self.bodies) 
        potential_energy = 0 # Initialise a variable to store PE
        # Iterate over all bodies
        for i, p1 in enumerate(self.bodies):
            for j, p2 in enumerate(self.bodies):
                if i < j:  # Avoid double-counting
                    r = np.linalg.norm(p1.pos - p2.pos) # Distance
                    # Calculate GPE
                    potential_energy += -G * p1.mass * p2.mass / r
        return kinetic_energy + potential_energy
    
    def simulate(self):
        '''
        Execute the simulation, i.e. move the planets 
        '''
        for step in tqdm.tqdm(range(self.num_steps)):
            time = step * dt # Time in years
            for p in self.bodies:
                # Set the previous acceleration for each planet before any have been updated 
                p.prev_as[1] = p.compute_acceleration(self.bodies)
            if self.bodies[0].integration_method == 'beeman':
                # First update the position for all bodies
                for p in self.bodies:
                    p.update_position()
                for p in self.bodies:
                    # Calculate acceleration now that the positions have updated
                    new_a = p.compute_acceleration(self.bodies)
                    # Update velocity using this new acceleration
                    p.update_velocity(new_a)
                    # Update the prev_as list 
                    p.prev_as[0] = p.prev_as[1]
            else: # Simulate for Euler Cromer / Direct Euler
                for p in self.bodies:
                    if p.integration_method == 'direct-euler': # Direct Euler
                        # First update the position
                        p.update_position() 
                        # Then update the velocity 
                        p.update_velocity(p.prev_as[1])
                    else: # euler cromer
                        # First update the velocity 
                        new_v = p.update_velocity(p.prev_as[1])
                        # Then update the position using this velocity
                        p.update_position_euler_cromer(new_v)
            # Log total system energy every 100 steps
            if step % 100 == 0:
                self.energy_log.append((time, self.compute_total_energy()))

        # Find the orbital period of each planet for experiment 1
        for p in self.bodies:
            if p.name != 'sun':
                p.check_orbital_period(self.bodies[0])

    # Experiment 4 - Planetary Alignments 

    def planetary_alignment(self):
        '''
        Determine the years at which alignment of the five innermost planets occurs.
        '''
        # Obtain the five innermost planets and the Sun
        innermost_five = self.bodies[1:6]   
        sun = self.bodies[0]
        colours = [p.colour for p in innermost_five]
        labels = [p.name for p in self.bodies[:6]]
        
        for i in range(1, num_steps):
            # Obtain the position vectors for the planets and adjust for Sun movement
            vectors = np.array([(p.positions[i] - sun.positions[i]) for p in innermost_five])
            # Find the mean of these vectors
            mean_vector = np.mean(vectors, axis=0)
            
            if np.linalg.norm(mean_vector) == 0:
                continue  # Skip this step if the mean vector is zero
            
            # Normalise this mean vector
            mean_unit_vector = mean_vector / np.linalg.norm(mean_vector)
            line_direction = mean_unit_vector
            # Normalise the position vectors
            normalised_vectors = vectors / np.linalg.norm(vectors, axis=1)[:, np.newaxis]
            a, b = line_direction
            # Perpendicular distance between the line and the normaalised points
            distances = np.abs(normalised_vectors[:, 0] * b - normalised_vectors[:, 1] * a) / np.linalg.norm(line_direction)
            if all(distance <= np.sin(np.pi / 36) for distance in distances): # Limit on distance corresponds to angular limit
                self.planetary_alignments.append(i * dt) # Gives time in years
                # Plot the alignment instance 
                pos_x = [v[0] for v in vectors]
                pos_y = [v[1] for v in vectors]
                plt.xlim(-5.5, 5.5)
                plt.ylim(-5.5, 5.5)
                plt.title(f'Planetary Alignment at {i*dt:.2f} years')
                # Include the mean line we find the distance from
                plt.axline((0,0), mean_vector, linestyle='--', c='black', linewidth=0.5)
                plt.scatter(pos_x, pos_y, c=colours)
                plt.scatter([0], [0], c=sun.colour)
                legend_handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=col, markersize=10, label=lab) 
                      for col, lab in zip([sun.colour]+colours, labels)]
                plt.legend(handles=legend_handles)
                plt.show()
        