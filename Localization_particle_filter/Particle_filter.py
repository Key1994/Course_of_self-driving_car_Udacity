from math import *
import random
import matplotlib.pyplot as plt

landmarks = [[20.0, 20.0],
             [80.0, 80.0],
             [20.0, 80.0],
             [80.0, 20.0]]
world_size = 100.0


class robot:
    def __init__(self):
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise    = 0.0
        self.sense_noise   = 0.0

    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise (ValueError, 'X coordinate out of bound')
        if new_y < 0 or new_y >= world_size:
            raise (ValueError, 'Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise (ValueError, 'Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise)
        self.turn_noise    = float(new_t_noise)
        self.sense_noise   = float(new_s_noise)

    def sense(self):
        # measure distance of landmarks and get a result with gaussian noise
        Z = []
        for i in range(len(landmarks)):
            # true value
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z

    def move(self, turn, forward):
        if forward < 0:
            raise (ValueError, 'Robot cant move backwards')
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size  # cyclic truncate
        y %= world_size

        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def Gaussian(self, mu, sigma, x):
        return exp(-((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):
        prob = 1.0
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob

    def __repr__(self):
        return '[x=%s y=%s heading=%s]\n' % (str(self.x), str(self.y), str(self.orientation))


myrobot = robot()
myrobot.set_noise(0.05, 0.05, 5.0)
myrobot.set(10.0, 10.0, 0)
R = robot()
R.set(10.0, 10.0, 0)
Z = myrobot.sense()
N = 1000
T = 5
p = []
px = []
py = []
for i in range(N):
    r = robot()
    r.set_noise(0.05, 0.05, 5.0)
    p.append(r)
    px.append(r.x)
    py.append(r.y)

plt.scatter(px, py, c = 'blue')
plt.scatter(myrobot.x, myrobot.y, c = 'red', marker = 'x', s = 300)
plt.xlim(0,100)
plt.ylim(0,100)
# plt.show()
for t in range(T):
    R = R.move(0.1, 5.0)    # Exact position
    myrobot = myrobot.move(0.1, 5.0)
    Z = myrobot.sense()
    p2 = []
    for i in range(N):
        p2.append(p[i].move(0.1, 5.0))
    p = p2

    # Calculating importance weights
    w = []
    for i in range(N):
        w.append(p[i].measurement_prob(Z))

    # Resampling wheel
    index = int(random.random() * N)
    beta = 0.0
    p3 = []
    mw = max(w)
    for i in range(N):
        beta += random.random() * 2 * mw
        while beta > w[index]:
            beta -= w[index]
            index = (index + 1) % N
        p3.append(p[index])
    p = p3


    px = []
    py = []
    for i in range(N):
        px.append(p[i].x)
        py.append(p[i].y)
    plt.scatter(px, py, c='blue')
    plt.scatter(R.x, R.y, c='red', marker='x', s=100)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    # plt.show()

# Results analysis
sum_x = 0
sum_y = 0
sum_o = 0
for i in range(N):
    sum_x += p[i].x
    sum_y += p[i].y
    sum_o += p[i].orientation
ax = sum_x / N
ay = sum_y / N
ao = sum_o / N
for j in range(N):
    p[j].set(ax, ay, ao)

print('The results by particle filter:', str(ax), str(ay), str(ao))

ex = R.x - ax
ey = R.y - ay
eo = R.orientation - ao
print('Error: x: %f; y: %f; heading: %f.' % (ex, ey, eo))



