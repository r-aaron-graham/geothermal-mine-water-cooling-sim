# Mine-water cooling simulation

This Python CLI estimates how much a stream of coolant warms while carrying heat away from a compute load. It illustrates the steady-state energy balance for a proposed mine-water heat exchange system.

`outlet temperature = inlet temperature + heat load / (mass flow × specific heat)`

The model uses a water density of 0.997 kg/L and a specific heat of 4.186 kJ/(kg·°C). It assumes the entire stated heat load enters the modeled stream at constant flow. It excludes pump electricity, heat exchanger losses, water chemistry, and mine thermal recovery.

## Run the example

```bash
python -m pip install -r requirements.txt
python simulation.py --inlet-temp 12 --flow-rate 100 --heat-load 500
```

Expected output is `Outlet temperature: 13.20 °C`. At 50 L/s the same modeled load produces about twice the temperature rise. These are illustrative inputs and outputs. Site feasibility would require field measurements and engineering validation.

See [simulation.py](simulation.py) for the CLI and energy balance.

## Compute scheduling experiment · v0.1.0 local build

Compare FIFO with cooling-aware dispatch over five synthetic one-hour slots on
one worker. The latter defers jobs that exceed available water-side cooling
until a cooler slot or the job's deadline. Both use backup cooling when a
running workload exceeds water-side capacity.

```bash
python -m unittest -q
python scheduler.py
```

[The example results](scheduler-results-v1.json) include per-slot dispatch,
deadline misses, and modeled kWh per completed job for backup chiller
coefficients of performance of 2, 3, and 5. The energy total includes IT
energy and backup chiller electricity. Pumping, idle consumption, thermal
storage, and backup capacity limits are outside this model. The scenario
illustrates scheduling trade-offs and uses no measured mine or facility data.
