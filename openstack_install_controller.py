# Script to automate the installation of various components needed to report
# memory bandwidth
# Author: Sudipto Biswas (sbiswas7@in.ibm.com)

import utils
import os
import sys

from nova import version

# Install Openstack components.

py_path = None


def check_openstack_compute():
    # Let's detect if we have nova-compute on the system
    nova_cmp = utils.helper.pack_exists("nova-compute")
    global py_path
    if nova_cmp:
        # check the openstack version
        if "12" not in version.version_string():
            print "This installation is not  based on openstack liberty"
            exit()
        # This is most likely the compute node. Let's try to detect where
        # nova is installed.
        for path in sys.path:
            if os.path.isdir(path + '/nova') and "python" in path:
                py_path = path + '/nova'
                apply_compute_changes()
                break


def apply_compute_changes():
    # checkout the files needed for the compute_nodes
    path_dict = {'compute/monitors/membw': 'virt_driver.py',
                 'compute/monitors/membw': '__init__.py',
                 'virt/libvirt': 'driver.py',
                 'virt/libvirt': 'pcp_utils.py',
                 'virt': 'driver.py',
                 'compute/monitors': '__init__.py',
                 'compute/monitors': 'base.py',
                 'compute': 'claims.py'}
    git_repo = "https://github.com/sudswas/nova.git"

    #utils.helper.git_clone(git_repo, 'nova', "stable/liberty")
    # Copy the changes now assuming all the files have been
    # copied into the present directory.
    dir_to_create = py_path + '/compute/monitors/membw'
    utils.helper.execute_command("mkdir " + dir_to_create)
    with utils.cd('nova/nova'):
        for dir, file_name in path_dict.iteritems():
            rel_path = dir + "/" + file_name
            sys_file_path = py_path + '/' + rel_path
            utils.helper.execute_command("cp -f " +
                                         rel_path + " " + sys_file_path)
    utils.helper.execute_command("openstack-config " + "--set " +
                                 "/etc/nova/nova.conf " + "DEFAULT" + " "
                                 + "compute_monitors" + " " +
                                 "membw.virt_driver")

    print "Please restart nova-compute"


def check_openstack_scheduler():
    # This changes the scheduler of openstack with the required changes.
    nova_cmp = utils.helper.pack_exists("nova-scheduler")
    global py_path
    if nova_cmp:
        # check the openstack version
        if "12" not in version.version_string():
            print "This installation is not  based on openstack liberty"
            exit()
        # This is most likely the compute node. Let's try to detect where
        # nova is installed.
        for path in sys.path:
            if os.path.isdir(path + '/nova') and "python" in path:
                py_path = path + '/nova'
                apply_scheduler_changes()
                break

def check_openstack_scheduler():
    # This changes the scheduler of openstack with the required changes.
    nova_cmp = utils.helper.pack_exists("nova-scheduler")
    global py_path
    if nova_cmp:
        # check the openstack version
        if "12" not in version.version_string():
            print "This installation is not  based on openstack liberty"
            exit()
        # This is most likely the compute node. Let's try to detect where
        # nova is installed.
        for path in sys.path:
            if os.path.isdir(path + '/nova') and "python" in path:
                py_path = path + '/nova'
                apply_scheduler_changes()
                break


def apply_scheduler_changes():
    # checkout the files needed for the compute_nodes
    path_dict = {'virt/': 'hardware.py',
                 'scheduler/filters' : 'numa_topology_filter.py'}
    git_repo = "https://github.com/openstack/nova.git"

    utils.helper.git_clone(git_repo, 'nova', "stable/liberty")
    # Copy the changes now assuming all the files have been
    # copied into the present directory.
    with utils.cd('nova/nova'):
        for dir, file_name in path_dict.iteritems():
            rel_path = dir + "/" + file_name
            sys_file_path = py_path + "/" + rel_path
            utils.helper.execute_command("cp -f " +
                                         rel_path + " " + sys_file_path)

    filters = utils.helper.execute_command("openstack-config " + "--get " +
                                    "/etc/nova/nova.conf " + "DEFAULT" + " "
                                    + "scheduler_default_filters")
    if "NUMA" not in filters:
        numa_added = filters.rstrip() + ",NUMATopologyFilter"
        set_property = "openstack-config --set /etc/nova/nova.conf DEFAULT default_scheduler_filters " + numa_added
        utils.helper.execute_command(set_property)

    print "please restart openstack-nova-scheduler"


#check_openstack_compute()
check_openstack_scheduler()
