# Blog
## Локальный запуск сервера
`python manage.py runserver`
____
## API
### Регистрация и авторизация
`POST /auth/users/` - регистрация пользователя.
```
{
    "username": string,
    "email": string,
    "password": string,
    "re_password": string
}
```

Возвращает:
```
HTTP 201 Created
{
    "email": string,
    "username": string,
    "id": integer
}
```
Посылает письмо для активации на почту.

В письме отправляется ссылка вида: `http://127.0.0.1:8000/activate/?uid=<str:uid>&token=<str:token>`
___
`POST /auth/users/activation/` - активирует зарегистрированного пользователя.
Без активации на возможно войти.

```
{
    "uid": string,
    "token": string
}
```
Возвращает:
```
HTTP 204 No Content
```
___
`POST /auth/token/login/` - возвращает `auth_token`.
```
{
    "username": string,
    "password": string
}
```
Возвращает:

```
HTTP 200 OK
{
    "auth_token": string
}
```
Данный токен надо прописывать в `Headers`

`Authorization : Token <str:token>`
___
`POST /auth/token/logout/` - уничтожает `token`.

Данный токен надо прописывать в `Headers`

`Authorization : Token <str:token>`
___
### Articles
`GET /api/articles?limit=<int:limit>&offset=<int:offset>&sort=<str:sort>&author_id=<int:author_id>` - возвращает список всех статей.
Все параметры передаваемые в url необязательны.

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