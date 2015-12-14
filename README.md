# membw-automation-scripts

This link provides a set of scripts that can be run to automate
the installation of pcp and openstack components needed to use
Host Memory Bandwidth Information for cloud placement decisions.

Following gives a brief description of each of the files:

1. **utils.py**: This file contains a set of utilities needed by the scripts below.

2. **libpfm_pcp.py**: This file is responsible for installing the libpfm
and pcp components. This script assumes that the kernel components needed
to expose Memory Bandwidth are already available on the system on which this
would be run.

3. **openstack_install_compute.py**: This file is responsible for installing the openstack
components needed to report the host memory bandwidth on the Compute node.

4. **openstack_install_controller.py**: This file should be executed on the OpenStack scheduler
node.

Note: In addition to running this script, ./nova-12.0.0-py2.7.egg-info/entry_points.txt
should be updated with the following entry:

```
[nova.compute.monitors.membw]
virt_driver = nova.compute.monitors.membw.virt_driver:Monitor
```

The minimum libvirt version required on the PowerPC compute node is **1.2.19**

