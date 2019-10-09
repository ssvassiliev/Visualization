#Installation:  pip install vtk tqdm

import pyevtk as pe
import numpy as np
import netCDF4 as nc
from tqdm import tqdm

f = nc.Dataset('dngridCSR_0001.nc', 'r', format='NETCDF4')
siglay = f.dimensions['siglay'].size
nele = f.dimensions['nele'].size
node = f.dimensions['node'].size
times = f.dimensions['time'].size

npoints = node * (siglay+1)
x, y, z = np.zeros((npoints), dtype=np.float32), np.zeros((npoints), dtype=np.float32), np.zeros((npoints), dtype=np.float32)
for layer in range(siglay+1):
    start, finish = layer*node, (layer+1)*node
    x[start:finish] = f.variables['x'][:]
    y[start:finish] = f.variables['y'][:]
    z[start:finish] = f.variables['siglev'][layer,:] * f.variables['h'][:] * 10.   # last number is the vertical zoom

print('creating unstructured mesh ...')
ncells = nele * siglay
conns = np.zeros((ncells*6), dtype=int)
count = 0
for triangle in tqdm(range(nele)):
    n1, n2, n3 = f.variables['nv'][:,triangle]   # nodes of this triangle
    for layer in range(siglay):
        conns[count:count+3] = n1+layer*node-1, n2+layer*node-1, n3+layer*node-1   # upper face
        conns[count+3:count+6] = n1+(layer+1)*node-1, n2+(layer+1)*node-1, n3+(layer+1)*node-1   # lower face
        count += 6

offs = 6 + 6*np.arange(ncells)
ctypes = np.full((ncells,), pe.vtk.VtkWedge.tid)

for time in range(50,times):
    print('writing hydro variables from step', time)
    u, v, ww = np.zeros((ncells), dtype=np.float32), np.zeros((ncells), dtype=np.float32), np.zeros((ncells), dtype=np.float32)
    u[0:ncells] = f.variables['u'][time,:,:].flatten('F')     # Eastward Water Velocity [m/s]
    v[0:ncells] = f.variables['v'][time,:,:].flatten('F')     # Northward Water Velocity [m/s]
    ww[0:ncells] = f.variables['ww'][time,:,:].flatten('F')   # Upward Water Velocity [m/s]
    cdata = {'u': u, 'v': v, 'ww': ww}
    filename = pe.hl.unstructuredGridToVTK('dn%03d'%time, x, y, z, connectivity=conns,
                                           offsets=offs, cell_types=ctypes, cellData=cdata)
