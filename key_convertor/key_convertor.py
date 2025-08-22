import sys


def number_to_key(number):
    # Define the base-26 to letter mapping
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Adjust number to be zero-indexed
    number -= 1

    # Calculate each character in the key
    key = []
    for _ in range(6):
        key.append(letters[number % 26])
        number //= 26

    # Reverse the key because we build it backwards
    key.reverse()

    # Join list into string
    return ''.join(key)


def key_to_number(key):
    # Ensure key is uppercase for consistency
    key = key.upper()

    # Define the base-26 to letter mapping
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Initialize the result number
    number = 0

    # Iterate through each character in the key
    for char in key:
        # Find the index of the character in letters
        index = letters.index(char)
        # Multiply the current number by 26 and add the index
        number = number * 26 + (index)  # +1 to adjust for 1-based indexing

    return number + 1



if __name__ == "__main__":

    # Open and read the file line by line
    # with open('keys.txt', 'r') as file:
    #     lines = [key_to_number(line.strip()) for line in file if line.strip()]  # remove empty lines and whitespace
    #
    # print(lines)  # This will print the whole array/list
    # sys.exit(1)

    while True:
        try:
            # Prompt the user for input
            user_input = input(
                "Enter a number between 1 and 308915776 (or type 'exit' to quit), or a 6-character key to convert to a number: ")

            if user_input.lower() == 'exit':
                break

            # Determine if input is a number or a key
            if user_input.isdigit():
                # Convert the input to an integer
                number = int(user_input)

                # Ensure the number is within the valid range
                if not (1 <= number <= 308915776):
                    print("Error: Number must be between 1 and 308915776")
                    continue

                # Generate and print the key
                key = number_to_key(number)
                print(f"The key for the number {number} is: {key}")

            elif len(user_input) == 6:
                # Convert key to number
                number = key_to_number(user_input)
                print(f"The number for the key '{user_input}' is: {number}")

            else:
                print("Error: Input must be a number between 1 and 308915776 or a 6-character key.")
                continue

        except ValueError:
            print("Error: Please provide a valid number or key")
