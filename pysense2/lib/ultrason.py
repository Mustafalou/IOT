import utime
from machine import Pin

class Ultrason:
    number=0
    list_Ultrason=[]
    def __init__(self,pinecho,pintrigger,mode):
        Ultrason.list_Ultrason.append(self)
        self.active=0
        self.mode = mode
        self.echo = Pin(pinecho, mode=Pin.IN) 
        self.trigger =Pin(pintrigger,mode=Pin.OUT)
        self.trigger(0)
    def getDistance(self):
        self.trigger(0)
        utime.sleep_us(2)
        self.trigger(1)
        utime.sleep_us(10)
        self.trigger(0)
        while not self.echo():
            pass
        start = utime.ticks_us()
        while self.echo():
            pass
        finish = utime.ticks_us()
        utime.sleep_ms(20)
        distance = ((utime.ticks_diff(start, finish)) * .034)/2

        return distance
    @staticmethod
    def callback():
        Ultrason.list_Ultrason=[]
        Ultrason(Pin.exp_board.G7,Pin.exp_board.G16, "ENTER")
        Ultrason(Pin.exp_board.G22,Pin.exp_board.G17, "EXIT")
        while True:
            print(Ultrason.number)
            for i  in  range(2):
                uon = Ultrason.list_Ultrason[i]
                uoff = Ultrason.list_Ultrason[i-1]
                if  not uon.active:
                    if abs(uon.getDistance())<50:
                        uon.active=1
                        
                        if uoff.active:
                            if uoff.mode=="EXIT":
                                if Ultrason.number>0:
                                    Ultrason.number-=1
                            else:
                                Ultrason.number+=1
                            uon.active=0
                            uoff.active=0
                            utime.sleep_ms(500)
                
                    
                    


