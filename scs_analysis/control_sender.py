#!/usr/bin/env python3

"""
Created on 17 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./control_sender.py scs-be2-3 5016BBBK202F shutdown now -v | \
./osio_topic_publisher.py -t /orgs/south-coast-science-dev/development/device/alpha-bb-eng-000003/control | \
./osio_mqtt_client.py -p -e
"""

import sys

from scs_analysis.cmd.cmd_control_sender import CmdControlSender

from scs_core.control.control_datum import ControlDatum
from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.sys.exception_report import ExceptionReport

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdControlSender()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    tag = Host.name()


    try:

        # ------------------------------------------------------------------------------------------------------------
        # run...

        now = LocalizedDatetime.now()

        datum = ControlDatum.construct(tag, cmd.attn, now, cmd.cmd_tokens, cmd.serial_number)

        print(JSONify.dumps(datum))
        sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
