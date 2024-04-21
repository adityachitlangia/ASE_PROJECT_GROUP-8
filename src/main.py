from utils import *
from data import DATA
from config import help_str,the
from test import Test
from datetime import datetime
import statistics
from stats import SAMPLE, eg0
import time
from functools import wraps

def calculate_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of '{func.__name__}{args[1]}': {execution_time:.6f} seconds")
        return result
    return wrapper

def calc_d2h(d, lst):
    def norm(d, x):
        return x if x == "?" else abs((x - d.lo) / (d.hi - d.lo + 1E-30))
    for col in d.cols.y:
        lst = [norm(col,val) for val in lst]
    return lst

def calculate_stats():
    d = DATA(src = the['file'])
    
    print("date:{}\nfile:{}\nrepeat:{}\nrows:{}\ncols:{}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),the['file'],"20",len(d.rows), len(d.rows[0].cells)))
    sortedRows =  sorted(d.rows, key=lambda x: x.d2h(d))
    print(f"best: {o(sortedRows[0].d2h(d),n=4)}")
    all = base(d)
    print(f"tiny: {o(statistics.stdev(all)*0.35,n=4)}")
    print("#base #bonr9 #rand9 #bonr15 #rand15 #bonr20 #rand20 #rand358 #rrp7")

    randN_time = calculate_execution_time(randN)
    bonrN_time = calculate_execution_time(bonrN)
    rrp_time = calculate_execution_time(rrp)
    
    # Optuna error vals
    opt5 = [2.3916,10.9243,4.421,4.8633,8.5064,4.6313,6.4961,4.875,6.3102,2.521,13.7911,6.1889,2.4301,7.3936,2.3496,2.7983,2.5527,2.5485,11.8741,6.6573]
    opt9 = [5.7446,6.3669,7.8597,2.7667,2.7397,4.7975,6.4326,5.2182,5.3797,2.311,2.7808,4.6822,2.6131,6.4475,2.4895,4.7716,7.9342,2.5773,5.0783,4.6448]
    opt15 = [2.593,2.7402,2.4336,2.5814,2.5716,5.0141,2.6337,4.8884,7.9002,2.8866,6.8548,2.2839,2.3515,4.7719,2.4443,2.2832,2.5349,4.9746,4.6846,4.8129]
    opt25 = [2.481,2.2791,2.3498,2.4754,2.4853,2.4704,2.4692,2.2877,2.5367,2.452,2.2305,2.4321,4.7532,2.3008,2.5495,2.5297,2.2787,2.4713,2.3053,4.9074]
    opt50 = [2.4531,2.2812,2.2624,2.4251,2.2561,2.2935,2.4973,2.4712,2.4683,2.41,2.5357,2.5328,2.2988,2.2646,2.3261,2.2747,2.2824,2.5501,2.3258,2.6013]
    opt5 = calc_d2h(d, opt5)
    opt9 = calc_d2h(d, opt9)
    opt15 = calc_d2h(d, opt15)
    opt25 = calc_d2h(d, opt25)
    opt50 = calc_d2h(d, opt50)

    # Hyperopt error vals
    hyperopt5 = [2.3916,10.9243,4.421,4.8633,8.5064,4.6313,6.4961,4.875,6.3102,2.521,13.7911,6.1889,2.4301,7.3936,2.3496,2.7983,2.5527,2.5485,11.8741,6.6573]
    hyperopt9 = [5.7446,6.3669,7.8597,2.7667,2.7397,4.7975,6.4326,5.2182,5.3797,2.311,2.7808,4.6822,2.6131,6.4475,2.4895,4.7716,7.9342,2.5773,5.0783,4.6448]
    hyperopt15 = [2.593,2.7402,2.4336,2.5814,2.5716,5.0141,2.6337,4.8884,7.9002,2.8866,6.8548,2.2839,2.3515,4.7719,2.4443,2.2832,2.5349,4.9746,4.6846,4.8129]
    hyperopt25 = [2.481,2.2791,2.3498,2.4754,2.4853,2.4704,2.4692,2.2877,2.5367,2.452,2.2305,2.4321,4.7532,2.3008,2.5495,2.5297,2.2787,2.4713,2.3053,4.9074]
    hyperopt50 = [2.4531,2.2812,2.2624,2.4251,2.2561,2.2935,2.4973,2.4712,2.4683,2.41,2.5357,2.5328,2.2988,2.2646,2.3261,2.2747,2.2824,2.5501,2.3258,2.6013]
    hyperopt5 = calc_d2h(d, hyperopt5)
    hyperopt9 = calc_d2h(d, hyperopt9)
    hyperopt15 = calc_d2h(d, hyperopt15)
    hypeopt25 = calc_d2h(d, hyperopt25)
    hyperopt50 = calc_d2h(d, hyperopt50)

    eg0([

        SAMPLE(hyperopt5, "hyperopt5"),
        SAMPLE(hyperopt9, "hyperopt9"),
        SAMPLE(hyperopt15, "hyperopt15"),
        SAMPLE(hyperopt25, "hyperopt25"),
        SAMPLE(hyperopt50, "hyperopt50"),

        SAMPLE(randN_time(d,5), "rand5"),
        SAMPLE(randN_time(d,9), "rand9"),
        SAMPLE(randN_time(d,15), "rand15"),
        SAMPLE(randN_time(d,25), "rand25"),
        SAMPLE(randN_time(d,50), "rand50"),

        SAMPLE(bonrN_time(d,5), "bonr5"),
        SAMPLE(bonrN_time(d,9), "bonr9"),
        SAMPLE(bonrN_time(d,15), "bonr15"),
        SAMPLE(bonrN_time(d,25), "bonr25"),
        SAMPLE(bonrN_time(d,50), "bonr50"),

        SAMPLE(rrp_time(d, 7), "rrp7"),
        SAMPLE(rrp_time(d, 8,(len(d.rows) ** 0.5)), "rrp8"),
        SAMPLE(rrp_time(d, 9,(len(d.rows) ** 0.5)/2), "rrp9"),
        SAMPLE(rrp_time(d, 10,(len(d.rows) ** 0.5)/4), "rrp10"),

        SAMPLE(base(d), "base")
    ])

def base(d):
    baseline_output = [row.d2h(d) for row in d.rows]
    return baseline_output

def randN(d, n):
    # random.seed(the['seed'])
    rand_arr = []
    for _ in range(20):
        random_seed = set_random_seed()
        random.seed(random_seed)
        rows = d.rows
        random.shuffle(rows)
        rowsN = random.sample(rows,n)
        rowsN.sort(key=lambda row: row.d2h(d))
        rand_arr.append(round(rowsN[0].d2h(d),4))
    return rand_arr

def bonrN(d, n):
    bonr_arr = []
    for _ in range(20):
        random_seed = set_random_seed()
        random.seed(random_seed)
        _,_, best_stats = d.gate(random_seed, 4, n-4, 0.5)
        bonr_arr.append(best_stats[1])
    return bonr_arr

def rrp(d, n, stop=None):
    # random.seed(the['seed'])
    rrp_arr = []
    for _ in range(20):
        random_seed = set_random_seed()
        random.seed(random_seed)
        best, rest, evals = d.branch(stop=stop)
        # print(o(best.mid().cells))
        best_rows = best.rows
        # print("evals=",n, len(best_rows), len(rest.rows))
        # print(best.mid().d2h(best))
        rrp_arr.append(best.mid().d2h(best))
    print("evals:", evals)
    return rrp_arr

if __name__ == "__main__":
    the = settings(help_str)

    if the['help']:
        print(help_str)
    else:
        ts = Test()
        tests = {
        'coerce': ts.test_coerce_with_loop,
        'cells': ts.test_cells_random_data,
        'round': ts.test_round_various_numbers,
        'num_mid': ts.test_add_and_mid_num,
        'sym_mid': ts.test_add_and_mid_sym,
        'div_sym': ts.test_div_sym,
        'div_num': ts.test_div_num,
        'set_random_seed': ts.test_set_random_seed,
        'test_far':ts.test_far
        }

        file_path = the['file']
        data = DATA(file_path)
        
        data_new = DATA(the['file'])
        full_mid, full_div = data_new.mid_div()
        print("names : {}\t{}".format(data.cols.names,"D2h-"))
        print("mid : \t{}\t\t\t\t{}".format(list(full_mid[0].values())[1:],full_mid[1]))
        print("div : \t{}\t\t\t{}".format(list(full_div[0].values())[1:],full_div[1]))

        calculate_stats()