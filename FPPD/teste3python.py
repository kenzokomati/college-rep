import multiprocessing
import random
import time

def calculate_element(i, j, A, B):
    return sum(A[i][k] * B[k][j] for k in range(len(A[0])))


def parallel_matrix_multiplication(A, B, num_proc=4):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    assert cols_A == rows_B, "ERROR: The matrices cannot be multiplied. Invalid dimensions."

    with multiprocessing.Pool(processes=num_proc) as pool:
        tasks = [(i, j, A, B) for i in range(rows_A) for j in range(cols_B)]
        results = pool.starmap(calculate_element, tasks)

    # Reshape the flat results into a matrix
    C = [results[i * cols_B:(i + 1) * cols_B] for i in range(rows_A)]
    return C


def serial_matrix_multiplication(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError("ERROR: The matrices cannot be multiplied. Invalid dimensions.")

    # Multiply matrices A and B Serially
    C = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
    return C


if __name__ == "__main__":
    # Matrix dimensions
    rows_A, cols_A = 200, 400
    rows_B, cols_B = 400, 100

    # Number of processes for parallel computation
    num_proc = 4

    # Generate random matrices
    A = [random.choices(range(1, 11), k=cols_A) for _ in range(rows_A)]
    B = [random.choices(range(1, 11), k=cols_B) for _ in range(rows_B)]

    # Serial multiplication
    start_serial = time.perf_counter()
    C_serial = serial_matrix_multiplication(A, B)
    end_serial = time.perf_counter()
    print(f"Serial \n\tTime: {end_serial - start_serial:.5f} seconds\n")
    
    # Parallel multiplication
    start_parallel = time.perf_counter()
    C_parallel = parallel_matrix_multiplication(A, B, num_proc=num_proc)
    end_parallel = time.perf_counter()
    print(f"Parallel \n\tTime: {end_parallel - start_parallel:.5f} seconds\n")

    # Verify the correctness of the results
    assert C_serial == C_parallel, "ERROR: Multiplied Matrixes results are not the same"
    
    # Calculate speedup
    speedup = (end_serial - start_serial) / (end_parallel - start_parallel)
    print(f"Achieved Speedup: {speedup:.2f}")
