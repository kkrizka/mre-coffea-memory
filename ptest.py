from coffea import processor, hist
from coffea.nanoevents import NanoAODSchema

import sys
if len(sys.argv)==1:
    print('usage: {0} input.root [input.root]'.format(sys.argv[0]))
    sys.exit(0)

import tracemalloc
tracemalloc.start()

snapshot1=None
class MyProcessor(processor.ProcessorABC):
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
    "DrellYan": sys.argv[1:]
}

result = processor.run_uproot_job(
    samples,
    "Events",
    MyProcessor(),
    processor.iterative_executor,
)
