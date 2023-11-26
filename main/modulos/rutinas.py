import numpy as np
import sympy as sp
from math import factorial


#####################################TAYLOR##################################
def taylor(f, x0, n):
    x = sp.symbols("x")
    p = 0
    for k in range(0, n + 1):
        df = sp.diff(f, x, k)
        df_x0 = df.evalf(subs={x: x0})
        T = (df_x0 * (x - x0) ** k) / factorial(k)
        p = p + T
    return p


def Cota_t(f, x_, n, xo):

    df = sp.diff(f, x, n + 1)
    df = sp.lambdify(x, df)
    u = np.linspace(min(x_, xo), max(x_, xo), 1000)
    Max = np.max(np.abs(df(u)))
    cota = Max * ((x_ - xo) ** 4) / factorial(n + 1)
    return cota


######################################CEROS#################################
def Biseccion(f, a, b, tol):
    if f(a) * f(b) > 0:
        print(f"La función no cumple el teorema en el intervalo")

    else:
        contador = 0
        while np.abs(b - a) > tol:
            c = (a + b) / 2
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
            contador += 1

        # print(f"La raiz de la función f es: {c}")
    return c


def Pos_falsa(f, a, b, tol):
    if f(a) * f(b) > 0:
        print(f"La función no cumple el teorema en el intervalo, busque otro intervalo")

    else:
        c = a - (f(a) * (a - b)) / (f(a) - f(b))
        while np.abs(f(c)) > tol:
            c = a - (f(a) * (a - b)) / (f(a) - f(b))
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c

    return c


def Newton(f, x0, tol):
    x=sp.symbols('x')
    df = sp.diff(f, x)
    N = x - f / df
    N = sp.lambdify(x, N)
    x1 = N(x0)

    while np.abs(x1 - x0) > tol:
        x0 = x1
        x1 = N(x0)

    return x1


def Secante(f, x0, x1, tol):
    x2 = x1 - f(x1) * (x0 - x1) / (f(x0) - f(x1))
    while np.abs(x2 - x1) > tol:
        x0 = x1
        x1 = x2
        x2 = x1 - f(x1) * (x0 - x1) / (f(x0) - f(x1))

    return x2


########################INTERPOLACIÓN##########################
def p_simple(xdata, ydata):
    x = sp.symbols("x")
    N = len(xdata)
    M = np.zeros([N, N])
    P = 0
    for i in range(N):
        M[i, 0] = 1
        for j in range(1, N):
            M[i, j] = M[i, j - 1] * xdata[i]
    ai = np.linalg.solve(M, ydata)
    for i in range(1, N):
        P = P + ai[i] * x**i

    return P


def lagrange(xdata, ydata):
    x = sp.symbols("x")
    N = len(xdata)
    P = 0
    for i in range(N):
        T = 1
        for j in range(N):
            if j != i:
                T = T * (x - xdata[j]) / (xdata[i] - xdata[j])
            P = P + T * ydata[i]

    return P
####################################################################################

def Euler(f,a,b,h,co):
    n = int((b-a)/h)
    t = np.linspace(a,b,n+1)
    yeu = [co]
    for i in range(n):
        yeu.append(yeu[i]+h*f(t[i],yeu[i]))

    return t,yeu

def Runge4(f,a,b,h,co):
    n = int((b-a)/h)
    t = np.linspace(a,b,n+1)
    yk = [co]
    for i in range(n):
        k1 = h*f(t[i],yk[i])
        k2 = h*f(t[i]+h/2,yk[i]+1/2*k1)
        k3 = h*f(t[i]+h/2, yk[i]+ 1/2*k2)
        k4 = h*f(t[i+1], yk[i]+k3)
        yk.append(yk[i]+1/6*(k1+2*k2+2*k3+k4))
    return t,yk

####################################################################################
def Trapecio(f,a,b,n):
    h=(b-a)/n
    S = 0
    for i in range(1,n):
      S+=f(a+i*h)
    I=h/2*(f(a)+2*S+f(b))
    return I

def simpson1_3(f,a,b,n):
  if(n%2!=0):
    #n= int(input("Ingrese un valor par para n => "))
    pass
  h = (b-a)/n
  S_i=0
  S_p=0
  for i in range(1,n):
    if i%2==0:
      S_p += f(a+i*h)
    else:
      S_i += f(a+i*h)

  I=(h/3)*(f(a)+2*S_p+4*S_i +f(b))
  return I

def simpson3_8(f,a,b,n):
  h = (b-a)/n
  S_m=0
  S_n=0
  for i in range(1,n):
    if i%3==0:
      S_m += f(a+i*h)
    else:
      S_n += f(a+i*h)

  I=(3*h/8)*(f(a)+2*S_m+3*S_n +f(b))
  return I