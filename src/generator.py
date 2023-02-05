import requests
from jinja2 import FileSystemLoader, Environment
import json
import yaml
import os

with open("generator_config.yaml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

file_translate = open('jsons/words_meaning.json')
translate_data = json.load(file_translate)

file_reader = FileSystemLoader('templates/base')
env = Environment(loader=file_reader)
base_template = env.get_template('maintemplate.htm')
translate_template = env.get_template('itemblock.htm')
# url = "http://51.75.89.19:8080/api/translate"
url = "https://api-b2b.backenster.com/b1/api/v3/translate"

payload = {
    "enableTransliteration": True,
    "translateMode": "html",
    "platform": "api",
    "from": config['source'],
    "to": config['target'],
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": config['api_token']
}
url_prefix ='#'

if config.get('url_prefix'):
    url_prefix = f"{config.get('url_prefix')}{config.get('source')}-{config.get('target')}/"

# translate_config = {
#   "source": config['source'],
#   "target": config['target'],
#   "translateMode": config['translateMode'],
# }


def render_and_save_html(data, translate):
    rendered_template = base_template.render(general={},
                               url_prefix= url_prefix,
                               meta_title=f'"{data.get("word")}" meaning',
                               url_dictionary=config['url_dictionary'],
                               url_main_page=config['url_main_page'],
                               result=data,
                               url={},
                               meta_description={},
                               fileAliases={},
                               translation=translate,
                               )

    directory = f'templates/generated/{config["source"]}-{config["target"]}/'

    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f'{directory}{data["word"]}.html', 'w') as file:
        file.write(rendered_template)


def render_translate(result):
    template_before_translate = translate_template.render(result=result)
    payload['data'] = template_before_translate
    response = requests.post(url, json=payload, headers=headers)
    # translate_config['q'] = template_before_translate
    # response = requests.post(url,headers=headers, data=translate_config)

    if response.status_code == 200:
        # template_after_translate = response.json()['translatedText']]
        template_after_translate = response.json()['result']
        return template_after_translate
    else:
        print("Request failed")
        return None

for obj in  translate_data:
    translate_block = render_translate(obj)
    render_and_save_html(obj, translate_block)
