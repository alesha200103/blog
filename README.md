# Blog
## Локальный запуск сервера
```
python manage.py makemigrations
python manage.py makemigrations article
python manage.py migrate
python manage.py runserver
```
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
`GET /api/articles?limit=<int:limit>&offset=<int:offset>&sort=<str:sort>&author_id=<int:author_id>&category=<str:category>&in_title=<str:in_title>&in_description=<str:in_description>&in_text=<str:in_text>` - возвращает список всех статей.
Все параметры передаваемые в url необязательны.

* При задании `in_title` находит статьи содержащие переданное значение в заголовке.

* При задании `in_description` находит статьи содержащие переданное значение в заголовке и описании.

* При задании `in_text` находит статьи содержащие переданное значение в заголовке, описании и тексте.

При этом, при задании нескольких параметров будет применён поиск по тому параметру, который стоит выше в списке.


Возвращает:
```
HTTP 200 OK
{
    "articles": [
        {
            "id": integet
            "title": string(120),
            "description": text,
            "body": text,
            "category": string(11),
            "author_id": integer,
            "created_at": datetime,
            "updated_at": datetime,
            "author_name": string(150),
            "likes_count": integer,
            "comments_count": integer
        }
        ...
    ]
}
```

```
HTTP 204 No Content
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
            "body": text,
            "category": string(11),
            "author_id": integer,
            "created_at": datetime,
            "updated_at": datetime,
            "author_name": string(150),
            "likes_count": integer,
            "comments_count": integer
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
        "category": string(11),
        "author_id": integer
    }
}
```

`category` может принимать следующие значения:

* cinema
* travelling
* science
* technology
* style
* celebrities
* culture
* sport
* finance
* politics

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
        "category": string(11),
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
HTTP 403 Forbidden
{
    "detail": "Нет прав на редактирование."
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
HTTP 403 Forbidden
{
    "detail": "Нет прав на удаление."
}
```
```
HTTP 404 Not Found
{
    "detail": "Страница не найдена."
}
```
____

## Comment

`Get /api/comments/<int:article_id>` - возвращает список комментариев к статье с id: `<int:article_id>`.

Возвращает:

```
HTTP 200 OK
{
    "comments": [
        {
            "id": integer,
            "content": text,
            "author_id": integer,
            "article_id": integer,
            "created_at": datetime,
            "author_name": string(150)
        },
        ...
    ]
}
```

```
HTTP 404 Not Found
{
    "detail": "Комментариев нет."
}
```
___

`POST /api/comments/<int:article_id>` - создаёт комментарий к статье с id: `<int:article_id>`.
```
{
    "comment": {
        "content": text,
        "author_id": integer
    }
}
```

Возвращает:

```
HTTP 200 OK
{
    "comment": {
        "id": integer,
        "content": text,
        "author_id": integer,
        "article_id": integer,
        "created_at": DateTime,
        "author_name": string(150)
    }
}
```

```
HTTP 400 Bad Request
{
    "detail": "Неверные данные."
}
```
___
## Likes

`GET /api/like/<int:article_id>` - проверяет, поставил ли текущий пользователь лайк.

Возвращает:

```
HTTP 200 OK
{
    "is_liked": bool
}
```
___

`PUT /api/like/<int:article_id>` - ставит/убирает лайк статьи с id `article_id`.

Возвращает:

```
HTTP 200 OK
{
    "likes_count": integer
}
```
___
