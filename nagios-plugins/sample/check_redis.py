#!/usr/bin/env python
'''
Created on May 31, 2012

@author: Yangming
'''
import re
import commands
import statsd
import nagios
from nagios import CommandBasedPlugin as plugin
import argparse

class RedisChecker(nagios.BatchStatusPlugin):
    def __init__(self, *args, **kwargs):
        super(RedisChecker, self).__init__(*args, **kwargs)
        # Hack to determine uniqueness of script defs
        check = argparse.ArgumentParser()
        check.add_argument("-H", "--host",     required=False, type=str)
        check.add_argument("-p", "--port",     required=False, type=int)
        chk, unknown = check.parse_known_args()

        self.parser.add_argument("-f", "--filename", required=False, type=str, default='pd@redis-cli_info')
        self.parser.add_argument("-u", "--user",     required=False, type=str)
        self.parser.add_argument("-s", "--password", required=False, type=str)
        self.parser.add_argument("-H", "--host",     required=False, type=str)
        self.parser.add_argument("-p", "--port",     required=False, type=int)
        self.parser.add_argument("-n", "--database", required=False, type=int)
        self.parser.add_argument("-z", "--appname",  required=False, type=str, default='redis')
        self.parser.add_argument("--unique",   required=False, type=str, default=str(chk.host)+str(chk.port))

    def _get_batch_status(self, request):
        cmd = "redis-cli --raw"
        if request.password:
            cmd += " -a %s" % request.password
        if request.database:
            cmd += " -n %s" % request.database
        if request.host:
            cmd += " -h %s" % request.host
        if request.port:
            cmd += " -p %s" % request.port
        cmd += " info"
        if request.user:
            cmd = nagios.rootify(cmd, request.user)
        return commands.getoutput(cmd)

    def _parse_output(self, request, output):
        for l in output.split('\r\n'):
            k, v = l.split(':')
            value = nagios.to_num(v)
            if value is not None:
                yield k, value

    def _validate_output(self, request, output):
        if "command not found" in output:
            raise nagios.ServiceInaccessibleError(request, output)
        elif output.strip() == "":
            raise nagios.ServiceInaccessibleError(request, output)
        return True

    @plugin.command("CURRENT_OPERATIONS")
    @statsd.counter
    def get_current_operations_rate(self, request):
        value = self.get_delta_value("total_commands_processed", request)
        return self.get_result(request, value, "%s commands" % value, 'current_commands')

    @plugin.command("AVERAGE_OPERATIONS_RATE")
    @statsd.gauge
    def get_average_operations_rate(self, request):
        queries = self.get_status_value("total_commands_processed", request)
        sec = self.get_status_value("uptime_in_seconds", request)
        value = queries / sec
        return self.get_result(request, value, '%s commands per second' % value, 'average_rate')

    @plugin.command("READ_WRITE_RATIO")
    @statsd.gauge
    def get_read_write_ratio(self, request):
        return nagios.Result(request.option, nagios.Status.UNKNOWN,
                                 "mysterious status", request.appname)

    @plugin.command("MEMORY_USED")
    @statsd.gauge
    def get_memory_used(self, request):
        value = nagios.BtoMB(self.get_status_value("used_memory", request))
        return self.get_result(request, value, "%sMB used_memory" % value, 'used_memory', UOM="MB")

    @plugin.command("CURRENT_CHANGES")
    @statsd.counter
    def get_current_changes(self, request):
        value = self.get_delta_value("changes_since_last_save", request)
        return self.get_result(request, value, "%s changes" % value, 'changes')

    @plugin.command("CHANGES_SINCE_LAST_SAVE")
    @statsd.gauge
    def get_changes_since_last_save(self, request):
        value = self.get_status_value("changes_since_last_save", request)
        return self.get_result(request, value, "%s changes since last save" % value, 'changes')

    @plugin.command("TOTAL_KEYS")
    @statsd.gauge
    def get_total_keys(self, request):
        cmd = "redis-cli dbsize"
        output = commands.getoutput(cmd)
        dbsize_pattern = re.compile(".*?(\d+)")
        matchResult = dbsize_pattern.match(output)
        if not matchResult:
            raise nagios.OutputFormatError(request, output)
        value = int(matchResult.groups(1)[0])
        return self.get_result(request, value, '%s total keys' % value, 'total_keys')

    @plugin.command("COMMAND_FREQUENCY")
    @statsd.gauge
    def get_command_frequency(self, request):
        return nagios.Result(request.option, nagios.Status.UNKNOWN,
                                 "mysterious status", request.appname)

if __name__ == "__main__":
    import sys
    RedisChecker().run(sys.argv[1:])
