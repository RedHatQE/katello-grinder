from java.lang import System
from jarray import array
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from java.lang import Class
from java.util import UUID as uuid
from jarray import array
from net.grinder.plugin.http import HTTPRequest
import java.util as util
import java.io as javaio
from org.python.core.util import StringUtil
from HTTPClient import AuthorizationInfo, NVPair
from net.grinder.plugin.http import HTTPPluginControl
from com.redhat.qe.katello.tasks import KatelloTasks
from com.redhat.qe.katello.common import KatelloUtils
from com.redhat.qe.katello.ssl import KatelloPemThreadLocal
from com.redhat.qe.katello.guice import KatelloApiModule
from com.redhat.qe.katello.guice import PlainSSLContext
from com.redhat.qe.katello.guice import CertSSLContext
from com.google.inject import Guice
from com.google.inject import Key
import random
import os

props = System.getProperties()

test1 = Test(1, "Get organization")
test2 = Test(2, "Create consumer with activation key")
test5 = Test(5, "Delele consumer")
test6 = Test(6, "Generic tasks")
test7 = Test(7, "Generic tasks with cert")
injector = Guice.createInjector(KatelloApiModule())

testOrganization = props['katello.test.organization']
if testOrganization == None:
    testOrganization = "ACME_Corporation"

testActivationKey = props['katello.test.activationkey']
if testActivationKey == None:
    testActivationKey = 'perf-activate'
    
class TestRunner:
    def __init__(self):
        self.phase1CompleteBarrier = grinder.barrier("Phase 1")
        self.uuids = []
        
    def __call__(self):        
        self.katelloTasks = injector.getInstance(Key.get(KatelloTasks,PlainSSLContext))
        self.katelloTasksWithCert = injector.getInstance(Key.get(KatelloTasks,CertSSLContext))
        test1.record(self.katelloTasks.getOrganization)
        test2.record(self.katelloTasks.registerSystemWithActivationKey)
        test5.record(self.katelloTasks.deleteConsumer)
        test6.record(self.katelloTasks)
        test7.record(self.katelloTasksWithCert)
        
        # Get the party started
        self.registerSystem()

    def registerSystem(self):
        organization = self.chooseAdmin()
        if organization.cpKey == None:
            organization.cpKey = "ACME_Corporation"
        consumer = self.createConsumer(organization)

    def chooseAdmin(self):
        organization = self.katelloTasks.getOrganization(testOrganization)
        grinder.logger.info( "organization selected: %s" % (organization.cpKey) )
        return organization

    def createConsumer(self, organization):
        # Register the system
        pid = KatelloUtils.getUniqueID()
        consumer_name = "auto-"+pid+".example.com"
        hostuuid = KatelloUtils.getUUID()
        grinder.logger.info( "uuid: %s" % (hostuuid))
        consumer = self.katelloTasks.registerSystemWithActivationKey(testActivationKey, organization.cpKey, consumer_name, hostuuid, None)
        
        self.uuids.append(clientUuid)
        return consumer

    def __del__(self):
        self.phase1CompleteBarrier.await()
        for uuid in self.uuids:
            self.katelloTasks.deleteConsumer(uuid)

def writeToFile(text):
    filename = "%s-page-%d.html" % (grinder.processName, grinder.runNumber)

    file = open(filename, "w")
    print >> file, text
    file.close()

