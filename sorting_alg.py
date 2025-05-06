import time
import random
import tracemalloc
import psutil
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns
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
def measure_performance(sort_func, data):
    tracemalloc.start()
    cpu_before = psutil.cpu_percent(interval=None)

    start_time = time.perf_counter()
    if sort_func == quick_sort:
        sort_func(list(data))  # quick_sort returns new list
    else:
        sort_func(data.copy())  # merge_sort is in-place
    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    cpu_after = psutil.cpu_percent(interval=0.1)

    execution_time = (end_time - start_time) * 1000  # in milliseconds
    memory_usage = peak / (1024 * 1024)  # in MB
    cpu_usage = (cpu_before + cpu_after) / 2

    return execution_time, memory_usage, cpu_usage

# --- Experimental Conditions ---
algorithms = [("Merge Sort", merge_sort), ("Quick Sort", quick_sort)]
data_sizes = [10000, 100000]

results = []

for algo_name, algo_func in algorithms:
    for size in data_sizes:
        for rep in range(2):  # 2 replicates
            data = list(range(size))
            random.shuffle(data)
            exec_time, mem_usage, cpu = measure_performance(algo_func, data)
            results.append({
                "Algorithm": algo_name,
                "Data Size": size,
                "Replicate": rep + 1,
                "Execution Time (ms)": round(exec_time, 2),
                "Memory Usage (MB)": round(mem_usage, 2),
                "CPU Usage (%)": round(cpu, 2)
            })

# --- Create DataFrame ---
df = pd.DataFrame(results)
print(df)

# --- Export to Excel ---
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"results.xlsx"
excel_title = "Full Factorial Experiment: Sorting Algorithms Performance Evaluation"

with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Results', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Results']
    worksheet.write('A1', excel_title)
    worksheet.set_row(0, 30)
    worksheet.set_column('A:F', 25)

print(f"\n Excel file created: {file_name}")

