my_dict = {
    "apple": 1,
    "banana": 2,
    "cherry": 3
}
for key, value in my_dict.items():
    print(f"{key}: {value}")
my_dict["date"] = 4
for key, value in my_dict.items():
    print(f"{key}: {value}")
my_dict.pop("banana")
for key, value in my_dict.items():
    print(f"{key}: {value}")