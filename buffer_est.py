from buffers_1 import FIFO
from scipy.stats import expon, norm
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

# global parameters
plt.ion()  # interactive plotting
dt = .01
sigma = 1
G = norm(loc=0, scale=sigma*np.sqrt(dt))
server_fifo = FIFO(5)
client_fifo = FIFO(1)
t = 0
x = 0
last_x = 0
client_fifo.write((0, 0))

epsilon = .5

fig, ax = plt.subplots()
plt.ion()  # interactive plotting

while t <= 100:
    t += dt
    x += G.rvs()
        
    if np.abs(x - last_x) >= epsilon:
        client_fifo.write((t, x), current_time=t)
        last_x = x
        print('added {} at t={}s'.format(x, t))
    if np.abs(t % 1) <= dt:
        server_fifo.write(client_fifo.read(), current_time=t)
        client_fifo.clear()

        print('update plot at t={}'.format(t))
        t_, x_ = zip(*server_fifo.read())
        ax.clear()
        ax.scatter(t_, x_)
        ax.set_xlim([t-5, t])
        ax.set_ylim([-10, 10])
        fig.canvas.draw()  # update figure
        fig.canvas.flush_events()
        sleep(.5)