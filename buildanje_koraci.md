Pratiti upute s: https://github.com/dragonlong/articulated-pose#setup

# Moja konfiguracija
Ubuntu 18.04
CUDA 10.0
CUDNN 7.6.5
NVIDIA driver neki 470.x.x
Tensorflow 1.15.0


Umjesto conda enva, koristio sam pythonov venv 
OBAVEZNO AKTIVIRATI VENV:
    `source ./venv/bin/activate  # sh, bash, or zsh`

Kod naredbe `pip install -r requirements.txt`, izbacivalo mi je grešku da ne može naći dobru verziju apptools-a. Umjesto 4.4.0, instalirao sam verziju 4.5.0. Za ostale ista stvar, ako ne može nać jednu verziju, koristiti sljedeću kompatibilnu. Moguće je promijeniti sve znakove '==' u '~=' da se automatski skidaju kompatibilne verzije.
Sve ostale verzije koje se ne mogu pronaći, skinuti i instalirati ručno. 


# DATOTEKA config.sh: 
- Promijeniti putanju u: CUDA_DIR=/usr/local/cuda-10.2
- Ako tf nije instaliran pomoću conda-e, promijeniti putanju u: CONDA_ENV_DIR=$VIRTUAL_ENV
- Promijeniti sljedeće naredbe: 
    tensorflow_include_dir=$CONDA_ENV_DIR/lib/python3.6/site-packages/tensorflow_core/include
    tensorflow_external_dir=$CONDA_ENV_DIR/lib/python3.6/site-packages/tensorflow_core/include/external/nsync/public

    tensorflow_library_dir=$CONDA_ENV_DIR/lib/python3.6/site-packages/tensorflow_core

Ako izbaci sljedeću grešku: "/usr/bin/ld: cannot find -ltensorflow_framework" navigirati do libtensorflow_framework.so.1:
    `$ cd $VIRTUAL_ENV/lib/python3.6/site-packages/tensorflow_core`
    i napraviti symbolic link na libtensorflow_framework.so.1: `ln -s libtensorflow_framework.so.1 libtensorflow_framework.so`

Vratiti se nazad u direktorij gdje je compile_op.sh 

Kompajlati pomoću `sh compile_op.sh`
Bacit će par warninga, al samo se errori gledaju!