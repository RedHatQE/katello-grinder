package com.redhat.qe.perf.katello

import com.google.inject.Guice
import com.google.inject.Injector
import com.google.inject.Key
import com.redhat.qe.katello.base.obj.KatelloSystem
import com.redhat.qe.katello.common.KatelloUtils
import com.redhat.qe.katello.guice.CertSSLContext
import com.redhat.qe.katello.guice.KatelloApiModule
import com.redhat.qe.katello.guice.PlainSSLContext
import com.redhat.qe.katello.ssl.KatelloPemThreadLocal
import com.redhat.qe.katello.tasks.KatelloTasks

class InitialSystems {
    Injector injector

    InitialSystems() {
        injector = Guice.createInjector(new KatelloApiModule())
        
    }
        
    def createInitialSystems() {
        KatelloTasks tasks = injector.getInstance(Key.get(KatelloTasks.class, PlainSSLContext.class))
        Integer systemCount = System.properties['katello.test.initialSystems'] as Integer
        def testOrganization = System.properties['katello.test.organization'] as String ?: "ACME_Corporation"
        systemCount.times {
            def pid = KatelloUtils.getUniqueID()
            def consumer_name = "auto-"+pid+".example.com"
            def hostuuid = KatelloUtils.getUUID()
            KatelloSystem consumer = tasks.createConsumer(testOrganization, consumer_name, hostuuid)
            KatelloPemThreadLocal.set(consumer.idCert.cert + consumer.idCert.key)            
            KatelloTasks tasksWithCert = injector.getInstance(Key.get(KatelloTasks.class, CertSSLContext.class))
            def result = tasksWithCert.updatePackages(consumer)
            def entitlements = tasksWithCert.subscribeConsumerWithProduct(consumer.uuid, [ "69" ] as String[])
        }
    }
    
    static main(args) {
        def initial = new InitialSystems()
        initial.createInitialSystems()
    }

}
