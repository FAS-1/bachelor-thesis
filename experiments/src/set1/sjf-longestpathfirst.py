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

        self.addLink(hosts[0], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[1], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[2], hosts[4], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[0], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[3], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[3], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[4], hosts[6], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[4], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[5], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[5], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[6], hosts[0], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[7], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        # LongestPathFirst
        self.addLink(hosts[4], hosts[9], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[8], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[7], hosts[0], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[5], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        return hosts


def perfTest(net):

    hosts = net.routers
    for router in net.routers:
        router.cmd('sysctl -w net.ipv4.ip_forward=1')
        router.cmd('sysctl -w net.ipv4.tcp_congestion_control=reno')

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
    h7.cmd('iperf3 -s -p 5000 &')
    h3.cmd('iperf3 -s -p 5000 &')
    h1.cmd('iperf3 -s -p 5001 &')
    h9.cmd('iperf3 -s -p 5002 &')
    h1.cmd('iperf3 -s -p 5002 &')
    h1.cmd('iperf3 -s -p 5003 &')
    h9.cmd('iperf3 -s -p 5004 &')
    h8.cmd('iperf3 -s -p 5004 &')
    h2.cmd('iperf3 -s -p 5005 &')
    h8.cmd('iperf3 -s -p 5005 &')
    h9.cmd('iperf3 -s -p 5006 &')
    h0.cmd('iperf3 -s -p 5006 &')
    h7.cmd('iperf3 -s -p 5007 &')
    h6.cmd('iperf3 -s -p 5007 &')
    h3.cmd('iperf3 -s -p 5007 &')
    h5.cmd('iperf3 -s -p 5008 &')
    h9.cmd('iperf3 -s -p 5008 &')
    h4.cmd('iperf3 -s -p 5008 &')
    h6.cmd('iperf3 -s -p 5008 &')

    h9.cmd('iperf3 -c h3 -p 5000 -n 989M -J --logfile experiments/results/h9-h3.json &&'
           'iperf3 -c h7 -p 5000 -n 1531M -J --logfile experiments/results/h9-h7.json &&'
           'iperf3 -c h0 -p 5000 -n 2021M -J --logfile experiments/results/h9-h0.json &')

    h7.cmd('iperf3 -c h1 -p 5001 -n 1358M -J --logfile experiments/results/h7-h1.json &')

    h6.cmd('iperf3 -c h9 -p 5002 -n 571M -J --logfile experiments/results/h6-h9.json &&'
           'iperf3 -c h1 -p 5002 -n 988M -J --logfile experiments/results/h6-h1.json &')

    h4.cmd('iperf3 -c h1 -p 5003 -n 2027M -J --logfile experiments/results/h4-h1.json &')

    h0.cmd('iperf3 -c h9 -p 5004 -n 156M -J --logfile experiments/results/h0-h9.json &&'
           'iperf3 -c h8 -p 5004 -n 364M -J --logfile experiments/results/h0-h8.json &')

    h3.cmd('iperf3 -c h2 -p 5005 -n 460M -J --logfile experiments/results/h3-h2.json &&'
           'iperf3 -c h8 -p 5005 -n 1194M -J --logfile experiments/results/h3-h8.json &')

    h1.cmd('iperf3 -c h9 -p 5006 -n 1834M -J --logfile experiments/results/h1-h9.json &&'
           'iperf3 -c h0 -p 5006 -n 2005M -J --logfile experiments/results/h1-h0.json &')

    h5.cmd('iperf3 -c h7 -p 5007 -n 296M -J --logfile experiments/results/h5-h7.json &&'
           'iperf3 -c h6 -p 5007 -n 653M -J --logfile experiments/results/h5-h6.json &&'
           'iperf3 -c h3 -p 5007 -n 756M -J --logfile experiments/results/h5-h3.json &')

    h2.cmd('iperf3 -c h5 -p 5008 -n 431M -J --logfile experiments/results/h2-h5.json &&'
           'iperf3 -c h9 -p 5008 -n 469M -J --logfile experiments/results/h2-h9.json &&'
           'iperf3 -c h4 -p 5008 -n 1434M -J --logfile experiments/results/h2-h4.json &&'
           'iperf3 -c h6 -p 5008 -n 1779M -J --logfile experiments/results/h2-h6.json &')

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
# IPCLI(net)
net.stop()
