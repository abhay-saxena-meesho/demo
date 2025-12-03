def greet(name):
    return f"Hello, {name}!"
def calculate_sum(a, b):
    return a + b
def main():
    user_name = "World"
    result = calculate_sum(5, 3)
    print(greet(user_name))
    print(f"Sum: {result}")
main()