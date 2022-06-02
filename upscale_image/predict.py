from pathlib import Path

import cv2
import numpy as np
from keras_preprocessing.image import array_to_img
from fastapi import UploadFile
from tensorflow import keras


class Predict:
    SIZE = 256
    img = None

    def __init__(self, file: UploadFile, base_path: Path):
        self.file = file
        self.file_location = f"{base_path}/static/images/source.png"
        self.model_path = f"{base_path}/model.h5"
        self.result_path = f'{base_path}/static/images/result.png'

    def save_image(self) -> None:
        extension = self.file.filename.split(".")[-1] in ("jpg", "jpeg", "png")

        if not extension:
            raise ValueError("Image must be in jpg or png format")

        with open(self.file_location, "wb+") as file_object:
            file_object.write(self.file.file.read())

    def _prepare_image(self) -> None:
        img = cv2.imread(self.file_location, 1)
        img = cv2.resize(img, (self.SIZE, self.SIZE))
        self.img = img.astype('float32') / 255.0

    def save_predict(self):
        self._prepare_image()
        loaded_model = keras.models.load_model(self.model_path)

        predicted = np.clip(loaded_model.predict(
            self.img.reshape(1, self.SIZE, self.SIZE, 3)
        ), 0.0, 1.0).reshape(self.SIZE, self.SIZE, 3)

        self.img = array_to_img(predicted)
        self._save_image()

    def _save_image(self):
        self.img.save(self.result_path)
