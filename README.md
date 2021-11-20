# Blog
## Локальный запуск сервера
`python manage.py runserver`
____
## API
`GET /api/articles/` - возвращает список всех статей.

Возвращает:
```
HTTP 200 OK
{
    "articles": [
        {
            "id": integet
            "title": string(120),
            "description": text,
            "body": text
            "author_id": integer
        }
        ...
    ]
}
```
___
`GET /api/articles/<int:article_id>` - возвращает статью.

Возвращает:
```
HTTP 200 OK
{
    "articles": [
        {
            "id": integet
            "title": string(120),
            "description": text,
            "body": text
            "author_id": integer
        }
    ]
}
```
```
HTTP 404 Not Found
{
    "detail": "Страница не найдена."
}
```
___
`POST /api/articles/` - создаёт статью.
```
{
    "article": {
        "title": string(120),
        "description": text,
        "body": text,
        "author_id": integer
    }
}
```
Возвращает:
```
HTTP 200 OK
{
    "success": "Article 'article_name' created successfully"
}
```
___
`PUT /api/articles/<int:article_id>` - редактирует статью.
```
{
    "article": {
        "title": string(120),
        "description": text,
        "body": text,
        "author_id": integer
    }
}
```
Все параметры не обязательны.

Возвращает:
```
HTTP 200 OK
{
    "success": "Article 'article_name' created successfully"
}
```
```
HTTP 404 Not Found
{
    "detail": "Страница не найдена."
}
```
___
`DELETE /api/articles/<int:article_id>` - удаляет статью.

Возвращает:
```
HTTP 204 No Content
{
    "message": "Article with id `2` has been deleted."
}
```
```
HTTP 404 Not Found
{
    "detail": "Страница не найдена."
}
```
____