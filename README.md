# membw-automation-scripts

This link provides a set of scripts that can be run to automate
the installation of pcp and openstack components needed to use
Host Memory Bandwidth Information for cloud placement decisions.

Following gives a brief description of each of the files:

1. utils.py: This file contains a set of utilities needed by the scripts below.

2. libpfm_pcp.py: This file is responsible for installing the libpfm
and pcp components. This script assumes that the kernel components needed
to expose Memory Bandwidth are already available on the system on which this
would be run.

3. openstack_install.py: This file is responsible for installing the openstack
components needed to report the host memory bandwidth and eventually take a scheduling
decision based on the metric. The changes are needed at two places:

- compute node 
- nova scheduler node.

The same script should be run on either places to kick start an automated way of getting the changes.

