# api_yamdb

![example workflow](https://github.com/ilyakhakhalkin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
A database of reviews for movies, books, and music.

Users can write reviews for various works, rate them, assign categories and genres. There is also the ability to leave comments under each review.

##### Access rights:

Unauthenticated users:
- Read-only access

Authenticated users:
- Read access
- Ability to add reviews
- Ability to add comments
- Ability to edit their own reviews
- Ability to edit their own comments

Moderators:
- Full access, including the ability to add works.


### How to run:

* Clone the repository
* Navigate to the directory containing the docker-compose.yaml file:
```
cd infra
```
* Build the containers:
```
docker-compose up -d
```
* Run migrations:
```
docker-compose exec web python manage.py migrate
```
* Create a superuser:
```
docker-compose exec web python manage.py createsuperuser
```
* Collect static files:
```
docker-compose exec web python manage.py collectstatic --no-input
```

### API usage

* Docs:
```
http://127.0.0.1/redoc/
```

* "Read" operations are available to all users:
```
GET /api/v1/genres/
```

* The write operations are available only to authenticated users.
```
POST /api/v1/genres/
```

* To authenticate, you need a confirmation code that can be viewed through the Django admin panel.
```
POST /api/v1/auth/token/
```

For more details see documentation at /redoc

### Tech stack

* Python
* Django
* Django Rest Framework
* Postgresql
* Docker
* Docker-Compose
* Nginx


##### Authors

```
Timofey Gorodilov - user management: registration and authentication system, access rights, token-based authentication, email confirmation system.
Ilya Khakhalkin - categories, genres, and works: models, views, and endpoints for them.
Anna Petrova - reviews and comments.
