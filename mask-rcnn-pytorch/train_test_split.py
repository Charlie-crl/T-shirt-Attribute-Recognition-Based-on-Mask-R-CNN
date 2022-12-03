import os
import random
import time
from shutil import copyfile
import shutil

def img_train_test_split(img_source_dir, train_size):
    """
    Randomly splits images over a train and validation folder, while preserving the folder structure

    Parameters
    ----------
    img_source_dir : string
        Path to the folder with the images to be split. Can be absolute or relative path

    train_size : float
        Proportion of the original images that need to be copied in the subdirectory in the train folder
    """
    if not (isinstance(img_source_dir, str)):
        raise AttributeError('img_source_dir must be a string')

    if not os.path.exists(img_source_dir):
        raise OSError('img_source_dir does not exist')

    if not (isinstance(train_size, float)):
        raise AttributeError('train_size must be a float')

    train_dir = img_source_dir + '\\train'
    val_dir = img_source_dir + '\\val'

    # Set up empty folder structure if not exists

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    train_counter = 0
    val_counter = 0

    # Randomly assign an image to train or validation folder
    # 针对labelme2coco，只需要分割json文件
    for filename in os.listdir(img_source_dir):
        # my images are end up with ".jpg" ## filename.endswith(".jpg") or filename.endswith(".png")
        if filename.endswith(".jpg"):
            fileparts = filename.split('.')
            json_file = fileparts[0] + '.' + 'json'

            if random.uniform(0, 1) <= train_size:
                # copyfile(os.path.join(img_source_dir, filename),
                #          os.path.join(train_dir, str(train_counter) + '.' + fileparts[1]))
                copyfile(os.path.join(img_source_dir, json_file),
                         os.path.join(train_dir, str(train_counter) + '.' + 'json'))
                train_counter += 1

            else:
                # copyfile(os.path.join(img_source_dir, filename),
                #          os.path.join(val_dir, str(val_counter) + '.' + fileparts[1]))
                copyfile(os.path.join(img_source_dir, json_file),
                         os.path.join(val_dir, str(val_counter) + '.' + 'json'))
                val_counter += 1

    print('Copied ' + str(train_counter) + ' images to ' + train_dir)
    print('Copied ' + str(val_counter) + ' images to ' + val_dir)

def cal_classes_balance(origin_data_dir,dir_name):
    """
    统计标签类别种类数与个数,如果val或train类别不包含12，则重新分类
    """
    import json

    classes_dict = {}
    for json_name in os.listdir(os.path.join(origin_data_dir, dir_name)):
        with open(os.path.join(os.path.join(origin_data_dir, dir_name), json_name), 'r', encoding='utf8') as fp:
            dict_data = json.load(fp)
            shapes_list = dict_data['shapes']
            for label_dict in shapes_list:
                if label_dict["label"] not in classes_dict:
                    classes_dict[label_dict["label"]] = [[1], [os.path.join(dir_name, json_name)]]
                else:
                    classes_dict[label_dict["label"]][0][0] += 1

    print(dir_name + " number:  ", len(classes_dict))
    return len(classes_dict)


if __name__ == '__main__':
    origin_data_dir = './origin_img_small'
    train_dir = './train'
    val_dir = './val'
    while True:
        img_train_test_split(origin_data_dir, 0.8)
        train_classes_num = cal_classes_balance(origin_data_dir,train_dir)
        val_classes_num = cal_classes_balance(origin_data_dir,val_dir)
        if train_classes_num == 12 and val_classes_num == 12:
            print("success!")
            break
        else:
            # 如果不满足则删除。本项目是小数据集才会这样
            shutil.rmtree(os.path.join(origin_data_dir,train_dir))
            shutil.rmtree(os.path.join(origin_data_dir, val_dir))
            print("next one ->")
