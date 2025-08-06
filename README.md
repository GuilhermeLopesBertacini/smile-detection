# Build Container
docker build -t smile-detection .

# Rodar script automaticamente
docker run --rm -it --device /dev/video0 smile-detection

# Rodar com volume
xhost +local:root  # libera acesso X11 para root local

docker run --rm -it \
  --device /dev/video0 \
  -v "$(pwd)":/app \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  smile-detection

# Rodar terminal para testes
docker run --rm -it smile-detection /bin/bash