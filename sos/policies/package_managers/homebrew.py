# Copyright 2020 Red Hat, Inc. Jake Hunsaker <jhunsake@redhat.com>

# This file is part of the sos project: https://github.com/sosreport/sos
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# version 2 of the GNU General Public License.
#
# See the LICENSE file in the source distribution for further information.

import os

from sos.policies.package_managers import PackageManager

class HomebrewPackageManager(PackageManager):
    """Subclass for Homebrew-based distrubitons
    """

    query_command = "/opt/homebrew/bin/brew list --versions"
    # How to look for a file in package
    #query_path_command = ""
    verify_command = "/opt/homebrew/bin/brew doctor"
    verify_filter = ""

    def _parse_pkg_list(self, pkg_list):
        for pkg in pkg_list.splitlines():
            if ' ' not in pkg:
                continue
            name, version = pkg.split(' ')
            yield (name, version, None)

# vim: set et ts=4 sw=4 :
