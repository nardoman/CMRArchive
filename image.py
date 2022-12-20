import png
import random
import math
import io
import IPython.display as ipd


red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)

cyan    = (  0, 255, 255)
magenta = (255,   0, 255)
yellow  = (255, 255,   0)

orange  = (255, 128,   0)

white   = (255, 255, 255)
black   = (  0,   0,   0)
grey    = (128, 128, 128)

class Immagine:
    '''Oggetto che contiene una immagine come lista di liste di colori (R,G,B) e che viene 
    direttamente visualizzate in IPython console/qtconsole/notebook col metodo _repr_png_'''
    def __init__(self, img):
        self.pixels = img
    def _repr_png_(self):
        '''Produce la rappresentazione binaria della immagine in formato PNG'''
        img = png.from_array(self.pixels, 'RGB')
        b = io.BytesIO()
        img.save(b)
        return b.getvalue()

def visd(img, didascalia=''):
    '''Visualizza una immagine in una console IPython seguita da una didascalia opzionale'''
    ipd.display(Immagine(img))
    if didascalia:
        print(didascalia)

def inside(img,x,y):
    '''controlla se le coordinate x, y sono dentro l'immagine'''
    w = len(img[0])
    h = len(img)
    return 0 <= x < w and 0 <= y < h

def create(iw,ih,c):
    '''crea una immagine ovvero una lista di liste del colore c larga iw e alta ih'''
    img = [ [ c for _ in range(iw) ] for _ in range(ih) ]
    return img

def save(filename, img):
    '''salva la immagine img nel file filename'''
    png_img = []
    for row in img:
        png_row = []
        for c in row:
            png_row += c
        png_img.append(png_row)
    with open(filename,'wb') as f:
        png.Writer(len(img[0]),len(img)).write(f,png_img)

def load(filename):
    '''carica l'immagine PNG dal file filename'''
    with open(filename,'rb') as f:
        iw, ih, png_img, _ = png.Reader(file=f).asRGB8()
        png_img = [ [ v for v in png_row ] for png_row in png_img ]
    img = []
    for png_row in png_img:
        row = []
        for i in range(0,len(png_row),3):
            row.append( (png_row[i+0],png_row[i+1],png_row[i+2]) )
        img.append( row )
    return img

def copy(dst,src,dx,dy,sx,sy,w,h):
    '''copia un rettangolo della immagine src alle coordinate sx,sy largo w ed alto h
    sulla immagine dst alle coordinate dx,dy'''
    for j in range(h):
        for i in range(w):
            di, dj = i+dx, j+dy
            si, sj = i+sx, j+sy
            if not inside(dst,di,dj): continue
            if not inside(src,si,sj): continue
            dst[dj][di] = src[sj][si]

def draw_quad_simple(img,x,y,w,h,c):
    '''disegna un rettangolo senza controllare se è all'interno della immagine img'''
    for j in range(y,y+h):
        for i in range(x,x+w):
            img[j][i] = c

def draw_quad(img,x,y,w,h,c):
    '''disegna sulla immagine img alle coordinate x,y un rettangolo di colore c largo w ed alto h'''
    for j in range(y,y+h):
        for i in range(x,x+w):
            if inside(img,i,j):
                img[j][i] = c

def draw_gradient_horizontal(img,c0,c1):
    '''colora l'immagine img con un gradiente orizzontale che va dal colore c0 al colore c1'''
    h, w = len(img), len(img[0])
    r0, g0, b0 = c0
    r1, g1, b1 = c1
    for i in range(w):
        u = i / w
        r = round(r0 * (1-u) + r1 * u)
        g = round(g0 * (1-u) + g1 * u)
        b = round(b0 * (1-u) + b1 * u)
        for j in range(h):
            img[j][i] = (r,g,b)

def draw_gradient_vertical(img,c0,c1):
    '''colora l'immagine img con un gradiente verticale che va dal colore c0 al colore c1'''
    h, w = len(img), len(img[0])
    r0, g0, b0 = c0
    r1, g1, b1 = c1
    for j in range(h):
        v = j / h
        r = round(r0 * (1-v) + r1 * v)
        g = round(g0 * (1-v) + g1 * v)
        b = round(b0 * (1-v) + b1 * v)
        for i in range(w):
            img[j][i] = (r,g,b)

def draw_gradient_quad(img,c00,c01,c10,c11):
    '''colora l'immagine img con un gradiente interpolato in modo che ai 4 angoli ci siano i 4 colori c00,c01,c10,c11'''
    h, w = len(img), len(img[0])
    for j in range(h):
        for i in range(w):
            u = i / w
            v = j / h
            c = [0,0,0]
            for k in range(3):
                c[k] = round(c00[k] * (1-u) * (1-v) + 
                             c01[k] * (1-u) * v +
                             c10[k] * u * (1-v) +
                             c11[k] * u * v)
            img[j][i] = tuple(c)

def draw_checkers(img,s,c0,c1):
    '''disegna sulla immagine img una scacchiera con quadrati di lato s e colori c0 e 01'''
    h, w = len(img), len(img[0])
    for jj in range(h//s + 1):
        for ii in range(w//s + 1):
            c = c1 if ((ii + jj) % 2) else c0
            draw_quad(img,ii*s,jj*s,s,s,c)

def draw_gradient_checkers(img,s,c0,c1):
    h, w = len(img), len(img[0])
    for j in range(h):
        for i in range(w):
            if (i//s + j//s) % 2: img[j][i] = c0
            else: img[j][i] = c1

def border(img,s,c):
    '''crea una nuova immagine aggiungendo ad img un bordo di colore c largo s'''
    h, w = len(img), len(img[0])
    ret = create(w+s*2,h+s*2,c)
    copy(ret,img,s,s,0,0,w,h)
    return ret

def flip_horizontal(img):
    '''crea l'immagine simmetrica rispetto all'asse verticale'''
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for j in range(h):
        for i in range(w):
            fi = w-1-i
            ret[j][i] = img[j][fi]
    return ret

def flip_vertical(img):
    '''crea l'immagine simmetrica rispetto all'asse orizzontale'''
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for j in range(h):
        for i in range(w):
            fj = h-1-j
            ret[j][i] = img[fj][i]
    return ret

def rotate_corner(img):
    '''crea l'immagine simmetrica rispetto alla diagonale principale'''
    h, w = len(img), len(img[0])
    ret = create(h,w,(0,0,0))
    for j in range(h):
        for i in range(w):
            ret[i][j] = img[j][i]
    return ret

def mosaic_nearest(img,s):
    '''crea una immagine a mosaico di lato s prendendo il colore dall'angolo in alto a sx di ciascun quadretto'''
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for jj in range(h//s):
        for ii in range(w//s):
            c = img[jj*s][ii*s]
            draw_quad(ret,ii*s,jj*s,s,s,c)
    return ret

def mosaic_average(img,s):
    '''crea una immagine a mosaico di lato s prendendo il colore dalla media di ciascun quadretto'''
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for jj in range(h//s):
        for ii in range(w//s):
            c = [0,0,0]
            n = 0
            for j in range(jj*s,(jj+1)*s):
                for i in range(ii*s,(ii+1)*s):
                    if inside(img, i, j):
                        n += 1
                        for idx in range(3):
                            c[idx] += img[j][i][idx]
            for idx in range(3):
                col = round(c[idx] / n)
                col = min(max(col, 0), 255)
                c[idx] = col
            draw_quad(ret,ii*s,jj*s,s,s,c)
    return ret

def mosaic_size(img,s):
    '''crea una immagine a mosaico bianco/nero con quadretti di lato proporzionale alla luminosità del quadretto'''
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for jj in range(h//s):
        for ii in range(w//s):
            r = 0
            n = 0
            for j in range(jj*s,(jj+1)*s):
                for i in range(ii*s,(ii+1)*s):
                    if inside(img, i, j):
                        n += 1
                        for idx in range(3):
                            r += img[j][i][idx]
            r = int(round(s * r / (n*3*255)))
            draw_quad(ret,ii*s+(s-r)//2,jj*s+(s-r)//2,r,r,(255,255,255))
    return ret

def scramble(img,s):
    '''crea una immagine che randomizza i pixel fino a distanza s'''
    random.seed(0)
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for j in range(h):
        for i in range(w):
            si = i + random.randint(-s,s)
            sj = j + random.randint(-s,s)
            si = max(0,min(w-1,si))
            sj = max(0,min(h-1,sj))
            ret[j][i] = img[sj][si]
    return ret
    
def invert(img):
    '''crea l'immagine negativa di img'''
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for j in range(h):
        for i in range(w):
            r, g, b = img[j][i]
            ret[j][i] = ( 255 - r, 255 - g, 255 - b)
    return ret

def _c(value,c):
    value = ((value - 128) * c) + 128
    return round( min(255,max(0,value)) )
    
def contrast(img,c):
    '''cre una immagine ottenuta aumentando/diminuendo il contrasto di un valore c (1=nulla, <1=diminuisce, >1=aumenta'''
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for j in range(h):
        for i in range(w):
            r, g, b = img[j][i]
            ret[j][i] = (_c(r,c), _c(g,c), _c(b,c))
    return ret
              
def lens_paraboloid(img,x,y,r,p):
    '''crea una immagine con effetto lente di raggio r centrata su x,y, con ingrandimento p 
    (ingrandisce se p>1, rimpicciolisce se p<1)'''
    h, w = len(img), len(img[0])
    ret = create(w,h,(0,0,0))
    for j in range(h):
        for i in range(w):
            li, lj = i - x, j - y
            if li*li+lj*lj < r*r:
                rr = math.sqrt(li*li+lj*lj) / r
                if rr > 0: ratio = rr ** p / rr
                else: ratio = 1
                ret[j][i] = img[int((j-y)*ratio+y)][int((i-x)*ratio+x)]
            else:
                ret[j][i] = img[j][i]
    return ret

