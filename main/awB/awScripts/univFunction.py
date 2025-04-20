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


if __name__ == "__main__":
    pass
