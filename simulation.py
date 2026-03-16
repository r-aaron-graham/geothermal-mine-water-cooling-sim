"""Simulation of geothermal and mine‑water cooling for data centers."""

from __future__ import annotations

import click

SPECIFIC_HEAT_WATER = 4.186  # kJ/(kg·°C)
DENSITY_WATER = 0.997  # kg/L at ~25°C


def simulate_cooling(inlet_temp: float, flow_rate_lps: float, heat_load_kw: float) -> float:
    """Compute outlet temperature of the cooling fluid.

    Parameters
    ----------
    inlet_temp: float
        Temperature of the fluid entering the data center in °C.
    flow_rate_lps: float
        Volumetric flow rate of fluid in litres per second.
    heat_load_kw: float
        Heat load to be removed from servers in kilowatts.

    Returns
    -------
    float
        Outlet temperature of the fluid in °C.
    """
    # Convert flow rate to kg/s (assuming density ~1 kg/L)
    mass_flow_kg_s = flow_rate_lps * DENSITY_WATER
    # Energy balance: Q = m*c*ΔT -> ΔT = Q/(m*c)
    # heat_load_kw is kW = kJ/s; convert to kJ/s
    heat_kj_s = heat_load_kw
    delta_temp = heat_kj_s / (mass_flow_kg_s * SPECIFIC_HEAT_WATER)
    return inlet_temp + delta_temp


@click.command()
@click.option("--inlet-temp", type=float, required=True, help="Inlet temperature (°C)")
@click.option("--flow-rate", type=float, required=True, help="Flow rate (L/s)")
@click.option("--heat-load", type=float, required=True, help="Heat load (kW)")
def main(inlet_temp: float, flow_rate: float, heat_load: float):
    outlet = simulate_cooling(inlet_temp, flow_rate, heat_load)
    click.echo(f"Outlet temperature: {outlet:.2f} °C")


if __name__ == "__main__":  # pragma: no cover
    main()