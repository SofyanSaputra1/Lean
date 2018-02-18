from __future__ import division
from __future__ import with_statement

import numpy as np
import sklearn
from sklearn.model_selection import ParameterGrid

import pprint
import json
import sys
import os
import pickle
import uuid
import subprocess

if sys.version_info[:2] != (2,7):
    sys.stderr.write('Platinum optimizer designed to work with python 2.7')
    exit(1)

class Optimizer(object):
    def __init__(self, params_json):
        self.params_json = params_json
        self.params = {}
        self.indicators = []
        self.param_grid = []

        self.parse_params()
        self.gen_param_grid()

    def parse_params(self):
        fh = open(self.params_json, 'r')
        self.params = json.load(fh)

    def gen_param_grid(self):
        ''' re-initialize parameter grid '''
        self.param_grid = []
        if '__GLOBALS__' not in self.params.keys():
            print('ERROR: {} does not have __GLOBALS__ field required \
                    for further processing'.format(self.params_json))
            sys.exit(0)

        self.indicators = self.params['__GLOBALS__']['__INDICATORS__']
        for indicator in self.indicators:
            if indicator not in self.params.keys():
                print('ERROR: {} does not have {} field required for \
                        further processing'.format(self.params_json, indicator))
                sys.exit(0)

        for _global_pgrid_elem in list(ParameterGrid(self.params['__GLOBALS__'])):
            current_indicator = _global_pgrid_elem['__INDICATORS__']
            for _indicator_pgrid_elem in list(ParameterGrid(self.params[current_indicator])):
                config_inst = _global_pgrid_elem.copy()
                config_inst.update(_indicator_pgrid_elem)
                self.param_grid.append(config_inst)

    def run_opt(self):
        pp = pprint.PrettyPrinter(indent=4)
        cwd = os.path.dirname(os.path.realpath(__file__))
        root_dir = os.path.realpath(os.path.join(cwd,'../../'))

        config_dir = os.path.join(root_dir,'OptRuns')
        run_launch_dir = os.path.join(root_dir,'Launcher/bin/Debug')

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        pp.pprint('root_dir = {}'.format(root_dir))
        pp.pprint('config_dir = {}'.format(config_dir))
        pp.pprint('run_launch_dir = {}'.format(run_launch_dir))

        for config in self.param_grid:
            pp.pprint('Generating and executing config:')
            pp.pprint(config)

            ''' export config pickle '''
            config_file = os.path.join(config_dir,'config_inst.p')
            pickle.dump(config, open(config_file, 'wb'))

            ''' call QuantConnectLauncher '''
            os.chdir(run_launch_dir)

            '''
            if python version > 3.5, use subprocess run; but conflicts with QC exist 
            backtest_out is of type subprocess.CompletedProcess
            '''
            # backtest_out = subprocess.run(['mono','./QuantConnect.Lean.Launcher.exe'],stdout=subprocess.PIPE)

            '''
            if python version == 2.7, use subprocess call/check_output
            backtest_out is of type str
            '''
            # backtest_out = subprocess.check_output(['mono','./QuantConnect.Lean.Launcher.exe'])
            # backtest_out = subprocess.call(['mono','./QuantConnect.Lean.Launcher.exe'])
            subprocess.call(['mono','./QuantConnect.Lean.Launcher.exe'])
            # for l in backtest_out.splitlines():
                # if l.contains('')



        os.chdir(root_dir)


    def __repr__(self):
        return json.dumps(self.params)

