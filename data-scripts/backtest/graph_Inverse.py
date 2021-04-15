import matplotlib.pyplot as plt 
import numpy as np 
  

def display(chart_):
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


quantity = 1
entry_price = 5
exit_price = 1
exit_price_c = exit_price-1
leverage = 1
short_long = int(input('long(1) or short(-1) : '))
chart_ = int(input('normal chart(1), inverse chart(2), all chart (3) : '))

#define x forward(long)(1) or backward(short))-1
if entry_price > exit_price:
    #start, stop(more 0.1 for graph display), step(0.1 graph จะได้ละเอียด)
    x = np.arange(entry_price, exit_price+(0.1*short_long), -0.1)
else :
    x = np.arange(entry_price, exit_price+(0.1*short_long), 0.1)
    
# print(x)

#ROE inverse calculate
entry_value = quantity/entry_price
exit_value = quantity/exit_price
profit = entry_value-exit_value
roe = profit/entry_value*100*leverage*short_long

#ROE linear calculate
roe_linear = short_long*leverage*(exit_price-entry_price)/entry_price*100

#graph calculate
y_roe_inverse = short_long*leverage*(quantity/entry_price - quantity/x)/entry_value*100
y_normal = short_long*leverage*(x-entry_price)/entry_price*100

display(chart_)