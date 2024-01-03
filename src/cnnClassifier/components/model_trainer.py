import os
from pathlib import Path
import sys

import tensorflow as tf

from cnnClassifier.entity.artifacts_entity import TrainingConfigArtifacts
from cnnClassifier.exception import CNNException
from cnnClassifier.logger import logger


class Training:
    def __init__(self, config: TrainingConfigArtifacts):
        self.config = config

    def get_base_model(self):
        logger.info("Entered the get_base_model method of Training class")
        try:
            logger.info(f"Updated model path: {self.config.updated_base_model_path}")
            logger.info(f"Current directory inside get_base_model method: {os.getcwd()}")
            self.model = tf.keras.models.load_model(self.config.updated_base_model_path)
            logger.info("Exited get_base_model method of Training class")
        except Exception as e:
            raise CNNException(e, sys) from e

    def train_valid_generator(self):
        logger.info("Entered the train_valid_generator method of Training class")
        try:
            datagenerator_kwargs = dict(rescale=1.0 / 255, validation_split=0.20)

            dataflow_kwargs = dict(
                target_size=self.config.params_image_size[:-1],
                batch_size=self.config.params_batch_size,
                interpolation="bilinear",
            )

            valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                **datagenerator_kwargs
            )

            self.valid_generator = valid_datagenerator.flow_from_directory(
                directory=self.config.training_data,
                subset="validation",
                shuffle=False,
                **dataflow_kwargs
            )

            if self.config.params_is_augmentation:
                train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                    rotation_range=40,
                    horizontal_flip=True,
                    width_shift_range=0.2,
                    height_shift_range=0.2,
                    shear_range=0.2,
                    zoom_range=0.2,
                    **datagenerator_kwargs
                )
            else:
                train_datagenerator = valid_datagenerator

            self.train_generator = train_datagenerator.flow_from_directory(
                directory=self.config.training_data,
                subset="training",
                shuffle=True,
                **dataflow_kwargs
            )

            logger.info("Exit train_valid_generator method of Training class")
        except Exception as e:
            raise CNNException(e, sys) from e
        
    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        logger.info("Entered the save_model method of Training class")
        try:
            model.save(path)
            logger.info("Exit the save_model method of Training class")
        except Exception as e:
            raise CNNException(e, sys) from e
        
        
    def train(self):
        logger.info("Entered the train method of Training class")
        try:
            self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
            self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

            self.model.fit(
                self.train_generator,
                epochs=self.config.params_epochs,
                steps_per_epoch=self.steps_per_epoch,
                validation_steps=self.validation_steps,
                validation_data=self.valid_generator
            )

            self.save_model(
                path=self.config.trained_model_path,
                model=self.model
            )
            
            logger.info("Exit the train method of Training class")
        except Exception as e:
            raise CNNException(e, sys) from e
