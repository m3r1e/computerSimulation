import random
import matplotlib.pyplot as plt
import numpy as np

N = int(input('length of road: '))
ITERATIONS = int(input('iterations: '))
CARDENSITY = float(input('car density: '))#as a decimal

class Traffic:
    def __init__(self, length, density, iterations):
        self.length = length
        self.density = density
        self.iterations = iterations
        self.num_cars = round(self.density * self.length) #ensure num_cars is an integer
        self.gen_road(self.num_cars)


    def gen_road(self, cars_on_road): #pass cars_on_road so can be used for steady state calculations
        '''
        Generate a road of 1s and 0s by randomly allocating the positions of the 1s
        '''
        self.road = [0]*self.length #create list of zeros
        indices = random.sample(range(self.length), cars_on_road) 
        for i in indices:
            self.road[i] = 1 #randomly change certain zeros to one by generating a set of indexes
    
  
    def update_road(self):
        '''
        Runs the road moving process and updates the road
        '''
        road = self.road[:]
        states = [] #all the roads, so i can plot them 
        average_speeds = []

        for _ in range(self.iterations): #running the movement process 'iteration' number of times
            new_road = road[:] #copy the road
            moves_this_timestep = 0

            for i in range(self.length): #implement 
                next_pos = (i + 1) % self.length
                prev_pos = (i - 1) % self.length

                if road[i] == 1:                    
                    if road[next_pos] == 1:
                        new_road[i] = 1
                    else:
                        new_road[i] = 0
                        moves_this_timestep += 1
                elif road[i] == 0:
                    if road[prev_pos] == 1:
                        new_road[i] = 1
                    else:
                        new_road[i] = 0

            road = new_road[:] #copy the new road
            states.append(road) #saving every road after every iteration so they can be plotted

            #average speed
            avg_speed = moves_this_timestep / self.num_cars if self.num_cars > 0 else 0
            average_speeds.append(avg_speed)

        return states, average_speeds

    

def plot_road(states):   
    '''
    Graphically representing the cars
    '''
    road_array = np.array(states)
    fig, ax = plt.subplots(figsize=(5, 6))
    cax = ax.imshow(road_array, cmap='Blues', vmin=0, vmax=1, aspect='auto', origin='lower')
    ax.set_xlabel('cell')
    ax.set_ylabel('timestep')
    plt.show()

def steady_state(N):
        '''
        Plotting the steady state speed against the number of cars on the road for a fixed length road
        '''
        steady_speeds = []
        for i in range(1, N+1):
            sim = Traffic(N, i/N, N)
            _, average_speeds = sim.update_road() 
            steady_speeds.append(average_speeds[-1]) #taking the last speed after running the update_road algorithm N times
        
        #Creating the plot
        x = np.arange(N)
        y = np.array(steady_speeds)
        plt.title('Steady State Speed against Number of Cars on Road')
        plt.xlabel('Number of Cars on Road')
        plt.ylabel('Steady State Speed')
        plt.plot(x,y)
        plt.show()

if __name__ == '__main__':
    simulation = Traffic(N, CARDENSITY, ITERATIONS) #takes user input
    states, average_speeds = simulation.update_road()

    for i, speed in enumerate(average_speeds, start=1):
        print(f"Iteration {i}: Average speed = {speed:.2f} moves per car")

    plot_road(states)
    steady_state(N)
