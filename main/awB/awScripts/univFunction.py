# -*- coding: utf-8 -*-

import json
import random


def randomName(gender="male"):
    """随机生成一个英文姓名。

    Args:
        gender: "male" 或 "female"，默认为 "male"

    Returns:
        "名 姓" 格式的字符串，如 "John Smith"；gender 无效时返回 False
    """
    firstNameMale = [
            'Brian', 'Charles', 'Christopher', 'Daniel', 'David', 'Edward',
            'George', 'James', 'John', 'Joseph', 'Kenneth', 'Mark', 'Michael',
            'Paul', 'Peter', 'Richard', 'Robert', 'Ronald', 'Steven', 'Thomas',
            'William',
            ]
    firstNameFemale = [
            'Ashley', 'Barbara', 'Betty', 'Donna', 'Dorothy', 'Elizabeth',
            'Emily', 'Jennifer', 'Jessica', 'Karen', 'Kimberly', 'Linda',
            'Lisa', 'Louise', 'Margaret', 'Mary', 'Meg', 'Nancy', 'Patricia',
            'Sandra', 'Sarah', 'Susan',
            ]
    lastName = [
            'Anderson', 'Brown', 'Davis', 'Garcia', 'Griffin', 'Hernandez',
            'Jackson', 'Johnson', 'Jones', 'Martin', 'Martinez', 'Miller',
            'Moore', 'Rodriguez', 'Smith', 'Taylor', 'Thomas', 'Thompson',
            'White', 'Williams', 'Wilson',
            ]

    if gender == "male":
        return random.choice(firstNameMale) + " " + random.choice(lastName)
    elif gender == "female":
        return random.choice(firstNameFemale) + " " + random.choice(lastName)
    else:
        return False


def arraySort(array):
    """按自定义字符权重对字符串列表排序，返回 JSON 字符串。

    排序规则：数字 0-9 → 大写 A-Z → 小写 a-z，同位置逐字符比较。
    """
    weight = {ch: idx for idx, ch in enumerate(
            "0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
            )}

    def sort_key(name):
        return [weight[ch] for ch in name]

    sorted_array = sorted(array, key=sort_key)
    return json.dumps(sorted_array)


def compare_versions(version1, version2):
    """比较两个语义化版本号。

    Returns:
        1  表示 version1 更新
        -1 表示 version2 更新
        0  表示版本相同
    """
    v1 = list(map(int, version1.split('.')))
    v2 = list(map(int, version2.split('.')))

    # 补齐较短版本号的缺位
    max_length = max(len(v1), len(v2))
    v1 += [0] * (max_length - len(v1))
    v2 += [0] * (max_length - len(v2))

    for a, b in zip(v1, v2):
        if a > b:
            return 1
        elif a < b:
            return -1
    return 0


# ============================================================
# AW 模组数据与工具函数
# ============================================================

AW_NAMESPACE = "aw"
AW_CAMPS = ["bandit", "desert", "native", "pirate", "player", "viking"]
AW_CAMPS_CN = ["土匪", "沙漠", "帝国", "海盗", "新星", "纳维亚海盗"]
AW_TYPES = [
        "archer", "archer_horse", "axeman", "axeman_pro", "general",
        "general_horse", "lance", "soldier", "soldier_horse",
        ]
AW_TYPES_CN = ["弓箭手", "游骑兵", "斧兵", "重斧兵", "首领", "铁骑", "矛兵", "战士", "骑兵"]


def getCampIndex(name):
    """根据阵营英文名返回索引，未找到返回 None"""
    try:
        return AW_CAMPS.index(name)
    except ValueError:
        return None


def getCampCN(name):
    """根据阵营英文名返回中文名，未找到返回 None"""
    idx = getCampIndex(name)
    if idx is not None:
        return AW_CAMPS_CN[idx]
    return None


def getTypeIndex(name):
    """根据兵种英文名返回索引，未找到返回 None"""
    try:
        return AW_TYPES.index(name)
    except ValueError:
        return None


def getTypeCN(name):
    """根据兵种英文名返回中文名，未找到返回 None"""
    idx = getTypeIndex(name)
    if idx is not None:
        return AW_TYPES_CN[idx]
    return None


def isAWEntity(identifier):
    """判断标识符是否属于 AW 模组实体"""
    return parseAWIdentifier(identifier) is not None


def parseAWIdentifier(identifier):
    """解析 AW 实体标识符，返回 {namespace, camp, type} 或 None。

    兼容两种格式：
      - aw:bandit_soldier
      - aw:old_bandit_soldier
    """
    parts = identifier.split(":")
    if len(parts) != 2:
        return None

    namespace, rest = parts
    if namespace not in (AW_NAMESPACE,):
        return None

    # 拆分 camp 和 type
    segments = rest.split("_", 1)
    if len(segments) != 2:
        return None

    first, second = segments
    if first == "old":
        # aw:old_{camp}_{type}
        sub = second.split("_", 1)
        if len(sub) != 2:
            return None
        camp, etype = sub
    else:
        # aw:{camp}_{type}
        camp, etype = first, second

    if camp not in AW_CAMPS:
        return None
    if etype not in AW_TYPES:
        return None

    return {
            "namespace": namespace,
            "camp": camp,
            "type": etype
            }


def buildAWIdentifier(camp, etype):
    """根据阵营和兵种英文名构建 AW 实体标识符。

    Example:
        buildAWIdentifier('bandit', 'soldier') → 'aw:bandit_soldier'
    """
    return "{}:{}_{}".format(AW_NAMESPACE, camp, etype)
