from pretty_html_table import build_table

DEFAULT_STYLE = 'blue_light'

def render(df=None,style=DEFAULT_STYLE,filename=None):
    html = build_table(df,style)
    with open(filename,'w') as f:
        f.write(html)