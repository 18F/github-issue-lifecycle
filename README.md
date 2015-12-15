# github-issue-lifecycle
Serve data on lifecycle (open -> milestones -> close) of a repo's issues

Summarizes the events in a Github repository's issues.
Output is available as

- An API (`/api/<owner>/repo/`), returning for each issue a list of `spans` -
time periods defined by the milestones in effect during that time

- A [Bokeh](http://bokeh.pydata.org/) graph ('/<owner>/<repo>/')
illustrating each issue as a horizontal bar, with
a different color for each span.  The bars show milestone and assignee information
when hovered over, and are hyperlinked to the issues' pages at Github.
