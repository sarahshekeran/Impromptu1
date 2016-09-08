import threading

class TimerThread(threading.Thread):
    #Thread that executes a task every N seconds

    def __init__(self,func,interval=2,daemon=True):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = interval
        self._func = func
        self.setDaemon(daemon)

    def setInterval(self, interval):
        #Set the number of seconds we sleep between executing our task
        self._interval = interval
    
    def shutdown(self):
        #Stop this thread
        self._finished.set()
    
    def run(self):
        while 1:
            if self._finished.isSet(): return
            self._func()
            
	    #if negative, Run only once.
            if self._interval < 0:
                self._interval = 0
                self.shutdown()
            # sleep for interval or until shutdown
            self._finished.wait(self._interval)


