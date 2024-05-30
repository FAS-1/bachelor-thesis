import time
from mininet.log import lg
import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo

"""This modified code is based on the original implementation by Julian Huhn available at 
https://github.com/huhndev/bachelor-thesis, used under ISC License."""

class SimpleTopo(IPTopo):
    def build(self):

        hosts = []

        for i in range(10):
            host = self.addRouter(f'h{i}')
            hosts.append(host)

        self.addLink(hosts[0], hosts[6], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[0], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[0], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[1], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[2], hosts[4], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[3], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[3], hosts[1], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[4], hosts[9], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[4], hosts[1], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[6], hosts[5], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[7], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[9], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[9], hosts[7], igp_metric=1000, bw=200, delay="5ms")

        # LongestPathFirst
        self.addLink(hosts[4], hosts[0], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[8], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[9], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[7], hosts[6], igp_metric=1000, bw=200, delay="5ms")

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

    h0.cmd('iperf3 -s -p 5000 &')
    h2.cmd('iperf3 -s -p 5000 &')
    h4.cmd('iperf3 -s -p 5001 &')
    h9.cmd('iperf3 -s -p 5001 &')
    h3.cmd('iperf3 -s -p 5002 &')
    h2.cmd('iperf3 -s -p 5002 &')
    h5.cmd('iperf3 -s -p 5003 &')
    h7.cmd('iperf3 -s -p 5003 &')
    h6.cmd('iperf3 -s -p 5004 &')
    h1.cmd('iperf3 -s -p 5005 &')
    h4.cmd('iperf3 -s -p 5005 &')
    h5.cmd('iperf3 -s -p 5006 &')
    h3.cmd('iperf3 -s -p 5006 &')
    h2.cmd('iperf3 -s -p 5006 &')
    h7.cmd('iperf3 -s -p 5006 &')
    h0.cmd('iperf3 -s -p 5006 &')
    h1.cmd('iperf3 -s -p 5007 &')
    h8.cmd('iperf3 -s -p 5007 &')
    h7.cmd('iperf3 -s -p 5008 &')
    h3.cmd('iperf3 -s -p 5008 &')

    h9.cmd('iperf3 -c h0 -p 5000 -n 772M -J --logfile experiments/results/h9-h0.json &&'
           'iperf3 -c h2 -p 5000 -n 1458M -J --logfile experiments/results/h9-h2.json &')

    h7.cmd('iperf3 -c h4 -p 5001 -n 356M -J --logfile experiments/results/h7-h4.json &&'
           'iperf3 -c h9 -p 5001 -n 867M -J --logfile experiments/results/h7-h9.json &')

    h6.cmd('iperf3 -c h3 -p 5002 -n 271M -J --logfile experiments/results/h6-h3.json &&'
           'iperf3 -c h2 -p 5002 -n 1835M -J --logfile experiments/results/h6-h2.json &')

    h4.cmd('iperf3 -c h5 -p 5003 -n 184M -J --logfile experiments/results/h4-h5.json &&'
           'iperf3 -c h7 -p 5003 -n 1387M -J --logfile experiments/results/h4-h7.json &')

    h0.cmd('iperf3 -c h6 -p 5004 -n 1458M -J --logfile experiments/results/h0-h6.json &')

    h8.cmd('iperf3 -c h1 -p 5005 -n 1105M -J --logfile experiments/results/h8-h1.json &&'
           'iperf3 -c h4 -p 5005 -n 1335M -J --logfile experiments/results/h8-h4.json &')

    h1.cmd('iperf3 -c h5 -p 5006 -n 812M -J --logfile experiments/results/h1-h5.json &&'
           'iperf3 -c h3 -p 5006 -n 1057M -J --logfile experiments/results/h1-h3.json &&'
           'iperf3 -c h2 -p 5006 -n 1339M -J --logfile experiments/results/h1-h2.json &&'
           'iperf3 -c h7 -p 5006 -n 1828M -J --logfile experiments/results/h1-h7.json &&'
           'iperf3 -c h0 -p 5006 -n 1971M -J --logfile experiments/results/h1-h0.json &')

    h5.cmd('iperf3 -c h8 -p 5007 -n 922M -J --logfile experiments/results/h5-h8.json &&'
           'iperf3 -c h1 -p 5007 -n 1152M -J --logfile experiments/results/h5-h1.json &')

    h2.cmd('iperf3 -c h7 -p 5008 -n 403M -J --logfile experiments/results/h2-h7.json &&'
           'iperf3 -c h3 -p 5008 -n 1381M -J --logfile experiments/results/h2-h3.json &')

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
