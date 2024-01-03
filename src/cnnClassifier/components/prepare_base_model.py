import os
import sys
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from pathlib import Path

from cnnClassifier.entity.artifacts_entity import DataIngestionArtifacts, PrepareBaseModelArtifacts
from cnnClassifier.entity.config_entity import PrepareBaseModelConfig
from cnnClassifier.exception import CNNException
from cnnClassifier.logger import logger
from cnnClassifier.utils.common import create_directories


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.model = None
        self.full_model = None
        self.config = config

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    def get_base_model(self):
        """_summary_

        Raises:
            CNNException: _description_
        """
        logger.info("Entered the get_base_model method of prepare base model class")

        try:
            self.model = tf.keras.applications.vgg16.VGG16(
                input_shape=self.config.params_image_size,
                weights=self.config.params_weights,
                include_top=self.config.params_include_top,
            )
            logger.info("Save base model")
            self.save_model(
                path=self.config.base_model_path, model=self.model
            )
        except Exception as e:
            raise CNNException(e, sys) from e

    def update_base_model(self):
        logger.info("Updating base model")
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=False,
            learning_rate=self.config.params_learning_rate,
        )

        logger.info("Updated base model")
        self.save_model(
            path=self.config.updated_base_model_path,
            model=self.full_model,
        )

    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        """_summary_

        Args:
            model (_type_): _description_
            classes (_type_): _description_
            freeze_all (_type_): _description_
            freeze_till (_type_): _description_
            learning_rate (_type_): _description_

        Returns:
            _type_: _description_
        """        
        logger.info("Preparing full model")
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False

        flatten_in = tf.keras.layers.Flatten()(model.output)
        prediction = tf.keras.layers.Dense(units=classes, activation="softmax")(
            flatten_in
        )

        full_model = tf.keras.models.Model(inputs=model.input, outputs=prediction)

        full_model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"],
        )

        full_model.summary()
        logger.info("Full Model summary")
        return full_model
    

