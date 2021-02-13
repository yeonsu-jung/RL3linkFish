# %%
from scipy import integrate
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from scipy import signal

import matplotlib as mpl

mpl.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'

# plt.style.use('default')
# plt.rcParams.update({'font.family': 'sans-serif','text.usetex': 'true'})
# plt.rcParams["figure.figsize"] = (2.2,1.8)
# plt.rcParams['figure.dpi'] = 150
# plt.rcParams['lines.linewidth'] = 0.5
# plt.rcParams['lines.color'] = 'r'
# plt.rcParams['axes.grid'] = 'false'
# #plt.rcParams.update({'figure.autolayout': True})
# plt.rcParams.update({'font.size': 8})
# plt.rcParams.update({'lines.markersize': 2})


# %%
def my_square(t):    
    A = 5
    B = 1
    r = 1/(1+A/B)

    mag = (A+B)/2
    offset = (A-B)/2

    tau = (np.pi/3*(1/A + 1/B))/2/np.pi

    sig = mag*signal.square(t/tau,duty=r) + offset
    # sig = mag*np.sin(t/tau) + offset

    return sig

tt = np.linspace(0,10,1000)
plt.plot(tt,my_square(tt),'o')
plt.plot([np.min(tt),np.max(tt)],[0,0],'k--')

# %%
def alphadot(t,y):    
    return my_square(t)

solution = integrate.solve_ivp(alphadot, [0,np.max(tt)], [np.pi/3], t_eval=tt)

plt.plot(solution.t,solution.y[0])


# %%    

def alphadot1(t):
    # return np.pi/3*np.cos(t)    
    return my_square(t)

def alphadot2(t):
    # return np.pi/3*np.cos(t)
    return my_square(t)

def function1(t, u, R, k, m, c_min):  #original function   

    if np.absolute(alphadot1(t)) > c_min:
        f0_1 = R*np.sin(np.pi/2 - u[4]) * (np.sign(alphadot1(t)))
        f2_1 = R*np.cos(np.pi/2 - u[4]) * (np.sign(alphadot1(t)))
    else:
        f0_1 = 0
        f2_1 = 0

    if np.absolute(alphadot2(t)) > c_min:
        f0_2 = -R*np.sin(np.pi/2 - u[5]) * (np.sign(alphadot1(t)))
        f2_2 = R*np.cos(np.pi/2 - u[5]) * (np.sign(alphadot1(t)))
    else:
        f0_2 = 0
        f2_2 = 0        
        
    f0 = (f0_1 + f0_2 - k*u[0])/m
    f1 = u[0]
    f2 = (f2_1 + f2_2 - k*u[2])/m
    f3 = u[2]    
    f4 = alphadot1(t)
    f5 = alphadot2(t)
    return f0, f1, f2, f3, f4, f5

function2 = lambda t, y: function1(t, y, R = 1, k = 1, m = 1, c_min = 1.5)  #function with only t and y

t = np.linspace(0, 10, 1000)

solution = integrate.solve_ivp(function2, (0, np.max(t)), (0,0,0,0,np.pi/3,np.pi/3), t_eval = t)

fig,ax = plt.subplots(6,figsize = (4,10))
for i in range(6):
    ax[i].plot(t,solution.y[i])

ax[0].set_ylabel('$\dot{x}$')
ax[0].set_ylabel('$x$')
ax[0].set_ylabel('$\dot{y}$')
ax[0].set_ylabel('$y$')
ax[5].set_xlabel('$t$')
# %%
L = 1

xx = solution.y[1]
yy = solution.y[3]
a1 = solution.y[4]
a2 = solution.y[5]

xx_left = xx - L*np.sin(a1)
yy_left = yy + L*np.cos(a1)
xx_right = xx + L*np.sin(a2)
yy_right = yy + L*np.cos(a2)

plt.plot(a1)

# %%
TL_x = []
TL_y = []
for ii in range(1000):
    TL_x.append([xx_left[ii],xx[ii],xx_right[ii]])
    TL_y.append([yy_left[ii],yy[ii],yy_right[ii]])


# %%
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-5, 5), ylim=(-2, 5))
ax.set_aspect('equal')
ax.set_axis_off()
# ax.grid()0

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
# %%

# matplotlib.use("TkAgg")
# plt.rcParams["backend"] = "TkAgg"

dt = 0.01

def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = TL_x[i]
    thisy = TL_y[i]

    line.set_data(thisx, thisy)
    # time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(TL_x)), init_func=init)
# plt.show()

writervideo = animation.FFMpegWriter(fps=120) 
ani.save('test.mp4', writervideo)

plt.show()

# %%
