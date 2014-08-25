#!/bin/env python

#   115.236.77.194

import ping
from time import sleep

print ping.do_one('61.147.72.236', 2, 64)
sleep(2)
print ping.quiet_ping('61.147.72.236')




'''

FUNCTIONS
    checksum(source_string)
        I'm not too confident that this is right but testing seems
        to suggest that it gives the same answers as in_cksum in ping.c

    do_one(dest_addr, timeout, psize)
        Returns either the delay (in seconds) or none on timeout.

    quiet_ping(dest_addr, timeout=2, count=4, psize=64)
        Send `count' ping with `psize' size to `dest_addr' with
        the given `timeout' and display the result.
        Returns `percent' lost packages, `max' round trip time
        and `avrg' round trip time.

    receive_one_ping(my_socket, id, timeout)
        Receive the ping from the socket.

    send_one_ping(my_socket, dest_addr, id, psize)
        Send one ping to the given >dest_addr<.

    verbose_ping(dest_addr, timeout=2, count=4, psize=64)
        Send `count' ping with `psize' size to `dest_addr' with
        the given `timeout' and display the result.

'''