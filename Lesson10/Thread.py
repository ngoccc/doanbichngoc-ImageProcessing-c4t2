from threading import Thread

def Tinh_Tong():
    a = 5 + 6
    print(a)
    return a

def Tru():
    a = 5 - 6
    print(a)
    return a

Thread(None, Tinh_Tong).start()
# Thread(Tru).start()
Tru()