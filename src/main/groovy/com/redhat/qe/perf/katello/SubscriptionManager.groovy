package com.redhat.qe.perf.katello

import groovyx.net.http.RESTClient
import static groovyx.net.http.ContentType.URLENC
import org.apache.http.conn.scheme.Scheme
import org.apache.http.conn.ssl.SSLSocketFactory
import javax.net.ssl.*
import java.security.cert.*

class SubscriptionManager {
    def restClient
    def uris = [:]
 
    SubscriptionManager(String protocol, String hostname, String port, String contextPath, String username, String password ) {
        // Get the API uris
        def url = "${protocol}://${hostname}:${port}/${contextPath}/"
        restClient = new RESTClient(url)

        // Ignore peer certificates
        SSLContext ctx = SSLContext.getInstance("TLS")
        X509TrustManager trustManager = new NoopTrustManager()
        ctx.init(null, [ trustManager ] as TrustManager[], null)
        SSLSocketFactory ssf = new SSLSocketFactory(ctx)
        ssf.setHostnameVerifier(SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER)
        restClient.client.connectionManager.schemeRegistry.register(new Scheme("https", ssf, 443))

        restClient.auth.basic username, password
        def apis = restClient.get(path: "api")
        apis.data.each { api ->
            uris."${api.rel}" = api.href
        }
    }

    def registerTo(def organization) {
        def uuid = java.util.UUID.randomUUID()
        def hostname = "${uuid}.example.com"
        def clientFacts = """{"facts": {"dmi.system.uuid":"${uuid}", "lcspu.l1d_cache": "32K"}, "type":"system", "name":"${hostname}"}"""
        def resp = restClient.post( path: uris.consumers,
                                    body: [ clientFacts ],
                                    requestContentType: URLENC )
        def assignedUuid = resp.data.uuid
        def cert = resp.data.idCert.cert
        def key = resp.data.idCert.key
        resp
    }
}

class NoopTrustManager implements X509TrustManager {
    // NO-OPs
    public void checkClientTrusted(X509Certificate[] xcs, String string) throws CertificateException {}
    public void checkServerTrusted(X509Certificate[] xcs, String string) throws CertificateException {}
    public X509Certificate[] getAcceptedIssuers() { return null }
}
