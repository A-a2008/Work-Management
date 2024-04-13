def print_rangoli(size):
    # your code goes here
    letter = 97 + size
    for i in range(size*2-1):
        mid = (size**2) // 2
        for j in range(size**2):
            if j == mid:
                print(letter-i, end="")
            else:
                print("-", end="")
        print()

print_rangoli(3)