import uproot
import numpy as np

file = uproot.recreate("example.root")

letters=['a','b','c','x','y','z']
file['Events'] = {l:np.random.rand(10000000) for l in letters}
