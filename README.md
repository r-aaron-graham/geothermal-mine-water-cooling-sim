# Geothermal and Mine‑Water Cooling Simulation

This repository contains a simple simulation of geothermal and
mine‑water cooling systems for data center applications.  It models
heat exchange between the data center and its cooling medium (e.g.,
geothermal brine or mine water) and estimates resulting outlet
temperatures based on flow rates and inlet temperatures.

## Overview

The simulation implements a steady‑state heat transfer model using
basic thermodynamics.  It calculates the temperature change of the
coolant as it absorbs heat from the server racks and returns cooler
fluid to the ground or mine.  The output can help compare cooling
efficiency under different conditions.

## Usage

Install dependencies and run the simulation script:

```bash
pip install -r requirements.txt
python simulation.py --inlet-temp 12 --flow-rate 100 --heat-load 500
```

The script will print the outlet temperature of the coolant.  All
temperatures are in degrees Celsius, flow rate is litres per second,
and heat load is kilowatts.

## Extending

To incorporate additional factors such as variable thermal
conductivity, pipe lengths, or transient dynamics, extend the
`simulate_cooling` function in `simulation.py`.  You can also add
visualizations or integrate the model into a larger capacity planning
tool.