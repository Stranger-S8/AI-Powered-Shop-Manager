file_path = "data/Category Data/category_data.csv"

with open(file_path, 'r') as f:
    lines = f.readlines()

A = []
for i in lines:
    if ". " in i:
        A.append(i.split(". ")[1])

with open(file_path, 'w') as f:
    f.writelines(lines)