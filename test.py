# from random import randint
# # for i in range(9):
# #     print(90 + 50 * i)

# platform_y = [[390, 440, 490], [240, 290, 340], [90, 140, 190]]
# colour = ["GREEN", "BLUE", "RED"]

# platform_variant = randint(0, 3)
# platform = f"{colour[platform_variant]} {platform_y[platform_variant][randint(0, 2)]}"
# print(platform)

# import random

# # random.seed(7)

# p = ["#__", "_#_", "__#", "#_#"]
# # "#|||#|||#|||#"
# for i in range(100):
#     r1, r2, r3 = random.randint(0, 3), random.randint(0, 3), random.randint(0, 3)
#     print(f"{p[r1]}|{p[r2]}|{p[r3]}")



# screen = 500
# screen -= screen / 25
# section = screen / 10
# sec = []

# for i in range(10):
#     sec.append(i * section)

# platforms = [
#     [sec[1], sec[2], sec[3]],
#     [sec[4], sec[5], sec[6]],
#     [sec[7], sec[8], sec[9]]
# ]

# for range in platforms:
#     print(range)


# for i in range(1, 501):
#     print(500 // (i ** 0.5))

import random

score = 0

for i in range(1, 481):
    # points = random.randint(1, 481)
    # score += int((points ** 0.6))
    # print(f"{score} + {int((points ** 0.6))}, {points}")
    # score += int((i ** 0.5))
    # score += int(((i ** 1.119) - 50) / 1.8)
    print(f"{int(((i ** 1.119) - 50) / 1.9)}, {i}")