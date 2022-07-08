import aiohttp
from bs4 import BeautifulSoup
from typing import List, Pattern, Optional
from modules.redis_client import redis_cache
import re

GROUP_NAME_REGEX = re.compile(r'Список абитуриентов группы (?P<group>.{1,})специальность (?P<speciality>.{1,})[\S\s]*План набора - (?P<plan>[0-9]{1,})')

class APTSiteParser:
    headers: dict

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 YaBrowser/20.12.1.179 Yowser/2.5 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "X-Requested-With": "XMLHttpRequest"
        }
    
    def __repr__(self) -> str:
        return 'APTParserObject'
    
    @redis_cache(86400)
    async def get_groups(self) -> List[dict]:
        groups = {}

        departments = ['Очное', 'Заочное']
        for department in departments:
            async with aiohttp.ClientSession(headers=self.headers) as client:
                async with client.get(
                    f'https://almetpt.ru/department?department={department}'
                ) as resp:
                    resp.raise_for_status()
                    cookies = resp.cookies
                
                async with client.get(
                    'https://almetpt.ru/abitGroups', cookies=cookies
                ) as resp:
                    resp_text = await resp.text()
            
            soup = BeautifulSoup(resp_text, 'html.parser')
            courses = {}

            for elem in soup.find_all('td', {'data-select': 0}):
                courses[elem.text] = {
                    'id': elem['data-id']
                }

            groups.update(courses)
        
        return [{'name': i[0], **i[1]} for i in groups.items()]
    
    async def get_all_students(self) -> dict:
        students = []
        for group in await self.get_groups():
            for student in (await self.get_students(group['id']))['students']:
                students.append(student)
        
        students.sort(key=lambda x: x['mark'], reverse=True)
        return {
            'students': students, 'group_info': None
        }

    @redis_cache(600)
    async def get_students(self, group_id: int) -> dict:
        async with aiohttp.ClientSession(headers=self.headers) as client:
            async with client.get(
                f'http://almetpt.ru/abiturients/freeList?abitGroup={group_id}'
            ) as resp:
                resp_text = await resp.text()

        soup = BeautifulSoup(resp_text, 'html.parser')
        
        list_title = soup.find_all('h3')[0].text
        group_info: Optional[dict] = None
        group_info_match = GROUP_NAME_REGEX.match(list_title)
        if group_info_match is not None:
            group_info = {
                'group_name': group_info_match.group('group'),
                'speciality_name': group_info_match.group('speciality'),
                'plan': int(group_info_match.group('plan'))
            }

        table_cells = soup.find_all('td')
        applicants_dict =  {
            table_cells[index + 1].text: float(
                table_cells[index + 2].text
            )
            for index in range(0, len(table_cells), 3)
        }

        applicants_items = list(applicants_dict.items())
        applicants_items.sort(key=lambda x: x[1], reverse=True)

        return {'students': [{'name': i[0], 'mark': i[1], 'group_id': group_id} for i in applicants_items], 'group_info': group_info}
