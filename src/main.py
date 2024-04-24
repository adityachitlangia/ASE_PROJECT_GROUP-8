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
        # print(f"Execution time of '{func.__name__}{args[1]}': {execution_time:.6f} seconds")
        return result
    return wrapper

def calc_d2h(d, lst, min_v, max_v):
    # print(lst)
    def norm(col, x, min_v, max_v):
        min_v = min(min_v, col.lo)
        max_v = max(max_v, col.hi)
        val = (abs((x - min_v) / (max_v - min_v + 1E-30)))
        # print(min_v, max_v, val, x)
        return x if x == "?" else val
    for col in d.cols.y:
        # print(col,col.lo,col.hi)
        lst = [round(norm(col,val, min_v, max_v), 5) for val in lst]
    # print(lst)
    return lst

def find_min_max(lists):
    min_values = []
    max_values = []
    for lst in lists:
        min_val = min(lst)
        max_val = max(lst)
        min_values.append(min_val)
        max_values.append(max_val)
    return min(min_values), max(max_values)

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
    opt5 = [369.6686881206441, 352.2115594957455, 368.2186456457971, 378.585200709752, 368.7666680531301, 371.3573660802364, 394.4486462667361, 350.5980298104797, 361.46571394369823, 361.283925866451, 376.5190448749286, 394.4486462667361, 394.4689765045764, 331.8734751285097, 400.2590567770097, 343.4021054780124, 364.09494627767526, 378.585200709752, 394.4486462667361, 381.6973993209264]
    opt9 = [364.09494627767526, 344.96848257897784, 334.16955528750174, 371.3573660802364, 345.0077637545043, 394.4486462667361, 368.7666680531301, 363.19763444593445, 350.9665571875183, 344.96848257897784, 345.2209795651097, 371.3573660802364, 376.5190448749286, 344.96848257897784, 350.5980298104798, 352.2115594957455, 352.2115594957455, 331.8734751285097, 356.51034284555675, 375.20648472017376]
    opt15 = [313.4360056772024, 262.5464503211191, 300.1391817597309, 269.844066200114, 269.844066200114, 301.8418957351597, 269.844066200114, 326.7578885173571, 317.65422552849, 268.44109155409, 246.02811392510924, 303.5628999745805, 309.96195281118594, 326.75788851735706, 261.7388357735399, 261.7388357735399, 269.844066200114, 284.2453285002329, 317.65422552849, 314.71416267685254]
    opt25 = [272.9075574217181, 302.00371401957943, 261.8904990041571, 265.89546909748105, 275.9442048885502, 318.77775704946777, 275.9442048885502, 305.2260327297087, 311.80911503503023, 268.44551961069936, 246.02811392510924, 284.62300666928763, 247.21932734839308, 268.44109155409, 265.89546909748105, 265.0183782264044, 268.44109155409, 265.89546909748105, 296.6949036649001, 288.22169205961603]
    opt50 = [276.71306065516944, 265.89546909748105, 273.9747601910399, 246.02811392510924, 263.08381180879275, 268.44109155409, 247.21932734839308, 261.7388357735399, 287.53974744806374, 290.2300725666344, 261.8904990041571, 261.7388357735399, 293.60334771342235, 261.8904990041571, 290.2584474775197, 261.7388357735399, 280.92331646213256, 293.52136560992045, 282.7398486866351, 277.2338340783124]

    # Hyperopt error vals
    hyperopt5 = [407.8711,331.575,345.4098,345.4098,397.5115,333.0865,413.9048,343.6764,331.575,414.3469,343.6764,416.8106,331.575,333.0865,397.5115,407.8711,407.8711,345.4098,331.575,333.0865]
    hyperopt9 = [407.8711,343.6764,416.8106,345.4098,331.575,331.575,407.8711,407.8711,331.575,333.0865,397.5115,343.6764,333.0865,397.5115,397.5115,331.575,397.5115,418.4124,403.1756,397.5115]
    hyperopt15 = [333.0865,333.0865,343.6764,331.575,345.4098,343.6764,331.575,333.0865,331.575,413.3432,343.6764,345.4098,333.0865,333.0865,331.575,331.575,343.6764,413.3432,331.575,331.575]
    hyperopt25 = [331.575,331.575,331.575,331.575,397.5115,331.575,331.575,333.0865,331.575,331.575,333.0865,331.575,345.4098,331.575,331.575,331.575,331.575,331.575,333.0865,331.575]
    hyperopt50 = [331.575,331.575,331.575,333.0865,333.0865,333.0865,331.575,331.575,331.575,333.0865,331.575,331.575,331.575,331.575,331.575,331.575,333.0865,331.575,331.575,331.575]

    min_v, max_v = find_min_max([opt5, opt9, opt15, opt25, opt50, hyperopt5, hyperopt9, hyperopt15, hyperopt25, hyperopt50])

    opt5 = calc_d2h(d, opt5,min_v, max_v)
    opt9 = calc_d2h(d, opt9,min_v, max_v)
    opt15 = calc_d2h(d, opt15,min_v, max_v)
    opt25 = calc_d2h(d, opt25,min_v, max_v)
    opt50 = calc_d2h(d, opt50,min_v, max_v)

    hyperopt5 = calc_d2h(d, hyperopt5,min_v, max_v)
    hyperopt9 = calc_d2h(d, hyperopt9,min_v, max_v)
    hyperopt15 = calc_d2h(d, hyperopt15,min_v, max_v)
    hyperopt25 = calc_d2h(d, hyperopt25,min_v, max_v)
    hyperopt50 = calc_d2h(d, hyperopt50,min_v, max_v)

    eg0([

        SAMPLE(rrp_time(d, 5), "rrp"),
        # SAMPLE(rrp_time(d, 6,(len(d.rows) ** 0.5)), "rrp6"),
        # SAMPLE(rrp_time(d, 7,(len(d.rows) ** 0.5)/2), "rrp7"),
        # SAMPLE(rrp_time(d, 8,(len(d.rows) ** 0.5)/4), "rrp8"),
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
    # print("evals:", evals)
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