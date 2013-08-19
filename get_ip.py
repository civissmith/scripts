#!/usr/bin/python -B
################################################################################
# @Title: get_ip.py
#
# @Author: Phil Smith
#
# @Date: 17-Aug-2013 9:18 PM
#
# @Project: Motorola Surfboard Hack
#
# @Purpose: Logs into the Motorola Surfboard Router, gets the current WAN IP
#           address.
#
# Exit Codes:
# 0 - Success
# 1 - Could not find config file
# 2 - Could not get IP, MAC, duration and expiration
# @Revision:
# $Id: get_ip.py,v 1.2 2013/08/19 02:04:39 alpha Exp $
#
################################################################################
import re
import os
import sys
import fcntl
import socket
import struct
import urllib2

#
# Global Constants
#
RCFILE = os.path.expanduser("~") + '/.motorolarc' # This can be made user-independent.

#
# get_credentials() - Gets the username and password from the rc file.
# Returns (None, None) on error
#
def get_credentials():
  if not os.path.exists(RCFILE):
    print 'Could not find configuration file! (~/.motorolarc)'
    exit(1)
  #
  # RCFILE should have the following two lines
  # USER: <username>
  # PASSwORD: <password>
  #
  rc = open(RCFILE, 'r')
  for line in rc:
    name     = re.search(r'USER:\s*(.*)', line, re.IGNORECASE)
    password = re.search(r'PASSWORD:\s*(.*)', line, re.IGNORECASE)
    if name:
      uname = name.group(1)
    if password:
      passwd = password.group(1)
  rc.close()

  if uname and passwd:
    return uname, passwd
  return None, None
#
# End get_credentials
#

#
# main(): Main entry point of this utility
#
def main( ADMIN_NAME, ADMIN_PASSWD ):
  #
  # Set the router address and port, these could be made into arguments -
  # but I really don't care.
  #
  ROUTER_ADDR = '192.168.0.1'
  ROUTER_PORT = 80
  TIMEOUT = 2.5 # Seconds
  # On the Motorola Surfboard SGB6580, the WAN IP addess is on the RgSetup.asp page.
  WAN_IP_PAGE = 'http://' + ROUTER_ADDR + '/RgSetup.asp'
  LOGOUT_PAGE = 'http://' + ROUTER_ADDR + '/logout.asp'

  # Grab any TCP port - completely arbitrary.
  TCP_PORT = 45555
  
  #
  # The LOGIN string will attempt to login into the router.
  #
  # All headers are taken from Wireshark capture.
  # Host: header is set to mimic how Wireshark captured the data, instead of the normal
  #       ADDR, PORT form.
  LOGIN =  'POST /goform/login HTTP/1.1\r\n' +\
           'Host:%s\r\n' % ROUTER_ADDR  +\
           'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0\r\n' +\
           'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n' +\
           'Accept-Language: en-US,en;q=0.5\r\n' +\
           'Accept-Encoding: gzip, deflate\r\n' +\
           'Referer: http://%s/login.asp\r\n' % ROUTER_ADDR +\
           'Connection: keep-alive\r\n' +\
           'Content-Type: application/x-www-form-urlencoded\r\n' +\
           'Content-Length: 42\r\n\r\n' +\
           'loginUsername=%s&loginPassword=%s' % (ADMIN_NAME, ADMIN_PASSWD)
  
  socket.setdefaulttimeout(TIMEOUT)
  
  #
  # Hackish way to get the IP address of the active interface. The
  # null_socket is never used, other than to get the address.
  #
  null_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  null_socket.connect((ROUTER_ADDR, ROUTER_PORT))
  loc_addr = null_socket.getsockname()[0]
  
  #
  # Setup and send the login request
  #
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) # Internet socket using TCP
  
  # Allow the kernel to reuse the socket even if TIME_WAIT has not expired.
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
  # Bind the socket to the chosen address and open the multicast port.
  sock.bind((loc_addr, TCP_PORT))
  sock.connect((ROUTER_ADDR, ROUTER_PORT))
  # Send the LOGIN string to gain access to the router
  sock.sendto(LOGIN, (ROUTER_ADDR, ROUTER_PORT))
  
  response = urllib2.urlopen(WAN_IP_PAGE) 
  
  page_source = response.read()

  # Parse the source looking for the WAN IP.
  # IP Address
  match = re.search(r'<td bgcolor=#E7DAAC><b>IP Address</b></td><td bgcolor=#E7DAAC>(.*)</td></tr>', page_source)
  if match:
    ip = match.group(1)

  # MAC Address
  match = re.search(r'<tr><td bgcolor=#E7DAAC>&nbsp;<td bgcolor=#E7DAAC><b>MAC Address</b></td><td bgcolor=#E7DAAC>(.*)</td></tr>', page_source)
  if match:
    mac = match.group(1)

  # Duration
  match = re.search(r'<tr><td bgcolor=#E7DAAC>&nbsp;</td><td bgcolor=#E7DAAC><b>Duration</b></td><td bgcolor=#E7DAAC>(.*)</td></tr>', page_source)
  if match:
    duration = match.group(1)

  # Expiration
  match = re.search(r'<tr><td bgcolor=#E7DAAC>&nbsp;</td><td bgcolor=#E7DAAC><b>Expires</b></td><td bgcolor=#E7DAAC>(.*)', page_source)
  if match:
    expire = match.group(1)
    
  #
  # Use urllib2 to request the logout, don't care about spoofing the browser anymore.
  # The logout needs to occur, otherwise any webbrowser can just point to a guarded page
  # and immediately have access.
  #
  response = urllib2.urlopen(LOGOUT_PAGE) 
  
  if ip and mac and duration and expire:
    print "WAN IP Address: %15s" % ip
    print "MAC Address: %23s" % mac
    print "Lease Duration: %26s" % duration
    print "Expiration Date: %26s" % expire
  else:
    print "Could not get all of the data elements!"
    exit(2)
#
# Invocation Check
#
if __name__ == "__main__":
  uname, passwd = get_credentials()
  if uname and passwd:
    main( uname, passwd)
