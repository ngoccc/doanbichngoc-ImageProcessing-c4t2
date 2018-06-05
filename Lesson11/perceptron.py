import numpy as np
import matplotlib.pyplot as plt

x1 = np.random.randint(0, 50, size=50)
y1 = np.random.randint(0, 50, size=50)
P1 = []
t1 = []
for i in range(50):
    P1.append([x1[i], y1[i]])
    t1.append(0)

x2 = np.random.randint(50, 100, size=50)
y2 = np.random.randint(50, 100, size=50)
P2 = []
t2 = []
for i in range(50):
    P2.append([x2[i], y2[i]])
    t2.append(1)

# init w
w_old = [0.1, -0.5]
w_new = w_old
b_new = 0.5
#
while True:
    count = 0
    for i in range(100):
        w_old = w_new
        b_old = b_new
        ti = 0
        if i < 50:
            pi = P1[i]
            ti = t1[i]
        else:
            pi = P2[i - 50]
            ti = t2[i - 50]
        a = (pi[0]*w_old[0]) + (pi[1]*w_old[1]) + b_old
        # print(a)
        if a > 0:
            a = 1
        else:
            a = 0
        e = ti - a
        if e == 0:
            count += 1
        else:
            w_new[0] = w_old[0] + e * pi[0]
            w_new[1] = w_old[1] + e * pi[1]
            b_new = b_old + e
    if count == 100:
        break
# print(w_new)
# print(b_new)
k = np.linspace(0, 100)
j = -(w_new[0] * k + b_new) / w_new[1]
plt.plot(k, j, color='b')
plt.scatter(x1, y1, color='r')
plt.scatter(x2, y2, color='g')
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.show()
