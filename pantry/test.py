import tensorflow as tf
import numpy as np
import cv2
import sys
import os


def main():

    classes = os.listdir('data')
    num_classes = len(classes)
    data_dict = {}
    class_dict = {}
    for i, folder in enumerate(classes):
        class_dict[i] = folder


    base_model = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
    base_model.trainable = False
    image_batch = tf.random.normal((224, 224, 3), dtype=tf.float32)
    image_batch = tf.expand_dims(image_batch, 0)
    feature_batch = base_model(image_batch)
    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    feature_batch_average = global_average_layer(feature_batch)
    prediction_layer = tf.keras.layers.Dense(num_classes)
    prediction_batch = prediction_layer(feature_batch_average)

    model = tf.keras.Sequential([
      base_model,
      global_average_layer,
      prediction_layer
    ])

    checkpoint = tf.train.Checkpoint(model=model)
    manager = tf.train.CheckpointManager(checkpoint, directory='checkpoints/', max_to_keep=1)
    checkpoint.restore(manager.latest_checkpoint).expect_partial()

    image_path = sys.argv[1]

    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = tf.convert_to_tensor(img, dtype=tf.float32)

    img = tf.image.resize(img, (224, 224))
    img = tf.keras.applications.vgg19.preprocess_input(img)
    img = tf.expand_dims(img, 0)

    logits = tf.nn.sigmoid(model(img).numpy())

    print(logits)
    print(np.argmax(logits))
    print(class_dict[np.argmax(logits)])

if __name__ == '__main__':
    main()
