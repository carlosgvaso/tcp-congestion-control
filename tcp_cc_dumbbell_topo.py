##
# Mininet code to compare 4 different TCP congestion control algorithms.
#

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


class DumbbellTopo(Topo):
    "Dumbbell topology for Shrew experiment"
    def build(self):
        #TODO:Add your code to create the topology.
        #Add 2 switches
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        #Left Side
        n0 = self.addHost('n0')
        n1 = self.addHost('n1')
        self.addLink(n0, s2, bw=16, delay='2ms')
        self.addLink(n1, s2, bw=24, delay='2ms')

        #Right Side
        n4 = self.addHost('n4')
        n5 = self.addHost('n5')
        self.addLink(n4, s3, bw=16, delay='2ms')
        self.addLink(n5, s3, bw=16, delay='2ms')

        self.addLink(s2, s3, bw=9.6, delay='10ms')


class DumbbellTopo2(Topo):
    """ Dumbbell topology class.

        The topology is described in section 5.4 of:
        https://www.nist.gov/sites/default/files/documents/itl/antd/P9-SP-500-282-Chapter5.pdf

          s1------s2    s1 & s2 are backbone routers 1 & 2
           |       |
          s3      s4    s3 and s4 are access routers 1 & 2
          /\      /\
        h1  h3  h2  h4  h1 & h3 are source hosts 1 & 2, and h2 & h4 are receiver hosts 1 & 2

        The hosts (h1..h4) can transmit/receive at 960Gbps.
        The backbone routers (s1 & s2) can transmit/receive at 984Gbps.
        There is a 21, 81, and 162ms one-way propagation delay in the link between s1 and s2 (RTTs 42, 162, 324ms).
        The access routers (s3 & s4) can transmit/receive at 250Mbps.
        The access routers have buffers = 20% * bandwidth * delay.
        Might need to use intf=TCIntf option in the link constructor instead of default Intf class for traffic control.
    """

    def build(self):
        """ Create the topology by overriding the class parent's method.
        """
        br_params = dict(bw='984m', delay='21ms')       # backbone router interface traffic control parameters
        ar_params = dict(bw='250m', max_queue_size='')  # access router interface traffic control parameters
        h_params = dict(bw='960m')                      # host interface traffic control parameters

        # Create backbone routers 1 & 2, and link them together
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        self.addLink(s1, s2, **br_params)

        # Create access routers 1 & 2, and link them to the backbone routers
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        self.addLink(s1, s3, params1=br_params, params2=ar_params)
        self.addLink(s2, s4, params1=br_params, params2=ar_params)

        # Create the source hosts (h1 & h3), and link them to access router 1
        h1 = self.addHost('h1')
        h3 = self.addHost('h3')
        self.addLink(s3, h1, params1=ar_params, params2=h_params)
        self.addLink(s3, h3, params1=ar_params, params2=h_params)

        # Create the receiver hosts (h2 & h4), and link them to access router 2
        h2 = self.addHost('h2')
        h4 = self.addHost('h4')
        self.addLink(s4, h2, params1=ar_params, params2=h_params)
        self.addLink(s4, h4, params1=ar_params, params2=h_params)


def dumbbell_test():
    """ Create and test a dumbbell network.
    """
    topo = DumbbellTopo()
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()


class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)


def simple_test():
    "Create and test a simple network"
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    net.stop()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    #simple_test()
    dumbbell_test()
