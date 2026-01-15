import random

# Take range input from the user
lower = int(input("Enter the lower bound: "))
upper = int(input("Enter the upper bound: "))

# Generate a random number within the given range
secret_number = random.randint(lower, upper)

print(f"Guess the number between {lower} and {upper}")

while True:
    guess = int(input("Enter your guess between lower and upper: "))

    if guess < secret_number:
        print("Too low, enter the high number ")
    elif guess > secret_number:
        print("Too high, enter the low number ")
    else:
        print("Congratulations! You guessed the correct number.")
        break
