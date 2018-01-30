shellimport fileinput
import re
import sys
s1 = ['section .data','section .bss','section .text']
d1 = ['dd','db','dw']
rr = ['resd','resb']
lineno=[]
line_no=0
symname=[]
symsize=[]
symdu=[]
symno=[]
symadd=[]
symtsize = []
pass01 = []
lit_val = []
lit_no = []
opt = []
lst = []
add1 = []
add2 = []
add3 = []
msg = []
string = ''
add=0
reg32 = ['eax','ecx','edx','ebx','esp','ebp','esi','edi']
reg16 = ['ax','cx','dx','bx','sp','bp','si','di']
reg8 = ['al','cl','dl','bl','ah','ch','dh','bh']
ins = ['mov','add','sub','mul','div','push']
sec=['section .data','section .bss','section .text']
opcode = ['000','001','010','011','100','101','110','111']
opr = ['r8','r16','r32','imm','dword','word','byte']
vals = ['88','89','8A','8B','8C','8E','A0','A1','A2','A3','B0','B8','C6','C7']
mod = ['00','01','10','11']
a=":"
ln=0

def address(val):
    val = int(val)
    val = format(val,'x').upper()
    if(len(val)%2 != 0):
        val = ''.join(('0',val))
    return str(val).zfill(8)
def index(x):
    y = str(x)
    l = 8-len(y)
    for i in range(l):
        y = ''.join((' ',y))
    return y

def read_symadd(symname):
    ind1 = symname.index(symname)
    return symadd[ind1]
def read_symno(symname):
    ind1 = symname.index(symname)
    return symno[ind1]
#def read_symname(symno):
 #   ind1 = symno.index(symno)
  #  return symname[ind1]
def big_endian(val):
        val = int(val)
        val = format(val,'x').upper()
        if(len(val)%2 != 0):
                val = ''.join(('0',val))
        val = rev_big(val)
        k = 8 - len(val)
        for i in range(k):
                val = ''.join((val,'0'))
        return val

def rev_big(val):
    l = [val[i:i+2] for i in range(0,len(val),2)]
    l = l[::-1]
    l = ''.join(l)
    return l
with open("palindrome.asm") as f:
    for line in f:
        ln=ln+1
        line_no+=1
        s=line.split()
        #print(s)
        if len(s)>1:
            n=s[1].split(',')
            #print(n)
            l1=len(s)
        if (sec[0] in line) or (sec[1] in line) or (sec[2] in line) :
            pass01.append([index(line_no)," "," ","  ",line])
        if ("global" in line or "extern" in line):
            pass01.append([index(line_no)," "," ","  ",line])
        if ":" in line:
            #if s[0].endswith(a):
             #   s1=s[0].split(":")
              #  s2 = s1.strip(' ')
                lineno.append(line_no)
                symname.append(s[0])
                symsize.append("-")
                symdu.append("UD")
                symadd.append("00000000")
                symno.append(len(symno)+1)
                pass01.append([index(line_no),' ',' ',line])
        else:
            if len(s)==2:
                if s[0] in ins:
                    if s[0]=='mov':
                        k = s[1].split(',')

                        if k[0] in reg32 and k[1] in reg32:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),reg32.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                        if k[0] in reg16 and k[1] in reg16:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg16.index(k[0])),reg16.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                        if k[0] in reg8 and k[1] in reg8:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg8.index(k[0])),reg8.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                        if k[0] in reg32 and 'dword' in k[1]:
                            lin = line.replace("\n",'')
                            #g = k[1].split('[')
                            #u = g[1].split(']')
                            #d = read_symname(u[0]) 
                            #pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),reg32.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                        if 'dword' in k[0] and k[1] in reg32:
                            lin = line.replace("\n",'')
                            s_no = read_symno(symname)
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),reg8.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                        if k[0] in reg16 and 'word' in s[1]:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),reg8.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                        if 'word' in k[0] and k[1] in reg16 :
                            lin = line.replace("\n",'')
                            pass1 = '#reg%d,reg%d'%((reg32.index(k[0])),reg8.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                        if k[0] in reg8 and 'byte' in k[1]:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg8.index(k[0])),reg32.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                        if 'byte' in k[0] and k[1] in reg8:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),reg8.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op1',pass1,"\n"])
                    elif s[0]=='add':
                        if k[0] in reg32 and k[1] in reg32:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),reg32.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                        if k[0] in reg16 and k[1] in reg16:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg16.index(k[0])),reg16.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                        if k[0] in reg8 and k[1] in reg8:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg8.index(k[0])),reg8.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                        if k[0] in reg32 and k[1] in reg16:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),reg16.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                        if k[0] in reg32 and k[1] in reg8:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),reg8.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                        if k[0] in reg16 and k[1] in reg8:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg16.index(k[0])),reg8.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                        if k[0] in reg32 and k[1].isdigit() == True:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),lit_no[0].index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                        if k[0] in reg16 and k[1].isdigit() == True:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),lit_no.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                        if k[0] in reg8 and k[1].isdigit() == True:
                            lin = line.replace("\n",'')
                            pass1 = 'reg%d,reg%d'%((reg32.index(k[0])),lit_no.index(k[1]))
                            pass01.append([index(line_no),' ',lin,"   ",'#op2',pass1,"\n"])
                   
            if len(s)>2:
                if s[1]=="db":
                    lineno.append(line_no)
                    symname.append(s[0])
                    symsize.append("1")
                    symdu.append("D")
                    symadd.append(address(add))
                    add=add+4
                    symno.append(len(symno)+1)
                    pass01.append([index(line_no),' ',' ',line])
                if s[1]=="dd":
                    q = line.split()
                    z = q[2].split(',')
                    z = len(z)
                    symtsize.append(z*4)
                    lineno.append(line_no)
                    symname.append(s[0])
                    symsize.append("4")
                    symdu.append("D")
                    symadd.append(address(add))
                    add=add+4
                    symno.append(len(symno)+1)
                    pass01.append([index(line_no),' ',' ',line])
                if s[1]=="dw":
                    q = line.split()
                    symtsize.append(z*4)
                    lineno.append(line_no)
                    symname.append(s[0])
                    symsize.append("4")
                    symdu.append("D")
                    symadd.append(address(add))
                    add=add+4
                    symno.append(len(symno)+1)
                    pass01.append([index(line_no),' ',' ',line])
                if s[1]=="dq":
                    q = line.split()
                    symtsize.append(z*8)
                    lineno.append(line_no)
                    symname.append(s[0])
                    symsize.append("8")
                    symdu.append("D")
                    symadd.append(address(add))
                    add=add+4
                    symno.append(len(symno)+1)
                    pass01.append([index(line_no),' ',' ',line])
                if s[1]=="resb":
                    q = line.split()
                    symtsize.append(len(q[2])*1)
                    lineno.append(line_no)
                    symname.append(s[0])
                    symsize.append("1")
                    symdu.append("D")
                    symadd.append(address(add))
                    add=add+4
                    symno.append(len(symno)+1)
                    pass01.append([index(line_no),' ',' ',line])
                if s[1]=="resd":
                    q = line.split()
                    symtsize.append(len(q[2]*4))
                    lineno.append(line_no)
                    symname.append(s[0])
                    symsize.append("4")
                    symdu.append("D")
                    symadd.append(address(add))
                    add=add+4
                    symno.append(len(symno)+1)
                    pass01.append([index(line_no),' ',' ',line])
                if s[1]=="resw":
                    q = line.split()
                    symtsize.append(len(q[2]*4))
                    lineno.append(line_no)
                    symname.append(s[0])
                    symsize.append("4")
                    symdu.append("D")
                    symadd.append(address(add))
                    add=add+4
                    symno.append(len(symno)+1)
                    pass01.append([index(line_no),' ',' ',line])
                if s[1]=="resq":
                    q = line.split()
                    symtsize.append(len(q[2]*8))
                    lineno.append(line_no)
                    symname.append(s[0])
                    symsize.append("8")
                    symdu.append("D")
                    symadd.append(address(add))
                    add=add+4
                    symno.append(len(symno)+1)
                    pass01.append([index(line_no),' ',' ',line])

#---------------------------------------MOV-----------------------#
line_no = 1
def add_Count(val):
    val = int(val)
    val = format(val,'x').upper()
    if len(val)%2 != 0:
        val = ''.join(('0',val))
    return str(val).zfill(8)

for line in fileinput.input("palindrome.asm"):
    line = line.split("\n")
    s.append(line)
    #print s
if(sec[0] == s[0][0]):
    #print hello
    lst.append([index(line_no)," ","\t\t\t\t",s[0][0]])
    line_no += 1
    for i in range(1,15):
        x = map(int,re.findall('\d+', s[i][0]))
        if(d1[0] in s[i][0]):
            if(len(s[i][0]) < 15):
                lst.append([index(line_no)," ",address(add)," ",big_endian(x[0]), "\t\t" ,s[i][0]])
                symname.append(s[i][0][1])
                symadd.append(address(add))
                add1.append(address(add))
                add = add + 4
                line_no += 1
            if(d1[1] in s[i][0]):
                msg = s[i][0].split('"')
                #print msg
                msg = msg[1]+msg[2]
                msg = msg.replace(',','')
            if(len(msg) > 9):
                for j in range(0,9):
                    string += (str(format(ord(str(msg[j])),'x'))).upper()
                string = string + '-'
                lst.append([index(line_no)," ",address(add)," ",string,"\t",s[i][0]])
                add1.append(address(add))
                add = add + 8
                line_no += 1
                string = ''
                for j in range(10,len(msg)):
                    string += (str(format(ord(str(msg[j])),'x')))
                lst.append([index(line_no)," ",address(add + 1)," ",string,"\t"])
                add1.append(address(add))
                line_no += 1
                add = add + (len(msg) - 9)
            if(len(msg) < 9):
                string = ''
                for j in range(0,len(msg)):
                    string += (str(format(ord(str(msg[j])),'x'))).upper()
                string = string
                lst.append([index(line_no)," ",address(add)," ",string,"\t\t\t",s[i][0]])
                add1.append(address(add))
                add = add + len(msg)
                line_no += 1
    lst.append(["     ",line_no," "])
    line_no += 1
    add = 0
    for j in range(len(s)):
        if(sec[1] == s[j][0]):
            lst.append([index(line_no)," ","\t\t\t\t",s1[1]])
            line_no += 1
            for m in range(1,20):
                bss = s[m][0].split('"')
                if(rr[0] in bss[0]):
                    x = map(int,re.findall('\d+', code[m][0]))
                    x[0] = 4 * x[0]
                    y = format(x[0],'x').upper()
                    lst.append([index(lin_no)," ",address(add)," ","<res",bss_assem(y),">", "\t\t" ,s[m][0]])
                    add2.append(address(add))
                    add = add + (x[0])
                    line_no += 1
            
                if(rr[1] in bss[0]):
                    x = map(int,re.findall('\d+', s[m][0]))
                    x[0] = 1 * x[0]
                    y = format(x[0],'x').upper()
                    lst.append([index(line_no)," ",address(add)," ","<res",bss_assem(y),">", "\t\t" ,s[m][0]])
                    add2.append(address(add))
                    add = add + x[0]
                    line_no += 1
    lst.append(["     ",line_no," "])
    line_no += 1
#------------------------------------------------------------------#
def gen_opcode(s):
    if(s[0] in reg32 and s[1] in reg32):
        ind1 = reg32.index(s[0])
        ind2 = reg32.index(s[1])
        x = mod[0] + opcode[ind2] + opcode[ind1]
        x1 = x[0:4]
        x2 = x[4:]
        x1 = format(int(x1,2),'x').upper()
        x2 = format(int(x2,2),'x').upper()
        return "89"+x1+x2

    if(s[0] in reg16 and s[1] in reg16):
        ind1 = reg16.index(s[0])
        ind2 = reg16.index(s[1])
        x = mod[0] + opcode[ind2] + opcode[ind1]
        x1 = x[0:4]
        x2 = x[4:]
        x1 = format(int(x1,2),'x').upper()
        x2 = format(int(x2,2),'x').upper()
        return "6689"+x1+x2

    if(s[0] in reg8 and s[1] in reg8):
        ind1 = reg8.index(s[0])
        ind2 = reg8.index(s[1])
        x = mod[0] + opcode[ind2] + opcode[ind1]
        x1 = x[0:4]
        x2 = x[4:]
        x1 = format(int(x1,2),'x').upper()
        x2 = format(int(x2,2),'x').upper()
        return "88"+x1+x2
    
    if(s[0] in reg32 and 'dword' in s[1]):
        if(s[0] == reg32[0]):
            return "A1"
        else:
            ind1 = reg32.index(s[0])
            x = mod[1] + opcode[ind1] + "101" 
            x1 = x[0:4]
            x2 = x[4:]
            x1 = format(int(x1,2),'x').upper()
            x2 = format(int(x2,2),'x').upper()
            return "8B"+x1+x2
    if('dword' in s[0] and s[1] in reg32):
        if(s[1] == reg32[0]):
            return "A3"
        else:
            ind1 = reg32.index(s[1])
            x = mod[1] + opcode[ind1] + "101" 
            x1 = x[0:4]
            x2 = x[4:]
            x1 = format(int(x1,2),'x').upper()
            x2 = format(int(x2,2),'x').upper()
            return "89"+x1+x2
        
    if(s[0] in reg16 and 'word' in s[1]):
        if(s[0] == reg16[0]):
            return "A1"
        else:
            ind1 = reg16.index(s[0])
            x = mod[1] + opcode[ind1] + "101" 
            x1 = x[0:4]
            x2 = x[4:]
            x1 = format(int(x1,2),'x').upper()
            x2 = format(int(x2,2),'x').upper()
            return "8B"+x1+x2
        
    if('word' in s[0] and s[1] in reg16):
        if(s[1] == reg16[0]):
            return "66A3"
        else:
            ind1 = reg16.index(s[1])
            x = mod[1] + opcode[ind1] + "101" 
            x1 = x[0:4]
            x2 = x[4:]
            x1 = format(int(x1,2),'x').upper()
            x2 = format(int(x2,2),'x').upper()
            return "6689"+x1+x2
        
    if(s[0] in reg8 and 'byte' in s[1]):
        ind1 = reg8.index(s[0])
        x = mod[1] + opcode[ind1] + "101" 
        x1 = x[0:4]
        x2 = x[4:]
        x1 = format(int(x1,2),'x').upper()
        x2 = format(int(x2,2),'x').upper()
        return "8A"+x1+x2
        
    if('byte' in s[0] and s[1] in reg8):
        if(s[1] == reg8[0] or s[1] == reg8[4]):
            return "A2"
        else:
            ind1 = reg16.index(s[1])
            x = mod[1] + opcode[ind1] + "101" 
            x1 = x[0:4]
            x2 = x[4:]
            x1 = format(int(x1,2),'x').upper()
            x2 = format(int(x2,2),'x').upper()
            return "89"+x1+x2
        
    if(s[0] in reg32 and s[1].isdigit() == True):
        x = format(int(s[1]),'08X').upper()
        x = rev_big(x)
        return "B8" + x
    
    if(s[0] in reg16 and s[1].isdigit() == True):
        x = format(int(s[1]),'X').upper()
        x = rev_big(x)
        return "66B8" + x
    
    if(s[0] in reg8 and s[1].isdigit() == True):
        x = format(int(s[1]),'02X').upper()
        x = rev_big(x)
        return "B0" + x
add = 0
for l in range(len(s)):
    if(sec[2] == s[l][0]):
        for n in range(len(s)):
            txt = s[n][0].split('\t')
            #print txt
            text = txt
            if(len(text) > 1):
                inst = text[1].split(' ')
                if(ins[0] in inst):
                    yo = inst[1].split(',')
                    if(yo[0] in reg32 and yo[1] in reg32):
                        op = gen_opcode(yo)
                        lst.append([(line_no)," ",add_Count(address(add))," ",op,"\t\t\t",s[n][0]])
                        line_no += 1
                        add = add + len(op)/2
                    if(yo[0]in reg16 and yo[1]in reg16):
                        op = gen_opcode(yo)
                        lst.append([(line_no)," ",add_Count(address(add))," ",op,"\t\t\t",s[n][0]])
                        line_no += 1
                        add = add + len(op)/2
                    if(yo[0]in reg8 and yo[1]in reg8):
                        op = gen_opcode(yo)
                        lst.append([(line_no)," ",add_Count(address(add))," ",op,"\t\t\t",s[n][0]])
                        line_no += 1
                        add = add + len(op)/2   
#------------------------------------------------------------------#
print("                         LITERAL TABLE                      ")
print("\nLIT_NO\t\tLIT_VAL\t\tHEX_VAL")
with open("palindrome.asm") as f:
    line1=f.read()
    z= line1.split()
    #print(z)
    for i in range (0,len(z)):
        if(z[i]=="mov" or z[i]=="add" or z[i]=="cmp"):
            a =z[i+1].split(',')
            #print(a)
            if(a[1].isdigit()):
                lit_val.append(a[1])
                #print (lit_val)
for i in range(0,len(lit_val)):
        hex_val = hex(int(lit_val[i]))
        #lit_no = (str(i+1)
        lit_no.append(str(i+1))
        #print (lit_no)
        print ("\n  "+lit_no[i]+"\t\t   "+lit_val[i]+"\t\t  "+hex_val)
print("\n")

#------------------------------------------------------------------#
new_fp = open('symbol','w+')
bind = zip(symadd,lineno,symno,symname,symsize,symdu)
new_fp.write("SYMBOL_ADDRESS\tLINE_NO\t\tSYMBOL_NO\tSYMBOL_NAME\tSYMBOL_SIZE\tSYMBOL_DU\n")
print_style = '{:<18}{:<19}{:<13}{:<16}{:<15}{}'
for i,(symadd,lineno,symno,symname,symsize,symdu) in enumerate(bind):
    new_fp.write(print_style.format(symadd,lineno,symno,symname,symsize,symdu))
    new_fp.write("\n")
    
new_fp1 = open('pass_01','w+')
for i in range(len(pass01)):
    new_fp1.write(str(' '.join(pass01[i])))

for k in range(len(lst)):
     lst[k].append("\n")
lst = [item for sublist in lst for item in sublist]
#print manil
new_fp2 = open('lst','w+')
for k in range(len(lst)):
    new_fp2.write(str(lst[k]))


