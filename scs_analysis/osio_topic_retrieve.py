#!/usr/bin/env python3

"""
Created on 20 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_analysis/osio_topic_subscribe.py /users/southcoastscience-dev/test/status
"""

import sys

from scs_analysis.cmd.cmd_osio_topic_retrieve import CmdOSIOTopicRetrieve

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.manager.message_manager import MessageManager
from scs_core.sys.exception_report import ExceptionReport

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    agent = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOTopicRetrieve()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    try:
        # ------------------------------------------------------------------------------------------------------------
        # resource...

        api_auth = APIAuth.load_from_host(Host)

        if api_auth is None:
            print("APIAuth not available.")
            exit()

        if cmd.verbose:
            print(api_auth, file=sys.stderr)

        http_client = HTTPClient()

        manager = MessageManager(http_client, api_auth.api_key)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        end = LocalizedDatetime.now() if cmd.end is None else cmd.end

        messages = manager.find_for_topic(cmd.path, cmd.start, end)

        for message in messages:
            print(JSONify.dumps(message.payload.payload))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt as ex:
        if cmd.verbose:
            print("osio_topic_retrieve: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
