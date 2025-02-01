"""
This module contains the calculation for the O(r^2) solution
"""

import logging
import numpy as np
from .util import mu0
import jax.numpy as jnp
from .calculate_r1_helpers import *
from .calculate_r2_helpers import * 
from .derive_r2 import *

#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def calculate_r2(self, _residual, _jacobian, rc, zs, rs, zc, nfp, etabar, sigma0, B0, I2, sG, spsi, nphi, B2s, B2c, p2):
    """
    Compute the O(r^2) quantities.
    """
    logger.debug('Calculating O(r^2) terms')
    # First, some shorthand:
    nphi = nphi
    G0 = calc_G0(sG,  nphi,  B0, nfp, rc, rs, zc, zs)
    B0_over_abs_G0 = calc_B0_over_abs_G0(B0, G0) 
    abs_G0_over_B0 = 1 / B0_over_abs_G0
    X1c = derive_calc_X1c(etabar, nphi, nfp, rc, rs, zc, zs)
    Y1s = derive_calc_Y1s(sG, spsi, nphi, nfp, rc, rs, zc, zs, etabar)
    Y1c = derive_calc_Y1c(_residual, _jacobian, sG, spsi, nphi, nfp, rc, rs, zc, zs, sigma0, etabar)
    helicity = derive_helicity(rc, nfp, zs, rs, zc, nphi, sG, spsi)
    sigma = solve_sigma_equation(_residual, _jacobian, nphi, sigma0, helicity, nfp)[0]
    d_d_varphi = calc_d_d_varphi(rc, zs, rs, zc, nfp, nphi)
    iota = solve_sigma_equation(_residual, _jacobian, nphi, sigma0, helicity, nfp)[1]
    
    iota_N = calc_iotaN(iota, helicity, nfp)
    curvature = calc_curvature(nphi, nfp, rc, rs, zc, zs)
    torsion = calc_torsion(_residual, _jacobian, nphi, nfp, rc, rs, zc, zs, sG, etabar, spsi, sigma0, B0)
    etabar = etabar
    B0 = B0
    I2 = I2
    B2s = B2s
    B2c = B2c
    p2 = p2
    sG = sG
    spsi = spsi
    I2_over_B0 = I2 / B0

    if jnp.abs(iota_N) < 1e-8:
        logger.warning('|iota_N| is very small so O(r^2) solve will be poorly conditioned. '
                       f'iota_N={iota_N}')

   
    V1 = calc_V1(X1c, Y1c, Y1s)
    V2 = calc_V2(Y1s, Y1c)
    V3 = calc_V3(X1c, Y1c, Y1s)

    factor = calc_factor(B0_over_abs_G0)

    Z20 = calc_Z20(factor, d_d_varphi, V1)
    Z2s = calc_Z2s(factor, d_d_varphi, V2, iota_N, V3)
    Z2c = calc_Z2c(factor, d_d_varphi, V3, iota_N, V2)

    qs = calc_qs(iota_N, X1c, Y1s, torsion, abs_G0_over_B0)
    qc = calc_qc(d_d_varphi, X1c, Y1c, torsion, abs_G0_over_B0)
    rs = calc_rs(d_d_varphi, Y1s, iota_N, Y1c) # recalculation 
    rc = calc_rc(d_d_varphi, Y1c, iota_N, Y1s, X1c, torsion, abs_G0_over_B0) # recalculation 

    X2s = calc_X2s(B0_over_abs_G0, d_d_varphi, Z2s, iota_N, Z2c, abs_G0_over_B0, B2s, B0, qc, qs, rc, rs, curvature)

    X2c = calc_X2c(B0_over_abs_G0, d_d_varphi, Z2c, iota_N, Z2s, abs_G0_over_B0, B2c, B0, etabar, qc, qs, rc, rs, curvature)
    
    beta_1s = calc_beta_1s(spsi, sG, mu0, p2, etabar, abs_G0_over_B0, iota_N, B0)

    Y2s_from_X20 = calc_Y2s_from_X20(sG, spsi, curvature, etabar)
    Y2s_inhomogeneous = calc_Y2s_inhomogeneous(sG, spsi, curvature, etabar, X2c, X2s, sigma)

    Y2c_from_X20 = calc_Y2c_from_X20(sG, spsi, curvature,sigma,  etabar)
    Y2c_inhomogeneous = calc_Y2c_inhomogeneous(sG, spsi, curvature, etabar, X2s, X2c, sigma)

    # Note: in the fX* and fY* quantities below, I've omitted the
    # contributions from X20 and Y20 to the d/dzeta terms. These
    # contributions are handled later when we assemble the large
    # matrix.

    fX0_from_X20 = -4 * sG * spsi * abs_G0_over_B0 * (Y2c_from_X20 * Z2s - Y2s_from_X20 * Z2c)
    fX0_from_Y20 = -torsion * abs_G0_over_B0 - 4 * sG * spsi * abs_G0_over_B0 * (Z2s) \
        - spsi * I2_over_B0 * (-2) * abs_G0_over_B0
    fX0_inhomogeneous = calc_fX0_inhomogeneous(curvature, abs_G0_over_B0, Z20, sG, spsi, Y2c_inhomogeneous, Z2s, Y2s_inhomogeneous, Z2c, I2_over_B0, beta_1s, Y1c)

    fXs_from_X20 = calc_fXs_from_X20(torsion, abs_G0_over_B0, Y2s_from_X20, spsi, sG, Y2c_from_X20, Z20, I2_over_B0)
    fXs_from_Y20 = calc_fXs_from_Y20(spsi, sG, abs_G0_over_B0, Z2c, Z20)
    fXs_inhomogeneous = calc_fXs_inhomogeneous(d_d_varphi, X2s, iota_N, X2c, torsion, abs_G0_over_B0, Y2s_inhomogeneous, curvature, Z2s, spsi, sG, Y2c_inhomogeneous, Z20, I2_over_B0, beta_1s, Y1s)

    fXc_from_X20 = calc_fXc_from_X20(torsion, abs_G0_over_B0, Y2c_from_X20, spsi, sG, Y2s_from_X20, Z20, I2_over_B0)
    fXc_from_Y20 = calc_fXc_from_Y20(torsion, abs_G0_over_B0, spsi, sG, Z2s,  I2_over_B0 )
    fXc_inhomogeneous = calc_fXc_inhomogeneous(d_d_varphi, X2c, iota_N, X2s, torsion, abs_G0_over_B0, Y2c_inhomogeneous, curvature, Z2c, spsi, sG, Y2s_inhomogeneous, Z20, I2_over_B0, beta_1s, Y1c)

    fY0_from_X20 = calc_fY0_from_X20(torsion, abs_G0_over_B0, spsi, I2_over_B0)
    fY0_from_Y20 = jnp.zeros(nphi)
    fY0_inhomogeneous = calc_fY0_inhomogeneous(spsi, sG, abs_G0_over_B0, X2s, Z2c, X2c, Z2s, I2_over_B0, curvature, X1c, beta_1s)

    fYs_from_X20 = calc_fYs_from_X20(torsion, abs_G0_over_B0, spsi, I2_over_B0)
    fYs_from_X20 = calc_fYs_from_X20(iota_N, Y2c_from_X20, spsi, sG, abs_G0_over_B0, Z2c)
    fYs_from_Y20 = jnp.full(nphi, -2 * iota_N)
    fYs_inhomogeneous = cacl_fYs_inhomogeneous(d_d_varphi, Y2s_inhomogeneous, iota_N, Y2c_inhomogeneous, torsion, abs_G0_over_B0, X2s, spsi, sG, X2c, Z20, I2_over_B0)

    fYc_from_X20 = calc_fYc_from_X20(iota_N, Y2s_from_X20, spsi, sG, abs_G0_over_B0, Z2s)
    fYc_from_Y20 = jnp.zeros(nphi)
    fYc_inhomogeneous = calc_fYc_inhomogeneous(d_d_varphi, Y2c_inhomogeneous, iota_N, Y2s_inhomogeneous, torsion, abs_G0_over_B0, X2c, spsi, sG, X2s, Z20, I2_over_B0, curvature, X1c, beta_1s)

    matrix = jnp.zeros((2 * nphi, 2 * nphi))
    right_hand_side = jnp.zeros(2 * nphi)
    for j in range(nphi):
        # Handle the terms involving d X_0 / d zeta and d Y_0 / d zeta:
        # ----------------------------------------------------------------

        # Equation 1, terms involving X0:
        # Contributions arise from Y1c * fYs - Y1s * fYc.
        matrix[j, 0:nphi] = Y1c[j] * d_d_varphi[j, :] * Y2s_from_X20 - Y1s[j] * d_d_varphi[j, :] * Y2c_from_X20

        # Equation 1, terms involving Y0:
        # Contributions arise from -Y1s * fY0 - Y1s * fYc, and they happen to be equal.
        matrix[j, nphi:(2*nphi)] = -2 * Y1s[j] * d_d_varphi[j, :]

        # Equation 2, terms involving X0:
        # Contributions arise from -X1c * fX0 + Y1s * fYs + Y1c * fYc
        matrix[j+nphi, 0:nphi] = -X1c[j] * d_d_varphi[j, :] + Y1s[j] * d_d_varphi[j, :] * Y2s_from_X20 + Y1c[j] * d_d_varphi[j, :] * Y2c_from_X20

        # Equation 2, terms involving Y0:
        # Contributions arise from -Y1c * fY0 + Y1c * fYc, but they happen to cancel.

        # Now handle the terms involving X_0 and Y_0 without d/dzeta derivatives:
        # ----------------------------------------------------------------

        matrix[j, j       ] = matrix[j, j       ] + X1c[j] * fXs_from_X20[j] - Y1s[j] * fY0_from_X20[j] + Y1c[j] * fYs_from_X20[j] - Y1s[j] * fYc_from_X20[j]
        matrix[j, j + nphi] = matrix[j, j + nphi] + X1c[j] * fXs_from_Y20[j] - Y1s[j] * fY0_from_Y20[j] + Y1c[j] * fYs_from_Y20[j] - Y1s[j] * fYc_from_Y20[j]

        matrix[j + nphi, j       ] = matrix[j + nphi, j       ] - X1c[j] * fX0_from_X20[j] + X1c[j] * fXc_from_X20[j] - Y1c[j] * fY0_from_X20[j] + Y1s[j] * fYs_from_X20[j] + Y1c[j] * fYc_from_X20[j]
        matrix[j + nphi, j + nphi] = matrix[j + nphi, j + nphi] - X1c[j] * fX0_from_Y20[j] + X1c[j] * fXc_from_Y20[j] - Y1c[j] * fY0_from_Y20[j] + Y1s[j] * fYs_from_Y20[j] + Y1c[j] * fYc_from_Y20[j]


    right_hand_side[0:nphi] = -(X1c * fXs_inhomogeneous - Y1s * fY0_inhomogeneous + Y1c * fYs_inhomogeneous - Y1s * fYc_inhomogeneous)
    right_hand_side[nphi:2 * nphi] = -(- X1c * fX0_inhomogeneous + X1c * fXc_inhomogeneous - Y1c * fY0_inhomogeneous + Y1s * fYs_inhomogeneous + Y1c * fYc_inhomogeneous)

    solution = jnp.linalg.solve(matrix, right_hand_side)
    X20 = solution[0:nphi]
    Y20 = solution[nphi:2 * nphi]

    # Now that we have X20 and Y20 explicitly, we can reconstruct Y2s, Y2c, and B20:
    Y2s = calc_Y2s(Y2s_inhomogeneous, Y2s_from_X20, X20)
    Y2c = calc_Y2c(Y2c_inhomogeneous, Y2c_from_X20, X20, Y20)

    B20 = derive_B20(rc, zs, rs, zc, nfp, etabar, sigma0, B0, I2, sG, spsi, nphi, B2s, B2c, p2)

    d_l_d_phi = self.d_l_d_phi
    normalizer = 1 / jnp.sum(d_l_d_phi)
    self.B20_mean = derive_B20_mean(rc, zs, rs, zc, nfp, etabar, sigma0, B0, I2, sG, spsi, nphi, B2s, B2c, p2)
    self.B20_anomaly = derive_B20_anomaly(rc, zs, rs, zc, nfp, etabar, sigma0, B0, I2, sG, spsi, nphi, B2s, B2c, p2)
    self.B20_residual = derive_B20_residual(rc, zs, rs, zc, nfp, etabar, sigma0, B0, I2, sG, spsi, nphi, B2s, B2c, p2)
    self.B20_variation = derive_B20_variation(rc, zs, rs, zc, nfp, etabar, sigma0, B0, I2, sG, spsi, nphi, B2s, B2c, p2)

    self.N_helicity = derive_N_helicity(rc, nfp, zs, rs, zc, nphi, sG, spsi)
    self.G2 = derive_G2(B0 ,I2, p2 ,sG ,nphi ,nfp, rc, rs, zc, zs, sigma0, spsi)

    self.d_curvature_d_varphi = derive_d_curvature_d_varphi(rc, zs, rs, zc, nfp, nphi)
    self.d_torsion_d_varphi = derive_d_torsion_d_varphi(rc, zs, rs, zc, nfp,  nphi, sG, etabar, spsi, sigma0)
    self.d_X20_d_varphi = derive_d_X20_d_varphi(rc, zs, rs, zc, nfp, nphi)
    self.d_X2s_d_varphi = derive_d_X2s_d_varphi(rc, zs, rs, zc, nfp, nphi, sG, B0, etabar, B2s, sigma0, spsi, B2c)
    self.d_X2c_d_varphi = derive_d_X2c_d_varphi(rc, zs, rs, zc, nfp, etabar, sigma0, B0, sG, spsi, nphi, B2c)
    self.d_Y20_d_varphi = derive_d_Y20_d_varphi(rc, zs, rs, zc, nfp, etabar, sigma0, I2, B0, sG, spsi, nphi, B2s, p2)
    self.d_Y2s_d_varphi = derive_d_Y2s_d_varphi(rc, zs, rs, zc, nfp, etabar, sigma0, I2, B0, sG, spsi, nphi, B2s, p2, B2c)
    self.d_Y2c_d_varphi = derive_d_Y2c_d_varphi(rc, zs, rs, zc, nfp, etabar, sigma0, I2, B0, sG, spsi, nphi, B2s, p2, B2c)
    self.d_Z20_d_varphi = derive_d_Z20_d_varphi(sG, spsi, nphi, nfp, rc, rs, zc, zs, sigma0, etabar)
    self.d_Z2s_d_varphi = derive_d_Z2s_d_varphi(sG, spsi, nphi, nfp, rc, rs, zc, zs, sigma0, etabar)
    self.d_Z2c_d_varphi = derive_d_Z2c_d_varphi(sG, spsi, nphi, nfp, rc, rs, zc, zs, sigma0, etabar)
    self.d2_X1c_d_varphi2 = derive_d2_X1c_d_varphi2(etabar, nphi, nfp, rc, rs, zc, zs)
    self.d2_Y1c_d_varphi2 = derive_d2_Y1c_d_varphi2(sG, spsi, nphi, nfp, rc, rs, zc, zs, sigma0, etabar)
    self.d2_Y1s_d_varphi2 = derive_d2_Y1s_d_varphi2(sG, spsi, nphi, nfp, rc, rs, zc, zs, etabar)

    # Store all important results in self:
    self.V1 = V1
    self.V2 = V2
    self.V3 = V3

    self.X20 = X20
    self.X2s = X2s
    self.X2c = X2c
    self.Y20 = Y20
    self.Y2s = Y2s
    self.Y2c = Y2c
    self.Z20 = Z20
    self.Z2s = Z2s
    self.Z2c = Z2c
    self.beta_1s = beta_1s
    self.B20 = B20

    # O(r^2) diagnostics:
    self.mercier()
    self.calculate_grad_grad_B_tensor()
    #self.grad_grad_B_inverse_scale_length_vs_varphi = t.grad_grad_B_inverse_scale_length_vs_varphi
    #self.grad_grad_B_inverse_scale_length = t.grad_grad_B_inverse_scale_length
    self.calculate_r_singularity()

    if self.helicity == 0:
        self.X20_untwisted = self.X20
        self.X2s_untwisted = self.X2s
        self.X2c_untwisted = self.X2c
        self.Y20_untwisted = self.Y20
        self.Y2s_untwisted = self.Y2s
        self.Y2c_untwisted = self.Y2c
        self.Z20_untwisted = self.Z20
        self.Z2s_untwisted = self.Z2s
        self.Z2c_untwisted = self.Z2c
    else:
        angle = -self.helicity * self.nfp * self.varphi
        sinangle = jnp.sin(angle)
        cosangle = jnp.cos(angle)
        self.X20_untwisted = self.X20
        self.Y20_untwisted = self.Y20
        self.Z20_untwisted = self.Z20
        sinangle = jnp.sin(2*angle)
        cosangle = jnp.cos(2*angle)
        self.X2s_untwisted = self.X2s *   cosangle  + self.X2c * sinangle
        self.X2c_untwisted = self.X2s * (-sinangle) + self.X2c * cosangle
        self.Y2s_untwisted = self.Y2s *   cosangle  + self.Y2c * sinangle
        self.Y2c_untwisted = self.Y2s * (-sinangle) + self.Y2c * cosangle
        self.Z2s_untwisted = self.Z2s *   cosangle  + self.Z2c * sinangle
        self.Z2c_untwisted = self.Z2s * (-sinangle) + self.Z2c * cosangle
