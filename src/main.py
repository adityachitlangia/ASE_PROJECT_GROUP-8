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
    opt5 = [85.99933333333333, 157.1942, 111.8965, 68.55406666666666, 69.38133333333333, 68.3944, 78.7495, 86.23926666666667, 85.93733333333334, 85.42466666666667, 26.275166666666667, 48.585, 82.0249, 94.0021, 48.32843333333333, 112.3065, 32.38786666666667, 92.45043333333332, 98.73836666666666, 85.83013333333334]
    opt9 = [68.41476666666667, 78.40433333333333, 34.88336666666667, 52.570366666666665, 53.6744, 85.16546666666666, 111.54413333333332, 52.21463333333333, 85.74156666666666, 71.20606666666667, 85.32766666666667, 111.3025, 82.73123333333332, 94.7291, 84.01209999999999, 84.38516666666668, 51.6698, 98.02926666666669, 131.95306666666667, 95.19316666666668]
    opt15 = [85.05803333333334, 47.80233333333333, 78.46103333333333, 69.90483333333333, 94.5781, 68.84826666666667, 64.89203333333333, 47.03926666666666, 26.824166666666667, 68.22663333333334, 51.48756666666666, 26.30933333333333, 34.956799999999994, 67.8148, 68.7162, 69.79253333333332, 63.2985, 34.9531, 48.53236666666667, 67.63183333333333]
    opt25 = [25.380433333333333, 48.58013333333333, 29.51903333333333, 51.78726666666666, 26.624866666666662, 53.75376666666667, 50.8064, 24.6853, 26.91673333333333, 26.77253333333333, 47.98926666666667, 85.69196666666666, 26.249566666666663, 26.55006666666667, 52.0003, 26.488, 47.70123333333333, 27.55213333333333, 26.9045, 25.503266666666665]
    opt50 = [69.27233333333332, 26.230666666666664, 26.4269, 27.518466666666665, 26.24023333333333, 25.976633333333336, 52.45343333333333, 50.90076666666666, 54.4444, 49.9982, 26.1376, 25.8442, 27.93816666666667, 24.941966666666666, 51.59046666666668, 68.5406, 27.32323333333333, 26.0817, 55.07906666666667, 29.6369]
    opt5 = calc_d2h(d, opt5)
    opt9 = calc_d2h(d, opt9)
    opt15 = calc_d2h(d, opt15)
    opt25 = calc_d2h(d, opt25)
    opt50 = calc_d2h(d, opt50)

    # Hyperopt error vals
    hyperopt5 = [182.4867,218.8694,331.2958,388.6371,137.4128,199.3936,184.0543,160.9822,178.5068,156.3472,213.0389,187.0547,148.7879,159.5665,157.4338,223.5416,192.5274,158.8697,181.1339,186.5491]
    hyperopt9 = [144.592,218.2259,148.8657,173.2815,149.0494,161.3025,213.0087,166.2408,162.8217,163.0501,153.2567,138.2588,145.104,185.7562,193.7622,151.9057,162.2962,163.5829,217.8078,146.5648]
    hyperopt15 = [154.5082,149.7764,187.2739,159.5658,180.4779,143.64,151.2242,148.7663,151.9281,153.3423,141.2645,161.1214,214.8879,141.7097,158.9604,180.4636,148.0288,145.2398,162.9608,156.243]
    hyperopt25 = [160.0089,148.7863,158.1165,153.4657,147.7038,132.153,156.8973,145.8404,145.7335,156.6683,180.9097,148.7026,156.2457,156.6943,147.7568,160.8004,138.6304,129.6381,152.9934,162.4121]
    hyperopt50 = [157.1133,135.2532,139.942,141.8247,113.1632,146.8958,128.2163,152.7071,124.3698,157.7302,145.8622,130.2181,131.8818,155.0369,149.3443,190.7396,133.2495,148.0005,127.708,158.9724]
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

        # SAMPLE(randN_time(d,5), "rand5"),
        # SAMPLE(randN_time(d,9), "rand9"),
        # SAMPLE(randN_time(d,15), "rand15"),
        # SAMPLE(randN_time(d,25), "rand25"),
        # SAMPLE(randN_time(d,50), "rand50"),

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