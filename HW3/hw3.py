import pandas as pd
import numpy as np
import random
import sys
import math

df = pd.read_csv('hw3_train.dat', sep="\t", header=None)
df.insert(0, -1, 1)
df_y = df[10]
df.drop(columns=10, axis=1, inplace=True)
df.rename(columns={-1: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10}, inplace=True)

df_inv = pd.DataFrame(np.linalg.pinv(df.values), df.columns, df.index)
w_lin = df_inv @ df_y

def cal_err(w):
    y_hat = df @ w
    err = df_y - y_hat
    err_in = err.transpose() @ err
    return err_in
e_wlin = cal_err(w_lin)

print(f"Problem 14 : {e_wlin / 1000}")

def linear_sgd():
    a = 1000000000
    zero_data = np.zeros(shape=(11, 1))
    w = pd.DataFrame(zero_data)
    count = 0
    while a > 1.01 * e_wlin:
        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)
        x = random.randint(0,999)
        x_n = df.loc[[x]]
        y_n = df_y.loc[x]
        dot = w.transpose() @ x_n.transpose()
        x_n_arr = x_n.transpose().values
        w = w + 0.002 * (y_n - dot.values)* x_n_arr
        a = cal_err(w[0])
        count += 1
    return count
c = 0
for _ in range(1000):
    c+=linear_sgd()
print(f"Problem 15 : {c / 1000}")

def sig(x):
    return 1/(1+math.exp(-1*x))

def err_log(w, x, y):
    dot = (w @ x).values
    return np.log(1 + math.exp(-1*y*dot[0]))

def log_sgd():
    zero_data = np.zeros(shape=(11, 1))
    w = pd.DataFrame(zero_data)
    for _ in range(500):
        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)
        x = random.randint(0,999)
        x_n = df.loc[[x]]
        y_n = df_y.loc[x]
        dot = (w.transpose() @ x_n.transpose()).values
        v = -1*y_n*dot
        x_n_arr = x_n.transpose().values
        w = w + 0.001 * sig(v)*y_n*x_n_arr
    su = 0
    for i in range(1000):
        x_i = df.loc[i]
        y_i = df_y.loc[i]
        su += err_log(w.transpose(), x_i.transpose(), y_i)
    return su /1000

print(f"Problem 16 : {log_sgd()}")

def log_sgd_with_init():
    w = pd.DataFrame(w_lin)
    for _ in range(500):
        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)
        x = random.randint(0,999)
        x_n = df.loc[[x]]
        y_n = df_y.loc[x]
        dot = (w.transpose() @ x_n.transpose()).values
        v = -1*y_n*dot
        x_n_arr = x_n.transpose().values
        w = w + 0.001 * sig(v)*y_n*x_n_arr
    su = 0
    for i in range(1000):
        x_i = df.loc[i]
        y_i = df_y.loc[i]
        su += err_log(w.transpose(), x_i.transpose(), y_i)
    return su /1000

print(f"Problem 17 : {log_sgd_with_init()}")