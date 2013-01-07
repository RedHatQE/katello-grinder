package com.redhat.qe.perf.katello

import java.util.logging.Logger

import com.google.inject.Guice
import com.google.inject.Inject
import com.google.inject.Injector
import com.google.inject.Key
import com.google.inject.name.Names
import com.redhat.qe.katello.base.obj.KatelloSystem
import com.redhat.qe.katello.guice.KatelloApiModule
import com.redhat.qe.katello.guice.PlainSSLContext
import com.redhat.qe.katello.tasks.KatelloTasks


Injector injector = Guice.createInjector(new KatelloApiModule())
KatelloTasks tasks = injector.getInstance(Key.get(KatelloTasks.class, PlainSSLContext.class))
List<KatelloSystem> systems = tasks.listConsumers()
Integer systemsToDelete = injector.getInstance(Key.get(String.class, Names.named("katello.test.systemsToDelete")))
@Inject Logger log
    
systemsToDelete.times { 
    KatelloSystem system = systems.remove(it)
    log.info("Delete system: ${system.uuid}")
    tasks.deleteConsumer(system.uuid)    
}

//systems.each { system ->
//    println(system.uuid)
//}