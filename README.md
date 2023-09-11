# Sibdev Test  
Тестовое задание на позицию Python разработчик


## Installation 
```poetry install```

## Testing 
```
poetry shell
pytest
```

## Запуск
### Docker 
```
docker-compose up --build
```
### Сбор котировок
```
docker exec -ti sibdev_test-backend-1 python manage.py load_quotes
```
