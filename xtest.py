from coffea import processor, hist
from coffea.nanoevents import NanoAODSchema
import awkward as ak
import matplotlib.pyplot as plt

import tracemalloc
tracemalloc.start()

snapshot1=None
class MyZPeak(processor.ProcessorABC):
    def __init__(self):
        self._accumulator = processor.list_accumulator()

    @property
    def accumulator(self):
        return self._accumulator

    # we will receive a NanoEvents instead of a coffea DataFrame
    def process(self, events):
        out = self.accumulator.identity()

        snapshot = tracemalloc.take_snapshot()
        out.append((tracemalloc.get_traced_memory()[0],snapshot))

        return out

    def postprocess(self, accumulator):
        return accumulator

samples = {
    "random": ['example.root']*1000
}

result = processor.run_uproot_job(
    samples,
    "Events",
    MyZPeak(),
    processor.iterative_executor,
)

memory=[]
for i in range(1,len(result)):
    top_stats = result[i][1].compare_to(result[i-1][1], 'lineno')
    memory.append(result[i][0])
    print("--- [ Top 5 ] --- (total: {})".format(result[i][0]))
    for stat in top_stats[:5]:
        print(stat)

plt.plot(memory)
plt.ylabel('memory usage [bytes]')
plt.tight_layout()
plt.savefig('xtest.png')
