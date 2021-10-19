from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
import matplotlib.pyplot as plt
# Create your views here.


def index(request):
    path = '/Users/derekdong/Documents/EasyFoundWarehouseSystem/templates/data/qvBox-warehouse-data-f21-v01.txt'
    request.session['path'] = path
    data = read(path)
    x, y = find_column_row(data)
    shelf = location(data)
    shelf_loc = exchange(list(shelf.keys()), x, y)
    #
    val = 0
    return render(request, "graph.html", {'x': x, 'y': y, 'shelf_location': shelf_loc, 'val': val})


# read the data from txt files
def read(path):
    data = pd.read_csv(path, sep="\t", header=None)
    data.columns = ["ProductID", "xLocation", "yLocation"]
    data_int = data.astype(int)
    return data_int


# Find the number of columns and rows
def find_column_row(data):
    x_max = data.max()['xLocation']
    y_max = data.max()['yLocation']
    return x_max+2, y_max+2


# Use dictionary to store the locations of shelves (key: location, value: [productID])
def location(data):
    x = (data['xLocation'] + 1).tolist()
    y = (data['yLocation'] + 1).tolist()
    pid = data['ProductID'].tolist()
    shelf = store(x,y,pid)
    return shelf


# the sub function  of the method (location)
def store(x, y, pid):
    shelf = {}
    for i in range(len(x)):
        #
        x_str = judge(x[i])
        y_str = judge(y[i])
        #
        key = x_str + y_str
        if key in list(shelf.keys()):
            shelf[key].append(pid[i])
        else:
            shelf[key] = [pid[i]]

    return shelf


# Change the shelf location from string to integer (td of the table)
def exchange(key, x, y):
    list_int = []
    for i in key:
        xn = int(i[0:2])
        yn = int(i[2:4])
        res = (y + 1 - yn - 1) * (x + 1) + xn
        list_int.append(res)
    return list_int


# according to the product id, search for the location
def search(request):
    value = request.GET['pid']
    #
    path = request.session['path']
    data = read(path)
    x, y = find_column_row(data)
    shelf = location(data)
    shelf_loc = exchange(list(shelf.keys()), x, y)
    #
    target = ''
    for i, j in shelf.items():
        if int(value) in j:
            target = i
            break
    xn = int(target[0:2])
    yn = int(target[2:4])
    res = (y + 1 - yn - 1) * (x + 1) + xn
    #
    path = draw(x, y, xn, yn)
    path_num = exchange(path, x, y)

    return render(request, "graph.html", {'x': x, 'y': y, 'shelf_location': shelf_loc, 'res':res, 'path':path_num, 'val':value})


#produce the route
def draw(x, y, xn, yn):
    path = []
    for i in range(2, yn):
        y_str = judge(i)
        path.append('01'+y_str)
    for j in range(1, xn+1):
        x_str = judge(j)
        path.append(x_str+str(yn-1))
    return path

# judge whether the number is > 0 or not
def judge(e):
    if e < 10:
        tr = '0' + str(e)
    else:
        tr = str(e)
    return tr
