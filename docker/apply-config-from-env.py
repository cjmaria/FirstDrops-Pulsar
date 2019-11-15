#!/usr/bin/env python

##
## Edit a properties config file and replace values based on
## the ENV variables
## export my-key=new-value
## ./apply-config-from-env file.conf
##

import os, sys

if len(sys.argv) < 2:
    print 'Usage: %s' % (sys.argv[0])
    sys.exit(1)

# Always apply env config to env scripts as well
conf_files = ['conf/pulsar_env.sh', 'conf/bkenv.sh'] + sys.argv[1:]

for conf_filename in conf_files:
    lines = []  # List of config file lines
    keys = {} # Map a key to its line number in the file

    # Load conf file
    for line in open(conf_filename):
        lines.append(line)
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        k,v = line.split('=', 1)
        keys[k] = len(lines) - 1

    # Update values from Env
    for k in sorted(os.environ.keys()):
        v = os.environ[k]
        if k in keys:
            print '[%s] Applying config %s = %s' % (conf_filename, k, v)
            idx = keys[k]
            lines[idx] = '%s=%s\n' % (k, v)

    # Store back the updated config in the same file
    f = open(conf_filename, 'w')
    for line in lines:
        f.write(line)
    f.close()
