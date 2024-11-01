# Parte 1: Implementação em Python usando Turtle

import turtle
import math

# Configuração inicial
screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("Morango 3D Giratório")

# Criando a tartaruga
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# Parâmetros do morango
R1 = 1
R2 = 2
K1 = 150
K2 = 5

# Função para desenhar o morango
def draw_strawberry(A, B):
    t.clear()
    for i in range(0, 628, 12):
        for j in range(0, 628, 12):
            c = math.sin(i)
            d = math.cos(j)
            e = math.sin(A)
            f = math.sin(j)
            g = math.cos(A)
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i)
            m = math.cos(B)
            n = math.sin(B)
            t1 = c * h * g - f * e
            x = int(40 + 30 * D * (l * h * m - t1 * n))
            y = int(12 + 15 * D * (l * h * n + t1 * m))
            o = int(x + 80 * y)
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
            if 22 > y and y > 0 and x > 0 and 80 > x and D > z[o]:
                z[o] = D
                b[o] = ".,-~:;=!*#$@"[N if N > 0 else 0]

    # Desenhando o morango
    t.penup()
    for i in range(1760):
        t.goto((i % 80 - 40) * 10, (20 - i // 80) * 12 - 100)
        t.color("red" if b[i] != " " else "black")
        t.write(b[i], font=("Arial", 16, "normal"))

# Loop principal
A = 0
B = 0
z = [0] * 1760
b = [' '] * 1760

while True:
    draw_strawberry(A, B)
    A += 0.04
    B += 0.02
    screen.update()
