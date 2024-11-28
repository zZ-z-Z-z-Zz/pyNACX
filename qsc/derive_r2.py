from calculate_r2_helpers import * 
from init_axis_helpers import * 
from calculate_r1 import solve_sigma_equation
from calculate_r1_helpers import *

import jax.numpy as jnp




def calc_solution():
  #TODO 



def recalc_rc(Y1c, Y1s, X1c, ): 
  """
  a different rc is used after curvature is calculated
  """
  d_d_varphi = 
    
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

  Y1c = derive_calc_Y1c(sG, spsi, nphi, nfp, rc, rs, zc, zs, sigma, etabar)

  Y1s = derive_calc_Y1s(sG, spsi, nphi, nfp, rc, rs, zc, zs, etabar)

  V1 = calc_V1(X1c, Y1c, Y1s) 

  Z20 = calc_Z20(factor, d_d_varphi , V1) # in ret  // done

  mu0 =  4 * jnp.pi * 1e-7

  qc = calc_qc(iota_N, X1c, Y1s, torsion, abs_G0_over_B0)
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
  B20 = derive_B20()
  d_l_d_phi = calc_d_l_d_phi(nphi, nfp, rc, rs, zc, zs)
  normalizer = 1/jnp.sum(d_l_d_phi)

  return jnp.sum(B20 * d_l_d_phi) * normalizer

def derive_B20_anomaly(nphi, nfp, rc, rs, zc, zs):
  B20_mean = derive_B20_mean(nphi, nfp, rc, rs, zc, zs) 
  B20 = derive_B20()
  return B20 - B20_mean

def derive_B20_residual(B0, nphi, nfp, rc, rs, zc, zs): 
  B20 = derive_B20()
  B20_mean = derive_B20_mean(nphi, nfp, rc, rs, zc, zs)
  d_l_d_phi = calc_d_l_d_phi(nphi, nfp, rc, rs, zc, zs)
  normalizer = 1/jnp.sum(d_l_d_phi)

  return jnp.sqrt(jnp.sum((B20 - B20_mean) * (B20 - B20_mean) * d_l_d_phi) * normalizer) / B0

def derive_B20_variation(): 
  B20 = derive_B20()
  return jnp.max(B20) - jnp.min(B20)

def derive_N_helicity(nfp): 
  helicity = # in init_axis // will take alot of untangaling
  return - helicity * nfp

def derive_G2(B0 ,I2, p2 ,sG ,nphi ,nfp, rc, rs, zc, zs): 
  mu0 = 4 * jnp.pi * 1e-7
  G0 = calc_G0(sG,  nphi,  B0, nfp, rc, rs, zc, zs)
  iota = # solve sigma equation
  return -mu0 * p2 * G0 / (B0 * B0) - iota * I2

def derive_d_curvature_d_varphi(rc, zs, rs, zc, nfp,  nphi): 
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  curvature = calc_curvature(nphi, nfp, rc, rs, zc, zs)
  jnp.matmul(d_d_varphi, curvature)

def derive_d_torsion_d_varphi(rc, zs, rs, zc, nfp,  nphi): 
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  torsion = # B20
  return jnp.matmul(d_d_varphi, torsion)

def derive_d_X20_d_varphi(rc, zs, rs, zc, nfp, nphi): 
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  solutions = calc_solutions()
  X20 = calc_X20(solutions, nphi)
  return jnp.matmul(d_d_varphi, X20)

def derive_d_X2s_d_varphi(rc, zs, rs, zc, nfp,  nphi): 
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  # this will be a pain should probably make a derive calc_X2s
  X2s = calc_X2s(B0_over_abs_G0, d_d_varphi, Z2s, iota_N, Z2c, abs_G0_over_B0, B2s, B0, qc, qs, rc, rs, curvature) 
  return jnp.matmul(d_d_varphi, X2s)

def derive_d_X2c_d_varphi(): 
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  X2c = calc_X2c()
  return jnp.matmul(d_d_varphi, X2c)

def derive_d_Y20_d_varphi(rc, zs, rs, zc, nfp,  nphi): 
  d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp,  nphi)
  solution = 
  Y20 = solution[nphi:2 * nphi]
  return jnp.matmul(d_d_varphi, Y20)