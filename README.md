Tries to reproduce a memory leak in the coffea framework that I noticed in running over a large dataset. The input is a simple TTree (all branches are basic types). The memory consumption of the python process is steadily increasing with each iteration of `processor.ProcessorABC.process` until it is fully filled up. While trying to reproduce this in a simple example, I've noticed that the problem can be reproduced when using a branch not supported by uproot (ie: unsigned long).

I've prepared a demonstrative MRE in my GitHub. It creates a simple TTree (100M events, 10 or 10k baskets, 3 branches of floats) and then processes it in different ways.

- `ptest.py` creates a `processor.ProcessorABC` and uses `run_uproot_job`+`iterative_executor`
- `ftest.py` calls `NanoEventsFactory.from_root` multiple times
- `utest.py` uses `uproot.iterate`

The observations are:
- `utest.py` is fine. So this is not an uproot problem.
- `ftest.py` is fine. So everything is cleaned up once a file is closed.
- `ptest.py` has memory usage slowly increasing at every call to `process`.

The tracemalloc shows the following top 5 memory users. The compression is slowly growing in each call to `processor.ProcessorABC.process` in `ptest.py`.
```
--- [ Top 5 ] --- (total: 27127337)
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.10/site-packages/uproot/compression.py:93: size=17.5 MiB, count=141, average=127 KiB
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.10/site-packages/uproot/model.py:754: size=561 KiB, count=7632, average=75 B
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.10/site-packages/uproot/source/cursor.py:48: size=446 KiB, count=8774, average=52 B
/usr/lib/python3.10/threading.py:258: size=410 KiB, count=1250, average=336 B
/home/kkrizka/MRE/mre-coffea-memory/.venv/lib/python3.10/site-packages/rich/text.py:676: size=389 KiB, count=2373, average=168 B```

The can be run as follows:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python create_input.py example.root 100000000 10000
python ptest.py example.root # or any of the other scripts
```
