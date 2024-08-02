import numpy as np
import random

# تعریف تابع برای محاسبه طول مسیر
def calculate_length(path, distances):
  total_length = 0
  for i in range(len(path) - 1):
    total_length += distances[path[i]][path[i+1]]
  return total_length

# تعریف تابع برای به روز رسانی فرومون
def update_pheromone(pheromone_matrix, evaporation_rate, q, path, distances):
  for i in range(len(path) - 1):
    pheromone_matrix[path[i]][path[i+1]] = (1 - evaporation_rate) * pheromone_matrix[path[i]][path[i+1]] + q / calculate_length(path, distances)

# تعریف تابع برای انتخاب مسیر بعدی
def select_next_city(current_city, pheromone_matrix, distances, visibility_factor):
  allowed_cities = [city for city in range(len(pheromone_matrix[current_city])) if city != current_city]
  probabilities = np.zeros(len(allowed_cities))
  for i, city in enumerate(allowed_cities):
    probabilities[i] = pheromone_matrix[current_city][city] ** visibility_factor / distances[current_city][city]
  return np.random.choice(allowed_cities, p=probabilities)

# تعریف الگوریتم سیستم مورچه
def ant_colony_optimization(distances, num_ants, num_iterations, evaporation_rate, q, visibility_factor):
  # مقداردهی اولیه ماتریس فرومون
  pheromone_matrix = np.zeros((len(distances), len(distances)))

  # حلقه اصلی الگوریتم
  for iteration in range(num_iterations):
    # ایجاد مورچه ها
    ants = []
    for _ in range(num_ants):
      starting_city = random.randint(0, len(distances) - 1)
      path = [starting_city]
      while len(path) < len(distances):
        next_city = select_next_city(path[-1], pheromone_matrix, distances, visibility_factor)
        path.append(next_city)
      ants.append(path)

    # محاسبه طول مسیر برای هر مورچه
    path_lengths = [calculate_length(path, distances) for path in ants]

    # به روز رسانی ماتریس فرومون
    for path, length in zip(ants, path_lengths):
      update_pheromone(pheromone_matrix, evaporation_rate, q, path, distances)

    # یافتن بهترین مسیر
    best_path = ants[np.argmin(path_lengths)]

  return best_path

# مثال استفاده از الگوریتم
if __name__ == "__main__":
  # تعریف ماتریس مسافت
  distances = np.array([
    [0, 2, 4, 6],
    [2, 0, 3, 4],
    [4, 3, 0, 2],
    [6, 4, 2, 0]
  ])

  # تنظیم پارامترهای الگوریتم
  num_ants = 10
  num_iterations = 100
  evaporation_rate = 0.5
  q = 1
  visibility_factor = 2

  # حل مسئله با استفاده از الگوریتم
  best_path = ant_colony_optimization(distances, num_ants, num_iterations, evaporation_rate, q, visibility_factor)

  # نمایش بهترین مسیر
  print("بهترین مسیر:", best_path)
