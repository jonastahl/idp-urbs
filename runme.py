import os
import shutil
import urbs


def run(config):
    result_name = 'Run'
    result_dir = urbs.prepare_result_directory(result_name)  # name + time stamp

    # objective function
    objective = 'cost'  # set either 'cost' or 'CO2' as objective

    # Choose Solver (cplex, glpk, gurobi, ...)
    solver = 'glpk'

    # simulation timesteps
    timesteps = range(config['c_timesteps'])
    dt = 1  # length of each time step (unit: hours)

    # detailed reporting commodity/sites
    report_tuples = []

    # optional: define names for sites in report_tuples
    report_sites_name = {}

    # plotting commodities/sites
    plot_tuples = []

    # optional: define names for sites in plot_tuples
    plot_sites_name = {}

    # plotting timesteps
    plot_periods = {
        'all': timesteps[1:]
    }

    # add or change plot colors
    my_colors = {}
    for country, color in my_colors.items():
        urbs.COLORS[country] = color

    # select scenarios to be run
    scenarios = [
        urbs.scenario_base
    ]

    for scenario in scenarios:
        urbs.run_scenario(solver, timesteps, scenario,
                          result_dir, dt, objective,
                          config=config,
                          plot_tuples=plot_tuples,
                          plot_sites_name=plot_sites_name,
                          plot_periods=plot_periods,
                          report_tuples=report_tuples,
                          report_sites_name=report_sites_name)
