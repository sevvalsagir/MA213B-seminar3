import time
import random
import pandas as pd
from datetime import datetime

# --- Sorting Algorithms ---
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

# --- Performance Measurement Function ---
def measure_execution_time(sort_func, data):
    start_time = time.perf_counter()
    if sort_func == quick_sort:
        sort_func(list(data))
    else:
        sort_func(data.copy())
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000  # in milliseconds

# --- Test Settings ---
algorithms = [("Merge Sort", merge_sort), ("Quick Sort", quick_sort)]
data_sizes = [10000, 100000]
system_id = "System B"  # Change this manually on the second system

results = []

for algo_name, algo_func in algorithms:
    for size in data_sizes:
        for rep in range(2):  # 2 replicates
            data = list(range(size))
            random.shuffle(data)
            exec_time = measure_execution_time(algo_func, data)
            results.append({
                "System": system_id,
                "Algorithm": algo_name,
                "Data Size": size,
                "Replicate": rep + 1,
                "Execution Time (ms)": round(exec_time, 2)
            })

# --- Save Results to Excel ---
df = pd.DataFrame(results)
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"results_{system_id.replace(' ', '_')}_{now}.xlsx"
df.to_excel(file_name, index=False)
print(f"\nResults saved to: {file_name}")
print(df)
