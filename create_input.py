import sys

import uproot
import numpy as np

if len(sys.argv)!=4:
    print('usage: {0} output.root nEvents nBaskets'.format(sys.argv[0]))
    sys.exit(0)

file = uproot.recreate(sys.argv[1])

nEvents=int(sys.argv[2])
nBaskets=int(sys.argv[3])
nEventsPerBasket=nEvents//nBaskets

letters=['x','y','z']
file['Events'] = {l:np.random.rand(nEventsPerBasket) for l in letters}
for i in range(1,nBaskets):
    file['Events'].extend({l:np.random.rand(nEventsPerBasket) for l in letters})
