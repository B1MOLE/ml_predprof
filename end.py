import tensorflow as tf
from keras.layers import TextVectorization
from keras import layers

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

def run():

    batch_size = 32
    raw_train_ds = tf.keras.utils.text_dataset_from_directory(
        "archive_full",
        label_mode='categorical',
        batch_size=batch_size,
        validation_split=0.01,
        subset="training",
        seed=1337,
    )

    raw_val_ds = tf.keras.utils.text_dataset_from_directory(
        "archive",
        label_mode='categorical',
        batch_size=batch_size,
        validation_split=0.01,
        subset="validation",
        seed=1337,
    )

    raw_test_ds = tf.keras.utils.text_dataset_from_directory(
        "test2",
        label_mode='categorical',
        batch_size=batch_size,
        validation_split=0.99,
        subset="validation",
        seed=1337,
    )

    max_features = 10000
    embedding_dim = 512
    sequence_length = 6000

    vectorize_layer = TextVectorization(
        max_tokens=max_features,
        output_mode="int",
        output_sequence_length=sequence_length,
    )

    adapt_ds = raw_train_ds.map(lambda x, y: x)

    vectorize_layer.adapt(adapt_ds)

    def vectorize_text(text, label):
        text = tf.expand_dims(text, -1)
        return vectorize_layer(text), label

    train_ds = raw_train_ds.map(vectorize_text)
    val_ds = raw_val_ds.map(vectorize_text)
    test_ds = raw_test_ds.map(vectorize_text)

    train_ds = train_ds.cache().prefetch(buffer_size=32)
    # val_ds = val_ds.cache().prefetch(buffer_size=14)
    test_ds = test_ds.cache().prefetch(buffer_size=32)

    # Create the model
    model = tf.keras.Sequential()
    model.add(layers.Embedding(max_features, embedding_dim, input_length=sequence_length))
    # model.add(layers.Dropout(0.3))
    model.add(layers.Dense(128, activation='relu'))
    # model.add(layers.Conv1D(64, 5, activation='relu'))
    model.add(layers.GlobalMaxPooling1D())
    model.add(layers.Dense(6, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(train_ds, epochs=4, validation_data=test_ds)

    # test_loss, test_acc = model.evaluate(test_ds)
    # print(f"Test Loss: {test_loss}, Test Accuracy: {test_acc}")

    # A string input
    inputs = tf.keras.Input(shape=(1,), dtype="string")
    # Turn strings into vocab indices
    indices = vectorize_layer(inputs)
    # Turn vocab indices into predictions
    outputs = model(indices)

    # Our end to end model
    end_to_end_model = tf.keras.Model(inputs, outputs)
    end_to_end_model.compile(
        loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )

    end_to_end_model.save("here/")

    # Test it with `raw_test_ds`, which yields raw strings
    # raw_test_ds = raw_test_ds.map(lambda x, y: x)
    # test_loss, test_acc = end_to_end_model.evaluate(raw_test_ds)
    # print(f"Test Loss: {test_loss}, Test Accuracy: {test_acc}")
