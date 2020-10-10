## @package eom
#  \brief     Equations of motion
#  \details   Equations of motion for various systems.
#  \author    Robyn Woollands
#  \pre       numpy, const.py, spacecraft_params.py
#  \bug       No bugs known
#  \warning   Eclipse model commented due to extremely long run times

import numpy as np
import const as cn
import spacecraft_params as sc
# from eclipse_model import eclipse_grazing_goat
from numba import njit

__all__ = ["eom_twobody","eom_mee_twobodyJ2_minfuel"]

################################################################################
@njit
def eom_twobody(t,x):
    """
    Two-body equations of motion.
    Parameters:
    ===========
    t -- time
    x -- state vector
    Returns:
    ========
    dx -- state derivative vector
    External:
    =========
    numpy, const.py
    """
    r3 = np.linalg.norm(x[0:3])**3
    dx = np.zeros(6)
    # Two-body equations of motion
    dx[0] = x[3]
    dx[1] = x[4]
    dx[2] = x[5]
    dx[3] = -cn.mu*x[0]/r3
    dx[4] = -cn.mu*x[1]/r3
    dx[5] = -cn.mu*x[2]/r3
    return dx
################################################################################
@njit
def eom_mee_twobodyJ2_minfuel(t,x,rho,eclipse):
    """
    MEE min-fuel equations of motion using two-body and J2
    Parameters:
    ===========
    t       -- time
    x       -- state vector
    rho     -- switch smoothing parameter
    eclipse -- boolean (true or false)
    Return:
    =======
    dxdt -- state vector derivative
    External:
    =========
    numpy, const.py, spacecraft_params.py
    """
    dxdt = np.zeros(14)

    J2     = cn.J2
    c      = sc.c
    si2can = sc.si2can

    # Eclipse Model
    # if (eclipse):
        # [TF,Pa,zetaE] = eclipse_grazing_goat(t,x,rho)
    #     Thr = Pa*sc.A*sc.eff/sc.Isp/cn.g0  # Available Thrust (N)
    # else:
    #     Thr = sc.Thr
    Thr = sc.Thr # temporary fix

    # MEE States
    p = x[0]
    f = x[1]
    g = x[2]
    h = x[3]
    k = x[4]
    L = x[5]
    m = x[6]

    # MEE Costates
    pco1 = x[7]
    pco2 = x[8]
    pco3 = x[9]
    pco4 = x[10]
    pco5 = x[11]
    pco6 = x[12]
    pco7 = x[13]

    # Computed Symbolically in MATLAB
    t2 = np.cos(L)
    t3 = np.sin(L)
    t8 = f*t2
    t9 = g*t3
    t4 = t8+t9+1.0
    t5 = t4**2.0
    t6 = 1.0/m
    t7 = h*t3
    t10 = np.sqrt(p)
    t11 = 1.0/t4
    t12 = h**2.0
    t13 = k**2.0
    t14 = t12+t13+1.0
    t29 = k*t2
    t15 = t7-t29
    t30 = pco5*t3*t10*t11*t14*(1.0/2.0)
    t31 = g*pco2*t10*t11*t15
    t32 = pco4*t2*t10*t11*t14*(1.0/2.0)
    t16 = np.abs(t30-t31+t32+pco6*t10*t11*t15+f*pco3*t10*t11*t15)
    t17 = p**1.5
    t18 = t8+t9+2.0
    t21 = pco1*t11*t17*2.0
    t22 = t2*t18
    t23 = f+t22
    t24 = pco2*t10*t11*t23
    t25 = t3*t18
    t26 = g+t25
    t27 = pco3*t10*t11*t26
    t28 = t21+t24+t27
    t19 = np.abs(t28)
    t35 = pco3*t2*t10
    t36 = pco2*t3*t10
    t37 = t35-t36
    t20 = np.abs(t37)
    t44 = pco6*t10*t11*(t7-t29)
    t45 = f*pco3*t10*t11*(t7-t29)
    t46 = t30-t31+t32+t44+t45
    t33 = np.abs(t46)
    t34 = t19**2.0
    t38 = t20**2.0
    t39 = 1.0/(p**4.0)
    t40 = t7-t29
    t41 = 1.0/(t14**2.0)
    t42 = t5**2.0
    t43 = 1.0/rho
    t47 = t33**2.0
    t48 = t34+t38+t47
    t49 = 1.0/np.sqrt(t48)
    t50 = h*t2
    t51 = k*t3
    t52 = t50+t51
    t53 = J2*t15*t39*t41*t42*t52*12.0
    t54 = np.sqrt(t48)
    t55 = c*si2can*t6*t54
    t56 = pco7+t55-1.0
    t57 = t43*t56
    t58 = np.tanh(t57)
    t59 = t58*(1.0/2.0)
    t60 = t59+1.0/2.0
    t61 = t7-t29
    t62 = Thr*si2can*t6*t37*t49*t60
    t63 = Thr*si2can*t6*t28*t49*t60
    t64 = t53+t63
    t65 = t12+t13-1.0
    t66 = Thr*si2can*t6*t46*t49*t60
    t68 = J2*t15*t39*t41*t42*t65*6.0
    t67 = t66-t68
    t69 = t7-t29
    t70 = 1.0/np.sqrt(p)
    t71 = t7-t29
    t72 = 1.0/(p**4.5)
    t73 = t7-t29
    t74 = t7-t29
    t75 = t7-t29
    t76 = t7-t29
    t77 = t7-t29
    t78 = 1.0/t14
    t79 = 1.0/(p**1.5)
    t80 = 1.0/(p**3.5)
    t81 = t7-t29
    t82 = 1.0/(t4**2.0)
    t83 = t7-t29
    t84 = t7-t29
    t85 = (t2**2.0)
    t86 = t7-t29
    t87 = t7-t29
    t88 = 1.0/(p**2.5)
    t89 = t7-t29
    t90 = t2*t3*t10*t11*t64
    t91 = t7-t29
    t92 = t3**2.0
    t93 = t7-t29
    t94 = t7-t29
    t95 = t7-t29
    t96 = -t7+t29
    t98 = pco6*t10*t11*t96
    t99 = f*pco3*t10*t11*t96
    t100 = g*pco2*t10*t11*t96
    t101 = t30+t32-t98-t99+t100
    t97 = np.abs(t101)
    t102 = t97**2.0
    t103 = t34+t38+t102
    t104 = 1.0/(t14**3.0)
    t105 = J2*t39*t41*t42*t65*t96*6.0
    t106 = np.sqrt(t103)
    t107 = c*si2can*t6*t106
    t108 = pco7+t107-1.0
    t109 = t43*t108
    t110 = np.tanh(t109)
    t111 = t110*(1.0/2.0)
    t112 = t111+1.0/2.0
    t113 = 1.0/np.sqrt(t103)
    t114 = Thr*si2can*t6*t101*t112*t113
    t115 = t105+t114
    t116 = J2*t3*t39*t41*t42*t65*6.0
    t117 = J2*h*t39*t42*t65*t96*t104*24.0
    t122 = J2*h*t39*t41*t42*t96*12.0
    t118 = t116+t117-t122
    t119 = J2*t3*t39*t41*t42*t52*12.0
    t120 = J2*h*t39*t42*t52*t96*t104*48.0
    t127 = J2*t2*t39*t41*t42*t96*12.0
    t121 = t119+t120-t127
    t123 = t3*t41*t96*24.0
    t124 = t9**2.0
    t125 = h*t104*t124*48.0
    t126 = t123+t125
    t128 = J2*t2*t39*t41*t42*t65*6.0
    t129 = J2*k*t39*t41*t42*t96*12.0
    t134 = J2*k*t39*t42*t65*t96*t104*24.0
    t130 = t128+t129-t134
    t131 = J2*t2*t39*t41*t42*t52*12.0
    t132 = J2*t3*t39*t41*t42*t96*12.0
    t137 = J2*k*t39*t42*t52*t96*t104*48.0
    t133 = t131+t132-t137
    t135 = k*t104*t124*48.0
    t136 = t135-t2*t41*t96*24.0
    t138 = t41*t124*12.0
    t139 = t138-1.0
    t140 = f*t3
    t142 = g*t2
    t141 = t140-t142
    t143 = Thr*si2can*t6*t28*t112*t113
    t151 = J2*t39*t41*t42*t52*t96*12.0
    t144 = t143-t151
    t145 = J2*t4*t5*t39*t139*t141*6.0
    t146 = J2*t39*t41*t42*t52*t96*36.0
    t147 = t145+t146
    t148 = J2*t39*t42*t139*(3.0/2.0)
    t149 = Thr*si2can*t6*t37*t112*t113
    t150 = t148+t149
    t152 = t52**2.0
    t153 = J2*t39*t41*t42*t152*12.0
    t154 = J2*t4*t5*t39*t41*t52*t96*t141*48.0
    t155 = J2*t39*t41*t42*t52*t65*6.0
    t156 = J2*t4*t5*t39*t41*t65*t96*(t140-t142)*24.0
    t157 = t155+t156
    t158 = 1.0/m**2.0

    dxdt[0] = t11*t17*(t53+Thr*si2can*t6*t28*t49*(np.tanh(t43*(pco7+c*si2can*t6*np.sqrt(t34+t38+(t16**2.0))-1.0))*(1.0/2.0)+1.0/2.0))*-2.0
    dxdt[1] = t3*t10*(t62+J2*t39*t42*((t40**2.0)*t41*1.2e1-1.0)*(3.0/2.0))-t10*t11*t23*t64+g*t10*t11*t15*t67
    dxdt[2] = -t2*t10*(t62+J2*t39*t42*(t41*(t61**2.0)*1.2e1-1.0)*(3.0/2.0))-t10*t11*t26*t64-f*t10*t11*t15*t67
    dxdt[3] = t2*t10*t11*t14*t67*(-1.0/2.0)
    dxdt[4] = t3*t10*t11*t14*t67*(-1.0/2.0)
    dxdt[5] = t5*t79-t10*t11*t15*t67
    dxdt[6] = -(Thr*t60)/c

    dxdt[7] = pco6*(t5*t88*(3.0/2.0)+t11*t67*t70*(t7-t29)*(1.0/2.0)+J2*t4*t5*t41*t65*(t69**2.0)*t72*2.4e1)-pco2*(t3*t70*(t62+J2*t39*t42*(t41*(t71**2.0)*1.2e1-1.0)*(3.0/2.0))*(1.0/2.0)-t11*t23*t64*t70*(1.0/2.0)-J2*t3*t42*t72*(t41*(t73**2.0)*1.2e1-1.0)*6.0+g*t11*t15*t67*t70*(1.0/2.0)+J2*g*t4*t5*t41*t65*t72*(t74**2.0)*2.4e1+J2*t4*t5*t15*t23*t41*t52*t72*4.8e1)+pco3*(t2*t70*(t62+J2*t39*t42*(t41*(t75**2.0)*1.2e1-1.0)*(3.0/2.0))*(1.0/2.0)+t11*t26*t70*(t53+t63)*(1.0/2.0)-J2*t2*t42*t72*(t41*(t76**2.0)*1.2e1-1.0)*6.0+f*t11*t67*t70*(t7-t29)*(1.0/2.0)+J2*f*t4*t5*t41*t65*t72*(t77**2.0)*2.4e1-J2*t4*t5*t15*t26*t41*t52*t72*4.8e1)+pco1*t10*t11*(t53+t63)*3.0+pco4*t2*t11*t14*t67*t70*(1.0/4.0)+pco5*t3*t11*t14*t67*t70*(1.0/4.0)-J2*pco1*t4*t5*t15*t41*t52*t80*9.6e1+J2*pco4*t2*t4*t5*t65*t72*t78*(t7-t29)*1.2e1+J2*pco5*t3*t4*t5*t65*t72*t78*(t7-t29)*1.2e1

    dxdt[8] = pco3*(t90+t10*t11*t15*t67-t2*t10*t26*t82*(t53+t63)-f*t2*t10*t67*t82*(t7-t29)+J2*t4*t5*t80*t85*(t41*(t86**2.0)*12.0-1.0)*6.0-J2*f*t2*t5*t41*t65*t80*(t87**2.0)*24.0+J2*t2*t5*t15*t26*t41*t52*t80*48.0)+pco2*(t10*t11*t64*(t85+1.0)-t2*t10*t23*t82*(t53+t63)+g*t2*t10*t15*t67*t82-J2*t2*t3*t4*t5*t80*(t41*(t83**2.0)*12.0-1.0)*6.0+J2*g*t2*t5*t41*t65*t80*(t84**2.0)*24.0+J2*t2*t5*t15*t23*t41*t52*t80*48.0)-pco6*(t2*t4*t79*2.0+t2*t10*t15*t67*t82+J2*t2*t5*t41*t65*t80*(t81**2.0)*24.0)-pco1*t2*t17*t64*t82*2.0-pco4*t10*t14*t67*t82*t85*(1.0/2.0)-pco5*t2*t3*t10*t14*t67*t82*(1.0/2.0)+J2*pco1*t2*t5*t41*t52*t88*(t7-t29)*96.0-J2*pco4*t5*t15*t65*t78*t80*t85*12.0-J2*pco5*t2*t3*t5*t15*t65*t78*t80*12.0

    dxdt[9] = pco2*(t90-t10*t11*t67*(t7-t29)-t3*t10*t23*t82*(t53+t63)+g*t3*t10*t15*t67*t82-J2*t4*t5*t80*t92*(t41*(t89**2.0)*12.0-1.0)*6.0+J2*g*t3*t5*t41*t65*t80*(t91**2.0)*24.0+J2*t3*t5*t15*t23*t41*t52*t80*48.0)-pco6*(t3*t4*t79*2.0+t3*t10*t15*t67*t82+J2*t3*t5*t41*t65*t80*(t95**2.0)*24.0)+pco3*(t10*t11*t64*(t92+1.0)-t3*t10*t26*t82*(t53+t63)-f*t3*t10*t67*t82*(t7-t29)+J2*t2*t3*t4*t5*t80*(t41*(t93**2.0)*12.0-1.0)*6.0-J2*f*t3*t5*t41*t65*t80*(t94**2.0)*24.0+J2*t3*t5*t15*t26*t41*t52*t80*48.0)-pco1*t3*t17*t64*t82*2.0-pco5*t10*t14*t67*t82*t92*(1.0/2.0)-pco4*t2*t3*t10*t14*t67*t82*(1.0/2.0)+J2*pco1*t3*t5*t41*t52*t88*(t7-t29)*96.0-J2*pco5*t5*t15*t65*t78*t80*t92*12.0-J2*pco4*t2*t3*t5*t15*t65*t78*t80*12.0

    dxdt[10] = pco3*(t10*t11*t26*t121-J2*t2*t42*t80*t126*(3.0/2.0)+f*t3*t10*t11*t115+f*t10*t11*t96*t118)+pco2*(t10*t11*t23*t121+J2*t3*t42*t80*t126*(3.0/2.0)-g*t3*t10*t11*t115-g*t10*t11*t96*t118)+pco6*(t3*t10*t11*t115+t10*t11*t96*t118)+pco1*t11*t17*t121*2.0+h*pco4*t2*t10*t11*t115+h*pco5*t3*t10*t11*t115-pco4*t2*t10*t11*t14*t118*(1.0/2.0)-pco5*t3*t10*t11*t14*t118*(1.0/2.0)

    dxdt[11] = -pco3*(t10*t11*t26*t133+J2*t2*t42*t80*t136*(3.0/2.0)+f*t2*t10*t11*t115+f*t10*t11*t96*t130)+pco2*(-t10*t11*t23*t133+J2*t3*t42*t80*t136*(3.0/2.0)+g*t2*t10*t11*t115+g*t10*t11*t96*t130)-pco6*(t2*t10*t11*t115+t10*t11*t96*t130)-pco1*t11*t17*t133*2.0+k*pco4*t2*t10*t11*t115+k*pco5*t3*t10*t11*t115+pco4*t2*t10*t11*t14*t130*(1.0/2.0)+pco5*t3*t10*t11*t14*t130*(1.0/2.0)

    dxdt[12] = pco6*(t4*t79*(t140-t142)*2.0+t10*t11*t52*t115+t10*t11*t96*t157-t10*t82*t96*t115*t141)+pco3*(-t2*t10*t147-t3*t10*t150+t10*t11*(t22-t3*t141)*(t143-t151)+t10*t11*t26*(t153+t154-J2*t39*t41*t42*t124*12.0)+t10*t26*t82*(t140-t142)*(t143-t151)+f*t10*t11*t52*t115+f*t10*t11*t96*t157-f*t10*t82*t96*t115*t141)+pco2*(t3*t10*t147-t2*t10*t150+t10*t11*t23*(t153+t154-J2*t39*t41*t42*t124*12.0)-t10*t11*t144*(t25+t2*t141)-g*t10*t11*t52*t115-g*t10*t11*t96*t157+t10*t23*t82*t141*t144+g*t10*t82*t96*t115*t141)+pco1*t11*t17*(t153+t154-J2*t39*t41*t42*t124*12.0)*2.0+pco1*t17*t82*(t140-t142)*(t143-t151)*2.0-pco4*t3*t10*t11*t14*t115*(1.0/2.0)+pco5*t2*t10*t11*t14*t115*(1.0/2.0)-pco4*t2*t10*t11*t14*t157*(1.0/2.0)-pco5*t3*t10*t11*t14*t157*(1.0/2.0)+pco4*t2*t10*t14*t82*t115*(t140-t142)*(1.0/2.0)+pco5*t3*t10*t14*t82*t115*(t140-t142)*(1.0/2.0)

    dxdt[13] = -pco3*(Thr*si2can*t2*t10*t37*t112*t113*t158+Thr*si2can*t10*t11*t26*t28*t112*t113*t158-Thr*si2can*f*t10*t11*t96*t101*t112*t113*t158)-pco2*(-Thr*si2can*t3*t10*t37*t112*t113*t158+Thr*si2can*t10*t11*t23*t28*t112*t113*t158+Thr*si2can*g*t10*t11*t96*t101*t112*t113*t158)-Thr*si2can*pco1*t11*t17*t28*t112*t113*t158*2.0+Thr*si2can*pco6*t10*t11*t96*t101*t112*t113*t158-Thr*si2can*pco4*t2*t10*t11*t14*t101*t112*t113*t158*(1.0/2.0)-Thr*si2can*pco5*t3*t10*t11*t14*t101*t112*t113*t158*(1.0/2.0)

    return dxdt
################################################################################
