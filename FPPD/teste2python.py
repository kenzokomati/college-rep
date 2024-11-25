import random
import numpy as np
import time
import csv
from multiprocessing import Pool

def read_csv_elements(file_path):
    """
    Reads elements from a CSV file and returns a flat list.
    """
    elements = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            elements.extend(row)
    return elements

def convert_to_integers(elements):
    """
    Converts a list of elements (including those in scientific notation) to integers.
    """
    return [int(round(float(element))) for element in elements if element.strip()]

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def serial_merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = serial_merge_sort(arr[:mid])
    right = serial_merge_sort(arr[mid:])
    return merge(left, right)

def parallel_merge_sort(arr, num_processes):
    length = len(arr)
    if length <= 1:
        return arr
    chunk_size = (length + num_processes - 1) // num_processes
    chunks = [
        arr[i * chunk_size: min((i + 1) * chunk_size, length)]
        for i in range(num_processes)
    ]
    
    with Pool(num_processes) as pool:
        sorted_chunks = pool.map(serial_merge_sort, chunks)
    
    while len(sorted_chunks) > 1:
        new_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                new_chunks.append(merge(sorted_chunks[i], sorted_chunks[i+1]))
            else:
                new_chunks.append(sorted_chunks[i])
        sorted_chunks = new_chunks
    
    return sorted_chunks[0]

if __name__ == "__main__":
    NUM_PROCESSES = 4
    file_path = "csvs/A.csv"

    # Read and convert elements to integers
    elements = read_csv_elements(file_path)
    array = np.array(convert_to_integers(elements), dtype=np.int32)

    # Serial merge sort
    start_time = time.perf_counter()
    sorted_serial = serial_merge_sort(array.copy())
    serial_time = time.perf_counter() - start_time
    print(f"Serial \n\tTime: {serial_time:.6f} seconds\n")

    # Parallel merge sort
    start_time = time.perf_counter()
    sorted_parallel = parallel_merge_sort(array.copy(), NUM_PROCESSES)
    parallel_time = time.perf_counter() - start_time
    print(f"Parallel \n\tTime: {parallel_time:.6f} seconds\n")
    
    # Check if both sorted arrays are equal
    assert np.array_equal(sorted_serial, sorted_parallel), "ERROR: Sorted arrays do NOT match"
    
    print(f"Achieved Speedup: {serial_time / parallel_time:.4f}")
