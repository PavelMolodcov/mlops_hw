### ДЗ MlOps Павел Молодцов

- За основу взял код из лекции, но переписал на FastApi
- Так как лучшее мое решение было на lightautoml предпроцессинга не потребовалось соостветственно этот пункт убрал
- Во время загрузки модели выводятся пользовательские логи об отсутствии некоторых пакетов, но в моей модели это не требуется
- Таккак модель тяжелая все происходит не быстро

### Запуск

docker build -t hw_mlos:1.0 .

Запускать рекомендую таким образом

docker run -it -p 3000:3000 --name=hw_mlops_molodtsov hw_mlos:1.0

Без ключей -it его сложно останавливать, необходимо через exec убивать процесс uvicorn, а так просто ctrl+C

### dockerhub

https://hub.docker.com/r/brerostern/hw_mlops_pavel_molodtsov - сама ссылка

docker pull brerostern/hw_mlops_pavel_molodtsov:1.0 -код для загрузки