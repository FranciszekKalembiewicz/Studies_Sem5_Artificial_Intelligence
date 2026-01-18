import random
import math

# KONFIGURACJA
POP_SIZE = 100  # Liczba osobników
GEN_LEN = 20  # Długość chromosomu (bitów)
MAX_GEN = 100  # Liczba generacji (epok)
P_CROSS = 0.8  # Prawdopodobieństwo krzyżowania
P_MUT = 0.05  # Prawdopodobieństwo mutacji
X_MIN = -1.0  # Zakres min
X_MAX = 2.0  # Zakres max


# (0) Kodowanie: Dekodowanie binarne na liczbę rzeczywistą
def decode(chromosom):
    max_val = 2 ** GEN_LEN - 1
    int_val = int(chromosom, 2)
    return X_MIN + int_val * (X_MAX - X_MIN) / max_val


# (1) Wybór populacji początkowej
def init_population(size, length):
    return [''.join(random.choice('01') for _ in range(length)) for _ in range(size)]


# (2) Ocena osobników (Funkcja przystosowania)
# Funkcja: f(x) = x * sin(10 * pi * x) + 1
def evaluate_fitness(chromosom):
    x = decode(chromosom)
    # Dodajemy 1.0, aby wartości były dodatnie (wymagane do ruletki)
    return x * math.sin(10 * math.pi * x) + 1.0


# (3) Sprawdzenie warunku stopu
def check_stop_condition(current_gen, max_gen):
    return current_gen >= max_gen


# (4) Selekcja osobników (Metoda koła ruletki)
def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    probs = [f / total_fitness for f in fitness_scores]

    # Losujemy nową populację na podstawie wag fitness
    new_pop = random.choices(population, weights=probs, k=len(population))
    return new_pop


# (5) Krzyżowanie (Jednopunktowe)
def crossover(parent1, parent2):
    if random.random() < P_CROSS:
        pt = random.randint(1, GEN_LEN - 1)
        return parent1[:pt] + parent2[pt:], parent2[:pt] + parent1[pt:]
    return parent1, parent2


# (6) Mutacja (Bitowa)
def mutation(chromosom):
    chrom_list = list(chromosom)
    for i in range(len(chrom_list)):
        if random.random() < P_MUT:
            chrom_list[i] = '1' if chrom_list[i] == '0' else '0'
    return "".join(chrom_list)


# Główna pętla algorytmu
def main():
    population = init_population(POP_SIZE, GEN_LEN)
    best_overall_x = 0
    best_overall_score = -float('inf')

    print(f"Start: Pop={POP_SIZE}, Gen={MAX_GEN}, Mut={P_MUT}")

    for gen in range(MAX_GEN):
        # Ocena
        scores = [evaluate_fitness(ind) for ind in population]

        # Logowanie najlepszego w tej generacji
        best_gen_score = max(scores)
        if best_gen_score > best_overall_score:
            best_overall_score = best_gen_score
            best_ind = population[scores.index(best_gen_score)]
            best_overall_x = decode(best_ind)

        if check_stop_condition(gen, MAX_GEN):
            break

        # Selekcja
        parents = selection(population, scores)

        # Nowa generacja przez Krzyżowanie i Mutację
        next_gen = []
        for i in range(0, POP_SIZE, 2):
            p1, p2 = parents[i], parents[i + 1]
            c1, c2 = crossover(p1, p2)
            next_gen.append(mutation(c1))
            next_gen.append(mutation(c2))

        population = next_gen

        if gen % 20 == 0:
            print(f"Gen {gen}: Max Fitness = {best_gen_score:.4f}")

    print("\n--- WYNIKI ---")
    print(f"Najlepsze x: {best_overall_x:.6f}")
    # Odejmujemy 1.0, by wrócić do oryginalnej wartości funkcji (bez przesunięcia)
    print(f"Wartość f(x): {best_overall_score - 1.0:.6f}")


if __name__ == "__main__":
    main()


