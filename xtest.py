from coffea import processor, hist
from coffea.nanoevents import NanoAODSchema
import awkward as ak
import matplotlib.pyplot as plt

import tracemalloc
tracemalloc.start()

snapshot1=None
class MyZPeak(processor.ProcessorABC):
    def __init__(self):
        self._accumulator = processor.dict_accumulator()

    @property
    def accumulator(self):
        return self._accumulator

    # we will receive a NanoEvents instead of a coffea DataFrame
    def process(self, events):
        out = self.accumulator.identity()

        current = tracemalloc.get_traced_memory()[0]
        snapshot = tracemalloc.take_snapshot()
        print("--- [ Top 5 ] --- (total: {})".format(current))
        for stat in snapshot.statistics('lineno')[:5]:
            print(stat)

        return out

    def postprocess(self, accumulator):
        return accumulator

samples = {
    "random": ['example.root']*100
}

result = processor.run_uproot_job(
    samples,
    "Events",
    MyZPeak(),
    processor.iterative_executor,
)
