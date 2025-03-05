import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class CelestialBody:
    def __init__(self, name, mass, position, velocity):
        self.mass = mass 
        self.name = name
        self.position = np.array(position, dtype=float) 
        self.velocity = np.array(velocity, dtype=float)

class OrbitalMotion:
    def __init__(self, bodies, dt):
        self.dt = dt #time step
        self.bodies = bodies #list of celestial bodies in the system
        self.G = 6.67430e-11 #gravitational constant
        self.positions = {body.name: [] for body in bodies} #dictionary to store positions over time
        self.kinetic_energies = [] #list to store KE at every time step

    def acceleration(self, body):
        '''
        Compute the acceleration on a body due to gravitational forces from all other bodies
        '''
        acceleration = np.zeros(2) #acceleration vector (initially zero)
        for thing in self.bodies:
            if thing != body:
                r = thing.position - body.position #displacement vector
                distance = np.linalg.norm(r) #magnitude of distance
                acceleration += self.G * thing.mass * r / distance**3 #applying gravitational acceleration formula
        return acceleration

    def kinetic_energy(self):
        '''
        Compute the total kinetic energy in the system
        '''
        return sum(0.5 * body.mass * np.linalg.norm(body.velocity)**2 for body in self.bodies) 

    def update(self):
        '''
        At each timestep, update the positions & velocities of all celestial bodies using Euler integration
        '''
        accelerations = {body.name: self.acceleration(body) for body in self.bodies} #compute accelerations for all bodies
        for body in self.bodies: #update velocity and position for each body
            body.velocity += accelerations[body.name] * self.dt 
            body.position += body.velocity * self.dt
            self.positions[body.name].append(body.position.copy()) #store the updated position
        self.kinetic_energies.append(self.kinetic_energy()) #store kinetic energy 
    
    def simulate(self, num_steps):
        '''
        Run the simulation for a given number of steps (num_steps)
        '''
        for _ in range(num_steps):
            self.update()
        return {name: np.array(pos) for name, pos in self.positions.items()}, np.array(self.kinetic_energies)
        #dictionary of positions for every celestial body and a list of kinetic energies over time

#defining mass, distance beteen mars and phobos, and speed
mars_mass = 6.4171e23
phobos_mass = 1.0659e16
distance_phobos_mars = 9378000
orbital_speed_phobos = 2138
orbital_speed_mars = (phobos_mass / mars_mass) * orbital_speed_phobos  


#create the celestial body objects
mars = CelestialBody("Mars", mars_mass, [0 * distance_phobos_mars, 0], [0, orbital_speed_mars])
phobos = CelestialBody("Phobos", phobos_mass, [distance_phobos_mars, 0], [0, -orbital_speed_phobos])

bodies = [mars, phobos]
sim = OrbitalMotion(bodies, dt=60)  #timestep is 60
positions, kinetic_energies = sim.simulate(5000) #run the simulation for 5000 steps

#set up the figure
fig, ax = plt.subplots()
ax.set_xlim(-3 * distance_phobos_mars, 3 * distance_phobos_mars)
ax.set_ylim(-3 * distance_phobos_mars, 3 * distance_phobos_mars)
ax.set_aspect('equal')

#create the bodies on the figure
mars_patch = plt.Circle((0, 0), 3e6, color='red', label='Mars')
phobos_patch = plt.Circle((0, 0), 1e6, color='blue', label='Phobos')
ax.add_patch(mars_patch)
ax.add_patch(phobos_patch)
ax.legend()

#extract the position arrays
mars_pos = positions["Mars"]
phobos_pos = positions["Phobos"]

def update(frame):
    '''
    The update function for the animation. Takes in the current frame index in the animation, 
    and outputs the updated figure
    '''
    mars_patch.center = mars_pos[frame] #update the position of mars
    phobos_patch.center = phobos_pos[frame] #update the position of phobos
    ax.set_title(f'{sim.kinetic_energies[frame]:.3e}') #display the KE at the current timestep
    return mars_patch, phobos_patch

#create and display the simulation
ani = animation.FuncAnimation(fig, update, frames=len(mars_pos), interval=1)
plt.show()

