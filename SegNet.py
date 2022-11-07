import tensorflow as tf
from tensorflow import keras
from tqdm import tqdm
import numpy as np
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.python.keras import layers as KL
from tensorflow.python.keras import engine as KE


IMAGE_ORDERING = 'channels_last'

class BatchNorm(KL.BatchNormalization):
    def call(self, inputs, training=None):
        return super(self.__class__, self).call(inputs, training=training)


def encoder_layer(input_tensor, train_bn): ## VGG 16 architecture
    x = KL.Conv2D(64, (3, 3), padding='same', name='encoder_block_1_conv1')(input_tensor)
    x = BatchNorm(name='encoder_block_1_conv1_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    x = KL.Conv2D(64, (3, 3), padding='same', name='encoder_block_1_conv2')(x)
    x = BatchNorm(name='encoder_block_1_conv2_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    f1 = x = KL.MaxPooling2D((2, 2), strides=(2, 2), name='block_1_pool')(x)
    ##############################################
    #                                            #
    #                  block 1                   #
    #                                            #
    ##############################################
    
    
    x = KL.Conv2D(128, (3, 3), padding='same', name='encoder_block_2_conv1')(x)
    x = BatchNorm(name='encoder_block_2_conv1_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    x = KL.Conv2D(128, (3, 3), padding='same', name='encoder_block_2_conv2')(x)
    x = BatchNorm(name='encoder_block_2_conv2_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    f2 = x = KL.MaxPooling2D((2, 2), strides=(2, 2), name='block_2_pool')(x)
    ##############################################
    #                                            #
    #                  block 2                   #
    #                                            #
    ##############################################
    
    
    x = KL.Conv2D(256, (3, 3), padding='same', name='encoder_block_3_conv1')(x)
    x = BatchNorm(name='encoder_block_3_conv1_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    x = KL.Conv2D(256, (3, 3), padding='same', name='encoder_block_3_conv2')(x)
    x = BatchNorm(name='encoder_block_3_conv2_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    x = KL.Conv2D(256, (3, 3), padding='same', name='encoder_block_3_conv3')(x)
    x = BatchNorm(name='encoder_block_3_conv3_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    f3 = x = KL.MaxPooling2D((2, 2), strides=(2, 2), name='block_3_pool')(x)
    ##############################################
    #                                            #
    #                  block 3                   #
    #                                            #
    ##############################################
    
    
    x = KL.Conv2D(512, (3, 3), padding='same', name='encoder_block_4_conv1')(x)
    x = BatchNorm(name='encoder_block_4_conv1_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    x = KL.Conv2D(512, (3, 3), padding='same', name='encoder_block_4_conv2')(x)
    x = BatchNorm(name='encoder_block_4_conv2_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    x = KL.Conv2D(512, (3, 3), padding='same', name='encoder_block_4_conv3')(x)
    x = BatchNorm(name='encoder_block_4_conv3_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    f4 = x = KL.MaxPooling2D((2, 2), strides=(2, 2), name='block_4_pool')(x)
    ##############################################
    #                                            #
    #                  block 4                   #
    #                                            #
    ##############################################
    
    
    x = KL.Conv2D(512, (3, 3), padding='same', name='encoder_block_5_conv1')(x)
    x = BatchNorm(name='encoder_block_5_conv1_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    x = KL.Conv2D(512, (3, 3), padding='same', name='encoder_block_5_conv2')(x)
    x = BatchNorm(name='encoder_block_5_conv2_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    
    x = KL.Conv2D(512, (3, 3), padding='same', name='encoder_block_5_conv3')(x)
    x = BatchNorm(name='encoder_block_5_conv3_bn')(x, training = train_bn)
    x = KL.Activation('relu')(x)
    f5 = x = KL.MaxPooling2D((2, 2), strides=(2, 2), name='block_5_pool')(x)
    ##############################################
    #                                            #
    #                  block 5                   #
    #                                            #
    ##############################################
    return [f1, f2, f3, f4, f5]
    
    

def decoder_layer(input_tensor, n_classes, n_upsample=3):
    x = KL.ZeroPadding2D(padding=(1, 1), data_format=IMAGE_ORDERING)(input_tensor)
    x = KL.Conv2D(512, (3, 3), name='decoder_conv1', padding='valid', data_format=IMAGE_ORDERING)(x)
    x = BatchNorm(name='decoder_conv1_bn')(x)
    
    x = KL.UpSampling2D((2, 2), data_format=IMAGE_ORDERING)(x)
    x = KL.ZeroPadding2D(padding=(1, 1), data_format=IMAGE_ORDERING)(x)
    x = KL.Conv2D(256, (3, 3), name='decoder_conv2', padding='valid', data_format=IMAGE_ORDERING)(x)
    x = BatchNorm(name='decoder_conv2_bn')(x)
    
    
    for _ in range(n_upsample-2):
        x = KL.UpSampling2D((2, 2), data_format=IMAGE_ORDERING)(x)
        x = KL.ZeroPadding2D(padding=(1, 1), data_format=IMAGE_ORDERING)(x)
        x = KL.Conv2D(128, (3, 3), padding='valid', data_format=IMAGE_ORDERING)(x)
        x = BatchNorm()(x)
    
    x = KL.UpSampling2D((2, 2))(x)
    x = KL.ZeroPadding2D(padding=(1, 1))(x)
    x = KL.Conv2D(64, (3, 3), name='decoder_conv4', padding='valid', data_format=IMAGE_ORDERING)(x)
    x = BatchNorm(name='decoder_conv4_bn')(x)
    
    x = KL.Conv2D(n_classes, (3, 3), name='decoder_conv_output', padding='same', data_format=IMAGE_ORDERING)(x)
    
    return x


def model_setting(height, width, n_classes):
    #height = 256
    #width = 256
    input_shape = keras.Input((height, width, 3))
    feature_maps = encoder_layer(input_shape, True)
    x = decoder_layer(feature_maps[3], n_classes, 3)
    x = tf.reshape(x, (-1, int(height/2), int(width/2), n_classes))
    x = KL.Activation('softmax')(x)
    
    model = Model(inputs = input_shape, outputs = x, name='SegNet')
    return model


def main():
    print('hello python!!!')
    
    model = model_Setting()
    #model=keras.Sequential()
    #model.add(conv_base)
    #model = Model(inputs = input_shape, outputs=x, name='dcnn')
    model.summary()

if __name__ == '__main__':
    main()