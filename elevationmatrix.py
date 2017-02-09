import googlemaps
import Image
import sys
G=500
keys=['AIzaSyDRloy67JLh8SRAcCacyfZ9BdK-gIlvE40',
     'AIzaSyBtAmjb8XlPcg7Rhp6VQxsI31CetVuhFws',
     'AIzaSyDoTk-qVxVmjushtgcPlFE5Qm-emaixsDw']

def generate_arrays(point1, rad=50, step=10):
    """
    rad: promien w metrach
    step: w metrach, co ile ma byc pomiar
    0.000141 ~=10m
    /\ x
    |
    |       y
    |_______>
    """

    x1, y1 = point1
    lx=[]
    ly=[]
    rad= (rad/(step*G)+1)*step*G
    for i in range(-(rad/step)/2,(rad/step)/2):
        lx.append(x1+(i*step*0.0000141))
        ly.append(y1+(i*step*0.0000141))
    return lx, ly


def normalize(matrix,minimum, maximum):
    new_matrix=[]
    maximum-=minimum
    for line in matrix:
        new_matrix.append([int(((el-minimum)*255)/maximum) for el in line])
    return new_matrix


def create_matrix(lx,ly):
    """lx,ly listy punktow rosnaco"""
    matrix=[]
    for i in range(0, lx.__len__()-1):
        matrix.append([(lx[i],el) for el in ly])
    return matrix

def main():
    gmaps = googlemaps.Client(key=keys[2])
    point=(float(sys.argv[1]),float(sys.argv[2])) 
   # lx, ly = generate_arrays(tuple(gmaps.geocode("Ligota Ksiazeca 11a")[0]['geometry']['location'].values()))
    lx, ly = generate_arrays(point,int(sys.argv[3]),int(sys.argv[4]))
    matrix=create_matrix(lx,ly)
    print len(lx),len(ly)
    elevation_matrix=[]
    maximum=[]
    minimum=[]
    licznik=0
    for lst in matrix:
        wiersz=[]
        for i in range(len(lst)/G):    
            licznik+=1
            if licznik%20 == 0:
                print licznik
            wiersz.extend([el['elevation'] for el in gmaps.elevation(lst[i*G:(i+1)*G])])
        maximum.append(max(wiersz))
        minimum.append(min(wiersz))
        elevation_matrix.append(wiersz)
    with open('elevationmatrix','w') as f:
        f.write(str(elevation_matrix))
    maximum=max(maximum)
    minimum=min(minimum)
    with open('minmax','w') as f:
        f.write("min:{0}\nmax:{1}".format(minimum,maximum))
    normalized_matrix=normalize(elevation_matrix,minimum, maximum)
    img=Image.new('L',(normalized_matrix[0].__len__(),normalized_matrix.__len__()))
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i,j] = normalized_matrix[-(j+1)][i]
    img.save('/home/kgacek/image3.bmp')

if __name__=="__main__":
    main()
