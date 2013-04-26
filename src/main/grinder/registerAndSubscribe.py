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
from com.redhat.qe.katello.ssl import PEMx509KeyManager
from com.redhat.qe.katello.guice import KatelloApiModule
from com.redhat.qe.katello.guice import PlainSSLContext
from com.redhat.qe.katello.guice import CertSSLContext
from com.google.inject import Guice
from com.google.inject import Key
import random
import os

props = System.getProperties()

test1 = Test(1, "Get organization")
test2 = Test(2, "Create consumer")
test3 = Test(3, "Update packages")
test4 = Test(4, "Subscribe consumer with product")
test5 = Test(5, "Delele consumer")
test6 = Test(6, "Generic tasks")
test7 = Test(7, "Generic tasks with cert")
injector = Guice.createInjector(KatelloApiModule())

keyManager = injector.getInstance(PEMx509KeyManager)
#test1.record(subscriptionManagerRequest)
#test1.record(katelloTasks)
#test1.record(katelloTasksWithCert)

class TestRunner:
    def __init__(self):
        self.phase1CompleteBarrier = grinder.barrier("Phase 1")
        self.uuids = []
        
    def __call__(self):        
        self.katelloTasks = injector.getInstance(Key.get(KatelloTasks,PlainSSLContext))
        self.katelloTasksWithCert = injector.getInstance(Key.get(KatelloTasks,CertSSLContext))
        test1.record(self.katelloTasks.getOrganization)
        test2.record(self.katelloTasks.createConsumer)
        test3.record(self.katelloTasksWithCert.updatePackages)
        test4.record(self.katelloTasksWithCert.subscribeConsumerWithProduct)
        test5.record(self.katelloTasks.deleteConsumer)
        test6.record(self.katelloTasks)
        test7.record(self.katelloTasksWithCert)
        
        # Get the party started
        self.registerSystem()

    def registerSystem(self):
        organization = self.chooseAdmin()
        consumer = self.createConsumer(organization.cpKey)
        clientUuid = consumer.uuid
        KatelloPemThreadLocal.set(consumer.idCert.cert + consumer.idCert.key)
#        keyManager.addPem(consumer.idCert.cert, consumer.idCert.key)
        self.uploadPackageList(consumer)
        self.consumeSubscription(consumer.uuid)
        KatelloPemThreadLocal.unset()

    def chooseAdmin(self):
        organization = self.katelloTasks.getOrganization("ACME_Corporation")
        grinder.logger.info( "organization selected: %s" % (organization.cpKey) )
        return organization

    def createConsumer(self, organization):
        # Register the system
        pid = KatelloUtils.getUniqueID()
        consumer_name = "auto-"+pid+".example.com"
        hostuuid = KatelloUtils.getUUID()
        grinder.logger.info( "uuid: %s" % (hostuuid))
        consumer = self.katelloTasks.createConsumer(organization, consumer_name, hostuuid)
        
        # Get the certs from the response
        clientUuid = consumer.uuid
        clientCert = consumer.idCert.cert
        clientKey = consumer.idCert.key
        self.uuids.append(clientUuid)
        return consumer

    def uploadPackageList(self, consumer):
        # Upload a package list
        result = self.katelloTasksWithCert.updatePackages(consumer)
        return result

    def consumeSubscription(self, uuid):
        entitlements = self.katelloTasksWithCert.subscribeConsumerWithProduct(uuid, [ "69" ])
        return entitlements 

    def __del__(self):
        self.phase1CompleteBarrier.await()
        for uuid in self.uuids:
            self.katelloTasks.deleteConsumer(uuid)

def writeToFile(text):
    filename = "%s-page-%d.html" % (grinder.processName, grinder.runNumber)

    file = open(filename, "w")
    print >> file, text
    file.close()

