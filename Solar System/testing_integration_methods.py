from solar_system import Planet, Simulation, dt, total_time, num_steps, config
import matplotlib.pyplot as plt

def main():
    # Generate a simulation using Beeman integration
    planets_beeman = [Planet(**p, integration_method='beeman') for p in config["bodies"]]
    sim_beeman = Simulation(dt, total_time, num_steps, planets_beeman)
    sim_beeman.simulate()


    # Generate a simulation using Euler Cromer integration
    planets_euler_cromer = [Planet(**p, integration_method='euler-cromer') for p in config["bodies"]]
    sim_euler_cromer = Simulation(dt, total_time, num_steps, planets_euler_cromer)
    sim_euler_cromer.simulate()


    # Generate a simulation using Direct Euler integration
    planets_direct_euler = [Planet(**p, integration_method='direct-euler') for p in config["bodies"]]
    sim_direct_euler = Simulation(dt, total_time, num_steps, planets_direct_euler)
    sim_direct_euler.simulate()


    # Create lists for the logged system energies for all three methods and a list for the corresponding times
    beeman_energies = [e for t,e in sim_beeman.energy_log]
    euler_cromer_energies = [e for t,e in sim_euler_cromer.energy_log]
    direct_euler_energies = [e for t,e in sim_direct_euler.energy_log]
    times = [t for t,e in sim_beeman.energy_log] # Diff num steps to energy log occurances

    # Plot all three methods

    plt.plot(times, beeman_energies, c='maroon', label='Beeman', linewidth=0.5)  
    plt.plot(times, euler_cromer_energies, c='lightblue', label='Euler Cromer', linewidth=0.5)
    plt.plot(times, direct_euler_energies, c='cadetblue', label='Direct Euler')
    plt.ylabel('Total System Energy')
    plt.xlabel('Time, years')
    plt.grid(linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show() 

    # Plot Beeman energies only

    plt.plot(times, beeman_energies, c='maroon', label='Beeman', linewidth=0.5)
    plt.ylabel('Total System Energy')
    plt.xlabel('Time, years')
    plt.grid(linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show() 

    # Plot Euler Cromer energies only

    plt.plot(times, euler_cromer_energies, c='lightblue', label='Euler Cromer', linewidth=0.5)
    plt.ylabel('Total System Energy')
    plt.xlabel('Time, years')
    plt.grid(linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show() 



if __name__ == '__main__':
    main()