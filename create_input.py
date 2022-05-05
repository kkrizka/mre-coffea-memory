import uproot
import numpy as np

file = uproot.recreate("example.root")

file['Events'] = {'x':np.random.rand(100000),'y':np.random.rand(100000),'z':np.random.rand(100000)}
