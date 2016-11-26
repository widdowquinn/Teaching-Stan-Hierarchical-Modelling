# -*- coding: utf-8 -*-
"""Module to make models available to notebooks after the ones in which they
are introduced

This module implements Python code from notebooks 04-pooled_model.ipynb and
05-unpooled_model.ipynb in order to enable their use in later notebooks.
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

# Unpooled model, from 05-unpooled_model.ipynb
unpooled_data = """
data {
  int<lower=0> N;
  int<lower=1, upper=85> county[N];
  vector[N] x;
  vector[N] y;
}
"""

unpooled_parameters = """
parameters {
  vector[85] a;
  real beta;
  real<lower=0, upper=100> sigma;
}
"""

unpooled_transformed_parameters = """
transformed parameters {
  vector[N] y_hat;
  
  for (i in 1:N)
    y_hat[i] <- beta * x[i] + a[county[i]];
}
"""

unpooled_model = """
model {
  y ~ normal(y_hat, sigma);
}
"""

unpooled_data_dict = {'N': len(clean_data.log_radon),
                      'county': clean_data.county + 1, 
                      'x': clean_data.floor_measure,
                      'y': clean_data.log_radon}

unpooled_fit = pystan.stan(model_code=unpooled_data + unpooled_parameters +
                           unpooled_transformed_parameters + unpooled_model,
                           data=unpooled_data_dict,
                           iter=1000,
                           chains=2)

unpooled_estimates = pd.Series(unpooled_fit['a'].mean(0),
                               index=clean_data.mn_counties)
unpooled_se = pd.Series(unpooled_fit['a'].std(0),
                        index=clean_data.mn_counties)
