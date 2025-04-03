# Computer Simulation Project

## Usage and Structure

There are five python files contained in this project. I use the package ```tqdm``` to display a loading bar so that the user can track progress. For the code to run, the user must have this package installed. Run
```
pip install tqdm
```

### Solar System

The [solar_system](./solar_system.py) file contains the constants read from the JSON parameters file, as well as the two classes ```Planet``` and ```Simulate```. These classes effectively build planet objects, and then simulate their interactions and orbits. If the user would like to alter the range of allowance for planetary allowance, then this can be done by altering line $206$, i.e. changing the parameter for $\sin$. It is initially set for a $\pm 5^\circ$ allowance.

### Animation

Running the [animation](./animation.py) file causes an animation of the solar system using Beeman integration to execute. It runs for (dt $\times$ num_steps) years. 

### Testing Orbial Periods

To find the orbital periods of the planets in the simulation, run the [testing_orbital_periods](./testing_orbital_period.py) file. This experiment uses Beeman integration. 

### Testing Energy Conservation under different Integration Schemes

The [testing_integration_methods](./testing_integration_methods.py) runs the simulation under Beeman, Euler Cromer, and Direct Euler integration. Every $100$ timesteps, the total system energy is calculated. Running this file will cause graphs showing energy of all three methods against time, Beeman energies against time, Euler Cromer energies against time, and finally both Beeman and Euler Cromer energies against time.

### Detecting Occurances of Planetary Alignment

To run the planetary alignment experiment, run this [file](./testing_planetary_alignment.py). The occurances of planetary alignment will be output, as well as images of the planet positions. Due to the allowance range, many time instances may be output for the same occurance, i.e. the times may be the same to the first decimal place, but differ slightly beyond that. I recorded one alignment instance as the time instance rounded to the nearest integer in my report.

## Parameters

The parameters file must be a JSON file named parameters.json, and must follow the following structure:

```yaml
{
    "num_iterations": 240000,
    "timestep": 0.001,
    "grav_const": 1.18638e-4,
    "bodies":
    [
	{
	    "name": "sun",
	    "mass": 332946.0,
	    "orbital_radius": 0.0,
	    "colour": "#ffcc33"
	},
	{
	    "name": "mercury",
	    "mass": 0.06,
	    "orbital_radius": 0.387,
	    "colour": "#b7b8b9"
	},
	{
	    "name": "venus",
	    "mass": 0.82,
	    "orbital_radius": 0.723,
	    "colour": "#f8e2b0"
	},
	{
	    "name": "earth",
	    "mass": 1.0,
	    "orbital_radius": 1.0,
	    "colour": "#9fc164"
	},
	{
	    "name": "mars",
	    "mass": 0.11,
	    "orbital_radius": 1.524,
	    "colour": "#9c003f"
	},
	{
	    "name": "jupiter",
	    "mass": 318,
	    "orbital_radius": 5.2,
	    "colour": "#c17d6b"
	},
	{
	    "name": "saturn",
	    "mass": 95,
	    "orbital_radius": 9.5,
	    "colour": "#f9a9a9"
	},
	{
	    "name": "uranus",
	    "mass": 14,
	    "orbital_radius": 19.2,
	    "colour": "#2e84ce"
	},
	{
	    "name": "neptune",
	    "mass": 17,
	    "orbital_radius": 30.1,
	    "colour": "#1f2255"
	}
    ]
}
```