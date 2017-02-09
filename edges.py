import numpy as np
import elevationmatrix as elemat
import ast
from scipy.ndimage.filters import laplace 
arr_list=None

with open('elevationmatrix') as f:
    arr_list=ast.literal_eval(f.read())
arr=np.array(arr_list)
new=laplace(arr)
elemat.save_image(new,new.min(),new.max(),'edges.bmp')
