import matplotlib.pyplot as plt 
import numpy as np 
from multiprocessing import Pool
from timeit import default_timer as timer

from functools import partial

def find_x(entry_price, exit_price, short_long):
    #start, stop(more 0.1 for graph display), step(0.1 graph จะได้ละเอียด)
    #สามารถทำเป็น parallel ได้มั้ง เพราะ เพิ่มหรือลด ค่าทีละ 0.1
    if entry_price > exit_price:
        return np.arange(entry_price, exit_price+(0.1*short_long), -0.1)
    else :
        return np.arange(entry_price, exit_price+(0.1*short_long), 0.1)

def inverse_calculate(x, quantity, entry_price, short_long, leverage, entry_value):
    # print(quantity, entry_price, short_long, leverage, entry_value)
    return short_long*leverage*(quantity/entry_price - quantity/x)/entry_value*100

def normal_calculate(x):
    return short_long*leverage*(x-entry_price)/entry_price*100

def display(chart_, x, y_normal, y_roe_inverse, roe, roe_linear):
    if chart_ == 1:
        plt.plot(x, y_normal, label = 'normal')
        plt.title('normal') 
    elif chart_ == 2:
        plt.plot(x, y_roe_inverse, label = "Inverse") 
        plt.title('Inverse') 
    else:
        plt.plot(x, y_normal, label = 'normal')
        plt.plot(x, y_roe_inverse, label = "Inverse") 
        plt.title('Inverse vs Linear') 
    print('ROE inverse return = %.2f%%' %(roe))
    print('ROE linear return = %.2f%%' %(roe_linear))

    plt.xlabel('price') 
    plt.ylabel('ROE%') 
    plt.legend()
    plt.grid()
    plt.show() 

if(__name__=='__main__'):
    quantity = 1
    entry_price = 1
    exit_price = 100
    exit_price_c = exit_price-1
    leverage = 1
    short_long = int(input('long(1) or short(-1) : '))
    chart_ = int(input('normal chart(1), inverse chart(2), all chart (3) : '))


    #define x forward(long)(1) or backward(short))-1
    x = find_x(entry_price, exit_price, short_long)

    # print('type in list :', x.dtype)
    # print('type of x :' ,type(x))

    #ROE inverse calculate
    entry_value = quantity/entry_price
    exit_value = quantity/exit_price
    profit = entry_value-exit_value
    roe = profit/entry_value*100*leverage*short_long

    #ROE linear calculate
    roe_linear = short_long*leverage*(exit_price-entry_price)/entry_price*100

    #graph calculate single thread
    start = timer()
    y_roe_inverse = short_long*leverage*(quantity/entry_price - quantity/x)/entry_value*100
    end = timer()
    print('sequence: ', (end-start)*10000)

    y_normal = short_long*leverage*(x-entry_price)/entry_price*100

    # print(type(x))

    #graph calculate parallel
    pool = Pool(processes = 4)
    xList = x.tolist()
    tupleX = list(zip(xList))
    #time
    start = timer()
    result_list_roeInverse = pool.starmap(
                                partial(
                                    inverse_calculate, 
                                    quantity = quantity, 
                                    entry_price = entry_price, 
                                    short_long = short_long, 
                                    leverage = leverage, 
                                    entry_value = entry_value
                                    ), 
                                tupleX
                            )
    end = timer()
    pool.close()
    pool.join()
    
    print('parallel: ', (end-start)*10000)

    # print('\nroe inverse')
    # print('multi', result_list_roeInverse)
    # print('x: ', x)
    # print('x list: ', x.tolist())
    # print('\nsingle', y_roe_inverse)

    # print('parallel %f ' % (timeit.timeit(pool.map(find_x))))
    # pool.close()

# if(__name__=='__main__'):
# pool = Pool(processes = 4)
# y_fast_roe_inverse = pool.map(inverse_calculate, x)
# # y_fast_normal = pool.map(normal_calculate, x)
# pool.close()
# pool.join()

    # display(chart_, x, y_normal, y_roe_inverse, roe, roe_linear)