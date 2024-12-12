import time
from multiprocessing import Pool, cpu_count

def factorize_single(number):
    """Факторизація одного числа."""
    factors = [i for i in range(1, number + 1) if number % i == 0]
    return factors

def factorize_sync(*numbers):
    """Синхронна версія факторизації."""
    return [factorize_single(number) for number in numbers]

def factorize_parallel(*numbers):
    """Паралельна версія факторизації."""
    with Pool(cpu_count()) as pool:
        results = pool.map(factorize_single, numbers)
    return results


if __name__ == "__main__":
    numbers_to_factorize = [128, 255, 99999, 10651060]

    
    start_time = time.time()
    sync_results = factorize_sync(*numbers_to_factorize)
    sync_duration = time.time() - start_time

    print(f"Синхронна факторизація завершена за {sync_duration:.2f} секунд.")
    
    
    print("Результати синхронної факторизації:", sync_results)

    
    start_time = time.time()
    parallel_results = factorize_parallel(*numbers_to_factorize)
    parallel_duration = time.time() - start_time

    print(f"Паралельна факторизація завершена за {parallel_duration:.2f} секунд.")
    
    
    print("Результати паралельної факторизації:", parallel_results)

    
    a, b, c, d = sync_results

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [
        1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
        380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060
    ]

    print("Всі тести пройдено успішно!")