import random
import matplotlib.pyplot as plt

# Parâmetros
N = 8
POPULATION_SIZE = 100
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.05
VISUALIZE_EVERY = 50
MAX_FITNESS = (N * (N - 1)) // 2  # Número máximo de pares não atacando

# Criar um indivíduo
def create_individual():
    genes = [random.randint(0, N - 1) for _ in range(N)]
    fitness = evaluate_fitness(genes)
    return {'genes': genes, 'fitness': fitness}

# Avaliação de fitness
def evaluate_fitness(genes):
    non_attacking = 0
    for i in range(N):
        for j in range(i + 1, N):
            if genes[i] != genes[j] and abs(genes[i] - genes[j]) != abs(i - j):
                non_attacking += 1
    return non_attacking

# Criar população inicial
def create_population():
    population = [create_individual() for _ in range(POPULATION_SIZE)]
    return sorted(population, key=lambda x: x['fitness'], reverse=True)

# Seleção por torneio
def select_parent(population):
    candidates = random.sample(population, 5)
    return max(candidates, key=lambda x: x['fitness'])

# Crossover
def crossover(parent1, parent2):
    point = random.randint(0, N - 1)
    child_genes = parent1['genes'][:point] + parent2['genes'][point:]
    return {'genes': child_genes, 'fitness': evaluate_fitness(child_genes)}

# Mutação
def mutate(individual):
    if random.random() < MUTATION_RATE:
        i = random.randint(0, N - 1)
        individual['genes'][i] = random.randint(0, N - 1)
        individual['fitness'] = evaluate_fitness(individual['genes'])

# Evolução
def evolve_population(population):
    new_generation = population[:10]  # elitismo
    while len(new_generation) < POPULATION_SIZE:
        parent1 = select_parent(population)
        parent2 = select_parent(population)
        child = crossover(parent1, parent2)
        mutate(child)
        new_generation.append(child)
    return sorted(new_generation, key=lambda x: x['fitness'], reverse=True)

# Visualização
def plot_board(genes, generation, fitness):
    plt.figure(figsize=(6, 6))
    plt.title(f"Geração: {generation} | Fitness: {fitness}")
    plt.xticks(range(N))
    plt.yticks(range(N))
    plt.grid(True)
    plt.gca().invert_yaxis()

    for col, row in enumerate(genes):
        plt.plot(col, row, 'ko', markersize=20)  # 'k' = black, 'o' = círculo
    plt.show()
    plt.close()

# Execução principal
def run_genetic_algorithm():
    population = create_population()
    for generation in range(1, MAX_GENERATIONS + 1):
        best = population[0]
        if best['fitness'] == MAX_FITNESS:
            print(f"Solução encontrada na geração {generation}")
            plot_board(best['genes'], generation, best['fitness'])
            return
        if generation % VISUALIZE_EVERY == 0:
            print(f"Geração {generation} | Melhor fitness: {best['fitness']}")
            plot_board(best['genes'], generation, best['fitness'])
        population = evolve_population(population)
    print("Nenhuma solução perfeita encontrada.")
    plot_board(population[0]['genes'], MAX_GENERATIONS, population[0]['fitness'])

# Executar
run_genetic_algorithm()

#Para o atributo população: Aumentando: Geralmente melhora o desempenho. Uma população maior tem mais diversidade genética, o que aumenta a chance de encontrar indivíduos com bom fitness inicial e explorar melhor o espaço de busca. No entanto, cada geração levará mais tempo para ser processada.
#Diminuindo: Pode piorar o desempenho. Uma população pequena tem menos diversidade, aumentando o risco de convergência prematura (o algoritmo fica preso em um ótimo local que não é a solução global) e pode não ser capaz de encontrar a solução ótima. É mais rápido por geração, mas pode exigir mais gerações no total, ou falhar em encontrar a solução.
#Para a taxa de mutação: Aumentando: Introduz mais aleatoriedade na população. Isso pode ajudar a sair de ótimos locais e explorar novas partes do espaço de busca. No entanto, uma taxa de mutação muito alta pode destruir indivíduos com bom fitness e dificultar a convergência para a solução.
#Diminuindo: Reduz a aleatoriedade. Isso pode ajudar a refinar soluções existentes e convergir mais rapidamente se a população já estiver perto da solução. No entanto, uma taxa de mutação muito baixa pode fazer com que o algoritmo fique preso em ótimos locais e não consiga encontrar a solução global.
