##
# Mininet code to compare 4 different TCP congestion control algorithms.
#

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class DumbbellTopo(Topo):
    """ Dumbbell topology class.

        This class requires the use of TCLink class instead of the default Link class to create the links.

        The topology is described in section 5.4 of:
        https://www.nist.gov/sites/default/files/documents/itl/antd/P9-SP-500-282-Chapter5.pdf

          s1------s2    s1 & s2 are backbone routers 1 & 2
           |       |
          s3      s4    s3 and s4 are access routers 1 & 2
          /\      /\
        h1  h3  h2  h4  h1 & h3 are source hosts 1 & 2, and h2 & h4 are receiver hosts 1 & 2

        The hosts (h1..h4) can transmit/receive at 960Mbps. The links between the the hosts and the access routers will
        have a bandwidth of 960Mbps and a delay of 0ms.
        The backbone routers (s1 & s2) can transmit/receive at 984Mbps. The link between the backbone routers will have
        a bandwidth of 984Mbps.
        There is a 21, 81, and 162ms one-way propagation delay in the link between s1 and s2 which makes RTTs of 42, 162
        and 324ms.
        The access routers (s3 & s4) can transmit/receive at 250Mbps. The links between the access routers and the
        backbone routers will have a bandwidth of 250Mbps and a delay of 0ms.
        The access routers have buffers = 20% * bandwidth * delay. The links between the access routers and the
        backbone routers will have a max queue size = 20% * bandwidth * delay.
    """

    def build(self, delay='2ms'):
        """ Create the topology by overriding the class parent's method.
        """
        # The bandwidth (bw) is in Mbps, delay in milliseconds and queue size is in packets
        br_params = dict(bw=984, delay=delay, use_htb=True)                       # backbone router interface tc params
        ar_params = dict(bw=250, delay='0ms', max_queue_size=1000, use_htb=True)  # access router interface tc params
        hi_params = dict(bw=960, delay='0ms', use_htb=True)                       # host interface tc params
        #hc_params = dict(cpu=.25)                                                 # host cpu limiting params

        # Create routers s1 to s4
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Link backbone routers (s1 & s2) together
        self.addLink(s1, s2, cls=TCLink, **br_params)

        # Link access routers (s3 & s4) to the backbone routers
        self.addLink(s1, s3, cls=TCLink, **ar_params)
        self.addLink(s2, s4, cls=TCLink, **ar_params)

        # Create the hosts h1 to h4, and link them to access router 1
        h1 = self.addHost('h1')#, **hc_params)
        h2 = self.addHost('h2')#, **hc_params)
        h3 = self.addHost('h3')#, **hc_params)
        h4 = self.addHost('h4')#, **hc_params)

        # Link the source hosts (h1 & h3) to access router 1 (s3)
        self.addLink(s3, h1, cls=TCLink, **hi_params)
        self.addLink(s3, h3, cls=TCLink, **hi_params)

        # Link the receiver hosts (h2 & h4) to access router 2 (s4)
        self.addLink(s4, h2, cls=TCLink, **hi_params)
        self.addLink(s4, h4, cls=TCLink, **hi_params)


def dumbbell_test():
    """ Create and test a dumbbell network.
    """
    topo = DumbbellTopo(delay='21ms')
    net = Mininet(topo)#, host=CPULimitedHost)
    net.start()

    print "Dumping host connections..."
    dumpNodeConnections(net.hosts)

    print "Testing network connectivity..."
    h1, h2 = net.get('h1', 'h2')
    h3, h4 = net.get('h3', 'h4')

    for i in xrange(1, 10):
        net.pingFull(hosts=(h1, h2))

    for i in xrange(1, 10):
        net.pingFull(hosts=(h2, h1))

    for i in xrange(1, 10):
        net.pingFull(hosts=(h4, h3))

    for i in xrange(1, 10):
        net.pingFull(hosts=(h3, h4))

    print "Testing bandwidth between h1 and h2..."
    net.iperf((h1, h2), seconds=10)

    print "Testing bandwidth between h3 and h4..."
    net.iperf((h3, h4), seconds=10)

    print "Stopping test..."
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    #linear_test()
    dumbbell_test()
