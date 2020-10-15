"""Console script for vmap_knife."""
import sys
import click
from vmap_knife import generate_report, process_trace_report, parse_vmap, parse_csv


@click.command()
@click.option('--csvfile')
@click.option('--vmapfile')
@click.option('--outputfile', default='report.html')
def main(csvfile, vmapfile, outputfile):
    click.echo(
        f"Generating report from CSV [{csvfile}], VMAP [{vmapfile}] to location [{outputfile}]")
    trace = parse_csv(csvfile)
    vmap = parse_vmap(vmapfile)
    trace_report = process_trace_report(vmap, trace)
    report = generate_report(trace_report)
    with open(outputfile, 'w') as out:
        out.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pylint: disable=no-value-for-parameter
