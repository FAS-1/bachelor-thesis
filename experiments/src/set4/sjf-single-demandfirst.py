import time
from mininet.log import lg
import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


class SimpleTopo(IPTopo):
    def build(self):

        hosts = []

        for i in range(10):
            host = self.addRouter(f'h{i}')
            hosts.append(host)

        self.addLink(hosts[0], hosts[4], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[0], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[0], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[1], hosts[6], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[2], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[3], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[4], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[4], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[7], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[7], hosts[1], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[8], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[9], hosts[5], igp_metric=1000, bw=200, delay="5ms")

        # DemandFirst
        self.addLink(hosts[6], hosts[8], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[9], hosts[1], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[4], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[5], hosts[2], igp_metric=1000, bw=200, delay="5ms")

        return hosts


def perfTest(net):

    hosts = net.routers
    print("*** Waiting for network to start")
    for i in range(20, 0, -1):
        print(f"{i}  ", end="\r", flush=True)
        time.sleep(1)

    print("*** Testing bandwidth between hosts")
    h0 = net.routers[0]
    h1 = net.routers[1]
    h2 = net.routers[2]
    h3 = net.routers[3]
    h4 = net.routers[4]
    h5 = net.routers[5]
    h6 = net.routers[6]
    h7 = net.routers[7]
    h8 = net.routers[8]
    h9 = net.routers[9]

    h1.cmd('iperf3 -s -p 5000 &')
    h6.cmd('iperf3 -s -p 5001 &')
    h8.cmd('iperf3 -s -p 5002 &')
    h3.cmd('iperf3 -s -p 5003 &')
    h7.cmd('iperf3 -s -p 5003 &')
    h4.cmd('iperf3 -s -p 5004 &')
    h9.cmd('iperf3 -s -p 5004 &')
    h5.cmd('iperf3 -s -p 5004 &')
    h6.cmd('iperf3 -s -p 5004 &')
    h7.cmd('iperf3 -s -p 5005 &')
    h4.cmd('iperf3 -s -p 5006 &')
    h0.cmd('iperf3 -s -p 5007 &')
    h6.cmd('iperf3 -s -p 5007 &')
    h4.cmd('iperf3 -s -p 5008 &')
    h0.cmd('iperf3 -s -p 5008 &')
    h2.cmd('iperf3 -s -p 5008 &')
    h9.cmd('iperf3 -s -p 5008 &')
    h9.cmd('iperf3 -s -p 5009 &')
    h5.cmd('iperf3 -s -p 5009 &')
    h8.cmd('iperf3 -s -p 5009 &')


    transfers = [
        (h9, 'h1', 5000, 1325),
        (h7, 'h6', 5001, 911),
        (h6, 'h8', 5002, 1642),
        (h4, 'h3', 5003, 278),
        (h4, 'h7', 5003, 889),
        (h0, 'h4', 5004, 1118),
        (h0, 'h9', 5004, 1355),
        (h0, 'h5', 5004, 1572),
        (h0, 'h6', 5004, 1631),
        (h3, 'h7', 5005, 1449),
        (h8, 'h4', 5006, 153),
        (h1, 'h6', 5007, 641),
        (h1, 'h0', 5007, 1152),
        (h5, 'h4', 5008, 288),
        (h5, 'h0', 5008, 1615),
        (h5, 'h2', 5008, 1769),
        (h5, 'h9', 5008, 2047),
        (h2, 'h9', 5009, 472),
        (h2, 'h5', 5009, 477),
        (h2, 'h8', 5009, 1664),
    ]


    transfers.sort(key=lambda x: x[3])

    for transfer in transfers:
        src, dest, port, size = transfer
        src.cmd(f'iperf3 -c {dest} -p {port} -n {size}M -J --logfile experiments/results/{src.name}-{dest}.json')

    for i in range(500, 0, -1):
        print(f"{i}  ", end="\r", flush=True)
        time.sleep(1)

    print("*** All traffic flows initiated and completed")

    print("*** Cleanup completed, stopping network.")
    for host in hosts:
        host.cmd('killall -q iperf3')


ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

net = IPNet(topo=SimpleTopo(), use_v6=False)
net.start()
perfTest(net)
net.stop()