from vpython import *
#GlowScript 2.7 VPython

#verson 6.0

G=6.7e-11

#-----------#v5 dt speed
scene.caption = "Vary the rotation speed ratio: \n\n"
def setspeed(s):
    wt.text = '{:1.3f}'.format(s.value)

sl = slider(min=1e-3, max=1, value=1e-1, length=220, bind=setspeed, right=15)

wt = wtext(text='{:1.3f}'.format(sl.value))

scene.append_to_caption(' /s\n')

#-----------# v4 Add Pause/Run button
run = True
def Runbutton(b):
    global run
    if b.text == 'Pause':
        run = False
        b.text = 'Run'
    else:
        run = True
        b.text = 'Pause'
#-----------# v5 orbit custom bt
eL = False
def eO(i):
    global eL
    if i.text == "Earth's Orbit : Enable":
        eL = True
        i.text = "Earth's Orbit : Disable"
    else:
        eL = False
        i.text = "Earth's Orbit : Enable"
        
mL = False
def mO(b):
    global mL
    if b.text == "Moon's Orbit : Enable":
        mL = True
        b.text = "Moon's Orbit : Disable"
    else:
        mL = False
        b.text = "Moon's Orbit : Enable"
    
sL = False
def sO(b):
    global sL
    if b.text == "Satellite's Orbit : Enable":
        sL = True
        b.text = "Satellite's Orbit : Disable"
    else:
        sL = False
        b.text = "Satellite's Orbit : Enable"
    

b0=button(text='Pause', bind=Runbutton,pos=scene.title_anchor)
b1=button(text="Earth's Orbit : Enable", bind=eO)
b2=button(text="Moon's Orbit : Enable", bind=mO)
b3=button(text="Satellite's Orbit : Enable", bind=sO)

sc=vector(0,0,0)
sz=vector(0,0,-1)
sf=vector(0,0,0)
sm=vector(0,0,0)
#-----------# v6
scene.append_to_caption('\n')
scene.append_to_caption('A central object ')

def cam(p):
    global a
    val=p.selected
    if val=='Sun':
        a=0
    elif val=='Earth':
        a=1
    elif val=='Moon':
        a=2
    elif val=='Satellite':
        a=3
#-----------#v6
menu(choices=['Choose an object', 'Sun', 'Earth', 'Moon', 'Satellite'], index=0, bind=cam)

EMsystemd=vector(3.8e5,0,0) #v3 Distance within the Earth-Moon system 
MMsystemd=vector(3e4,0,0)
Sun=sphere(pos=vector(0,0,0),radius=6e6,color=color.yellow)
Sunlight=local_light(pos=Sun.pos,color=Sun.color)
#-----------# v3 Earth's orbit have disappeared
Earth=sphere(pos=vector(1.47e8,0,0),radius=6e3, color=color.cyan,make_trail=False,interval=1e-3,retain=10000)
#-----------# v3 Add the Moon
Moon=sphere(pos=Earth.pos+EMsystemd,radius=1e3, color=color.white,make_trail=False,interval=1e-3,retain=10000)
#-----------# v4 Add the Satellite
Moon2=sphere(pos=Earth.pos+EMsystemd+MMsystemd,radius=3e2, color=color.gray(0.5),make_trail=False,interval=1e-3,retain=10000)

Earth.m=6e24
#-----------# v2 Modified plant of velocity
Earth.p=vector(0,(G*2e30/1.47e8)**0.5,0)*Earth.m
Sun.m=2e30
#-----------# v3 Add the Moon and defined momentum
Moon.m=7.3e22
Moon.p=vector(0,(G*6e24/3.8e5)**0.5,0)*Moon.m
#-----------# v4 Add the Satellite and defined momentum
Moon2.m=1.4e20
Moon2.p=vector(0,(G*7.3e22/3e4)**0.5,0)*Moon2.m

autoscale = False

while True:
    dt=sl.value
    rate(300)
    if run:
        rse=-Earth.pos+Sun.pos
        Fse=-G*Sun.m*Earth.m*rse.hat/mag2(rse)
        #-----------# v3
        rem=-Moon.pos+Earth.pos
        Fem=-G*Earth.m*Moon.m*rem.hat/mag2(rem)
        #-----------# v4
        rmm=-Moon2.pos+Moon.pos
        Fmm=-G*Moon2.m*Moon.m*rmm.hat/mag2(rmm)
        #-----------#
        Earth.p=Earth.p-Fse*dt+Fem*dt
        Earth.pos=Earth.pos+(Earth.p/Earth.m)*dt
        #-----------# v3
        Moon.p=Moon.p-Fem*dt+Fmm*dt
        EMsystemd=EMsystemd+(Moon.p/Moon.m)*dt
        Moon.pos=Earth.pos+EMsystemd
        #-----------# v4
        Moon2.p=Moon2.p-Fmm*dt
        MMsystemd=MMsystemd+(Moon2.p/Moon2.m)*dt
        Moon2.pos=Moon.pos+MMsystemd
        #-----------#v6
        if a==0:
            scene.center=Sun.pos
        elif a==1:
            scene.center=Earth.pos
        elif a==2:
            scene.center=Moon.pos
        elif a==3:
            scene.center=Moon2.pos
    #-----------#v5
    Earth.make_trail=eL
    Moon.make_trail=mL
    Moon2.make_trail=sL
