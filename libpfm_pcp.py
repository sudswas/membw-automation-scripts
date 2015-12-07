# Script to automate the installation of various components needed to report
# memory bandwidth
# Author: Sudipto Biswas (sbiswas7@in.ibm.com)

import utils


def install_libpfm():
    git_path = "git://git.code.sf.net/u/hkshaw1990/perfmon2 perfmon2-libpfm4"

    utils.helper.git_clone(git_path, "perfmon2-libpfm4")

    commands = ['make', 'make install PREFIX=']
    with utils.cd("~/perfmon2-libpfm4"):
        utils.helper.execute_command(commands)

    with utils.cd("~/perfmon2-libpfm4/examples"):
        out, err = utils.helper.execute_command('./check_events')
        if out:
            if "POWERPC_NEST_MEM_BW" in out:
                print "Libpfm is ready for Memory BW measurement"
        else:
            print "There was an error during make of libpfm", err


def install_pcp():

    with utils.su("root"):
        utils.helper.execute_command("groupadd -r pcp")
        commands = ['useradd -c "Performance Co-Pilot"',
                    ' -g pcp -d /var/lib/pcp',
                    ' -M -r -s /usr/sbin/nologin pcp']
        utils.helper.execute_command(commands)

    configure = ['./configure --prefix=/usr --libexecdir=/usr/lib',
                ' --sysconfdir=/etc --localstatedir=/var',
                ' --libdir=/lib64/ --with-rcdir=/etc/init.d']
    with utils.cd("~/pcp"):
        utils.helper.execute_command(configure)
        utils.helper.execute_command("make")
        utils.helper.execute_command("make install")

    with utils.cd("src/pmdas/perfevent"):
        utils.helper.execute_command("sh install")
    print "please restart pcp to let the changes take effect"

install_libpfm()
install_pcp()
