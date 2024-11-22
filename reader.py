import os

with open("output.txt","r") as file:
    string = file.readline().strip()

if string == "go":
    os.system("python forward.py")
elif string == "back":
    os.system("python backward.py")
elif string == "left":
    os.system("python left.py")
elif string == "right":
    os.system("python right.py")
elif string == "stop":
    os.system("python stop.py")

