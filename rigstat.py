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
      parser.add_argument("-d", "--rigcommand", 
                         help="command to rig\n\r \
                           on      = rig on\n\r \
                           off     = rig off\n \
                           freq    = display rig frequency\n \
                           mode    = display rig mode\n \
                           id      = display rig ID\n \
                           time    = set/display rig time\n \
                           hexdata = raw command to send in hex\n"),
      parser.add_argument("-t", "--newtime", 
                         help="New time (if setting rig time")
                          
      args = parser.parse_args()
      return args

   def runApp(self):

      args = self.getArgs()
      
      os = platform.platform()
      
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
         #print("No port name specified -- setting to {}".format(args.portname) )

      test = icomCIVUtils.icomCIVUtils(args.portname, args.baudrate, 0)

      if (args.rigcommand == None):
         print('Powering rig OFF...')
         #test = icomCIVUtils.icomCIVUtils(args.portname, args.baudrate, 0)
         test.sendciv_off(test.sport, args.civaddress)
      else:
         #test = icomCIVUtils.icomCIVUtils(args.portname, args.baudrate, 0)
         if (args.rigcommand.lower() == 'on'):
            print('Powering rig ON...')
            test.sendciv_on(test.sport, args.civaddress)
         elif (args.rigcommand.lower() == 'off'):
            print('Powering rig OFF...')
            test.sendciv_off(test.sport, args.civaddress)
         elif (args.rigcommand.lower() == 'freq'):
            freq = test.getrig_frequency(test.sport, args.civaddress)
            print("Frequency = {}".format(freq))
         elif (args.rigcommand.lower() == 'mode'):
            mode = test.getrig_mode(test.sport, args.civaddress)
            print("Mode = {}".format(mode))
         elif (args.rigcommand.lower() == 'id'):
            rig_id = test.getrig_ID(test.sport, args.civaddress)
            print("Rig ID = {:02x}".format(ord(rig_id)))
         elif (args.rigcommand.lower() == 'time'):
            if (args.newtime != None):
               time = test.setrig_time(test.sport, args.civaddress, args.newtime)
               print("Time = {}".format(time))
            else:
               time = test.getrig_time(test.sport, args.civaddress)
               print("Time = {}".format(time))
         else:
            resp=test.civcommand(test.sport, args.civaddress, args.rigcommand)
            test.hexdump(resp)



if(__name__ == '__main__'):
   app = mainApp()
