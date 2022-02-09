#単純多角形から凸多面体を折ることができるか
#チャック接着で検証
#一般化
import numpy as np
import copy
import pandas as pd

M=14
#角度情報
Arg=[[90,270,90,90,270,180,90,90,180,270,90,90,270,90],[],[],[],[],[],[],[],[]]
#頂点のナンバリング
N=[[1,2,3,4,5,6,7,8,9,10,11,12,13,14],[],[],[],[],[],[],[],[]]
#一時保管用配列
TMP=[[],[],[],[],[],[],[]]
#同値にみなす頂点の格納
V=[[[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14]],[],[],[],[],[],[],[]]

Equ=[]
T=[]

#チャック折り可否判定 0:可能 1:不可能
def check(i,n):
    i1=i % (M-2*n)
    i2=(i-1) % (M-2*n)
    i3=(i+1) % (M-2*n)
    if (Arg[n][i3]+Arg[n][i2])<361:
        return 0
    elif n==(int(M/2)-1):
        return 0
    else:
        return 1

#一回の折り関数
def ori(i,n):
    i1=i % (M-2*n)
    i2=(i-1) % (M-2*n)
    i3=(i+1) % (M-2*n)
    arg=copy.deepcopy(Arg[n])
    num=copy.deepcopy(N[n])
    ver=copy.deepcopy(V[n])
    tmp1=arg[i1]
    tmp2=arg[i2]
    tmp3=arg[i3]
    arg[i1]=tmp1
    arg[i2]=tmp2+tmp3
    arg[i3]=tmp2+tmp3
    v1=ver[num[i2]-1]
    v2=ver[num[i3]-1]
    for i in range(len(v1)):
        for j in range(len(v2)):
            y=v2[j] in ver[v1[i]-1]
            if y==False:
                ver[v1[i]-1].append(v2[j])
    for i in range(len(v2)):
        for j in range(len(v1)):
            y=v1[j] in ver[v2[i]-1]
            if y==False:
                ver[v2[i]-1].append(v1[j])
    if i2>i3:
        if i1<i2:
            arg.pop(i2);arg.pop(i1)
            num.pop(i2);num.pop(i1)
        else:
            arg.pop(i1);arg.pop(i2)
            num.pop(i1);num.pop(i2)
    else:
        if i1<i3:
            arg.pop(i3);arg.pop(i1)
            num.pop(i3);num.pop(i1)
        else:
            arg.pop(i1);arg.pop(i3)
            num.pop(i1);num.pop(i3)
    arg.extend([0,0])
    num.extend([0,0])
    Arg[n+1]=arg;N[n+1]=num
    V[n+1]=ver

#繰り返し関数
def saiki(i,n):
    ori(i,n)
    TMP[n]=N[n][i]
    n=n+1
    for j in range(M-2*n):
        Arg[n+2]=Arg[n+1];N[n+2]=N[n+1]
        if check(j,n)==0:
            if n==(int(M/2-1)):
                saikiend(j,n)
            else:
                saiki(j,n)

#最終曲面
def saikiend(i,n):
    ori(i,n)
    TMP[n]=N[n][i]
    T1=copy.deepcopy(TMP)
    T.append(T1)
    Equ.append(V[n+1])

def show(l):
    print(len(l))
    for i in range(len(l)):
        n=0
        for j in range(i+1,len(l)-n):
            print(i,j)
            if l[j]==l[i]:
                l.pop(j)
                n=n+1
    return l

#メイン関数
def main():
    for i in range(int(M/2)):
        V[0]=[[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14]]
        n=0 #カウンタ n=0が始点
        if check(i,n)==0:
            saiki(i,n)
    for i in range(len(Equ)):
        for j in range(len(Equ[i])):
            Equ[i][j].sort()
        Equ[i].sort()
    #同値分類
    #まず左右対称
    A=[]
    for i in range(len(Equ)):
        A.append([])
        for j in range(len(Equ[i])):
            A[i].append([])
            for k in range(len(Equ[i][j])):
                A[i][j].append(15-Equ[i][j][k])
            A[i][j].sort()
        A[i].sort()
    #同値でないものの数え上げ
    tmp=[0]
    for i in range(len(T)):
        m=0
        for j in range(len(tmp)):
            if Equ[tmp[j]]==Equ[i]:
                m=m+1
            if Equ[tmp[j]]==A[i]:
                m=m+1
        if m==0:
            tmp.append(i)
    print("同値で分類")
    print(len(tmp))
    for i in range(len(tmp)):
        arr=list(map(list, set(map(tuple, Equ[tmp[i]]))))
        arr.sort()
        print("折り順:", T[tmp[i]],"接着される点:",arr)

if __name__ == "__main__":
    main()
