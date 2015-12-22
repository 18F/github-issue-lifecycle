"""
Generate Bokeh chart for a repository's issue history.
"""

from bokeh.embed import components
from bokeh.models import ColumnDataSource, OpenURL, TapTool, HoverTool
from bokeh.plotting import figure

WIDTH = 800
HEIGHT = 400
THICKNESS = 3
MARGIN = 6


def lifecycles(data):
    "Returns (script, div) tuple of Bokeh chart of Issue lifecycles for a repo"

    source = ColumnDataSource(data=dict(
        left=[s['span']['start'] for s in data['spans']],
        date=[s['span']['start'].strftime('%d %B %Y') for s in data['spans']],
        right=[s['span']['end'] for s in data['spans']],
        bottom=[s['index'] * (THICKNESS + 2 * MARGIN) for s in data['spans']],
        top=[s['index'] * (THICKNESS + 2 * MARGIN) + THICKNESS
             for s in data['spans']],
        color=data['colors'],
        issue=[s['issue'].title for s in data['spans']],
        status=[', '.join(s['span']['milestones']) for s in data['spans']],
        assignee=[s['issue'].assignee_login for s in data['spans']],
        url=[s['issue'].html_url for s in data['spans']],
        final=[s['final'] for s in data['spans']], ))

    fig = figure(x_axis_type='datetime', title='Issue progress', )
    fig.yaxis.major_label_text_color = None

    fig.quad(left='left',
             bottom='bottom',
             right='right',
             top='top',
             source=source,
             color='color',
             )

    hover = HoverTool(tooltips=[("issue", "@issue"),
                                ("date", "@date"),
                                ("status", "@status"),
                                ("final", "@final"),
                                ("assignee", "@assignee"),
                                ("url", "@url"), ])
    fig.add_tools(hover)
    taptool = TapTool(callback=OpenURL(url="@url"))
    fig.add_tools(taptool)

    result = components(fig)
    result = {'script': result[0], 'div': result[1]}
    return result
