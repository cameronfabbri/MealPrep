import tensorflow as tf
import numpy as np
import cv2
import os


def main():

    os.makedirs('checkpoints', exist_ok=True)

    classes = os.listdir('data')

    num_classes = len(classes)

    data_dict = {}

    for i, folder in enumerate(classes):

        folder = os.path.join('data',folder)

        images = [os.path.join(folder, x) for x in os.listdir(folder)]

        for im in images:
            data_dict[im] = i


    train_len = len(list(data_dict.keys()))
    all_paths = np.asarray(list(data_dict.keys()))

    base_model = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
    base_model.trainable = False

    image_batch = tf.convert_to_tensor(cv2.imread(list(data_dict.keys())[0]), dtype=tf.float32)
    image_batch = tf.image.resize(image_batch, (224, 224))
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

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)

    checkpoint = tf.train.Checkpoint(model=model, optimizer=optimizer)
    manager = tf.train.CheckpointManager(checkpoint, directory='checkpoints/', max_to_keep=1)
    checkpoint.restore(manager.latest_checkpoint)

    def get_batch(batch_paths, batch_labels_):

        batch_images = []
        batch_labels = []

        for path, label in zip(batch_paths, batch_labels_):

            img = cv2.imread(path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = tf.convert_to_tensor(img, dtype=tf.float32)

            img = tf.image.random_flip_left_right(img)
            img = tf.image.random_flip_up_down(img)

            img = tf.image.resize(img, (224, 224))
            img = tf.keras.applications.vgg19.preprocess_input(img)
            img = tf.expand_dims(img, 0)

            label = tf.one_hot(label, num_classes)
            label = tf.expand_dims(label, 0)

            batch_labels.append(label)
            batch_images.append(img)

        batch_images = tf.concat(batch_images, axis=0)
        batch_labels = tf.concat(batch_labels, axis=0)
   
        return batch_images, batch_labels

    for step in range(1000):

        idx = np.random.choice(np.arange(train_len), 8, replace=False)

        batch_paths = all_paths[idx]
        batch_labels = []

        for p in batch_paths:
            batch_labels.append(data_dict[p])

        batch_images, batch_labels = get_batch(batch_paths, batch_labels)

        with tf.GradientTape() as tape:

            logits = model(batch_images)

            loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=batch_labels, logits=logits))

        gradients = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(gradients, model.trainable_variables))

        print(' | step:',step,'| loss:',loss.numpy())

        if step % 100 == 0:
            print('\nSaving model...')
            manager.save()
            print('Saved')

    manager.save()

if __name__ == '__main__':
    main()
