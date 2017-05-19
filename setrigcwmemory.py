import argparse
import icomCIVUtils
import platform

class mainApp:
   def __init__(self):
      self.runApp()
      pass

   def getArgs(self):
      parser = argparse.ArgumentParser()
      parser.add_argument("-p", "--portname", 
         help="serial port name")
      parser.add_argument("-b", "--baudrate", 
         help="serial port baud rate")
      parser.add_argument("-a", "--civaddress", 
         help="CIV address")
      parser.add_argument("-m", "--memoryno",
         help="Rig memory slot (1-5) -- also requires --memorytext")
      parser.add_argument("-t", "--memorytext", 
         help="Text string to place in memory slot -- also requires --memoryno")
      args = parser.parse_args()
      return args

   def runApp(self):

      args = self.getArgs()
      
      #Set some defaults if not supplied by calller
      if (args.baudrate == None):
         #print("No baud rate specified -- setting to 19200...")
         args.baudrate = 19200
      if (args.civaddress == None):
         #print("No CIV address specified -- setting to 6E (IC-756-ProIII)...")
         args.civaddress = '6e'
      if (args.portname == None):
         os = platform.platform()
         if ('Windows' in os):
            args.portname = "COM3:"
         else:
            args.portname = "/dev/ttyS0"
         #print("No port name specified -- setting to{}".format(args.portname) )

      test = icomCIVUtils.icomCIVUtils(args.portname, args.baudrate, 0)
      
      if (args.memorytext == None):
         resp=test.getrig_cwmemory(test.sport, args.civaddress, args.memoryno)
         print("CW Memory {} = {}".format(args.memoryno, resp.decode("utf-8")))
      else:
         resp=test.setrig_cwmemory(test.sport, args.civaddress,
                                     args.memoryno, args.memorytext)


if(__name__ == '__main__'):
   app = mainApp()
