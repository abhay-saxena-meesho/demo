n = int(input("Enter n: "))

for i in range(1,n+1):
    sum_of_first_i = i * (i+1) // 2
    print(f"Sum of first {i} numbers: {sum_of_first_i}")