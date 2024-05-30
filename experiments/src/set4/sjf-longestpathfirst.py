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

        # LongestPathFirst
        self.addLink(hosts[0], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[3], hosts[9], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[4], hosts[8], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[6], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[5], igp_metric=1000, bw=200, delay="5ms")

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

    h9.cmd('iperf3 -c h1 -p 5000 -n 1325M -J --logfile experiments/results/h9-h1.json &')

    h7.cmd('iperf3 -c h6 -p 5001 -n 911M -J --logfile experiments/results/h7-h6.json &')

    h6.cmd('iperf3 -c h8 -p 5002 -n 1642M -J --logfile experiments/results/h6-h8.json &')

    h4.cmd('iperf3 -c h3 -p 5003 -n 278M -J --logfile experiments/results/h4-h3.json &&'
           'iperf3 -c h7 -p 5003 -n 889M -J --logfile experiments/results/h4-h7.json &')

    h0.cmd('iperf3 -c h4 -p 5004 -n 1118M -J --logfile experiments/results/h0-h4.json &&'
           'iperf3 -c h9 -p 5004 -n 1355M -J --logfile experiments/results/h0-h9.json &&'
           'iperf3 -c h5 -p 5004 -n 1572M -J --logfile experiments/results/h0-h5.json &&'
           'iperf3 -c h6 -p 5004 -n 1631M -J --logfile experiments/results/h0-h6.json &')

    h3.cmd('iperf3 -c h7 -p 5005 -n 1449M -J --logfile experiments/results/h3-h7.json &&')

    h8.cmd('iperf3 -c h4 -p 5006 -n 153M -J --logfile experiments/results/h8-h4.json &')

    h1.cmd('iperf3 -c h6 -p 5007 -n 641M -J --logfile experiments/results/h1-h6.json &&'
           'iperf3 -c h0 -p 5007 -n 1152M -J --logfile experiments/results/h1-h0.json &')

    h5.cmd('iperf3 -c h4 -p 5008 -n 288M -J --logfile experiments/results/h5-h4.json &&'
           'iperf3 -c h0 -p 5008 -n 1615M -J --logfile experiments/results/h5-h0.json &&'
           'iperf3 -c h2 -p 5008 -n 1769M -J --logfile experiments/results/h5-h2.json &&'
           'iperf3 -c h9 -p 5008 -n 2047M -J --logfile experiments/results/h5-h9.json &')

    h2.cmd('iperf3 -c h9 -p 5009 -n 472M -J --logfile experiments/results/h2-h9.json &&'
           'iperf3 -c h5 -p 5009 -n 477M -J --logfile experiments/results/h2-h5.json &&'
           'iperf3 -c h8 -p 5009 -n 1664M -J --logfile experiments/results/h2-h8.json &')

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
