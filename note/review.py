#review

#1
nums = [randint(1,10) for i in range(2)]
nums
[2,4]


#2 (p275)
@decorator(dec_opt_args)
def func2Bdecorated(func_opt_args):
    
 
#3 (p278 11.4) 

#4 (p282 11.6)
def newfoo(arg1, arg2, *nkw, **kw):
    print 'arg1 is %s' % arg1
    print 'rag2 is %s' % arg2
    for eachNKW in nkw:
        print 'additional non-keyword arg: %s' % eachNKW
    for eachKW in kw.keys():
        print "additional keyword arg '%s': %s" % (eachKW, kw[eachKW])

newfoo('wolf', 3, 'projects', foo=90, bar=80)
        
arg1 is wolf
arg2 is 3
additional non-keyword arg: projects
additional keyword arg 'foo': 90
additional keyword arg 'bar' : 80
    
>>> def cc(*nkwargs, **kwargs):
	print nkwargs
	print kwargs

	
>>> cc('a', 'b', c=3, d=4)
('a', 'b')
{'c': 3, 'd': 4}
        

#5 (p286 11.7.1)
def add(x, y): return x + y   <=> lambda x, y: x + y
def add(x, y=2): return x + y <=> lambda x, y=2: x + y

