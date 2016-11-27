# -*- coding: utf-8 -*-
"""Module to make models available to notebooks after the ones in which they
are introduced

This module implements Python code from the notebook
10-partial_pooling_varying_slope_and_intercept.ipynb in order to enable model
use in later notebooks.
"""

import numpy as np
import pandas as pd
import pystan
import clean_data


# Partial-pooled model, varying slope and intercept, from
# 10-partial_pooling_varying_slope_and_intercept.ipynb
varying_intercept_slope = """
data {
  int<lower=0> J;
  int<lower=0> N;
  int<lower=1,upper=J> county[N];
  vector[N] x;
  vector[N] y;
}
parameters{
  vector[J] a;
  real mu_a;
  vector[J] b;
  real mu_b;
  real<lower=0,upper=100> sigma_a;
  real<lower=0,upper=100> sigma_b;
  real<lower=0,upper=100> sigma_y;
}
transformed parameters {
  vector[N] y_hat;
  for(i in 1:N)
    y_hat[i] <- a[county[i]] + x[i] * b[county[i]];
}
model {
  sigma_a ~ uniform(0, 100);
  a ~ normal(mu_a, sigma_a);

  sigma_b ~ uniform(0, 100);
  b ~ normal(mu_b, sigma_b);
    
  sigma_y ~ uniform(0, 100);
  y ~ normal(y_hat, sigma_y);
}
"""

# number of samples from each county
n_county = clean_data.srrs_mn.groupby('county')['idnum'].count()  

varying_intercept_slope_data = {'N': len(clean_data.log_radon),
                                'J': len(n_county),
                                'county': clean_data.county + 1,
                                'x': clean_data.floor_measure,
                                'y': clean_data.log_radon}

varying_intercept_slope_fit = pystan.stan(model_code=varying_intercept_slope,
                                          data=varying_intercept_slope_data,
                                          iter=1000, chains=2)

b_sample = varying_intercept_slope_fit['a']
m_sample = varying_intercept_slope_fit['b']
bp = b_sample.mean(axis=0)
mp = m_sample.mean(axis=0)
bse = b_sample.std(axis=0)
mse = m_sample.std(axis=0)
