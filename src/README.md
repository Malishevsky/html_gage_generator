1) устанавливаем зависимости pip install -r requirements.txt
2) переходим в папку src "cd src"
2) настраиваем файл parser_config
3) запускаем парсер командой python3 parser.py , создастся json words_meaning с такой структурой:
{
            'word': string,
            'syns': list,
            'audio': string(url),
            'transcription': string,
            'partsOfSpeech': {
                'nouns': list(внутри дикты с описанием),
                'verbs': list(внутри дикты с описанием),
                'adjectives': list(внутри дикты с описанием),
            }
        }
не спаршеные слова добавляются в 'not_parse_words.txt'
4) настраиваем generator_config.yaml 
5) запускаем python3 generator.py