from .calculate_r2_helpers import * 
from .init_axis_helpers import * 
from .calculate_r1 import solve_sigma_equation
from .calculate_r1_helpers import *

import jax.numpy as jnp

"""
note all calculations computed after line 60 require a recalcuation of rc and rs (basically everything)
"""



def calc_solution():
  matrix = calc_matrix()
  right_hand_side = calc_right_hand_side()
  return jnp.linalg.solve(matrix, right_hand_side)

def calc_matrix(): 


def calc_right_hand_side(rc, zs, rs, zc, nfp, etabar, sigma0, B0, I2, sG, spsi, nphi, B2s, B2c, p2): 
  mu0 =  4 * jnp.pi * 1e-7
  right_hand_side = jnp.zeros(2 * nphi)

  X1c = derive_calc_X1c(etabar, nphi, nfp, rc, rs, zc, zs)
  Y1s = derive_calc_X1s(nphi)
  Y1c = derive_calc_Y1c() #needs updating 

  rc = recalc_rc
  rs = recalc_rs

  G0 = calc_G0(sG,  nphi,  B0, nfp, rc, rs, zc, zs)

  B0_over_abs_G0 = calc_B0_over_abs_G0(B0, G0)

  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)

  qc = calc_qc(d_d_varphi, X1c, Y1c, torsion, abs_G0_over_B0)
  qs = calc_qs(iota_N, X1c, Y1s, torsion, abs_G0_over_B0)

  V1 = 
  V2 = 
  V3 = 

  X2s = calc_X2s(B0_over_abs_G0, d_d_varphi, Z2s, iota_N, Z2c, abs_G0_over_B0, B2s, B0, qc, qs, rc, rs, curvature) 
  iota_N = # calculated in solve sigma equation 
  X2c = calc_X2c() # needs a derivalbe helper
  torsion = # need from init axis 
  abs_G0_over_B0 = # found in init axit 
  Y2s_inhomogeneous = calc_Y2s_inhomogeneous(sG, spsi, curvature, etabar, X2c, X2s, sigma)
  curvature = calc_curvature(nphi, nfp, rc, rs, zc, zs)
  Z2s = calc_Z2c(factor, d_d_varphi, V3, iota_N, V2)
  Y2c_inhomogeneous = calc_Y2c_inhomogeneous()
  Z20 = calc_Z20(factor, d_d_varphi, V1)
  I2_over_B0 = I2 / B0
  beta_1s = calc_beta_1s(spsi, sG, mu0, p2, etabar, abs_G0_over_B0, iota_N, B0)
  Z2c = calc_Z2c(factor, d_d_varphi, V3, iota_N, V2)

  fXs_inhomogeneous = calc_fXs_inhomogeneous(d_d_varphi, X2s, iota_N, X2c, torsion, abs_G0_over_B0, Y2s_inhomogeneous, curvature, Z2s, spsi, sG, Y2c_inhomogeneous, Z20, I2_over_B0, beta_1s, Y1s)
  fY0_inhomogeneous = calc_fY0_inhomogeneous(spsi, sG, abs_G0_over_B0, X2s, Z2c, X2c, Z2s, I2_over_B0, curvature, X1c, beta_1s)
  fYs_inhomogeneous = cacl_fYs_inhomogeneous(d_d_varphi, Y2s_inhomogeneous, iota_N, Y2c_inhomogeneous, torsion, abs_G0_over_B0, X2s, spsi, sG, X2c, Z20, I2_over_B0)
  fYc_inhomogeneous = calc_fYc_inhomogeneous(d_d_varphi, Y2c_inhomogeneous, iota_N, Y2s_inhomogeneous, torsion, abs_G0_over_B0, X2c, spsi, sG, X2s, Z20, I2_over_B0, curvature, X1c, beta_1s)

  fX0_inhomogeneous = calc_fX0_inhomogeneous(curvature, abs_G0_over_B0, Z20, sG, spsi, Y2c_inhomogeneous, Z2s, Y2s_inhomogeneous, Z2c, I2_over_B0, beta_1s, Y1c)
  fXc_inhomogeneous = calc_fXc_inhomogeneous(d_d_varphi, X2c, iota_N, X2s, torsion, abs_G0_over_B0, Y2c_inhomogeneous, curvature, Z2c, spsi, sG, Y2s_inhomogeneous, Z20, I2_over_B0, beta_1s, Y1c)

  right_hand_side[0:nphi] = -(X1c * fXs_inhomogeneous - Y1s * fY0_inhomogeneous + Y1c * fYs_inhomogeneous - Y1s * fYc_inhomogeneous)
  
  right_hand_side[nphi:2 * nphi] = -(- X1c * fX0_inhomogeneous + X1c * fXc_inhomogeneous - Y1c * fY0_inhomogeneous + Y1s * fYs_inhomogeneous + Y1c * fYc_inhomogeneous)
  
  return right_hand_side

def recalc_rc(Y1c, Y1s, X1c, rc, zs, rs, zc, nfp,  nphi): 
  """
  a different rc is used after curvature is calculated
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
    
  return calc_rc(d_d_varphi, Y1c, iota_N, Y1s, X1c, torsion, abs_G0_over_B0) 

def recalc_rs():
  """
  a different rs is used after curvature is calculated
  """ 
  #TODO


def calc_X20(solution, nphi):
  return solution[0:nphi]

def calc_Z20(factor, d_d_varphi , V1): 
  return factor* jnp.matmul(d_d_varphi,V1)




def derive_B20(rc, zs, rs=[], zc=[], nfp=1, etabar=1., sigma0=0., B0=1., I2=0., sG=1, spsi=1, nphi=61, B2s=0., B2c=0., p2=0., order="r1"): 
  """
  calculate B20 as a fucntion of inputed parameters
  """
  curvature = calc_curvature(nphi, nfp, rc, rs, zc, zs)
  # rc and rs are recalculated after curvature is calculated 
  

  solution = calc_solution()

  X20 = calc_X20(solution, nphi) # X20 is solutions[0:nphi] /// in ret

  G0 = calc_G0(sG,  nphi,  B0, nfp, rc, rs, zc, zs) # done in init axit helpers

  B0_over_abs_G0 = calc_B0_over_abs_G0(B0, G0) # in ret // done 

  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi) # in ret // done 

  factor = calc_factor(B0_over_abs_G0)
  
  X1c = derive_calc_X1c(etabar, nphi, nfp, rc, rs, zc, zs)

  Y1c = derive_calc_Y1c(sG, spsi, nphi, nfp, rc, rs, zc, zs, sigma, etabar) # relies on newtons 

  Y1s = derive_calc_Y1s(sG, spsi, nphi, nfp, rc, rs, zc, zs, etabar)

  V1 = calc_V1(X1c, Y1c, Y1s) 

  Z20 = calc_Z20(factor, d_d_varphi , V1) # in ret  // done

  mu0 =  4 * jnp.pi * 1e-7

  qc = calc_qc(iota_N, X1c, Y1s, torsion, abs_G0_over_B0) #
  qs = calc_qs(iota_N, X1c, Y1s, torsion, abs_G0_over_B0)

  rc = calc_rc(d_d_varphi, Y1c, iota_N, Y1s, X1c, torsion, abs_G0_over_B0)
  rs = calc_rs(d_d_varphi, Y1s, iota_N, Y1c)

  # need from solve sigma equation : iota_N, sigma
  # need from init_axis : torsion ,  abs_G0_over_B0
  return calc_B20(B0, curvature, X20, B0_over_abs_G0, d_d_varphi, Z20, etabar, mu0, p2, qc, qs, rc, rs)

def derive_B20_mean(nphi, nfp, rc, rs, zc, zs): 
  """
  calculates B20 mean as a function of inputed parameters
  """
  #need b20 , d_l_d_phi and normalizer
  # for b20 need : B0-good, curvature, X20, B0_over_abs_G0, d_d_varphi, Z20, etabar, mu0, p2, qc, qs, rc-good, rs- good 
  B20 = derive_B20() # needs B20 to be finished 
  d_l_d_phi = calc_d_l_d_phi(nphi, nfp, rc, rs, zc, zs)
  normalizer = 1/jnp.sum(d_l_d_phi)

  return jnp.sum(B20 * d_l_d_phi) * normalizer

def derive_B20_anomaly(nphi, nfp, rc, rs, zc, zs):
  """
  calculates B20 anomaly as a function of inputed parameters
  """
  B20_mean = derive_B20_mean(nphi, nfp, rc, rs, zc, zs) 
  B20 = derive_B20() # needs B20 to be finished 
  return B20 - B20_mean

def derive_B20_residual(B0, nphi, nfp, rc, rs, zc, zs): 
  """
  calculates B20 residual as a fucntion of inputed parameters 
  """
  B20 = derive_B20()   # needs B20 to be finished 
  B20_mean = derive_B20_mean(nphi, nfp, rc, rs, zc, zs)
  d_l_d_phi = calc_d_l_d_phi(nphi, nfp, rc, rs, zc, zs)
  normalizer = 1/jnp.sum(d_l_d_phi)

  return jnp.sqrt(jnp.sum((B20 - B20_mean) * (B20 - B20_mean) * d_l_d_phi) * normalizer) / B0

def derive_B20_variation(): 
  """
  calcultes B20_variation as a function of inputed parameters
  """
  B20 = derive_B20()  # needs B20 to be finished 
  return jnp.max(B20) - jnp.min(B20)

def derive_N_helicity(nfp): 
  """
  calculates N_helicity as a function of inputed parameters
  """
  helicity = # in init_axis // will take alot of untangaling
  return - helicity * nfp

def derive_G2(B0 ,I2, p2 ,sG ,nphi ,nfp, rc, rs, zc, zs): 
  """
  calculates G2 as a function of inputed parameters
  """
  mu0 = 4 * jnp.pi * 1e-7
  G0 = calc_G0(sG,  nphi,  B0, nfp, rc, rs, zc, zs)
  iota = # solve sigma equation
  return -mu0 * p2 * G0 / (B0 * B0) - iota * I2

def derive_d_curvature_d_varphi(rc, zs, rs, zc, nfp,  nphi): # should work
  """
  calculates d_curvature_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  curvature = calc_curvature(nphi, nfp, rc, rs, zc, zs)
  jnp.matmul(d_d_varphi, curvature)

def derive_d_torsion_d_varphi(rc, zs, rs, zc, nfp,  nphi): 
  """
  calculates d_torsion_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  torsion = # B20
  return jnp.matmul(d_d_varphi, torsion)

def derive_d_X20_d_varphi(rc, zs, rs, zc, nfp, nphi): 
  """
  calculates d_X20_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  solutions = calc_solutions()
  X20 = calc_X20(solutions, nphi)
  return jnp.matmul(d_d_varphi, X20)

def derive_d_X2s_d_varphi(rc, zs, rs, zc, nfp,  nphi): 
  """
  calculates d_X2s_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  # this will be a pain should probably make a derive calc_X2s
  X2s = calc_X2s(B0_over_abs_G0, d_d_varphi, Z2s, iota_N, Z2c, abs_G0_over_B0, B2s, B0, qc, qs, rc, rs, curvature) 
  return jnp.matmul(d_d_varphi, X2s)

def derive_d_X2c_d_varphi(): 
  """
  calculates d_X2c_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  X2c = calc_X2c() # not derivable 
  return jnp.matmul(d_d_varphi, X2c)

def derive_d_Y20_d_varphi(rc, zs, rs, zc, nfp,  nphi): 
  """
  calculates d_Y20_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  solution = 
  Y20 = solution[nphi:2 * nphi]
  return jnp.matmul(d_d_varphi, Y20)

def derive_Y2s(): 
  Y2s_inhomogeneous = calc_Y2s_inhomogeneous(sG, spsi, curvature, etabar, X2c, X2s, sigma)
  Y2s_from_X20 = calc_Y2s_from_X20(sG, spsi, curvature, etabar)
  solution = calc_solution() # needs to be done 
  X20 = solution[0:nphi] 
  return calc_Y2s(Y2s_inhomogeneous, Y2s_from_X20, X20)

def derive_d_Y2s_d_varphi():
  """
  calculates d_Y2s_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)

  Y2s = derive_Y2s()
  return jnp.matmul(d_d_varphi, Y2s)

def derive_d_Y2c_d_varphi():
  """
  calculates d_Y2c_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  Y2c =
  return jnp.matmul(d_d_varphi, Y2c)
  
def derive_d_Z20_d_varphi():
  """
  calculates d_Z20_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  Z20 = 
  return jnp.matmul(d_d_varphi, Z20)

def derive_d_Z2s_d_varphi():
  """
  calculates d_Z2s_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  Z2s = 
  return jnp.matmul(d_d_varphi, Z2s)

def derive_d_Z2c_d_varphi():
  """
  calculates d_Z2c_d_varphi as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  Z2c = 
  return jnp.matmul(d_d_varphi, Z2c)

def derive_d2_X1c_d_varphi2(): 
  """
  calculates d2_X1c_d_varphi2 as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  d_X1c_d_varphi = # should be in r1 derive 
  return jnp.matmul(d_d_varphi, d_X1c_d_varphi)
  
def derive_d2_Y1c_d_varphi2(): 
  """
  calculates d2_Y1c_d_varphi2 as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  d_Y1c_d_varphi = #should be in r1 derive 
  return jnp.matmul(d_d_varphi, d_Y1c_d_varphi)

def derive_d2_Y1s_d_varphi2(): 
  """
  calculates d2_Y1s_d_varphi2 as a function of inputed parameters
  """
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  d_Y1s_d_varphi = # should be in r1 derive 
  return jnp.matmul(d_d_varphi, d_Y1s_d_varphi)