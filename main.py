import uvicorn
from modules.parser import APTSiteParser
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from templates.renderer import render_template
from typing import *
from configs.reader import get_config_variable

app = FastAPI()
parser = APTSiteParser()

app.mount(
    get_config_variable('static.path'),
    StaticFiles(directory=get_config_variable('static.folder')),
    name='static'
)

@app.get('/')
async def show_app_page():
    return render_template('index.html')

@app.get('/health')
async def healthcheck():
    return {'response': 'ok'}

@app.get('/groups')
async def show_groups():
    return await parser.get_groups()

@app.get('/students')
async def show_students(group_id: str):
    group_ids: List[str] = [
        i['id'] for i in await parser.get_groups()
    ]

    if group_id.lower() != 'all' and group_id not in group_ids:
        return HTMLResponse({'error': "Invalid group_id parameter!"}, status_code=400)

    if group_id.lower() == 'all':
        return await parser.get_all_students()
    else:
        return await parser.get_students(int(group_id))

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host=get_config_variable('server.address'),
        port=int(get_config_variable('server.port'))
    )
