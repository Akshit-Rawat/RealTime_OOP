#%% python circular buffer class

class CircBuff():
    ''' A class implementing elementary circular buffers of varying size

    A circular buffer can be updated with arbitrary length data
    - it starts filling memory at the position `head` 
      and continues to do so modulo the buffer size

    Reading out data is done as if it were a FIFO buffer
    - when reading the data, it starts reading from the current `head` position 
      and reads out all valid data
    '''
    def __init__(self, size=8):
        '''
        :params size: the size of the circular buffer (max. number of elements stored)
        '''
        self.__size = size
        self.__valid = [False] * self.__size
        self.__buffer = [None] * self.__size
        self.__head = 0

    @property
    def size(self):
        return self.__size

    @property
    def head(self):
        return self.__head

    def write(self, data):
        ''' write data into the cicrular buffer
        can be done element-wise or batch-wise
        :params data: the data to be written into the circular buffer, should be a tuple or a list of tuples
        '''
        if isinstance(data, tuple):
            self.__buffer[self.__head] = data  # write data at current head
            self.__valid[self.__head] = True  # validate
            self.__head += 1  # advance the head
            self.__head %= self.__size  # make sure to be circular
        elif isinstance(data, list):
            self.__update(data)  # more intelligent updating than going one-by-one through the list
        else:
            raise TypeError('Implementation not defined for {}'.format(type(data)))

    def read(self):
        ''' reading out the data from oldest to newest sample
        the read-out only reports valid data
        '''
        ix = self.__get_indices()
        return [self.__buffer[i] for i in ix if self.__valid[i]]

    def clear(self):
        ''' clear the current buffer
        clearing is simply done by setting the validation mask to False
        '''
        self.__valid = [False] * self.__size

    def __update(self, data):
        ''' write data, n at a time
        | | | |*| | | | |
               ^
               |
               head : start writing here
        '''
        # we write data backwards from the new head position
        # to avoid unnecessarily writing data that will be overwritten
        n = len(data)

        self.__head = (self.__head + n) % self.__size  # new head position after writing
        w = min(n, self.__size)  # total number of elements to write (must be no greater than buffer size)
        k = min(self.__head, w)  # number of elements that will be written before head
        m = w - k  # number of elements that will be written at end of buffer

        # write the last k samples
        if k>0:
            self.__buffer[self.__head-k:self.__head] = data[-k:]
            self.__valid[self.__head-k:self.__head] = [True] * k
            if m>0:
                self.__buffer[-m:] = data[-k-m:-k]
                self.__valid[-m:] = [True] * m
        else:
            self.__buffer[-w:] = data[-w:]
            self.__valid[-w:] = [True] * w
        
    def __get_indices(self):
        ''' give the circular indices starting with head
        '''
        ix = range(self.__head, self.__head+self.__size)
        return [i%self.__size for i in ix]


class FIFO():
    ''' implementation of a FIFO buffer based on temporal windowing
    incoming data are presented as a list of tuples (timestamp, data0, data1, ...)
    '''
    def __init__(self, win_len=1):
        self.__win_len = win_len
        self.__buffer = []

    def write(self, data, current_time=None):
        if isinstance(data, list):
            self.__buffer.extend(data)
        elif isinstance(data, tuple):
            self.__buffer.append(data)

        # filter the entries based on the current time and window length
        if current_time is not None:
            self.filter(current_time)

    def read(self):
        return self.__buffer

    def filter(self, current_time):
        self.__buffer = [x for x in self.__buffer if x[0] > current_time - self.__win_len]
        self.sort()

    def sort(self):
        self.__buffer.sort(key = lambda x: x[0])  # sort entries by time

    def clear(self):
        self.__buffer = []

        

#%% use the buffer

if __name__ == "__main__":
    from scipy.stats import expon, norm
    import numpy as np
    import matplotlib.pyplot as plt
    from time import sleep
    # %matplotlib qt

    # global parameters
    plt.ion()  # interactive plotting
    dt = .01
    sigma = 1
    G = norm(loc=0, scale=sigma*np.sqrt(dt))

#%% regular sampling (circular buffer)
client_cb = CircBuff(size=101)
server_cb = CircBuff(size=501)
t = 0
x = 0
client_cb.write((0, 0))

fig_cb, ax_cb = plt.subplots()

while t <= 100:
    t += dt
    x += G.rvs()
    client_cb.write((t, x))
    cb = client_cb.read()

    if np.abs(t % 1) <= dt:
        server_cb.write(cb)
        server_cb.read()
        client_cb.clear()

        print('update plot at t={}'.format(t))
        t_, x_ = zip(*server_cb.read())
        ax_cb.clear()
        ax_cb.plot(t_, x_)
        ax_cb.set_xlim([t-5, t])
        ax_cb.set_ylim([-10, 10])
        fig_cb.canvas.draw()  # update figure
        fig_cb.canvas.flush_events()
        sleep(.5)


#%% Event-based (FIFO queue)
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


# %%
