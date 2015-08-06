from matplotlib import pyplot as plt
from lattice import Lattice
from matplotlib.patches import FancyBboxPatch
from matplotlib.transforms import Bbox
from mpl_toolkits.mplot3d import Axes3D
from numpy import sqrt, array
from numpy.linalg import norm
from fancyArrows import Arrow3D

lv = [[1, 0, 0],[.5, .5 * sqrt(3), 0],[.5, .5 * 1/sqrt(3), sqrt(2. / 3)]]
lb = [[0, 0, 0], [.5, 0, 0], [0, .5, 0], [0, 0, .5]]
pyro = Lattice(lv, lb)
h = {(1, 0, 0): array([[ 0., -1.,  0.,  0.],
                       [ 0.,  0.,  0.,  0.],
                       [ 0.,  0.,  0.,  0.],
                       [ 0.,  0.,  0.,  0.]]), 
     (0, 0, 1): array([[ 0.,  0.,  0., -1.],
                       [ 0.,  0.,  0.,  0.],
                       [ 0.,  0.,  0.,  0.],
                       [ 0.,  0.,  0.,  0.]]), 
     (0, -1, 1): array([[ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0., -1.],
                        [ 0.,  0.,  0.,  0.]]), 
     (0, 0, 0): array([[ 0., -1., -1., -1.],
                       [-1.,  0., -1., -1.],
                       [-1., -1.,  0., -1.],
                       [-1., -1., -1.,  0.]]), 
     (-1, 1, 0): array([[ 0.,  0.,  0.,  0.],
                        [ 0.,  0., -1.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.]]), 
     (1, 0, -1): array([[ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0., -1.,  0.,  0.]]), 
     (1, -1, 0): array([[ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0., -1.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.]]), 
     (0, 0, -1): array([[ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [-1.,  0.,  0.,  0.]]), 
     (-1, 0, 1): array([[ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0., -1.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.]]), 
     (-1, 0, 0): array([[ 0.,  0.,  0.,  0.],
                        [-1.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.]]), 
     (0, 1, 0): array([[ 0.,  0., -1.,  0.],
                       [ 0.,  0.,  0.,  0.],
                       [ 0.,  0.,  0.,  0.],
                       [ 0.,  0.,  0.,  0.]]), 
     (0, 1, -1): array([[ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [ 0.,  0., -1.,  0.]]), 
     (0, -1, 0): array([[ 0.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.],
                        [-1.,  0.,  0.,  0.],
                        [ 0.,  0.,  0.,  0.]])}
offset = .7
minlim = -.1
zlimextra = -offset
maxlim = 1.9
ylimextra = offset
xlimextra = -offset
pyro.generatePoints([2,2,2])
pyro.generateHoppings(h)

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
ax.set_aspect('equal')

points = pyro.getPointsCartesian()
ax.scatter(points[:, 0], points[:, 1], points[:, 2], color = 'black', zorder = 5)

for linegroup in pyro.getHoppingsCartesian():
    for line in linegroup:
        pltkwargs = {'color': 'red', 'linestyle': '-', 'linewidth': .5, 'alpha': .5, 'zorder': 4}
        ax.plot(line[:, 0], line[:, 1], line[:, 2], **pltkwargs)
        pltkwargs = {'color': 'darkred', 'linestyle': '-', 'linewidth': .5, 'zorder': 3}
        ax.plot(line[:, 0], line[:, 1], [minlim+zlimextra]*len(line[:,0]), **pltkwargs)
        ax.plot( [minlim+xlimextra]*len(line[:,0]), line[:, 1],line[:, 2], **pltkwargs)
        ax.plot(line[:,0], [maxlim+ylimextra]*len(line[:,0]),line[:, 2], **pltkwargs)

lvlines = [array([[0,0,0], v]) for v in lv]
for line in lvlines:
    pltkwargs = {'color': 'blue', 'linewidth': 1}
    arrow = Arrow3D(line[:, 0], line[:, 1], line[:, 2], arrowstyle = "-|>", mutation_scale = 5, **pltkwargs)
    ax.add_artist(arrow)

ax.set_xlim(minlim+xlimextra, maxlim)
ax.set_ylim(minlim,maxlim+ylimextra)
ax.set_zlim(minlim+zlimextra, maxlim)
ax.set_axis_off()
ax.view_init(15, 320)
plt.tight_layout()
plt.savefig('ex_pyrochlore.pdf', dpi = 300)


