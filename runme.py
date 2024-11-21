from collections import defaultdict
from urbs.input import get_input
from urbs.output import get_timeseries
import urbs
from urbs import get_constants
from datetime import date


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

    # select scenarios to be run - only use base scenario
    prob = urbs.run_scenario_config(config, solver, timesteps, urbs.scenario_base,
                                    result_dir, dt, objective,
                                    plot_tuples=plot_tuples,
                                    plot_sites_name=plot_sites_name,
                                    plot_periods=plot_periods,
                                    report_tuples=report_tuples,
                                    report_sites_name=report_sites_name)

    costs, cpro, ctra, csto = get_constants(prob)

    def default():
        return defaultdict(default)

    proc = default()
    for ((year, site, commodity), row) in cpro.iterrows():
        proc[site][commodity]['New'] = row['New']
        proc[site][commodity]['Total'] = row['Total']

    results = default()
    for (site, com) in get_input(prob, 'demand').columns.values.tolist():
        data = get_timeseries(prob, date.today().year, "Elec", "Main", timesteps=None)
        results[site][com] = {
            'created': {k: list(v.values()) for k,v in data[0].to_dict().items()},
            'demand': list(data[1].to_dict()['Demand'].values()),
            'storage': {k: list(v.values()) for k,v in data[2].to_dict().items()}
        }
    return {
        'costs': costs.to_dict(),
        'process': proc,
        'results': results,
    }
