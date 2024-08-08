# Copyright (C) Red Hat, Inc. 2019

# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

import os

from sos.policies.distros import LinuxPolicy
from sos.report.plugins import DarwinPlugin, IndependentPlugin

from sos.policies.package_managers import MultiPackageManager
from sos.policies.package_managers.homebrew import HomebrewPackageManager

# FIXME: Using LinuxPolicy since defining a lot of additional features (s3...)
class DarwinPolicy(LinuxPolicy):

    distro = "Darwin"
    vendor = "Apple"
    vendor_urls = [('Distribution Website', 'https://apple.com')]

    # TODO: Review Plugin and IndependentPlugin which are linux oriented only
    valid_subclasses = [ DarwinPlugin, IndependentPlugin ]

    def __init__(self, sysroot=None, init=None, probe_runtime=True,
                 remote_exec=None):
        super().__init__(sysroot=sysroot, init=init,
                         probe_runtime=probe_runtime,
                         remote_exec=remote_exec)
        self.package_manager = MultiPackageManager(
            primary=HomebrewPackageManager,
            fallbacks=[HomebrewPackageManager], # FIXME: ports/...
            chroot=self.sysroot,
            remote_exec=remote_exec)

        try:
            if self.package_manager.pkg_by_name('sos')['pkg_manager'] == 'homebrew':
                if os.uname().machine in [ 'arm64' ]:
                    self.sos_bin_path='/opt/homebrew/bin'
                else:
                    self.sos_bin_path='/usr/local/homebrew/bin'
        except TypeError:
            # Use the default sos_bin_path
            pass

    def init_kernel_modules(self):
      pass

    @classmethod
    def check(cls, remote=''):

        if remote:
            return cls.distro in remote

        if os.uname().sysname == 'Darwin' :
            return True

        return False

# vim: set et ts=4 sw=4 :
