from solar_system import Planet, Simulation, dt, total_time, num_steps, config

def main():
    # Run the simulation
    planets_beeman = [Planet(**p, integration_method='beeman') for p in config["bodies"]]
    sim_beeman = Simulation(dt, total_time, num_steps, planets_beeman)
    sim_beeman.simulate()

    # Print the orbital period for each planet
    for p in planets_beeman:
        if p.name != 'sun' and p.orbital_period is not None:
            print(f"{p.name} orbital period: {p.orbital_period:.2f} Earth years")

if __name__ == '__main__':
    main()