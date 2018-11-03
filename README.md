# Инструкция по запуску

## Требования

Для корректной работы приложения требуются:

- Python 3.5+

## Установка приложения

Склонировать репозиторий:

```
git clone https://github.com/alexm93/articlecheck.git
```

Создать виртуальное окружение:

```
cd articlecheck
virtualenv ./venv
source ./venv/bin/activate
```

Установить все зависимости:
```
pip install -r ./requirements/requirements.txt
```

## Запуск приложения

```
python ./articlecheck/main.py
```

## API

- POST 127.0.0.1:5000/api/v1/conditions/

    Пример тела запроса:
    ```
    {
        "article": "Текст, который необходимо проверить",
        "conditions": {
            "operator": "and",
            "rules": [
                {
                    "object": "text",
                    "property": "content",
                    "expression": "contains",
                    "value": "Привет"
                },
                {
                    "object": "text",
                    "property": "length",
                    "expression": "more",
                    "value": 10
                }
            ],
            "groups": [
                {
                    "operator": "or",
                    "rules": [
                        {
                            "object": "category",
                            "property": "title",
                            "expression": "equal",
                            "value": "Новости"
                        },
                        {
                            "object": "category",
                            "property": "title",
                            "expression": "equal",
                            "value": "Животные"
                        }
                    ]
                },
                {
                    "operator": "and",
                    "rules": [
                        {
                            "object": "category",
                            "property": "title",
                            "expression": "in",
                            "value": ["Животные", "Новости"]
                        }
                    ]
                }
            ]
        }
    }

    ```

    Пример тела ответа:
    ```
    {   "is_valid": false,
        "rules": [
            {
                "error": "Текст не содержит Привет.",
                "is_valid": false
            },
            {
                "error": "",
                "is_valid": true
            }
        ],
        "groups": [
            {
                "is_valid": true,
                "rules": [
                    {
                        "error": "",
                        "is_valid": true
                    },
                    {
                        "error": "Категория не Животные.",
                        "is_valid": false
                    }
                ]
            },
            {
                "is_valid": true,
                "rules": [
                    {
                        "error": "",
                        "is_valid": true
                    }
                ]
            }
        ]
    }
    ```
