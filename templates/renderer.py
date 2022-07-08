import jinja2
from fastapi.responses import HTMLResponse
from configs.reader import get_config_variable

loader = jinja2.FileSystemLoader('templates')
env = jinja2.Environment(loader=loader)

def render_template(template_name: str, **kwargs) -> HTMLResponse:
    template = env.get_template(template_name)
    kwargs.update({
        'static_path': get_config_variable('static.path'),
        'root_path': get_config_variable('server.root_path')
    })
    return HTMLResponse(template.render(**kwargs))
