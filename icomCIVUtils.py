import serial
import binascii
from time import sleep
import argparse

class icomCIVUtils:

   def __init__(self, portname='', baudrate = 0, demo = 0):
      if (portname != ''):
         if (baudrate == 0):
            baudrate = 9600
         sport = self.civopen(portname, baudrate)
         if (demo):
            self.demo(sport)
         else:
            self.sport = sport
      pass

   def civopen(self, portname, baudrate, timeout = 3):
      ser = serial.Serial(port=portname,
                          baudrate=baudrate,
                          timeout = timeout
                          )
      self.sport = ser
      return ser

   def civcommand(self, port, address, data, echo = 1, rawdata=None):
      fulldata = binascii.unhexlify('FEFE'+address+'E0'+data)
      if (rawdata != None):
         fulldata += rawdata.encode('utf-8')
      fulldata += binascii.unhexlify('FD')
      port.write(fulldata)
      if (echo == 1):
          resp=self.civread(port, address)
      sleep(0.200)
      resp=self.civread(port, address)
      return resp

   def civread(self, port, address):
      resp = b'\x00'
      endchar = b'\xfd'
      nextchar=0
      while (nextchar != endchar):
         nextchar = port.read(1)
         resp+=nextchar
      return resp[1:] # Drop first byte 

   def sendciv_on(self, port, address):
      fulldata = binascii.unhexlify('FEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFEFE'+address+'E01801FD')
      port.write(fulldata)
      sleep(0.500)
      resp=self.civread(port, address)
      return resp

   def sendciv_off(self, port, address):
      resp=self.civcommand(port, address, '1800')
      #fulldata = binascii.unhexlify('FEFE'+address+'E01800FD')
      #port.write(fulldata)
      #sleep(0.200)
      #resp=self.civread(port, address)
      return resp
   
   def getrig_frequency(self, port, address):
      resp=self.civcommand(port, address, '03')
      rawfreq=self.bcdDigits(resp[5:10])
      rawfreq=rawfreq[::-1]
      i=0
      dfreq = ''
      for nb in rawfreq:
         if (i == 4):
            dfreq+='.'
         dfreq+=chr(nb + 0x30)
         i+=1
      return dfreq

   def getrig_ID(self, port, address):
      resp=self.civcommand(port, address, '1900')
      id = resp[6:7]
      #print ("Length = {}".format(len(resp)))
      #print ("Length = {}".format(len(id)))
      #print ("ID = {}".format(id))
      return id

   def getrig_time(self, port, address):
      resp=self.civcommand(port, address, '1A0516')
      bcdtime=self.bcdDigits(resp[7:9])
      bcdtime=bcdtime[::-1]
      i = 0
      ts = ''
      for nb in bcdtime:
         if (i==0):
            d1=chr(nb + 0x30)
         elif (i==1):
            d2=chr(nb + 0x30)
         elif (i==2):
            d3=chr(nb + 0x30)
         else:
            d4=chr(nb + 0x30)
         i+=1
      ts =  d3 + d4 + d1 + d2
      return ts

   def setrig_time(self, port, address, time):
      resp=self.civcommand(port, address, '1A0516'+time,0)
      #resp=self.getrig_time(port, address)
      return resp

   def getrig_mode(self, port, address):
      resp=self.civcommand(port, address, '04')
      rawMode=self.bcdDigits(resp[5:7])
      return rawMode

   def getrig_cwmemory(self, port, address, memory):
      ld = chr(48)+memory
      memstg = '1A02'+ld
      resp=self.civcommand(port, address, memstg)
      memtext=resp[7:54]
      return memtext

   def setrig_cwmemory(self, port, address, memory, memtext):
      ld = chr(48)+memory
      memstg = '1A02'+ld
      resp=self.civcommand(port, address, memstg, 1, memtext)
      rettext=resp[7:54]
      return rettext

   def bcdDigits(self, chars):
      resp = bytes(0)
      for char in chars:
         n1=int(char/16)
         n2=int(char%16)
         resp+=n2.to_bytes(1, byteorder='little')
         resp+=n1.to_bytes(1, byteorder='little')
      return resp
 
   def demo(self, port):
      resp=self.sendciv_on(port, '86')
      print("raw response: ", resp)
      return resp

   def hexdump(self, data):
      for b in data:
         print( "{:02x}".format(b), )
         
