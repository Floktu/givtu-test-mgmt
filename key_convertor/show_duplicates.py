

if __name__ == "__main__":
    with open('keys.txt', 'r') as file:
        A = [line.strip() for line in file if line.strip()]  # remove empty lines and whitespace
    with open('duplicates.txt', 'r') as file:
        B = [line.strip() for line in file if line.strip()]  # remove empty lines and whitespace

    print("A:", A)
    print("   ", end="")

    for value in A:
        if value in B:
            print(" ^ ", end="")  # Match found
        else:
            print("   ", end="")  # No match

    print("\nMatching indices:", [i for i, val in enumerate(A) if val in B])