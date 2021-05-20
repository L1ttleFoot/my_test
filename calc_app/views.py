from django.shortcuts import render
import math as m

class Vector():
  ''' Класс расчета NF -numeric factor, числовой множитель, после применения оператора к вектору '''
  def __init__(self, vec):
    self._vec = list(vec)
    self._NF=[]
    self._const=[]
  def vec(self):
    return tuple(self._vec)
  def NF(self):
    return '*'.join(['sqrt(n__%s)' % (VECTOR_INDEX[i] + num2str(j)) for i,j in self._NF])
  def const(self):
    if len(self._const)>0:
      return '*'.join(['(%s)' % (i) for i in self._const if len(i)>0])
    else:return ''

def born(vec,i):
  ''' Оператор рождения '''
  while len(vec._vec)<i+1:
      vec._vec.append(0)
  vec._vec[i] +=1
  vec._NF.append((i,vec._vec[i]))
def dead(vec,i):
  ''' Оператор уничтожения '''
  while len(vec._vec)<i+1:
      vec._vec.append(0)
  vec._NF.append((i,vec._vec[i]))
  vec._vec[i] -=1

def ksi_polinom(n:int)->list:
  ''' Разложение ksi()^j в полином  '''
  ksi = [dead,born]
  return [x[::-1] for x in product(ksi,repeat=n)]  # декартово произведение [[z,y,x] for x in a for y in a for z in a ]  


def CALC(bra,fksi,ket,ijk):
    ''' Считает матричный элемент <bra|fksi(ijk)|ket> fksi - оператор ksi()^j, ijk-список индексов на которые нужно подействовать '''
    const=''
    NF=''
    if isinstance(ket, Vector):
        const+=ket.const()
        NF+=ket.NF()
        ket=ket._vec
    if isinstance(bra, Vector):
        const+='*'+bra.const()
        NF+='*'+bra.NF()
        bra=bra._vec
    if isinstance(bra, tuple):bra=list(bra)
    if isinstance(ket, tuple):ket=list(ket)
    result = [Vector(ket) for i in range(len(fksi))]
    for vec,operations in zip(result,fksi):
        for op,i in zip(operations,ijk):
            op(vec,i) # применить оператор (A|a) к элементу номер i вектора vec
    RESULT=[]
    for i in result:
        if bra==i._vec: RESULT.append('*'.join([c for c in ['1',i.NF(),const,i.const(),NF,] if c!='']))
    return '(%s)'% ('+'.join([i for i in RESULT if i!=''])) if len(RESULT)>0 else 0

##################################################
    #расчет поправки к вектору состояния#
from collections import namedtuple
Index = namedtuple('Index','p q betta gamma nu')

def PP2(ket=[0,0,0,0],ind=0):
  '''Расчитывает вектор |ket,ind>'''
  if ind==0:return [[tuple(ket),'']]#Vector(ket)
  N=[]
  for i in [Index(*i) for i in product(range(0,ind+1), repeat=5) if sum(i)==ind and i[1]%2==0 and i[0]>0]:#(p,q,бетта,гамма,ню)
    KET=PP2(ket,i.gamma)
    fksi=ksi_polinom(i.p+2)
    NF1='(%s/%s)'%(i.p,ind)
    for bra in element_index(3*(i.betta+i.gamma)+i.p+2,ket): # i[0]+2=степени в которую будем возводить ksi
      if list(bra)==list(ket):continue
      if pravilo_otbora(bra,ket,i.p+2,i.betta,i.gamma)==0:continue
      DELTA=delta(bra,ket,i.q)
      if DELTA==0:continue
      BRA=PP2(bra,i.betta)
  ##  if i.betta!=i.nu: P=PP2(bra,i.nu)
##    else:P=[k for k in BRA]
      for ijk in INDEX(i.p,ket):
        A='(A__%s)'%(ijk) # это ангармоническая постоянная
        IJK =[ VECTOR_INDEX_MAP[x] for x in ijk]
        NF2=calc(BRA,KET,fksi,IJK,'s')
        if NF2==0:continue
        const='*'.join([k for k in [NF1,A,DELTA,NF2]])
        PP=[[V[0],'*'.join([k for k in [const,V[1]]if k!=''])] for V in PP2(bra,i.nu)]
        N+=PP
  return N

def calc(BRA,KET,fksi,IJK,flag='s'):
  '''Расчитывает матричный элемент вида <BRA,alfa|fksi(IJK)|KET,betta>
     flag='s' вернуть рассчитанные матричные элементы в виде строки 'M1+M2+...'
     flag='l' вернуть рассчитанные матричные элементы в виде списка [M1,M2,...]'''
  result=[]
  for i in BRA:
    for j in KET:
      A=CALC(i[0],fksi,j[0],IJK)
      if A==0:continue
      I='*'.join([k for k in [A,i[1],j[1]] if k!=''])
      if len(I)>0:result.append(I)
  if flag=='s': return '(%s)'%('+'.join([k for k in result if k!=''])) if len(result)>0 else 0
  if flag=='l': return [k for k in result if k!='']
##################################################
        #Расчет поправки к энергии
Index2 = namedtuple('Index2','p betta gamma')
def PE(vec=[0,0,0,0],ind=0,flag='s'):
  '''Расчитывает вектор |ket,ind>'''
  if ind%2==1:return 0
  N=[]
  X=[]
  for i in [Index2(*i) for i in product(range(0,ind+1), repeat=3) if sum(i)==ind and i[0]>0]:#(p,бетта,гамма)
    KET=PP2(vec,i.gamma)
    BRA=PP2(vec,i.betta)
    fksi=ksi_polinom(i.p+2)
    NF1='(%s/%s)'%(i.p,ind)
    E_ijk=[]
    for ijk in INDEX(i.p,vec):
      A='(A__%s)'%(ijk)
      IJK =[ VECTOR_INDEX_MAP[x] for x in ijk]
      E=calc(BRA,KET,fksi,IJK,'s')
      if E==0:continue
      E_ijk.append(str(sy.simplify(E+'*'+A)))
    E_ijk='+'.join(E_ijk)
    N.append('%s*%s'%(NF1,E_ijk))
  if flag=='s': return '+'.join(N)
  if flag=='l': return N
##################################################         
def pravilo_otbora(bra,ket,nksi,alfa,betta):
    k = sum(bra)-sum(ket)
    return 0 if (alfa+betta+nksi) % 2 != k % 2 else 1

def delta(bra,ket,q):
    if q==0:
        omega = ['(%s*omega__%s)' % (r-l,VECTOR_INDEX[i])  for i,(l,r) in enumerate(zip(bra,ket)) if l!=r]
        return '(1/(%s))' % '+'.join(omega) if omega else 0
    if q==2:
        A=delta(bra,ket,0)
        B='-'.join([PE(ket,2,'s'),PE(bra,2,'s')])
        return '*'.join([A,A,B]) if A else 0
    else: return 0
##################################################
## добавленные функции и библиотеки
from itertools import product, combinations_with_replacement
import numpy as np

def num2str(n):
  ''' Число в строку со знаком, ноль - пусто'''
  return '%+d' % n if n else ''

VECTOR_INDEX = 'ijklmnopq'
VECTOR_INDEX_MAP = {k:i for i,k in enumerate(VECTOR_INDEX)}
operator_index = lambda i: [ VECTOR_INDEX_MAP[x] for x in i]

def INDEX(n:int,vec)->list:
  ''' Индексы вектора vec, степени возмущения n, vec дб tuple для хэширования '''
  return [''.join(sorted(i)) for i in combinations_with_replacement(VECTOR_INDEX[:len(vec)], n+2) ]    

def element_index(n:int,vec):
  '''генерирует список с возможными значениями k для вектора m_i=n_i+k_i, k_i принимает значение [-n:n] и сумма модулей k_i   меньше или равна n
  пример: element_index(1,(0,0))== [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]'''
  ''' Индексы элементов к которым будут применяться операторы '''
  rng = range(-n,n+1)
  el = [i for i in product(rng, repeat=len(vec)) if sum(map(abs,i)) <=n]
  el = np.array(el) + vec
  return list(map(tuple,el))
###############################################
import sympy as sy
A__iiii, A__iiij, A__iiik, A__iiil, A__iijj, A__iijk, A__iijl, A__iikk, A__iikl, A__iill, A__ijjj, A__ijjk, A__ijjl, A__ijkk, A__ijkl, A__ijll, A__ikkk, A__ikkl, A__ikll, A__illl, A__jjjj, A__jjjk, A__jjjl, A__jjkk, A__jjkl, A__jjll, A__jkkk, A__jkkl, A__jkll, A__jlll, A__kkkk, A__kkkl, A__kkll, A__klll, A__llll = sy.symbols('A__iiii, A__iiij, A__iiik, A__iiil, A__iijj, A__iijk, A__iijl, A__iikk, A__iikl, A__iill, A__ijjj, A__ijjk, A__ijjl, A__ijkk, A__ijkl, A__ijll, A__ikkk, A__ikkl, A__ikll, A__illl, A__jjjj, A__jjjk, A__jjjl, A__jjkk, A__jjkl, A__jjll, A__jkkk, A__jkkl, A__jkll, A__jlll, A__kkkk, A__kkkl, A__kkll, A__klll, A__llll')
A__iii, A__iij, A__iik, A__iil, A__ijj, A__ijk, A__ijl, A__ikk, A__ikl, A__ill, A__jjj, A__jjk, A__jjl, A__jkk, A__jkl, A__jll, A__kkk, A__kkl, A__kll, A__lll = sy.symbols('A__iii, A__iij, A__iik, A__iil, A__ijj, A__ijk, A__ijl, A__ikk, A__ikl, A__ill, A__jjj, A__jjk, A__jjl, A__jkk, A__jkl, A__jll, A__kkk, A__kkl, A__kll, A__lll')
n__i, n__j, n__k, n__l=sy.symbols('n__i, n__j, n__k, n__l')
omega__i, omega__j, omega__k, omega__l=sy.symbols('omega__i, omega__j, omega__k, omega__l')

n__i=0
n__j=0
n__k=0
n__l=0

nn=['n__i',n__i,'n__j',n__j,'n__k',n__k,'n__l',n__l]

start_2=0
start_3=0
start_4=0
end_2=0
end_3=0
end_4=0
with open('AM1Anharm.log') as text_file:
    my_lines = text_file.readlines() 
    for num in range(len(my_lines)):
        if 'QUADRATIC' in my_lines[num]:
            start_2=num+9
        if 'CUBIC' in my_lines[num]:
            start_3=num+9
        if 'QUARTIC' in my_lines[num]:
            start_4=num+9
        if 'Num. of 2nd' in my_lines[num]:
            end_2=num-1
        if 'Num. of 3rd' in my_lines[num]:
            end_3=num-1
        if 'Num. of 4th' in my_lines[num]:
            end_4=num-1
            break
            
freq=''.join(my_lines[start_2:end_2])
c3=''.join(my_lines[start_3:end_3])
c4=''.join(my_lines[start_4:end_4])  
    
def const_repr(x):

    n_elem=len(x.split())
    n_str=len(x.split('\n'))-1
    n_rows=n_elem//n_str

    h=x.split()
    b=x.split()

    for i in range(len(b)):
        b[i]=float(b[i])

    const_list=[0]*n_str*2
    l=0
    for j in range(0,n_elem,n_rows):
        i_c=0
        j_c=0
        k_c=0
        o=[0]*((n_elem-3*n_str)//n_str)
        for i in range ((n_elem-3*n_str)//n_str):
            o[i]=h[i+j]
            if(o[i]=='1'):
                o[i]='i'
                i_c=i_c+1
            if(o[i]=='2'):
                o[i]='j'
                j_c=j_c+1
            if(o[i]=='3'):
                o[i]='k'
                k_c=k_c+1
        o.reverse()
        o.insert(0,'A__')
        if len(o)==3:
            o[0]='omega__'
            const_list[l]=''.join(o)
            const_list[l]=const_list[l][:-1]
            l=l+1
            const_list[l]=(b[j+((n_elem-3*n_str))//n_str])
            l=l+1
        else:
            factor=m.factorial(i_c)*m.factorial(j_c)*m.factorial(k_c)
            const_list[l]=''.join(o)
            l=l+1
            const_list[l]=(b[j+((n_elem-3*n_str))//n_str]/factor)*2**(-(((n_elem-3*n_str))//n_str/2))
            l=l+1
    return(const_list)

def final_repr():
    all_of_them=nn+const_repr(freq)+const_repr(c3)+const_repr(c4)
  
    final_eq=''
    for i in range(len(all_of_them)//2):
        print('(',all_of_them[i*2],',',all_of_them[i*2+1],')',',',sep="",end="")
        final_eq=final_eq+'('+str(all_of_them[i*2])+','+str(all_of_them[i*2+1])+')'+','
    final_eq=final_eq[:-1]
    final_eq='['+final_eq+']'
    return(final_eq)
    
def index(request):
    context = {}
    channel_id =final_repr()
    context['channel_id'] = channel_id
    return render(request, 'calc_app/index.html', context)