import json
from collections import defaultdict

import pandas as pd
from flask import Flask, request

import urbs
from urbs import get_constants, get_input, get_timeseries
from urbs.util import is_string

app = Flask(__name__)

@app.post('/simulate')
def simulate():
    config = request.get_json()
    run(config)

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
    print("REPORTING")
    for ((year, site, commodity), row) in cpro.iterrows():
        proc[site][commodity]['New'] = row['New']
        proc[site][commodity]['Total'] = row['Total']

    # TESTING ONLY
    # quick and dirty

    (site) = get_input(prob, 'demand').columns

    elec = get_timeseries(prob, 2024, "Elec", "Main", timesteps=None)
    return {
        'costs': costs.to_dict(),
        'process': proc,
        'created': json.loads(elec[0].to_json()),
        'demand': json.loads(elec[1].to_json()),
        'storage': json.loads(elec[2].to_json()),
    }

if __name__ == '__main__':
    app.run()
