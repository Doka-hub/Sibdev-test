# Sibdev Test  
Тестовое задание на позицию Python разработчика

## Запуск
### Docker 
```
docker-compose up --build
```
### Сбор котировок
```
docker exec -ti sibdev_test-backend-1 python manage.py load_quotes
```

## Testing 
```
docker exec -it sibdev_test-backend-1 pytest
```
