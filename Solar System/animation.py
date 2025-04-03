from solar_system import Planet, Simulation, dt, total_time, num_steps, config
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

def main():
    # Run the simulation  

    planets_beeman = [Planet(**p, integration_method='beeman') for p in config["bodies"]]
    sim_beeman = Simulation(dt, total_time, num_steps, planets_beeman)
    sim_beeman.simulate()

    # Initialise the animation figure

    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    ax.set_xlabel("X Position, AUs")
    ax.set_ylabel("Y Position, AUs")
    ax.set_title("Planetary Orbit Simulation")
    ax.legend()

    # Plot the bodies

    xs = [p.positions[0][0] for p in planets_beeman]
    ys = [p.positions[0][1] for p in planets_beeman]
    colours = [p.colour for p in planets_beeman]
    labels = [p.name for p in planets_beeman]
    planet_plots = ax.scatter(xs, ys, color=colours)

    # Create a legend - stack overflow!

    legend_handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=col, markersize=10, label=lab) 
                      for col, lab in zip(colours, labels)]
    ax.legend(handles=legend_handles) 

    # Animate simulation

    def update(frame):
        positions = [p.positions[frame] for p in planets_beeman]
        planet_plots.set_offsets(positions)
        return planet_plots,

    ani = animation.FuncAnimation(fig, update, frames=min(num_steps, len(planets_beeman[0].positions)), interval=1, blit=False)

    plt.show()

if __name__ == '__main__':
    main()