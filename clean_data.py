# -*- coding: utf-8 -*-
"""Module to clean data for Stan Hierarchical Modelling notebooks

This module implements Python code from notebook 02-Data_Import.ipynb
so as to make variables available in the subsequent notebooks, for
modelling.
"""

import numpy as np
import pandas as pd

# Import radon data
srrs2 = pd.read_csv('data/srrs2.dat')
srrs2.columns = srrs2.columns.map(str.strip)

# Make a combined state and county ID, by household
srrs_mn = srrs2.assign(fips=srrs2.stfips * 1000 +
                       srrs2.cntyfips)[srrs2.state == 'MN']

# Obtain the uranium level as a county-level predictor
cty = pd.read_csv('data/cty.dat')
cty_mn = cty[cty.st == 'MN'].copy()  # MN only data

# Make a combined state and county id, by county
cty_mn['fips'] = 1000 * cty_mn.stfips + cty_mn.ctfips

# Combine data into a single dataframe
# Get uranium level by household (on county basis)
srrs_mn = srrs_mn.merge(cty_mn[['fips', 'Uppm']], on='fips')  
srrs_mn = srrs_mn.drop_duplicates(subset='idnum')  # Lose duplicate houses
u = np.log(srrs_mn.Uppm)  # log-transform uranium level
n = len(srrs_mn)  # number of households

# Index counties with a lookup dictionary
srrs_mn.county = srrs_mn.county.str.strip()
mn_counties = srrs_mn.county.unique()
counties = len(mn_counties)
county_lookup = dict(zip(mn_counties, range(len(mn_counties))))

# Make local copies of variables
county = srrs_mn['county_code'] = srrs_mn.county.replace(county_lookup).values
radon = srrs_mn.activity
srrs_mn['log_radon'] = log_radon = np.log(radon + 0.1).values
floor_measure = srrs_mn.floor.values
