import scipy.integrate
import numpy as np
import scipy.special as ss

##################################################################################
# DEFINE MIN AND MAX MASS SELECTOR
##################################################################################
def mass_min_max_select(kstar_1, kstar_2):
    primary_max = 150.0
    secondary_max = 150.0

    primary_min = 0.08
    secondary_min = 0.08
    
    min_mass = [primary_min, secondary_min]
    max_mass = [primary_max, secondary_max]

    if len(kstar_1) == 1:
        # there is a range of final kstar_1s to save
        kstar_1_lo = kstar_1
        kstar_1_hi = kstar_1
    else:
        kstar_1_lo = kstar_1[0]
        kstar_1_hi = kstar_1[1]

    if len(kstar_2) == 1:
        # there is a range of final kstar_1s to save
        kstar_2_lo = kstar_2
        kstar_2_hi = kstar_2
    else:
        kstar_2_lo = kstar_2[0]
        kstar_2_hi = kstar_2[1]

    kstar_lo = [kstar_1_lo, kstar_2_lo]
    kstar_hi = [kstar_1_hi, kstar_2_hi]

    ii = 0
    for k in kstar_lo:
        if k == 14:
            min_mass[ii] = 15.0
        elif k == 13:
            min_mass[ii] = 8.0
        elif k == 12:
            min_mass[ii] = 5.0
        elif k == 11:
            min_mass[ii] = 2.0
        elif k == 10:
            min_mass[ii] = 0.5
        ii += 1

    ii = 0
    for k in kstar_hi:
        if k == 13:
            max_mass[ii] = 20.0
        elif k == 12:
            max_mass[ii] = 12.0
        elif k== 11:
            max_mass[ii] = 8.0
        elif k == 10:
            max_mass[ii] = 5.0
        ii += 1

    return min_mass[0], max_mass[0], min_mass[1], max_mass[1]


def idl_tabulate(x, f, p=5) :
    def newton_cotes(x, f) :
        if x.shape[0] < 2 :
            return 0
        rn = (x.shape[0] - 1) * (x - x[0]) / (x[-1] - x[0])
        weights = scipy.integrate.newton_cotes(rn)[0]
        return (x[-1] - x[0]) / (x.shape[0] - 1) * np.dot(weights, f)
    ret = 0
    for idx in range(0, x.shape[0], p - 1) :
        ret += newton_cotes(x[idx:idx + p], f[idx:idx + p])
    return ret


def rndm(a, b, g, size):
    """Power-law gen for pdf(x)\propto x^{g-1} for a<=x<=b"""
    r = np.random.random(size=size)
    ag, bg = a**g, b**g
    return (ag + (bg - ag)*r)**(1./g)

def param_transform(dat):
    '''
    Transforms a data set to limits between zero and one
    '''

    datMin = min(dat)-0.000001
    datMax = max(dat)+0.000001
    datZeroed = dat-datMin

    datTransformed = datZeroed/((datMax-datMin)*1.000001)
    return datTransformed


def dat_transform(dat):
    '''
    Transform a data set to have limits between zero and one using 
    param_transform, then transform to logit space
    '''

    m1_trans = param_transform(dat.mass_1)
    m2_trans = param_transform(dat.mass_2)
    porb_trans = param_transform(dat.porb)
    #note: ecc is between zero and one
    ecc_trans = dat.ecc
    ecc_trans[ecc_trans < 1.0e-6] = 1.0e-6
    dat_trans = ss.logit(np.vstack([m1_trans, m2_trans, porb_trans, ecc_trans]))

    return dat_trans

def dat_un_transform(gx_sample, dat_set):
    m1_untrans = ss.expit(gx_sample[0, :]) *\
                 (max(dat_set.mass_1) - min(dat_set.mass_1)) +\
                 min(dat_set.mass_1)
    m2_untrans = ss.expit(gx_sample[1, :]) *\
                 (max(dat_set.mass_2) - min(dat_set.mass_2)) +\
                 min(dat_set.mass_2)
    porb_untrans = ss.expit(gx_sample[2, :]) *\
                   (max(dat_set.porb) - min(dat_set.porb)) +\
                   min(dat_set.porb)
    ecc_untrans = ss.expit(gx_sample[3, :])

    dat = np.vstack([m1_untrans, m2_untrans, porb_untrans, ecc_untrans])

    return dat
