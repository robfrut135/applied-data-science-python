import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

%matplotlib notebook

# generate 4 random variables from the random, gamma, exponential, and uniform distributions
x1 = np.random.normal(-2.5, 1, 10000)
x2 = np.random.gamma(2, 1.5, 10000)
x3 = np.random.exponential(2, 10000)+7
x4 = np.random.uniform(14,20, 10000)

# plot the histograms
plt.figure(figsize=(9,3))
plt.hist(x1, normed=True, bins=20, alpha=0.5)
plt.hist(x2, normed=True, bins=20, alpha=0.5)
plt.hist(x3, normed=True, bins=20, alpha=0.5)
plt.hist(x4, normed=True, bins=20, alpha=0.5);
plt.axis([-7,21,0,0.6])

plt.text(x1.mean()-1.5, 0.5, 'x1\nNormal')
plt.text(x2.mean()-1.5, 0.5, 'x2\nGamma')
plt.text(x3.mean()-1.5, 0.5, 'x3\nExponential')
plt.text(x4.mean()-1.5, 0.5, 'x4\nUniform')


##############################################################

n = 1000
x1 = np.random.normal(-2.5, 1, n)
x2 = np.random.gamma(2, 1.5, n)
x3 = np.random.exponential(2, n)
x4 = np.random.uniform(14,20, n)

axis_normal = [-6,1,0,50]
axis_gamma = [-1,15,0,70]
axis_exp = [-1,15,0,70]
axis_unif = [13,21,0,20]
axis_dist =[axis_normal, axis_gamma, axis_exp, axis_unif]

xs = [x1,x2,x3,x4]

def update(curr):
    if curr == n:
        a.event_source.stop()
    bins_normal = np.arange(-6, 2, 0.8)
    bins_gamma = np.arange(0, 30, 3)
    bins_exp = np.arange(0, 10, 0.5)
    bins_unif = np.arange(14, 20, 0.6)
    bin_sample = [bins_normal, bins_gamma, bins_exp, bins_unif]
    for i in range(0, len(axs)):
        axs[i].cla()
        axs[i].hist(xs[i][:curr], bins = bin_sample[i])
        axs[i].axis(axis_dist[i])

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
axs = [ax1,ax2,ax3,ax4]
a = animation.FuncAnimation(fig, update, interval=5)


