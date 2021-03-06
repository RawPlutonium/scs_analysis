#!/usr/bin/env python3

"""
Created on 3 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The histo_chart utility is used to create Matplotlib histogram charts and comma-separated value (CSV) histogram files.
The utility analyses a given path to a leaf node of the input JSON data stream.

Depending on operating system, it may be necessary to edit the matplotlibrc file, which specifies the Matplotlib
back-end graphics system.

EXAMPLES
./socket_receiver.py | ./histo_chart.py val.CO2.cnc -x -10 10 -e -o CO.csv

FILES
~/SCS/scs_analysis/scs_analysis/matplotlibrc

SEE ALSO
scs_analysis/multi_chart
scs_analysis/single_chart
"""

import sys
import warnings

from scs_analysis.chart.histo_chart import HistoChart
from scs_analysis.cmd.cmd_histo_chart import CmdHistoChart

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_core.sync.line_reader import LineReader

from scs_core.sys.exception_report import ExceptionReport


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    warnings.filterwarnings("ignore", module="matplotlib")

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdHistoChart()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)

    chart = None
    proc = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # reader...
        reader = LineReader(sys.stdin.fileno())

        if cmd.verbose:
            print(reader, file=sys.stderr)

        # chart...
        chart = HistoChart(cmd.batch_mode, cmd.x[0], cmd.x[1], cmd.bin_count, cmd.path, cmd.outfile)

        if cmd.verbose:
            print(chart, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        proc = reader.start()

        for line in reader.lines:
            if chart.closed:
                break

            if line is None:
                chart.pause()
                continue

            datum = PathDict.construct_from_jstr(line)

            if datum is None:
                break

            if cmd.echo:
                print(JSONify.dumps(datum.node()))
                sys.stdout.flush()

            chart.plot(datum)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        if cmd.verbose:
            print("histo_chart: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # close...

    finally:
        if proc:
            proc.terminate()

        if chart is not None and not chart.closed:
            if cmd.verbose:
                print("histo_chart: holding", file=sys.stderr)

            # noinspection PyBroadException

            try:
                chart.hold()

            except Exception:
                pass
