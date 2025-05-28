# -*- coding: utf-8 -*-

import json
import random


def randomName(gender="male"):
    firstNameMale = ['Brian', 'Charles', 'Christopher', 'Daniel', 'David', 'Edward', 'George', 'James', 'John', 'Joseph', 'Kenneth', 'Mark', 'Michael', 'Paul', 'Peter', 'Richard', 'Robert', 'Ronald', 'Steven', 'Thomas', 'William']
    firstNameFemale = ["Ashley", "Barbara", "Betty", "Donna", "Dorothy", "Elizabeth", "Emily", "Jennifer", "Jessica", "Karen", "Kimberly", "Linda", "Lisa", "Louise", "Margaret", "Mary", "Meg", "Nancy", "Patricia", "Sandra", "Sarah", "Susan"]
    lastName = ['Anderson', 'Brown', 'Davis', 'Garcia', 'Griffin', 'Hernandez', 'Jackson', 'Johnson', 'Jones', 'Martin', 'Martinez', 'Miller', 'Moore', 'Rodriguez', 'Smith', 'Taylor', 'Thomas', 'Thompson', 'White', 'Williams', 'Wilson']
    if gender == "male":
        return firstNameMale[random.randint(0, len(firstNameMale) - 1)] + " " + lastName[random.randint(0, len(lastName) - 1)]
    elif gender == "female":
        return firstNameFemale[random.randint(0, len(firstNameFemale) - 1)] + " " + lastName[random.randint(0, len(lastName) - 1)]
    else:
        return False


def arraySort(array):
    weight = {ch: idx for idx, ch in enumerate("0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")}

    def sort_key(name):
        return [weight[ch] for ch in name]

    sorted_array = sorted(array, key=sort_key)
    return json.dumps(sorted_array)


def compare_versions(version1, version2):
    """
    1 表示第一个版本更新
    -1 表示第二个版本更新
    0 表示版本相同
    """
    # 将版本号分割为数字列表
    v1 = list(map(int, version1.split('.')))
    v2 = list(map(int, version2.split('.')))

    # 确定最大长度并填充0
    max_length = max(len(v1), len(v2))
    v1 += [0] * (max_length - len(v1))
    v2 += [0] * (max_length - len(v2))

    # 逐位比较版本号
    for a, b in zip(v1, v2):
        if a > b:
            return 1
        elif a < b:
            return -1
    return 0


if __name__ == "__main__":
    pass
