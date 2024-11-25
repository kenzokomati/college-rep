import csv
import time
import multiprocessing
import numpy as np

# Optimized CSV file reading
def read_csv(file_path):
    return np.loadtxt(file_path, delimiter=',').astype(np.int64)

# Function to calculate the prefix sum for a segment
def sliding_window_sum(A, start_index, end_index):
    B_chunk = np.zeros(end_index - start_index, dtype=int)
    for i in range(start_index, end_index):
        if i == 0:
            B_chunk[i - start_index] = A[0]
        else:
            B_chunk[i - start_index] = A[i - 1] + A[i]
    return (start_index, B_chunk)

# Parallel prefix sum using Pool
def parallel_window_sum(A, num_processes):
    chunk_size = len(A) // num_processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Distribute the work among processes
        tasks = [
            (A, i * chunk_size, (i + 1) * chunk_size if i < num_processes - 1 else len(A))
            for i in range(num_processes)
        ]
        results = pool.starmap(sliding_window_sum, tasks)

    # Combine results
    result = np.zeros(len(A), dtype=int)
    for start_index, B_chunk in results:
        result[start_index:start_index + len(B_chunk)] = B_chunk

    return result

if __name__ == "__main__":
    csv_file = "C.csv"
    num_processes = 4  # Number of parallel processes

    # Load the array A
    A = read_csv(csv_file)

    # Serial sum
    print("\nExecuting serial sliding window sum...")
    start_time = time.time()
    B_serial = parallel_window_sum(A, 1)  # 1 process is equivalent to serial execution
    serial_time = time.time() - start_time
    print(f"Serial sliding window sum completed. \n\tTime: {serial_time:.4f} seconds")

    # Parallel prefix sum
    print("\nExecuting parallel sliding window sum...")
    start_time = time.time()
    B_parallel = parallel_window_sum(A, num_processes)
    parallel_time = time.time() - start_time
    print(f"Parallel sliding window sum completed. \n\tTime: {parallel_time:.4f} seconds")

    # Verify the correctness of the results
    assert np.array_equal(B_serial, B_parallel), "ERROR: The results DO NOT match!"
    
    # Calculate the speedup
    speedup = serial_time / parallel_time
    print(f"\nAchieved Speedup: {speedup:.4f}")
