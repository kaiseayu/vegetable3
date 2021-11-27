from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras.optimizers import SGD
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

n_categories=5
batch_size=32
train_dir='vegetable_images/train'
validation_dir='vegetable_images/validation'
test_dir='vegetable_images/test'
file_name='vgg16_vegetable_name'

ClassNames=['キャベツ', 'ニンジン', 'レモン', 'タマネギ', 'カブ']

SAVE_DATA_DIR_PATH = './model'

#VGG16のモデルをインポート(include_top=Falseで全結合層を除く)
base_model=VGG16(weights='imagenet',include_top=False,
                 input_tensor=Input(shape=(224,224,3)))

#新しく全結合層を取り付ける
x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x)
prediction=Dense(n_categories,activation='softmax')(x)
#一連の層をモデルとしてまとめる
model=Model(inputs=base_model.input,outputs=prediction)

#14層目までの重みを更新しない
for layer in base_model.layers[:15]:
    layer.trainable=False

#学習プロセスの設定
model.compile(optimizer=SGD(lr=0.0001,momentum=0.9),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
#モデルの要約を出力
model.summary()

#trainデータを正規化、ランダムにシアー変換・ズーム・反転
train_datagen=ImageDataGenerator(
    rescale=1.0/255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

#validationデータを正規化
validation_datagen=ImageDataGenerator(rescale=1.0/255)

#ディレクトリへのパス(train_dir)を受け取り、拡張・正規化したtrainデータのバッチを生成
train_generator=train_datagen.flow_from_directory(
    train_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)
#ディレクトリへのパス(validation_dir)を受け取り、正規化したvalidationデータのバッチを生成
validation_generator=validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

#学習開始(バッチサイズ32, エポック10)
hist=model.fit(x=train_generator,
                epochs=30,
                verbose=1,
                validation_data=validation_generator,
                callbacks=[CSVLogger(file_name+'.csv')])

#モデル構造, 野菜の名前の保存
json_string=model.to_json()
json_string+='##########' + str(ClassNames)
open(file_name + 'model.json',"w").write(json_string)
#モデルの重みの保存
model.save(file_name+'weight.h5')

#testデータの前処理
test_datagen=ImageDataGenerator(rescale=1.0/255)
test_generator=test_datagen.flow_from_directory(
    test_dir,
    target_size=(224,224),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

#モデルの評価
score=model.evaluate_generator(test_generator)
print('\n test loss:',score[0])
print('\n test_acc:',score[1])