#!/usr/bin/python

# loadsync.py - Creates a provider, product and subsequent repos within
# katello, pulling from a list of repo URLs stored in a flat file. The
# main purpose of this is to exercise the sync capabilities of katello.
# Using this script, one could queue up any number of repos and/or run
# the script multiple times to implement a whole bunch of sync requests
# within katello.

import sys,random
from subprocess import Popen
if len(sys.argv) == 1:
  print "This program requires a file containing repo URLs."
  print "Ex: loadsync.py </path/to/repo_url_file>"
  sys.exit()

try:
   open(sys.argv[1])
except IOError as e:
   print 'Repo URL file "', sys.argv[1], '" not found.  Check the location and try again.'
   sys.exit(1)

def populate_ppr(ppr_name):
  if not ppr_name:
     ppr_name = ''.join(random.choice('ABCDEF0123456789') for x in xrange(16))
  username = "admin"
  password = "admin"
  authstuff = "katello --username " + username + " --password " + password 
  provider_name = ppr_name + "_provider"
  product_name = ppr_name + "_product"
  create_provider = authstuff + " provider create --name " + provider_name  
  create_product = authstuff + " product create --name " + product_name + " --provider " + provider_name
  repo_count = 0
  p = Popen(create_provider, shell=True)
  p.wait()
  p =  Popen(create_product, shell=True)
  p.wait()
  input_file = open(sys.argv[1])
  for repourl in input_file:
  # Skip any commented-out URLs
    result = repourl.startswith ('#')
    if result == True:
      pass
    else:
      repo_name =  ppr_name + "_repo_" + str(repo_count) 
      create_repo = authstuff + " repo create --name " + repo_name + " --product " + product_name + " --url " + repourl
      p = Popen(create_repo, shell=True)
      p.wait()
      # Note lack of ".wait() below - we want to slam as many in as possible
      sync_repo = authstuff + " repo synchronize --name " + repo_name + " --product " + product_name
      p = Popen(sync_repo, shell=True)
      repo_count += 1
  # Can probably just comment this out.
  sync_provider = authstuff + " provider synchronize --name " + provider_name
  p = Popen(sync_provider, shell=True)
  p.wait()

# Call the function.  Alternately, you can provide a name if there is a defined
# name you want to use for the provider/product/repo.
# ex: 
# populate_ppr(ppr_name='RPMFusion') 

populate_ppr(ppr_name=None)
 
