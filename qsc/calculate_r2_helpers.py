"""
This module contains methods for performing mathematical operations in calculate_r2.py
"""


import jax.numpy as jnp

def calc_B0_over_abs_G0(B0, G0): 
  return B0 / jnp.abs(G0) 

def calc_V1(X1c, Y1c, Y1s): 
  return  X1c * X1c + Y1c * Y1c + Y1s * Y1s

def calc_V2(Y1s, Y1c): 
  return 2 * Y1s * Y1c

def calc_V3(X1c, Y1c, Y1s): 
  return X1c * X1c + Y1c * Y1c - Y1s * Y1s

def calc_qs(iota_N, X1c, Y1s, torsion, abs_G0_over_B0): 
  return  -iota_N * X1c - Y1s * torsion * abs_G0_over_B0

def calc_beta_1s(spsi, sG, mu0, p2, etabar, abs_G0_over_B0, iota_N, B0): 
  return -4 * spsi * sG * mu0 * p2 * etabar * abs_G0_over_B0 / (iota_N * B0 * B0)

def calc_Y2s_from_X20(sG, spsi, curvature, etabar): 
  return -sG * spsi * curvature * curvature / (etabar * etabar)

def calc_Y2s_inhomogeneous(sG, spsi, curvature, etabar, X2c, X2s, sigma): 
  return sG * spsi * (-curvature/2 + curvature*curvature/(etabar*etabar)*(-X2c + X2s * sigma))

def calc_Y2c_from_X20(sG, spsi, curvature,sigma,  etabar): 
  return -sG * spsi * curvature * curvature * sigma / (etabar * etabar)

def calc_Y2c_inhomogeneous(sG, spsi, curvature, etabar, X2s, X2c, sigma): 
  return sG * spsi * curvature * curvature / (etabar * etabar) * (X2s + X2c * sigma)

def calc_fX0_from_X20(sG, spsi, abs_G0_over_B0, Y2c_from_X20, Z2s, Y2s_from_X20, Z2c): 
  return -4 * sG * spsi * abs_G0_over_B0 * (Y2c_from_X20 * Z2s - Y2s_from_X20 * Z2c)

def calc_fX0_from_Y20(torsion, abs_G0_over_B0, sG, spsi, Z2s, I2_over_B0): 
  return -torsion * abs_G0_over_B0 - 4 * sG * spsi * abs_G0_over_B0 * (Z2s) \
        - spsi * I2_over_B0 * (-2) * abs_G0_over_B0

def calc_fX0_inhomogeneous(curvature, abs_G0_over_B0, Z20, sG, spsi, Y2c_inhomogeneous, Z2s, Y2s_inhomogeneous, Z2c, I2_over_B0, beta_1s, Y1c): 
  return curvature * abs_G0_over_B0 * Z20 - 4 * sG * spsi * abs_G0_over_B0 * (Y2c_inhomogeneous * Z2s - Y2s_inhomogeneous * Z2c) \
        - spsi * I2_over_B0 * (0.5 * curvature * sG * spsi) * abs_G0_over_B0 + beta_1s * abs_G0_over_B0 / 2 * Y1c

def calc_fXs_from_X20(torsion, abs_G0_over_B0, Y2s_from_X20, spsi, sG, Y2c_from_X20, Z20, I2_over_B0): 
  return -torsion * abs_G0_over_B0 * Y2s_from_X20 - 4 * spsi * sG * abs_G0_over_B0 * (Y2c_from_X20 * Z20) \
        - spsi * I2_over_B0 * (- 2 * Y2s_from_X20) * abs_G0_over_B0

def calc_fXs_from_Y20(spsi, sG, abs_G0_over_B0, Z2c, Z20): 
  return - 4 * spsi * sG * abs_G0_over_B0 * (-Z2c + Z20)

def calc_fXs_inhomogeneous(d_d_varphi, X2s, iota_N, X2c, torsion, abs_G0_over_B0, Y2s_inhomogeneous, curvature, Z2s, spsi, sG, Y2c_inhomogeneous, Z20, I2_over_B0, beta_1s, Y1s):
  return jnp.matmul(d_d_varphi,X2s) - 2 * iota_N * X2c - torsion * abs_G0_over_B0 * Y2s_inhomogeneous + curvature * abs_G0_over_B0 * Z2s \
        - 4 * spsi * sG * abs_G0_over_B0 * (Y2c_inhomogeneous * Z20) \
        - spsi * I2_over_B0 * (0.5 * curvature * spsi * sG - 2 * Y2s_inhomogeneous) * abs_G0_over_B0 \
        - (0.5) * abs_G0_over_B0 * beta_1s * Y1s
  
def calc_fXc_from_X20(torsion, abs_G0_over_B0, Y2c_from_X20, spsi, sG, Y2s_from_X20, Z20, I2_over_B0): 
  return - torsion * abs_G0_over_B0 * Y2c_from_X20 - 4 * spsi * sG * abs_G0_over_B0 * (-Y2s_from_X20 * Z20) \
        - spsi * I2_over_B0 * (- 2 * Y2c_from_X20) * abs_G0_over_B0

def calc_fXc_from_Y20(torsion, abs_G0_over_B0, spsi, sG, Z2s,  I2_over_B0 ): 
  return - torsion * abs_G0_over_B0 - 4 * spsi * sG * abs_G0_over_B0 * (Z2s) \
        - spsi * I2_over_B0 * (-2) * abs_G0_over_B0

def calc_fXc_inhomogeneous(d_d_varphi, X2c, iota_N, X2s, torsion, abs_G0_over_B0, Y2c_inhomogeneous, curvature, Z2c, spsi, sG, Y2s_inhomogeneous, Z20, I2_over_B0, beta_1s, Y1c): 
  return jnp.matmul(d_d_varphi,X2c) + 2 * iota_N * X2s - torsion * abs_G0_over_B0 * Y2c_inhomogeneous + curvature * abs_G0_over_B0 * Z2c \
        - 4 * spsi * sG * abs_G0_over_B0 * (-Y2s_inhomogeneous * Z20) \
        - spsi * I2_over_B0 * (0.5 * curvature * sG * spsi - 2 * Y2c_inhomogeneous) * abs_G0_over_B0 \
        - (0.5) * abs_G0_over_B0 * beta_1s * Y1c

def calc_fY0_from_X20(torsion, abs_G0_over_B0, spsi, I2_over_B0): 
  return torsion * abs_G0_over_B0 - spsi * I2_over_B0 * (2) * abs_G0_over_B0

def calc_fY0_inhomogeneous(spsi, sG, abs_G0_over_B0, X2s, Z2c, X2c, Z2s, I2_over_B0, curvature, X1c, beta_1s):
  return -4 * spsi * sG * abs_G0_over_B0 * (X2s * Z2c - X2c * Z2s) \
        - spsi * I2_over_B0 * (-0.5 * curvature * X1c * X1c) * abs_G0_over_B0 - (0.5) * abs_G0_over_B0 * beta_1s * X1c

def calc_fYs_from_X20(iota_N, Y2c_from_X20, spsi, sG, abs_G0_over_B0, Z2c): 
  return -2 * iota_N * Y2c_from_X20 - 4 * spsi * sG * abs_G0_over_B0 * (Z2c)
