from keras import backend as K
from keras.models import Model
from keras.layers import (BatchNormalization, Conv1D, Dense, Input,
                          TimeDistributed, Activation, Bidirectional, SimpleRNN, GRU, LSTM, MaxPooling1D, Dropout)


def simple_rnn_model(input_dim, output_dim=29):
    """ Build a recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(output_dim, return_sequences=True,
                   implementation=2, name='rnn')(input_data)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(simp_rnn)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def rnn_model(input_dim, units, activation, output_dim=29):
    """ Build a recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(units, activation=activation,
                   return_sequences=True, implementation=2, name='rnn')(input_data)
    # Add batch normalization 
    bn_rnn = BatchNormalization(axis=-1)(simp_rnn)
    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def cnn_rnn_model(input_dim, filters, kernel_size, conv_stride,
                  conv_border_mode, units, output_dim=29):
    """ Build a recurrent + convolutional network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add convolutional layer
    conv_1d = Conv1D(filters, kernel_size,
                     strides=conv_stride,
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d')(input_data)
    # Add batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)
    # Add a recurrent layer
    rnn = GRU(units, activation='relu',
              return_sequences=True, implementation=2, dropout=0.2, name='rnn')(bn_cnn)
    # Add batch normalization
    bn_rnn = BatchNormalization(axis=-1)(rnn)
    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())
    return model


def cnn_output_length(input_length, filter_size, border_mode, stride,
                      dilation=1, pooling=1):
    """ Compute the length of the output sequence after 1D convolution along
        time. Note that this function is in line with the function used in
        Convolution1D class from Keras.
    Params:
        input_length (int): Length of the input sequence.
        filter_size (int): Width of the convolution kernel.
        border_mode (str): Only support `same` or `valid`.
        stride (int): Stride size used in 1D convolution.
        dilation (int)
    """
    if input_length is None:
        return None
    assert border_mode in {'same', 'valid', 'causal'}
    dilated_filter_size = filter_size + (filter_size - 1) * (dilation - 1)
    if border_mode == 'same':
        output_length = input_length
    elif border_mode == 'causal':
        output_length = input_length
    elif border_mode == 'valid':
        output_length = input_length - dilated_filter_size + 1
    return (output_length + stride - 1) // (stride * pooling)


def deep_rnn_model(input_dim, units, recur_layers, output_dim=29):
    """ Build a deep recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layers, each with batch normalization

    layer = input_data
    for i in range(recur_aleyers):
        rnn = GRU(units, activation='relu',
                  return_sequences=True, implementation=2, dropout=0.1, name=''.join('rnn', str(i)))(layer)
        layer = BatchNormalization(axis=-1)(rnn)

    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(layer)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def bidirectional_rnn_model(input_dim, units, output_dim=29):
    """ Build a bidirectional recurrent network for speech
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add bidirectional recurrent layer
    bidir_rnn = Bidirectional(GRU(units, activation='relu',
                                  return_sequences=True, implementation=2, dropout=0.2, name='rnn2'),
                              merge_mode='concat')(input_data)
    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bidir_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def extra_model(input_dim, units, recur_layers, output_dim=29):
    """ Build a deep bidirectional recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layers, each with batch normalization

    layer = input_data
    for i in range(recur_layers):
        bidir_rnn = Bidirectional(GRU(units, activation='relu',
                                      return_sequences=True, implementation=2, dropout=0.1,
                                      name=''.join(['rnn', str(i)])), merge_mode='concat')(layer)
        layer = BatchNormalization(axis=-1)(bidir_rnn)

    # Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(layer)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def final_model(input_dim, filters, kernel_size, conv_stride,
                conv_border_mode, units, recur_layers, maxpool, output_dim=29):
    """ Build a deep network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Specify the layers in your network

    #     next_layer = input_data
    conv_1d = Conv1D(filters, kernel_size,
                     strides=conv_stride,
                     padding=conv_border_mode,
                     activation='relu',
                     name='cnn')(input_data)
    bn_layer = BatchNormalization(name='bn_cnn')(conv_1d)
    max_pool_cnn = MaxPooling1D(maxpool, name='max_pool_cnn')(bn_layer)
    next_layer = Dropout(0.3, name='dropout_cnn')(max_pool_cnn)

    #     next_layer = bn_layer

    for i in range(recur_layers):
        bidir_rnn = Bidirectional(GRU(units,
                                      activation='relu',
                                      return_sequences=True,
                                      implementation=2,
                                      #                                       dropout=0.2,
                                      name='_'.join(['bidir_rnn', str(i)]),
                                      #                                       dropout_W=0.3, # input units to drop for input gates
                                      dropout_U=0.3),  # input units to drop for recurrent connections
                                  merge_mode='concat')(next_layer)

        bn_layer = BatchNormalization(axis=-1)(bidir_rnn)
        next_layer = Dropout(0.3, name='_'.join(['dropout_bidir_rnn', str(i)]))(bn_layer)

    time_dense = TimeDistributed(Dense(output_dim))(next_layer)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    # Specify model.output_length
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride, pooling=maxpool)
    print(model.summary())
    return model
