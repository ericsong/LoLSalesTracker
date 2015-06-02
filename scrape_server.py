import threading
import scrape as LWL

def f():
  # do something here ...
  data = LWL.checkForNewSales()
  for sale in data:
    print sale['title']
    print sale['champs']
    print sale['skins']

  # call f() again in 60 seconds
  threading.Timer(60, f).start()

# start calling f now and every 60 sec thereafter
f()
