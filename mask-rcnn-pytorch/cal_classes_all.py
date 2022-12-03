"""
统计标签类别种类数与个数
"""
import os
import json

classes_dict = {}
origin_data_dir = './origin_img_small'
train_dir = './train'
val_dir = './val'

for dir_name in os.listdir(origin_data_dir):
    for json_name in os.listdir(os.path.join(origin_data_dir, dir_name)):
        with open(os.path.join(os.path.join(origin_data_dir, dir_name), json_name), 'r', encoding='utf8') as fp:
            dict_data = json.load(fp)
            shapes_list = dict_data['shapes']
            for label_dict in shapes_list:
                if label_dict["label"] not in classes_dict:
                    classes_dict[label_dict["label"]] = [[1], [os.path.join(dir_name, json_name)]]
                else:
                    classes_dict[label_dict["label"]][0][0] += 1
                    classes_dict[label_dict["label"]][1].append(os.path.join(dir_name, json_name))

print(classes_dict)
print(len(classes_dict))
with open('./cal_classes_all.json', 'w', encoding='utf8') as fp:
    json.dump(classes_dict, fp, ensure_ascii=False)
