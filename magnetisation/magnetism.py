"""
The actual Boltzmann constant is
k = 1.38064852 × 10-23 m^2 kg s^-2 K^-1
"""
from math import tanh, sinh, cosh, exp, log
from functools import partial
from colorsys import hsv_to_rgb

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm

import plotly.graph_objs as go
import plotly


# k = 1.38064852e-23 # Boltzmann constant
k = 1.0  # Boltzmann constant
mu_0 = 1.0  # Magnetic moment
T = 1.0  # Temperature
beta = 1/(k * T)
J = 1  # Spin interaction coefficient

# Plotting params for external field variable H.
H_min = -3.
H_max = 3.
H_step = 100
Hs = np.linspace(H_min, H_max, H_step)  # list of values for H

# Setting ticks for y-axis.
margin = 0.1
m_min = - mu_0 * (1 + margin)
m_max = mu_0 * (1 + margin)
yticks = np.linspace(-mu_0, mu_0, 10)


def vanilla_mag_func(H, beta):
    return mu_0 * tanh(mu_0 * beta * H)


def mag_func_two_spin(H, beta, J):
    H_ = 2 * beta * mu_0 * H
    return mu_0 * sinh(H_)/(cosh(H_) + exp(- 2 * beta * J))


beta_steps = 100
max_temp = 100000
min_temp = 0.2
beta_range = np.linspace(1/(k * max_temp), 1/(k * min_temp), beta_steps)
# beta_range = [log(e) for e in np.linspace(exp(1/300), exp(4), beta_steps)]
col_range = np.linspace(3/3, 2/3, beta_steps)
# beta_range = [1/(k * T) for T in np.linspace(min_temp, max_temp, beta_steps)]
# col_range = np.linspace(2/3, 3/3, beta_steps)

# fig = plt.figure()
# st = fig.suptitle(r'Magnetisation curves')
# for i, J in enumerate([+1, -1]):
#     # Settings for each subplot
#     ax = fig.add_subplot(2, 1, i + 1)
#     ax.set_title(r'$J={}$, ${} < T < {}$ '.format(J, min_temp, max_temp))
#     ax.set_xlim([H_min, H_max])
#     ax.set_ylim([m_min, m_max])
#     ax.set_xlabel(r'External field strength: $H$')
#     ax.set_ylabel(r'Average magnetisation $<\hat{m}>$')
#     ax.set_aspect('auto')

#     # Get color function on hue
#     color_func = partial(hsv_to_rgb, s=1.0, v=1.0)
#     # Just include the vanilla tanh curve
#     func_list = [(partial(vanilla_mag_func, beta=beta), color_func(1/3))]

#     # Get a list of mag_func's with beta and J partially substituted
#     for b, c in zip(beta_range, col_range):
#         func_list.append((partial(mag_func_two_spin, beta=b, J=J), color_func(c)))

#     for func, color in func_list:
#         ms = [func(H) for H in Hs]
#         ax.plot(Hs, ms,
#                 color=color,
#                 lw=1,
#                 alpha=0.6)

# Avoid overlaps btwn the subplots
# plt.tight_layout()
# # Avoid overlaps between the supertitle and the subplots
# st.set_y(0.95)
# fig.subplots_adjust(top=0.85)

# fig.savefig("magnetisation.png")


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Make data
#X, Y = np.meshgrid(Hs, beta_range)
X, Y = np.meshgrid(beta_range, Hs)


def np_mag_func_two_spin(H, beta, J):
    nume = np.sinh(2 * beta * mu_0 * H)
    denom = np.cosh(2 * beta * mu_0 * H) + np.exp(- 2 * beta * J)
    mu = mu_0 * np.divide(nume, denom)
    return mu


Z = np_mag_func_two_spin(Y, X, -1)

# Plot the surface.
surf = ax.plot_surface(X, Y, Z,
                       linewidth=0, antialiased=False)

# Customize the z axis.

ax.set_zlim(m_min, m_max)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)


fig.savefig("magnetisation-3d.png")

# plt.show()


# steps = 100
# max_temp = 10
# min_temp = 0.01

# beta_range_dict = {'inverse_temp': np.linspace(1/(k * max_temp), 1/(k * min_temp), steps),
#                    'inverse_temp_log': [log(e) for e in np.linspace(exp(1/300), exp(4), steps)],
#                    'temp': [1/(k * T) for T in np.linspace(min_temp, max_temp, steps)]}
# # beta_range_type = 'inverse_temp'
# beta_range_type = 'temp'
# beta_range = beta_range_dict[beta_range_type]
# J = -1

# z = []
# for b in beta_range:
#     row = []
#     for H in Hs:
#         row.append(mag_func_two_spin(H, b, J=J))
#     z.append(row)

# # Create a trace
# trace = go.Surface(z=z)

# data = [trace]
# # Plot and embed in ipython notebook
# filename = 'magnetisation-surface-for-double-spin-interaction-J_{}-T{}-{}-{}'.format(
#     J, min_temp, max_temp, beta_range_type)
# plotly.offline.plot(data, filename=filename)
