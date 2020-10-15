from jinja2 import Environment, PackageLoader, select_autoescape
from vmap_knife import TraceReport

env = Environment(
    loader=PackageLoader('vmap_knife', 'template'),
    autoescape=select_autoescape(['html', 'xml'])
)


def generate_report(trace_report: TraceReport) -> str:
    template = env.get_template('report_template.html')
    return template.render(report=trace_report)
