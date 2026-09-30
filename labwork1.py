"""Completed solutions for Lab Session 1: Python Basics."""


PI = 3.14


def calculate_circle_area(radius):
    return PI * radius * radius


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def is_prime(number):
    if number < 2:
        return False
    for divisor in range(2, number):
        if number % divisor == 0:
            return False
    return True


def is_perfect(number):
    if number < 2:
        return False
    total = 0
    for divisor in range(1, number):
        if number % divisor == 0:
            total += divisor
    return total == number


def find_color(colors, favorite_color):
    if favorite_color in colors:
        return colors.index(favorite_color)
    return -1


def create_ranges():
    range1 = list(range(7))
    range2 = list(range(1, 11, 3))
    range3 = list(range(5, 0, -1))
    range4 = list(range(6, -3, -2))
    return range1, range2, range3, range4


def remove_dollar_sign(s):
    result = ""
    for character in s:
        if character != "$":
            result += character
    return result


def extract_even(l):
    even_numbers = []
    for number in l:
        if number % 2 == 0:
            even_numbers.append(number)
    return even_numbers


def factorial(number):
    if number < 0:
        raise ValueError("Factorial is only defined for non-negative integers")
    result = 1
    for value in range(1, number + 1):
        result *= value
    return result


def get_divisors(number):
    if number == 0:
        raise ValueError("Zero has infinitely many divisors")
    positive_number = abs(number)
    divisors = []
    for value in range(1, positive_number + 1):
        if positive_number % value == 0:
            divisors.append(value)
    return divisors


def distance_between_points(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def create_pattern(m, n):
    if m <= 0 or n <= 0:
        return ""

    rows = []
    for row in range(m):
        if row == 0 or row == m - 1:
            rows.append(" ".join(["*"] * n))
        elif n == 1:
            rows.append("*")
        else:
            rows.append("*" + " " * (2 * n - 3) + "*")
    return "\n".join(rows)


def print_pattern(m, n):
    print(create_pattern(m, n))


def main():
    radius = float(input("Enter circle radius? "))
    print("Circle area =", calculate_circle_area(radius))

    celsius = float(input("Enter the temperature in Celsius? "))
    print(f"{celsius:g} (C) = {celsius_to_fahrenheit(celsius)} (F)")

    number = int(input("Enter a number? "))
    if is_prime(number):
        print(number, "is a prime number")
    else:
        print(number, "is a NOT prime number")

    number = int(input("Enter a number? "))
    if is_perfect(number):
        print(number, "is a perfect number")
    else:
        print(number, "is a NOT perfect number")

    # The PDF does not show the original color list. This sample keeps Red at index 3.
    colors = ["Blue", "Yellow", "White", "Red"]
    favorite_color = input("What is your favorite color? ")
    color_index = find_color(colors, favorite_color)
    if color_index == -1:
        print("Sorry, I could not find your color")
    else:
        print(f"Your color is at index {color_index} in my list")

    range1, range2, range3, range4 = create_ranges()
    print("range1:", range1)
    print("range2:", range2)
    print("range3:", range3)
    print("range4:", range4)

    print(remove_dollar_sign(input("Enter a string containing dollar signs: ")))

    numbers = [int(value) for value in input("Enter integers separated by spaces: ").split()]
    print("Even numbers:", extract_even(numbers))

    number = int(input("Enter a non-negative integer: "))
    print("Factorial:", factorial(number))

    number = int(input("Enter a non-zero integer: "))
    print("Divisors:", get_divisors(number))

    x1 = float(input("Enter x1: "))
    y1 = float(input("Enter y1: "))
    x2 = float(input("Enter x2: "))
    y2 = float(input("Enter y2: "))
    print("Distance:", distance_between_points(x1, y1, x2, y2))

    m = int(input("Enter pattern height m: "))
    n = int(input("Enter pattern width n: "))
    print_pattern(m, n)


if __name__ == "__main__":
    main()

