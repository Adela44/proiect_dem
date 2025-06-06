import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

# Incarcare imag
img = cv2.imread("/home/ubuntu/Downloads/imag_noua.jpg")  # calea fisierului
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.title("Imagine Original")
plt.axis("off")
plt.savefig("Imagine Original.png")


# Procesare imag (alb - negru -> blurred -> edges)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 75, 130)

#cv2.imwrite("gray.jpg", gray)

# Detectectarea liniilor
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=75, minLineLength=90, maxLineGap=10)

# Criterii pt filtrare
filtered_lines = []
angle_threshold_min = 45
angle_threshold_max = 230
min_length = 150         # pixeli (in functie de rezolutia imaginii)

for line in lines:
    x1, y1, x2, y2 = line[0]
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    angle = abs(math.degrees(math.atan2(dy, dx)))

    # unghiul intre -180 si 180
    angle = angle if angle <= 180 else 360 - angle

    if min_length < length and angle_threshold_min < angle < angle_threshold_max:
        filtered_lines.append((x1, y1, x2, y2))

# Desenam doar liniile gasite
img_lines = img.copy()
for x1, y1, x2, y2 in filtered_lines:
    cv2.line(img_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Afis
img_rgb_lines = cv2.cvtColor(img_lines, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb_lines)
plt.title("Linii detectate filtrate")
plt.axis("off")
plt.savefig("Linii_filtrate.png")

# Calculam si afisam unghiul pentru cea mai lunga linie  filtrata (presupunem ca e acul)
x = None
if filtered_lines:
    longest_line = max(filtered_lines, key=lambda l: math.hypot(l[2] - l[0], l[3] - l[1]))
    x1, y1, x2, y2 = longest_line
    dx = x2 - x1
    dy = y2 - y1
    angle = math.degrees(math.atan2(dy, dx))
    x = round(angle,2)
    print(f"Unghiul calculat inainte de transformare: {x:.2f} grade")
else:
    print("Nu a fost detectată nicio linie potrivită.")

# Transformări pentru unghi (valoarea data de atan2)
if x < 0:
    x = -x
else:
    x = 180 - x

print("Unghiul final (dupa transformare) este:")
print(x)

def f_interp(n):
    return 0.0024*n*n + 0.832*n - 41.72777

"""
Valorile pentru care calculez functia de interpolare in matlab

x = [-50.85, -51, -53.08, -55.93, -61.04, -69.86, -88.03, 83.02, 74.85, 62.80]; //unghi
y_Amp = [6, 7, 9, 13, 19, 28, 50, 61, 73, 89]; //mA
z_Ohm = [820, 680, 560, 390, 270, 180, 100, 82, 68, 56]; //Ohm

"""
print("Valoare in mA")
val_mA = round(f_interp(x), 2)
print(val_mA)
