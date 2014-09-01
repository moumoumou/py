#!/usr/bin/env python
'''
Created on Jun 11, 2012

@author: Yangming
'''
import nagios
from nagios import CommandBasedPlugin as plugin
import commands
import statsd
import argparse

class MemcachedChecker(nagios.BatchStatusPlugin):
    def __init__(self, *args, **kwargs):
        super(MemcachedChecker, self).__init__(*args, **kwargs)
        # Hack to determine uniqueness of script defs
        check = argparse.ArgumentParser()
        check.add_argument("-H", "--host",     required=False, type=str)
        check.add_argument("-p", "--port",     required=False, type=int)
        chk, unknown = check.parse_known_args()

        self.parser.add_argument("-f", "--filename", required=False, type=str, default='pd@memcached_stats')
        self.parser.add_argument("-H", "--host",     required=False, type=str, default="localhost")
        self.parser.add_argument("-p", "--port",     required=False, type=int, default=11211)
        self.parser.add_argument("-z", "--appname",  required=False, type=str, default='memcached')
        self.parser.add_argument("--unique",   required=False, type=str, default=str(chk.host)+str(chk.port))

    def _get_batch_status(self, request):
        cmd = "echo 'stats' | nc"
        cmd += " %s %s" % (request.host, request.port)
#        output = commands.getoutput(cmd)
#        if output.strip() == "":
        import subprocess
        cmd = "exec 5<>/dev/tcp/%s/%s;echo -e \"stats\nquit\" >&5;cat <&5" % (request.host, request.port)
        proc = subprocess.Popen(['bash', '-c', cmd],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)
        output, _ = proc.communicate()
        return output


    def _parse_output(self, request, output):
        for l in output.split('\r\n'):
            triple = l.split(" ")
            if triple[0] != "STAT":
                continue
            k = triple[1]
            v = triple[2]
            value = nagios.to_num(v)
            if value is not None:
                yield k, value

    def _validate_output(self, request, output):
        if output.strip() == "":
            raise nagios.ServiceInaccessibleError(request)
        elif "STAT" not in output or "END" not in output:
            raise nagios.ServiceInaccessibleError(request, output)
        return True

    @plugin.command("OPERATIONS_SET_REQUESTS")
    @statsd.counter
    def get_cmd_set(self, request):
        value = self.get_delta_value("cmd_set", request)
        return self.get_result(request, value, '%s set requests' % value, 'set_requests')

    @plugin.command("OPERATIONS_GET_REQUESTS")
    @statsd.counter
    def get_cmd_get(self, request):
        value = self.get_delta_value("cmd_get", request)
        return self.get_result(request, value, '%s get resquests' % value, 'get_requests')

    @plugin.command("BYTES_READ")
    @statsd.counter
    def get_bytes_read(self, request):
        value = self.get_delta_value("bytes_read", request)
        return self.get_result(request, value, '%s bytes read' % value, 'bytes_read')

    @plugin.command("BYTES_WRITTEN")
    @statsd.counter
    def get_bytes_written(self, request):
        value = self.get_delta_value("bytes_written", request)
        return self.get_result(request, value, '%s bytes written' % value, 'bytes_written')

    @plugin.command("BYTES_ALLOCATED")
    @statsd.gauge
    def get_bytes_allocated(self, request):
        value = self.get_status_value("bytes", request)
        return self.get_result(request, value, '%s bytes allocated' % value, 'bytes_allocated')

    @plugin.command("TOTAL_ITEMS")
    @statsd.gauge
    def get_total_items(self, request):
        value = self.get_status_value("total_items", request)
        return self.get_result(request, value, '%s total items' % value, 'items')

    @plugin.command("CURRENT_CONNECTIONS")
    @statsd.gauge
    def get_current_connections(self, request):
        value = self.get_status_value("curr_connections", request)
        return self.get_result(request, value, '%s current connections' % value, "connections")

if __name__ == "__main__":
    import sys
    MemcachedChecker().run(sys.argv[1:])
