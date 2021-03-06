#
# Copyright (C) 2019  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Vendula Poncova <vponcova@redhat.com>
#
import unittest
from unittest.mock import patch, call

from blivet.devices import DASDDevice
from blivet.formats import get_format
from blivet.size import Size

from pyanaconda.modules.common.errors.configuration import StorageDiscoveryError
from pyanaconda.modules.common.errors.storage import UnavailableStorageError, UnknownDeviceError
from pyanaconda.modules.storage.dasd import DASDModule
from pyanaconda.modules.storage.dasd.dasd_interface import DASDInterface
from pyanaconda.modules.storage.dasd.discover import DASDDiscoverTask
from pyanaconda.modules.storage.dasd.format import DASDFormatTask
from pyanaconda.storage.initialization import create_storage
from tests.nosetests.pyanaconda_tests import patch_dbus_publish_object, check_task_creation


class DASDInterfaceTestCase(unittest.TestCase):
    """Test DBus interface of the DASD module."""

    def setUp(self):
        """Set up the module."""
        self.dasd_module = DASDModule()
        self.dasd_interface = DASDInterface(self.dasd_module)

    @patch_dbus_publish_object
    def discover_with_task_test(self, publisher):
        """Test DiscoverWithTask."""
        task_path = self.dasd_interface.DiscoverWithTask("0.0.A100")

        obj = check_task_creation(self, task_path, publisher, DASDDiscoverTask)

        self.assertEqual(obj.implementation._device_number, "0.0.A100")

    @patch_dbus_publish_object
    def format_with_task_test(self, publisher):
        """Test the discover task."""
        task_path = self.dasd_interface.FormatWithTask(["/dev/sda", "/dev/sdb"])

        obj = check_task_creation(self, task_path, publisher, DASDFormatTask)

        self.assertEqual(obj.implementation._dasds, ["/dev/sda", "/dev/sdb"])

    @patch('pyanaconda.modules.storage.dasd.format.blockdev')
    def find_formattable_test(self, blockdev):
        """Test FindFormattable."""
        with self.assertRaises(UnavailableStorageError):
            self.dasd_interface.FindFormattable(["dev1"])

        storage = create_storage()
        self.dasd_module.on_storage_changed(storage)

        with self.assertRaises(UnknownDeviceError):
            self.dasd_interface.FindFormattable(["dev1"])

        storage.devicetree._add_device(
            DASDDevice(
                "dev1",
                fmt=get_format("ext4"),
                size=Size("10 GiB"),
                busid="0.0.0201",
                opts={}
            )
        )

        # The policy doesn't allow tp format anything.
        self.assertEqual(self.dasd_interface.FindFormattable(["dev1"]), [])

        # The policy allows to format unformatted, but there are none.
        self.dasd_module.on_format_unrecognized_enabled_changed(True)
        blockdev.s390.dasd_needs_format.return_value = False
        self.assertEqual(self.dasd_interface.FindFormattable(["dev1"]), [])

        # The policy allows to format LDL, but there are none.
        self.dasd_module.on_format_unrecognized_enabled_changed(False)
        self.dasd_module.on_format_ldl_enabled_changed(True)
        blockdev.s390.dasd_is_ldl.return_value = False
        self.assertEqual(self.dasd_interface.FindFormattable(["dev1"]), [])

        # The policy allows to format all and there are all.
        self.dasd_module.on_format_unrecognized_enabled_changed(True)
        blockdev.s390.dasd_needs_format.return_value = True
        blockdev.s390.dasd_is_ldl.return_value = True
        self.assertEqual(self.dasd_interface.FindFormattable(["dev1"]), ["dev1"])


class DASDTasksTestCase(unittest.TestCase):
    """Test DASD tasks."""

    def discovery_fails_test(self):
        """Test the failing discovery task."""
        with self.assertRaises(StorageDiscoveryError):
            DASDDiscoverTask("x.y.z").run()

    @patch('pyanaconda.modules.storage.dasd.discover.blockdev')
    def discovery_test(self, blockdev):
        """Test the discovery task."""
        DASDDiscoverTask("0.0.A100").run()
        blockdev.s390.sanitize_dev_input.assert_called_once_with("0.0.A100")

        sanitized_input = blockdev.s390.sanitize_dev_input.return_value
        blockdev.s390.dasd_online.assert_called_once_with(sanitized_input)

    @patch('pyanaconda.modules.storage.dasd.format.blockdev')
    def format_test(self, blockdev):
        """Test the format task."""
        DASDFormatTask(["/dev/sda", "/dev/sdb"]).run()
        blockdev.s390.dasd_format.assert_has_calls([
            call("/dev/sda"),
            call("/dev/sdb")
        ])
