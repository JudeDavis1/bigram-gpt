# pip3 install pipenv
# pipenv --python $(which python3)
# pipenv install

device=$1

<<<<<<< Updated upstream
python3 -m src.model.train -ga 2 -mp -e 5 --device $device -b 48 --lr 0.0003 -d 0.2 --from-pretrained model_cache
=======
poetry run train -ga 1 -mp -e 1 --device $device -b 40 --lr 0.0003 -d 0.0 --from-pretrained model_cache
>>>>>>> Stashed changes
