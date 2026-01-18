import matplotlib.pyplot as plt
import numpy as np

# Przygotowanie danych
x = np.linspace(-1, 2, 1000)  # 1000 punktów od -1 do 2
y = x * np.sin(10 * np.pi * x) + 1

# Rysowanie
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='f(x) = x * sin(10*pi*x) + 1', color='blue')

# Zaznaczenie Twojego wyniku (1.85)
plt.plot(1.85, 2.85, 'ro', label='Twój wynik (Szczyt)')

plt.title("Krajobraz, po którym porusza się algorytm")
plt.axhline(0, color='black', linewidth=0.5) # Oś pozioma
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()