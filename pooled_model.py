# -*- coding: utf-8 -*-
"""Module to make models available to notebooks after the ones in which they
are introduced

This module implements Python code from notebooks 04-pooled_model.ipynb in
order to enable model use in later notebooks.
"""

import numpy as np
import pandas as pd
import pystan
import clean_data

# Pooled model, from 04-pooled_model.ipynb
pooled_data = """
data {
  int<lower=0> N;
  vector[N] x;
  vector[N] y;
}
"""

pooled_parameters = """
parameters {
    vector[2] beta;
    real<lower=0> sigma;
}
"""

pooled_model = """
model {
  y ~ normal(beta[1] + beta[2] * x, sigma);
}
"""

pooled_data_dict = {'N': len(clean_data.log_radon),
                    'x': clean_data.floor_measure,
                    'y': clean_data.log_radon}

pooled_fit = pystan.stan(model_code=pooled_data + pooled_parameters +
                         pooled_model,
                         data=pooled_data_dict,
                         iter=1000,
                         chains=2)

pooled_sample = pooled_fit.extract(permuted=True)
b0, m0 = pooled_sample['beta'].T.mean(1)
