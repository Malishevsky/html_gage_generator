import json
import requests
import yaml
from threading import Thread, Semaphore
import os

semaphore = Semaphore()

file_path = "not_parse_words.txt"

if os.path.exists(file_path):
    os.remove(file_path)

with open("parser_config.yaml", "r") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    start_index = config.get('start_index')
    finish_index = config.get('finish_index')
    thread_count = config.get('thread_count')
    word_list_path = config.get('word_list_path')
    words_meaning_path = config.get('words_meaning_path')

with open(word_list_path) as words:
    word_list = json.load(words)['list']

result_list = []


def get_word_definition(word, num):
    print(num)
    resp = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    if resp.status_code == 200:
        meanings = resp.json()
        audio = ''
        transcription = '/----/'
        noun_list = []
        adj_list = []
        verb_list = []
        all_syn = []
        for meaning in meanings:
            meaning.pop('license', None)
            meaning.pop('sourceUrls', None)
            if meaning.get('phonetic') and transcription == '/----/':
                transcription = meaning.get('phonetic')
            if meaning.get('phonetics'):
                for phonetic in meaning['phonetics']:
                    if phonetic.get('audio') and not audio:
                        audio = phonetic.get('audio')
                    phonetic.pop('license', None)
                    phonetic.pop('sourceUrl', None)
            for meaning_elem in meaning['meanings']:
                cur_defin = []
                cur_example = []
                cur_syn = []
                cur_ant = []
                meaning_elem.pop('antonyms', None)
                part_speach = meaning_elem.get('partOfSpeech')
                if meaning_elem.get('synonyms'):
                    all_syn = meaning_elem.get('synonyms')
                for defenition in meaning_elem['definitions']:
                    def_ant_list = defenition.get('antonyms')
                    example_text = defenition.get('example')
                    defin_text = defenition.get('definition')
                    def_syn_list = defenition.get('synonyms')
                    if def_ant_list:
                        cur_ant = def_ant_list
                    if def_syn_list:
                        cur_syn = def_syn_list
                    if defin_text:
                        cur_defin.append(defin_text)
                    if example_text:
                        cur_example.append(defin_text)

                part = {
                    'meaning': ' ; '.join(cur_defin),
                    'syn': cur_syn,
                    'ant': cur_ant,
                    'example': cur_example
                }

                if part_speach == 'noun':
                    noun_list.append(part)
                elif part_speach == 'verb':
                    verb_list.append(part)
                elif part_speach == 'adjective':
                    adj_list.append(part)

        new_word_data = {
            'word': word,
            'syns': all_syn,
            'audio': audio,
            'transcription': transcription,
            'partsOfSpeech': {
                'nouns': noun_list,
                'verbs': verb_list,
                'adjectives': adj_list,
            }
        }
        semaphore.acquire()
        result_list.append(new_word_data)
        semaphore.release()
    else:
        with open(file_path, 'a') as log:
            log.write(f'{word}\n')

thread_list = []

for i in range(start_index, finish_index, thread_count):
    for j in range(thread_count):
        if i + j > len(word_list):
            break
        word = word_list[i + j]
        th = Thread(target=get_word_definition, args=(word, i + j))
        thread_list.append(th)
        th.start()
    for th in thread_list:
        th.join()
    thread_list = []

with open(words_meaning_path, 'w') as new_file:
    json.dump(result_list, new_file, indent=4)

