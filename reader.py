import os

input = open("output.txt").read()

if input == "go":
    os.system("python forward.py| nc "+IPAdd+" 1200")
elif input == "back":
    os.system("python backward.py| nc "+IPAdd+" 1200")
elif input == "left":
    os.system("python left.py| nc "+IPAdd+" 1200")
elif input == "right":
    os.system("python right.py| nc "+IPAdd+" 1200")
elif input == "stop":
    os.system("python stop.py| nc "+IPAdd+" 1200")