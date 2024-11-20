import os
import shutil
from collections import defaultdict
import json
import sys
sys.path.append("./urbs")
from input import get_input
from output import get_constants, get_timeseries
from util import is_string

import urbs
from urbs import get_constants

sys.path.append("/home/merhart/Documents/vurbs/lib/python3.12/site-packages/glpk.cpython-312-x86_64-linux-gnu.so")

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
    print("REPORTING")
    for ((year, site, commodity), row) in cpro.iterrows():
        proc[site][commodity]['New'] = row['New']
        proc[site][commodity]['Total'] = row['Total']

    # TESTING ONLY
    # quick and dirty 
    #
    
    report_tuples = get_input(prob, 'demand').columns



    print(report_tuples)

    energies = []
    timeseries = {}
    help_ts = {}

    # collect timeseries data
    for stf, sit, com in report_tuples:

        # wrap single site name in 1-element list for consistent behavior
        if is_string(sit):
            help_sit = [sit]
        else:
            help_sit = sit
            sit = tuple(sit)

        # check existence of predefined names, else define them
        try:
            report_sites_name[sit]
        except BaseException:
            report_sites_name[sit] = str(sit)

        for lv in help_sit:
            (created, consumed, stored, imported, exported,
                dsm, voltage_angle) = get_timeseries(instance, stf, com, lv)

            overprod = pd.DataFrame(
                columns=['Overproduction'],
                data=created.sum(axis=1) - consumed.sum(axis=1) +
                imported.sum(axis=1) - exported.sum(axis=1) +
                stored['Retrieved'] - stored['Stored'])

            tableau = pd.concat(
                [created, consumed, stored, imported, exported, overprod,
                    dsm, voltage_angle],
                axis=1,
                keys=['Created', 'Consumed', 'Storage', 'Import from',
                        'Export to', 'Balance', 'DSM', 'Voltage Angle'])
            help_ts[(stf, lv, com)] = tableau.copy()

            # timeseries sums
            help_sums = pd.concat([created.sum(), consumed.sum(),
                                    stored.sum().drop('Level'),
                                    imported.sum(), exported.sum(),
                                    overprod.sum(), dsm.sum()],
                                    axis=0,
                                    keys=['Created', 'Consumed', 'Storage',
                                        'Import', 'Export', 'Balance',
                                        'DSM'])
            print(help_sums)
            try:
                timeseries[(stf, report_sites_name[sit], com)] = \
                    timeseries[(stf, report_sites_name[sit], com)].add(
                    help_ts[(stf, lv, com)], axis=1, fill_value=0)
                sums = sums.add(help_sums, fill_value=0)
            except BaseException:
                timeseries[(stf, report_sites_name[sit], com)] = help_ts[
                    (stf, lv, com)]
                sums = help_sums

        # timeseries sums
        sums = pd.concat([created.sum(), consumed.sum(),
                            stored.sum().drop('Level'),
                            imported.sum(), exported.sum(), overprod.sum(),
                            dsm.sum()],
                            axis=0,
                            keys=['Created', 'Consumed', 'Storage', 'Import',
                                'Export', 'Balance', 'DSM'])
        energies.append(sums.to_frame("{}.{}.{}".format(stf, sit, com)))

        print(energies)

    return {
        'costs': costs.to_dict(),
        'process': proc,
        'sum': json.dumps(energies),
        "test": "test"
    }