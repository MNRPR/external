#!/usr/bin/env python3

""" Simple keep-alive of file mounts so they don't go stale and have input/output errors"""
mount_list = [
        "/mnt/.mounted",
        "/mnt/.mounted",
		"/mnt/public/.mounted",
]

error_list = []

for mount in mount_list:
        try:
                with open(mount, "r") as mount_point:
                        pass
        except Exception as err:
                error_list.append(mount)

if error_list:
        print("Failed mounts: {}".format(error_list))