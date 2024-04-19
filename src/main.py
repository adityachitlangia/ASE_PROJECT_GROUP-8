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

    eg0([
        SAMPLE(randN_time(d,9), "rand9"),
        SAMPLE(randN_time(d,15), "rand15"),
        SAMPLE(randN_time(d,20), "rand20"), 
        SAMPLE(randN_time(d,358), "rand358"), 
        SAMPLE(bonrN_time(d,9), "bonr9"),
        SAMPLE(bonrN_time(d,15), "bonr15"),
        SAMPLE(bonrN_time(d,20), "bonr20"),
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