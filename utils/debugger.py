
def DEBUG(string):
    print("\033[32m[DEBUG] " + string + "\033[0m")

def INFO(string):
    print("[INFO] " + string)

def WARNING(string):
    print("\033[35m[WARNING] " + string + "\033[0m")

def ERROR(string):
    print("\033[31m[ERROR] " + string + "\033[0m")
    # assert False

def LOG(string):
    with open(".\\resources\log.txt", "w") as f:
        f.write(string)
    f.close()