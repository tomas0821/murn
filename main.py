from scipy.optimize import leastsq
import numpy as np
import matplotlib.pyplot as plt

alat,energies_Ry = np.loadtxt("alE.in", delimiter=" ", dtype='f, f', unpack=True)
#print alat

#Calculate the volume
vols = alat**3

#Change to eV
energies = energies_Ry*13.6

# Estimate an initial guess
x0 = [np.amin(energies), 1, 4, np.mean(vols)]
print x0

def Murnaghan(parameters, vol):
    'From Phys. Rev. B 28, 5480 (1983)'
    E0, B0, BP, V0 = parameters

    E = E0 + B0 * vol / BP * (((V0 / vol)**BP) / (BP - 1) + 1) - V0 * B0 / (BP - 1.0)

    return E

def objective(pars, y, x):
    #we will minimize this function
    err =  y - Murnaghan(pars, x)
    return err

plsq = leastsq(objective, x0, args=(energies, vols))

print 'Fitted parameters = {0}'.format(plsq[0])

#plot the fitted curve on top
x = np.linspace(min(vols), max(vols), 50)
y = Murnaghan(plsq[0], x)
plt.plot(x, y, 'k-')
plt.xlabel('Volume')
plt.ylabel('Energy')
plt.savefig('images/nonlinear-curve-fitting.png')