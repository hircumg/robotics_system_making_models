import time
import numpy as np
import random
np.random.seed(int(time.time()))
max_boxes_per_color = 9
shortcuts = {'Y': 'Yellow', 'B': "Blue", 'G': "Green", 'b': 'Black', 'R': 'Red'}
print(f"Сокращения: {shortcuts}")
for att in range(2):
    # Y -- yellow
    # B -- Blue
    # G -- Green
    # b -- Black
    # R -- Red
    colors = ['Y', 'B', 'G', 'b', 'R']
    max_boxes = 28

    ind = np.random.randint(0, len(colors))
    four_boxes = colors[ind]
    del colors[ind]


    ind = np.random.randint(0, len(colors))
    five_boxes = colors[ind]
    del colors[ind]


    max_boxes = max_boxes - 4 - 5

    elements = []
    el = np.random.randint(1, max_boxes_per_color-2+1)
    el = el if el < 4 else el + 2

    elements.append(el)
    max_boxes -= el
    el = np.random.randint(max_boxes-max_boxes_per_color-2, max_boxes_per_color-2+1)
    el = el if el < 4 else el + 2
    elements.append(el)
    max_boxes -= el

    elements.append(max_boxes)
    bag = []
    print(f"\nПопытка: {att+1}")
    for _ in range(4):
        bag.append(four_boxes)
    print(f"4 кубика цвета {shortcuts[four_boxes]}")
    for _ in range(5):
        bag.append(five_boxes)
    print(f"5 кубиков цвета {shortcuts[five_boxes]}")
    for i in range(3):
        print(f"{elements[i]} кубиков(а) цвета {shortcuts[colors[i]]}")
        for _ in range(elements[i]):
            bag.append(colors[i])

    random.shuffle(bag)
    print(f"Finish:{bag}:Start")