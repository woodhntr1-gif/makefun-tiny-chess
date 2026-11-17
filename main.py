import sys
V=[0,100,320,330,500,900,0]
ND=[-33,-31,-18,-14,14,18,31,33]
BD=[-17,-15,15,17];RD=[-16,-1,1,16]
CC=[(1,4,6,(5,6)),(2,4,2,(1,2,3)),(4,116,118,(117,118)),(8,116,114,(113,114,115))]
F="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
Q=[i for i in range(128)if not i&0x88]
B=[0]*128;H=[];S=C=N=0;E=-1
K=lambda m:10*V[abs(B[(m>>7)&127])]-V[abs(B[m&127])]
def AT(s,a):
 for D,T in(((-15*a,-17*a),1),(ND,2),(BD+RD,6)):
  for d in D:
   if not(s+d)&0x88 and B[s+d]==a*T:return 1
 for D,T in((BD,3),(RD,4)):
  for d in D:
   j=s+d
   while not j&0x88 and not B[j]:j+=d
   if not j&0x88 and B[j]in(a*T,a*5):return 1
 return 0
def GN():
 M=[];d=16*S;A=lambda j:i|j<<7|(5<<14 if(j>>4)%7==0 else 0)
 for i in Q:
  t=B[i]*S
  if t<=0:continue
  if t==1:
   j=i+d
   if not B[j]:
    M.append(A(j))
    if(i>>4)==6-5*(S>0)and not B[i+2*d]:M.append(i|(i+2*d)<<7)
   for x in(d-1,d+1):
    j=i+x
    if not j&0x88 and(B[j]*S<0 or j==E):M.append(A(j))
  elif t in(2,6):
   for x in ND if t==2 else BD+RD:
    j=i+x
    if not j&0x88 and B[j]*S<=0:M.append(i|j<<7)
   if t==6:
    for bt,k,t2,em in CC:
     if C&bt and k==i and all(not B[x]for x in em)and not any(AT(x,-S)for x in(k,(k+t2)//2,t2)):M.append(k|t2<<7)
  else:
   for x in BD if t==3 else RD if t==4 else BD+RD:
    j=i+x
    while not j&0x88:
     if B[j]*S>0:break
     M.append(i|j<<7)
     if B[j]:break
     j+=x
 return M
def MK(m):
 global S,C,E,N;N+=1
 if N>60000:N=N/0
 f=m&127;t=(m>>7)&127;pr=m>>14;p=B[f];c=B[t]
 H.append((m,c,C,E))
 if p*S==1 and t==E and not c:B[t-16*S]=0
 B[t]=pr*S if pr else p;B[f]=0
 if p*S==6 and abs(t-f)==2:
  rf,rt=(f+3,f+1)if t>f else(f-4,f-1);B[rt]=B[rf];B[rf]=0
 for s,n in((4,12),(116,3),(0,13),(7,14),(112,7),(119,11)):
  if f==s or t==s:C&=n
 E=f+16*S if p*S==1 and abs(t-f)==32 else-1;S=-S
def UM():
 global S,C,E
 m,c,C,E=H.pop();S=-S;f=m&127;t=(m>>7)&127;p=B[t]
 if m>>14:p=S
 B[f]=p;B[t]=c
 if p*S==1 and t==E and not c:B[t]=0;B[t-16*S]=-S
 if p*S==6 and abs(t-f)==2:
  rf,rt=(f+3,f+1)if t>f else(f-4,f-1);B[rf]=B[rt];B[rt]=0
def LG():
 R=[]
 for m in GN():
  MK(m)
  if not AT(B.index(-S*6),S):R.append(m)
  UM()
 return R
def EV():
 s=0
 for i in Q:
  p=B[i]
  if p:
   t=abs(p);r=i>>4;u=r if p>0 else 7-r;cn=7-abs(3.5-(i&7))-abs(3.5-r)
   s+=(V[t]+[0,u*6,cn*8,cn*5,0,cn,-cn*3][t])*(1 if p>0 else-1)
 return s*S
def QS(a,b):
 if S*6 not in B:return-100000
 e=EV()
 if e>=b:return b
 a=max(a,e)
 for m in GN():
  if B[(m>>7)&127]or m>>14:
   MK(m);s=-QS(-b,-a);UM()
   if s>=b:return b
   if s>a:a=s
 return a
def NG(d,a,b):
 if S*6 not in B:return-100000+d
 if d==0:return QS(a,b)
 M=GN()
 if not M:return-100000-d if AT(B.index(S*6),-S)else 0
 M.sort(key=K,reverse=1)
 for m in M:
  MK(m);s=-NG(d-1,-b,-a);UM()
  if s>=b:return b
  if s>a:a=s
 return a
def SF(fen):
 global B,S,C,E,N;B=[0]*128;w=fen.split();r=7;f=0
 for ch in w[0]:
  if ch=='/':r-=1;f=0
  elif ch.isdigit():f+=int(ch)
  else:B[r*16+f]=(1 if ch.isupper()else-1)*("pnbrqk".index(ch.lower())+1);f+=1
 S=1 if len(w)<2 or w[1]=='w'else-1;C=0;E=-1;N=0
 if len(w)>2:C=sum(k for ch,k in zip("KQkq",(1,2,4,8))if ch in w[2])
 if len(w)>3 and w[3]!='-':E=(int(w[3][1])-1)*16+ord(w[3][0])-97
def MS(m):
 f=m&127;t=(m>>7)&127;return chr(97+(f&7))+str((f>>4)+1)+chr(97+(t&7))+str((t>>4)+1)+("q"if m>>14 else"")
def GO(g):
 global N;N=0;M=LG();best=M[0]
 try:
  for d in range(1,99):
   a=-10**9;bm=best
   for m in sorted(M,key=K,reverse=1):
    MK(m);s=-NG(d-1,-10**9,-a);UM()
    if s>a:a=s;bm=m
   best=bm
 except:pass
 print("bestmove "+MS(best),flush=1)
SF(F)
for L in sys.stdin:
 w=L.split()
 if w[0]=='uci':print("id name T\nuciok",flush=1)
 elif w[0]=='isready':print("readyok",flush=1)
 elif w[0]=='position':
  if w[1]=='startpos':SF(F)
  else:j=w.index('moves')if'moves'in w else len(w);SF(' '.join(w[2:j]))
  if'moves'in w:
   for x in w[w.index('moves')+1:]:
    f=(int(x[1])-1)*16+ord(x[0])-97;t=(int(x[3])-1)*16+ord(x[2])-97
    MK(f|t<<7|(("nbrq".index(x[4])+2 if len(x)>4 else 0)<<14))
 elif w[0]=='go':GO(w)
