import datetime

from bokeh.embed import components
from bokeh.models import ColumnDataSource, OpenURL, TapTool, HoverTool, CustomJS
from bokeh.models.annotations import Legend
from bokeh.plotting import figure

WIDTH = 800
HEIGHT = 400
THICKNESS = 3
MARGIN = 6


def lifecycles(repo):
    "Returns (script, div) tuple of Bokeh chart of Issue lifecycles for a repo"

    spans = list(repo.spans())
    stones = list(repo.stones())
    source = ColumnDataSource(data=dict(
        left=[s['span'][1] for s in spans],
        right=[s['span'][2] for s in spans],
        bottom=[s['index'] * (THICKNESS + 2 * MARGIN) for s in spans],
        top=[s['index'] * (THICKNESS + 2 * MARGIN) + THICKNESS for s in spans],
        color=[repo.milestone_colors[s['span'][0][-1]] for s in spans],
        issue=[s['issue'].title for s in spans],
        date=[s['span'][1].strftime("%b %d") for s in spans],
        status=[', '.join(s['span'][0]) for s in spans],
        assignee=[s['issue'].assignee_login for s in spans],
        url=[s['issue'].html_url for s in spans],
        final=[s['final'] for s in spans],
        x=[s['stone'][1] for s in stones],
        y=[s['index'] * (THICKNESS + 2 * MARGIN) + THICKNESS / 2 for s in
           stones],
        stone_color=[repo.milestone_colors[s['stone'][0]] for s in stones], ))

    stone_source = ColumnDataSource(
        data=dict(x=[s['stone'][1] for s in stones],
                  y=[s['index'] * (THICKNESS + 2 * MARGIN) + THICKNESS / 2
                     for s in stones],
                  color=[repo.milestone_colors[s['stone'][0]] for s in stones],
                  issue=[s['issue'].title for s in stones],
                  date=[s['stone'][1].strftime("%b %d") for s in stones],
                  milestone=[s['stone'][0] for s in stones],
                  assignee=[s['issue'].assignee_login for s in stones],
                  url=[s['issue'].url for s in stones],
                  size=THICKNESS * 2, ))

    fig = figure(x_axis_type='datetime', title='Issue progress', )
    fig.yaxis.major_label_text_color = None

    fig.quad(left='left',
             bottom='bottom',
             right='right',
             top='top',
             source=source,
             color='color',
             alpha='alpha', )

    # fig.x(x='x', y='y', color='stone_color', source=source, size=THICKNESS * 2)
    # the hovers don't correspond

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
