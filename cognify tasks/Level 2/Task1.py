import random

# Generate a random number between 1 and 100
secret_number = random.randint(1, 100)

print("Guess the number between 1 and 100")

while True:
    guess = int(input("Enter your guess: "))

    if guess < secret_number:
        print("Too low, enter the high number")
    elif guess > secret_number:
        print("Too high, enter the low number")
    else:
        print("Congratulations! You guessed the correct number.")
        break