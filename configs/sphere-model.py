from mergexp import *

net = Network('bacfuzz-isolated')
runner = net.node('runner', image == '2404', proc.cores >= 4, memory.capacity >= gb(8))
# No experiment links or public ingresses. Target web ports bind to loopback.
experiment(net)
