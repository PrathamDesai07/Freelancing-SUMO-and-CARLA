#!/bin/bash
sudo docker run --rm -it --gpus all --privileged --net=host \
   --shm-size=2g \
   carlasim/carla:0.9.15 \
   bash -c "./CarlaUE4.sh -opengl -carla-server -nosound -RenderOffScreen -quality-level=Low" 4.26.2-0+++UE4+Release-4.26 522 0