# Usage:
#   iwd-scan.py [ssid]
# DESCRIPTION:
#   Outputs scanned SSIDs from of all wifi devices via dbus.
#   Outputs in the following format:
#     SSID/n
#     Signal Strength dBm\n
#     psk|wpa|open \n
# OPTIONS:
#   ssid
#     print just the SSID data, followed by a newline character

import sys
import dbus
import collections


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


bus = dbus.SystemBus()

manager = dbus.Interface(
    bus.get_object("net.connman.iwd", "/"),
    "org.freedesktop.DBus.ObjectManager"
)
objects = manager.GetManagedObjects()
two_args = len(sys.argv) == 2

Obj = collections.namedtuple('Obj', ['interfaces', 'ch'])
tree = Obj({}, {})
for path in objects:
    node = tree
    elems = path.split('/')
    for subpath in ['/'.join(elems[:x + 1]) for x in range(1, len(elems))]:
        if subpath not in node.ch:
            node.ch[subpath] = Obj({}, {})
        node = node.ch[subpath]
    node.interfaces.update(objects[path])

root = tree.ch['/net'].ch['/net/connman'].ch['/net/connman/iwd']
for path, phy in root.ch.items():
    if 'net.connman.iwd.Adapter' not in phy.interfaces:
        continue

    properties = phy.interfaces['net.connman.iwd.Adapter']

    for path2, device in phy.ch.items():
        if 'net.connman.iwd.Device' not in device.interfaces:
            continue

        if not two_args or (two_args and sys.argv[1] != 'ssid'):
            edevice = dbus.Interface(
                bus.get_object("net.connman.iwd", path2),
                "net.connman.iwd.Station"
            )
            eprint("Scanning: [ %s ]" % path2)
            try:
                edevice.Scan()
            except dbus.exceptions.DBusException as e:
                eprint("Scan already in progress: %s" % e)
                eprint("Defaulting to use existing scan")

        for interface in device.interfaces:
            name = interface.rsplit('.', 1)[-1]
            if name not in ('Device', 'Station', 'AccessPoint', 'AdHoc'):
                continue

            properties = device.interfaces[interface]

            if name != 'Station':
                continue

            eprint("Networks:")

            station = dbus.Interface(bus.get_object("net.connman.iwd", path2),
                                     'net.connman.iwd.Station')
            for path3, rssi in station.GetOrderedNetworks():

                properties2 = objects[path3]['net.connman.iwd.Network']
                prompt = ">" if properties2['Connected'] == 1 else " "
                if not two_args or (two_args and sys.argv[1] != 'ssid'):
                    print("%s%ls" % (prompt, properties2['Name'], ))
                    print("%i dBm" % (rssi / 100,))
                    print("%s" % (properties2['Type'],))
                else:
                    print("%ls" % (properties2['Name'],))
