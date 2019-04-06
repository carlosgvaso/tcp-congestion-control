tcp-congestion-control
======================

Mininet code to compare 4 different TCP congestion control algorithms.


> Copyright :copyright: 2019 of Jose Carlos Martinez Garcia-Vaso. All rights reserved.


TCP Congestion Algorithms
-------------------------

> WIP

* Reno
* CUBIC
* TBD
* TBD


Usage
-----

Use the `requirements.txt` file to install the required packages. The script must be run with root privileges (e.i.
using `sudo`). Please, run `sudo mn -c` before running the script to ensure there is nothing else running in mininet.

To run all the tests back to back run:

```bash
sudo python tcp_cc_dumbbell_topo.py
```

To select the settings and tests to run, here is the script usage:

```bash
usage: tcp_cc_dumbbell_topo.py [-h] [-a ALGORITHMS [ALGORITHMS ...]]
                               [-d DELAYS [DELAYS ...]] [-i IPERF_RUNTIME]
                               [-j IPERF_DELAYED_START] [-l LOG_LEVEL] [-t]

TCP Congestion Control tests in a dumbbell topology.

optional arguments:
  -h, --help            show this help message and exit
  -a ALGORITHMS [ALGORITHMS ...], --algorithms ALGORITHMS [ALGORITHMS ...]
                        List TCP Congestion Control algorithms to test.
  -d DELAYS [DELAYS ...], --delays DELAYS [DELAYS ...]
                        List of backbone router one-way propagation delays to
                        test.
  -i IPERF_RUNTIME, --iperf-runtime IPERF_RUNTIME
                        Time to run the iperf clients.
  -j IPERF_DELAYED_START, --iperf-delayed-start IPERF_DELAYED_START
                        Time to wait before starting the second iperf client.
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Verbosity level of the logger. Uses `info` by default.
  -t, --run-test        Run the dumbbell topology test.
```

For example, the following command runs the script for algorithms Reno and CUBIC, with one-way propagation delays of 21,
81 and 162, the iperf commands will run for 1000sec and the second iperf will start 250sec after the first command:

```bash
sudo python tcp_cc_dumbbell_topo.py --algorithms reno cubic --delays 21 81 162 --iperf-runtime 1000 --iperf-delayed-start 250
```
