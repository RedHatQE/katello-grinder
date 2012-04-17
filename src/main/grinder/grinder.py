from java.lang import System
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from com.redhat.qe.perf.katello import SubscriptionManager

test1 = Test(1, "Subscription Manager")

props = System.getProperties()
protocol = props['katello.protocol']
hostname = props['katello.hostname']
port = props['katello.port']
context = props['katello.context']
username = props['katello.username']
password = props['katello.password']
orgToTest = props['katello.org']
request1 = test1.record(SubscriptionManager(protocol, hostname, port, context, username, password))

class TestRunner:
    def __call__(self):
        result = request1.registerTo(orgToTest)
        writeToFile(result)

def writeToFile(text):
    filename = "%s-page-%d.html" % (grinder.processName, grinder.runNumber)

    file = open(filename, "w")
    print >> file, text
    file.close()

