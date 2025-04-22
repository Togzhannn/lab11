import json

# Открытие JSON-файла в текущей папке
with open("example.json", "r") as file:
    data = json.load(file)

# Изменение значения
data["price"] = 900

# Запись обратно в файл
with open("example.json", "w") as file:
    json.dump(data, file, indent=4)
