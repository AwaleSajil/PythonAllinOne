import multiprocessing

def calc_square(numbers, result, v):
    v.value = 5.67
    for idx, n in enumerate(numbers):
        result[idx] = n*n

def calc_cube(numbers):
    for n in (numbers):
        print("Cube:", n*n*n)
    

if __name__ == "__main__":
    numbers = [2,3,5]
    result = multiprocessing.Array('i',3)
    v = multiprocessing.Value('d', 0.0)
    p1 = multiprocessing.Process(target=calc_square, args=(numbers, result, v))
    p2 = multiprocessing.Process(target=calc_cube, args=(numbers,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(v.value)
    print(result[:])