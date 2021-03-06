#
# Known DBus objects.
#
# Copyright (C) 2018  Red Hat, Inc.  All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from dasbus.identifier import DBusObjectIdentifier
from pyanaconda.modules.common.constants.namespaces import STORAGE_NAMESPACE, NETWORK_NAMESPACE, \
    PARTITIONING_NAMESPACE, DEVICE_TREE_NAMESPACE, \
    PAYLOADS_NAMESPACE, DNF_NAMESPACE

# Storage objects.

BOOTLOADER = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="Bootloader"
)

DASD = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="DASD"
)

DEVICE_TREE = DBusObjectIdentifier(
    namespace=DEVICE_TREE_NAMESPACE
)

DISK_INITIALIZATION = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="DiskInitialization"
)

DISK_SELECTION = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="DiskSelection"
)

AUTO_PARTITIONING = DBusObjectIdentifier(
    namespace=PARTITIONING_NAMESPACE,
    basename="Automatic"
)

MANUAL_PARTITIONING = DBusObjectIdentifier(
    namespace=PARTITIONING_NAMESPACE,
    basename="Manual"
)

CUSTOM_PARTITIONING = DBusObjectIdentifier(
    namespace=PARTITIONING_NAMESPACE,
    basename="Custom"
)

INTERACTIVE_PARTITIONING = DBusObjectIdentifier(
    namespace=PARTITIONING_NAMESPACE,
    basename="Interactive"
)

BLIVET_PARTITIONING = DBusObjectIdentifier(
    namespace=PARTITIONING_NAMESPACE,
    basename="Blivet"
)

FCOE = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="FCoE"
)

ISCSI = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="iSCSI"
)

NVDIMM = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="NVDIMM"
)

SNAPSHOT = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="Snapshot"
)

STORAGE_CHECKER = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="Checker"
)

ZFCP = DBusObjectIdentifier(
    namespace=STORAGE_NAMESPACE,
    basename="zFCP"
)

# Network objects.

FIREWALL = DBusObjectIdentifier(
    namespace=NETWORK_NAMESPACE,
    basename="Firewall"
)

# Payload objects.

PAYLOAD_DEFAULT = DBusObjectIdentifier(
    namespace=PAYLOADS_NAMESPACE,
    basename="Default"
)

PAYLOAD_PACKAGES = DBusObjectIdentifier(
    namespace=DNF_NAMESPACE,
    basename="Packages"
)

PAYLOAD_LIVE_IMAGE = DBusObjectIdentifier(
    namespace=PAYLOADS_NAMESPACE,
    basename="LiveImage"
)

PAYLOAD_LIVE_OS = DBusObjectIdentifier(
    namespace=PAYLOADS_NAMESPACE,
    basename="LiveOS"
)
