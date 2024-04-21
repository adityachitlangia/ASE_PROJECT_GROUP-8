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
        lst = [round(norm(col,val), 5) for val in lst]
    return lst

def calculate_stats():
    d = DATA(src = the['file'])
    
    print("date:{}\nfile:{}\nrepeat:{}\nrows:{}\ncols:{}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),the['file'],"20",len(d.rows), len(d.rows[0].cells)))
    sortedRows =  sorted(d.rows, key=lambda x: x.d2h(d))
    print(f"best: {o(sortedRows[0].d2h(d),n=4)}")
    all = base(d)
    print(f"tiny: {o(statistics.stdev(all)*0.35,n=4)}")
    # print("#base #bonr9 #rand9 #bonr15 #rand15 #bonr20 #rand20 #rand358 #rrp7")

    randN_time = calculate_execution_time(randN)
    bonrN_time = calculate_execution_time(bonrN)
    rrp_time = calculate_execution_time(rrp)
    
    # Optuna error vals
    opt5 = [4.8556, 3.8237, 9.7683, 8.422699, 7.920299, 6.41590, 8.1015, 2.9804, 5.7875, 11.4368, 7.5947, 3.8802, 3.953, 7.629, 3.0815, 5.6604, 4.1547, 4.77999, 3.7046, 3.8583]
    opt9 = [4.9137, 3.8103, 4.0241, 2.5384, 9.1385, 8.21699, 4.1584, 5.6907, 2.5392, 3.26970, 4.1134, 3.7223, 4.78710, 2.3936, 4.9078, 3.6042, 3.5489, 2.9461, 5.6472, 3.8672]
    opt15 = [3.8574, 3.9082, 3.9585, 2.9813, 3.6898, 2.7784, 4.2572, 3.7514, 3.7473, 3.5788, 5.5625, 4.0763, 5.4757, 2.8216, 3.9001, 3.9797, 3.0735, 3.8879, 4.408, 4.1545]
    opt25 = [4.5708, 2.7585, 3.9932, 2.5298, 1.8751, 4.1223, 3.2634, 2.7624, 3.8902, 3.7532, 3.6955, 5.6177, 1.8504, 2.5365, 1.9282, 2.8013, 3.9787, 3.8872, 3.7609, 2.7108]
    opt50 =  [3.031, 1.8489, 3.872, 1.7885, 1.8471, 1.8648, 1.8701, 1.8639, 2.7503, 3.0387, 1.9206, 3.7292, 1.8623, 3.2421, 2.7875, 3.7671, 4.0709, 3.9746, 2.7543, 3.2346]
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
    hyperopt25 = calc_d2h(d, hyperopt25)
    hyperopt50 = calc_d2h(d, hyperopt50)

    eg0([
        SAMPLE(opt5, "opt5"),
        SAMPLE(opt9, "opt9"),
        SAMPLE(opt15, "opt15"),
        SAMPLE(opt25, "opt25"),
        SAMPLE(opt50, "opt50"),

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