from random import randint
# for i in range(9):
#     print(90 + 50 * i)

platform_y = [[390, 440, 490], [240, 290, 340], [90, 140, 190]]
colour = ["GREEN", "BLUE", "RED"]

platform_variant = randint(0, 3)
platform = f"{colour[platform_variant]} {platform_y[platform_variant][randint(0, 2)]}"
print(platform)