from solar_system import Planet, Simulation, dt, total_time, num_steps, config

def main():
    # Run the simulation
    planets_beeman = [Planet(**p, integration_method='beeman') for p in config["bodies"]]
    sim_beeman = Simulation(dt, total_time, num_steps, planets_beeman)
    sim_beeman.simulate()
    sim_beeman.planetary_alignment()

    # Print the alignment occurances 
    print(f"Planetary alignments: {sim_beeman.planetary_alignments}")

if __name__ == '__main__':
    main()