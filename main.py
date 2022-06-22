import numpy as np
import os

def search(filename,s):
    #search the key words:0 for no, 1 for yes
    f = open(filename, 'r')
    ls = f.readlines()
    p = []
    for m in ls:
        for n in m.split():
            p.append(n)
    s=s.lower()
    s=s.split()
    flag = 0
    for i in range(len(p)):
        if p[i].lower() == s[0]:
            for j in range(1,len(s)-1):
                if p[i+j].lower() == s[j]:
                    flag = 1
                else:
                    flag = 0
                    break
            if flag == 1:
                return 1
        else:
            continue
    return 0

def atomtyp(alist,s):
    for atom in alist:
        if s == atom:
            return 1
        else:
            continue
    return 0

def label(filename):
    #Determine the input:QE or VASP
    if search(filename,'CELL_PARAMETERS'):
        return 1 #1 for QE input
    elif search(filename,'direct'):
        return 2 #2 for vasp input
    else:
        return 0


def readvasp(filename):
    f = open(filename,'r')
    l = f.readlines()
    ls = []
    for item in l:
        if item.split():
            ls.append(item)
        else:
            continue
    sysn = str(ls[0])
    multi = float(ls[1])
    lv=[]
    for i in range(3):
        lv.append(ls[2+i].split())
    lv = np.array(lv,dtype='double')
    lv = multi * lv
    aname = ls[5].split()
    anum = ls[6].split()
    anum = np.array(anum,dtype='int')
    acat = []
    j = 0
    for item in ls[8:]:
        acat.append(item.split())
    return sysn,lv,aname,anum,acat

def readqe(filename):
    f=open(filename,'r')
    l = f.readlines()
    ls = []
    for item in l:
        if item.split():
            ls.append(item)
        else:
            continue
    cell = ls[1:4]
    ainf = ls[5:]
    acat = []
    atyp = []
    aname = []
    anum = []
    for a in ainf:
        aname.append(a.split()[0])
        acat.append(a.split()[1:])
    k = 0
    for atom in aname:
        if atomtyp(atyp,atom):
            k = k + 1
        else:
            atyp.append(atom)
            if k != 0:
                anum.append(k)
            k = 1
    anum.append(k)
    return cell,atyp,anum,acat

def writeqe(sysn,lv,aname,anum,acat):
    f = open('coordinate.txt','w+')
    f.write('CELL_PARAMETERS (angstrom)\n')
    for i in range(3):
        f.write('  '+str(lv[i][0])+'  '+str(lv[i][1])+'  '+str(lv[i][2])+'\n')
    f.write('ATOMIC_POSITIONS (crystal)\n')
    for k in range(len(anum)):
        for s in range(anum[k]):
            f.write(aname[k]+'  '+acat[sum(anum[:k])+s][0]+'  '+acat[sum(anum[:k])+s][1]+'  '+acat[sum(anum[:k])+s][2]+'\n')
    f.close()

def writevasp(cell,atyp,anum,acat):
    f = open('coordinate.vasp','w+')
    f.write('qe_to_vasp\n'+'1.0\n')
    for vec in cell:
        f.write(vec)
    for type in atyp:
        f.write(type+'  ')
    f.write('\n')
    for num in anum:
        f.write(str(num)+'  ')
    f.write('\n'+'direct\n')
    for cor in acat:
        for x in cor:
            f.write(x+' ')
        f.write('\n')
    f.close()

if os.path.exists('coordinate.txt') and not os.path.exists('coordinate.vasp'):
    #qe to vasp
    cell,atyp,anum,acat=readqe('coordinate.txt')
    writevasp(cell,atyp,anum,acat)
elif os.path.exists('coordinate.vasp') and not os.path.exists('coordinate.txt'):
    #vasp to qe
    sysn,lv,aname,anum,acat=readvasp('coordinate.vasp')
    writeqe(sysn,lv,aname,anum,acat)
elif os.path.exists('coordinate.vasp') and os.path.exists('coordinate.txt'):
    ind=input('vasp to qe(1) or qe to vasp(2)?\n')
    if int(ind)==1:#vasp to qe
        sysn, lv, aname, anum, acat = readvasp('coordinate.vasp')
        writeqe(sysn, lv, aname, anum, acat)
    elif int(ind)==2:#qe to vasp
        cell, atyp, anum, acat = readqe('coordinate.txt')
        writevasp(cell, atyp, anum, acat)
    else:
        print('invalid\n')
        exit()
else:
    print('no input\n')