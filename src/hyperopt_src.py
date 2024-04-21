from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from hyperopt import hp, tpe, fmin, Trials
import warnings
import os
import shutil
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'hyperopt_outputs')
data_dir = "../se_data/"

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def objective(params):
  params['max_iter'] = int(params['max_iter'])
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=23)
  logistic = linear_model.LogisticRegression(**params)
  accuracy = logistic.fit(X_train, y_train).score(X_test, y_test)

  return -accuracy

inputs = ['dtlz2','dtlz3','pom3a','pom3b','pom3c','SS-A','SS-B','SS-C','SS-D','Wine_quality']
n_trials_list = [6,12,20,60,100] #50,100,200,500
iters =20

params = {
    'tol' : hp.uniform('tol' , 1e-6 , 1e-3),
    'C' : hp.loguniform("C", 1e-2, 1),
    'max_iter' : hp.quniform('max_iter', 100, 5000, 100),
    'fit_intercept' : hp.choice('fit_intercept', [True, False]),
    'penalty' : hp.choice('penalty', ['l2', 'none'])
}

res = {}
for inputf in inputs:
    acc_dict = {}
    time_dict = {}
    res[inputf] = {}
    for n_trials in n_trials_list:
        start_time = time.time()
        with open((os.path.join(output_dir,inputf+'.txt')), 'a') as file:
            file.write('\n_______________________________\nhyperopt' + str(n_trials)+'\n_______________________________\n')
        acc_list = []
        acc = 0
        i = iters
        while i > 0:
            X = pd.read_csv(os.path.join(data_dir,inputf+'_X.csv')).values
            y = pd.read_csv(os.path.join(data_dir,inputf+'_y.csv')).values
            tpe_algo = tpe.suggest
            trials = Trials()
            best_params = fmin(fn=objective,space=params,algo=tpe_algo,max_evals=n_trials,trials=trials)
            best_loss = min(trials.losses())
            acc_list.append(-best_loss)
            acc += -float(best_loss)
            with open((os.path.join(output_dir,inputf+'.txt')), 'a') as file:
                file.write('\n\nthe best params:' + str(best_params))
                file.write('\nthe best value:' + str(-best_loss))
            i -= 1
        with open((os.path.join(output_dir,inputf+'.txt')), 'a') as file:
            file.write('\n*****************************\nAverage optimal accuracy:' + str(acc/iters)+'\n*****************************\n')
        end_time = time.time()
        acc_dict['hyperopt'+str(n_trials)] = acc_list
        acc_r_list = [round(x, 2) for x in acc_list]
        res[inputf]['hyperopt'+str(n_trials)] = acc_r_list
        time_dict['hyperopt'+str(n_trials)] = end_time - start_time
    with open((os.path.join(output_dir,inputf+'.txt')), 'a') as file:
        file.write('\n---------------------\nAccuracy\n---------------------\n' + str(acc_dict)+'\n---------------------\n')
        file.write('\n---------------------\nTime\n---------------------\n' + str(time_dict)+'\n---------------------\n')
with open((os.path.join(output_dir,'hyperopt_final.txt')), 'a') as file:
    file.write('\n---------------------\nAggregate\n---------------------\n' + str(res)+'\n---------------------\n')