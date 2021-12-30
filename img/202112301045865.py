import turtle as t
import math

# 等边三角形内切圆
t.setup(500, 500, 200, 200)
t.hideturtle()

for i in range(3):
    t.fd(200)
    t.seth((i + 1) * 120)
t.seth(360)
t.fd(100)
t.circle((math.sqrt(3) / 6) * 200)
t.mainloop()