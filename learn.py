#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from copy import deepcopy

import numpy as np
import pandas as pd

from ordinor.io import read_disco_csv
from ordinor.execution_context.rule_based import ODTMiner

# input log
#fn_log = sys.argv[1]

#el = read_disco_csv(fn_log)
el = pd.read_csv("bpic15_amended_typed.csv")

# specification

spec = {
    'type_def_attrs': {
        # BPIC15
        'ct:permit_type': {'attr_type': 'categorical', 'attr_dim': 'CT'},
        'at:phase': {'attr_type': 'categorical', 'attr_dim': 'AT'},
        'tt:weekday': {'attr_type': 'categorical', 'attr_dim': 'TT'}, 
        'tt:ampm': {'attr_type': 'categorical', 'attr_dim': 'TT'},
    }
}

# run algorithm

miner = ODTMiner(el, spec, max_height=12, trace_history=True)

