#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

'''
Copyright (c) 2019 Klaus Tachtler. All Rights Reserved.
Klaus Tachtler. <klaus@tachtler.net>
http://www.tachtler.net
'''

'''
Milter for Sendmail or Postfix to log all possible parts of the e-Mail 
communication, written in Python.
 
pymilter is an Open Source implementation of the Sendmail milter protocol, for
implementing milters in Python that can interface with the Sendmail or Postfix
MTA.
 
Python implementation of the Sendmail Milter protocol based on the project of
pymilter from Stuart D. Gathman (stuart@gathman.org).

@author Klaus Tachtler. <klaus@tachtler.net>
 
    Homepage : http://www.tachtler.net

    Licensed under the Apache License, Version 2.0 (the "License"); you
    may not use this file except in compliance with the License. You may
    obtain a copy of the License at
         
    http://www.apache.org/licenses/LICENSE-2.0
 
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
    implied. See the License for the specific language governing
    permissions and limitations under the License.
 
    Copyright (c) 2019 by Klaus Tachtler.
'''

'''
See also:
https://pypi.org/project/log4p/
https://github.com/sdgathman/pymilter
https://pythonhosted.org/pymilter/milter_api/api.html
https://pythonhosted.org/pymilter/classMilter_1_1Milter.html
'''

'''
RPM installation CentOS-7 for python36 from EPEL:
    # yum install python36-pymilter
    # pip3 install log4p
    # pip3 install ipaddress
'''

'''
TEST with swaks:
    # swaks --to klaus@localhost --from root@localhost --server 127.0.0.1
'''

import os
import sys
import ipaddress

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2019-09-10'
__updated__ = '2019-09-10'
__author__ = 'Klaus Tachtler <klaus@tachtler.net>'
__organisation__ = 'Klaus Tachtler'

import Milter
import log4p

from socket import AF_INET, AF_INET6, AF_UNIX

__logger__ = log4p.GetLogger(__name__, config="./log4p.json")
__log__ = __logger__.logger

__socketName__ = None
__listener__ = "127.0.0.1"
__port__ = 10099
__timeout__ = 600
__flags__ = 0

__clipChar__ = "="
__lineChar__ = "-"
__lineCharCount__ = 40
__listFormat__ = "{:39}:"
__lineFormat__ = "{:39}: {:1}"


class InfoMilter(Milter.Milter):
    
    # Create a new instance with each new connection.
    def __init__(self):
        # Integer incremented with each call.
        self.id = Milter.uniqueID() 

    def connect(self, hostname, family, hostaddr):
        headLine("connect")
        itemLine("hostname", hostname)
        itemLine("family", family)
        
        if family == AF_INET:
            itemLine(" - family", "IPv4 (socket.AF_INET)")
        elif family == AF_INET6:
            itemLine(" - family", "IPv6 (socket.AF_INET6)")
        elif family == AF_UNIX:
            itemLine(" - family", "UNIX (socket.AF_UNIX)")
        else:
            itemLine(" - family", "unknown")
        
        itemLine("hostaddr", str(hostaddr))
        
        if family == AF_INET:
            itemLine(" - address", str(hostaddr[0]))
            itemLine(" - port", str(hostaddr[1]))
        elif family == AF_INET6:
            itemLine(" - address", str(hostaddr[2]))
            itemLine(" - port", str(hostaddr[3]))
        elif family == AF_UNIX:   
            itemLine(" - socket", "UNIX")
        else:
            itemLine(" - result", "unknown")                        
        
        lineLine()
        itemLine("self.getsymval('{client_connections}')", str(self.getsymval('{client_connections}')))
        itemLine("self.getsymval('{client_ptr}')", str(self.getsymval('{client_ptr}')))
        itemLine("self.getsymval('{if_addr}')", str(self.getsymval('{if_addr}')))
        itemLine("self.getsymval('{if_name}')", str(self.getsymval('{if_name}')))
        
        allmarco(self)
        footLine("connect")
        return Milter.CONTINUE
    
    def hello(self, heloname):
        headLine("helo/ehlo")
        itemLine("heloname", heloname)
        
        lineLine()  
        itemLine("self.getsymval('{client_ptr}')", str(self.getsymval('{client_ptr}')))
        itemLine("self.getsymval('{cert_issuer} ')", str(self.getsymval('{cert_issuer} ')))
        itemLine("self.getsymval('{cert_subject}')", str(self.getsymval('{cert_subject}')))
        itemLine("self.getsymval('{cipher_bits}')", str(self.getsymval('{cipher_bits}')))
        itemLine("self.getsymval('{cipher}')", str(self.getsymval('{cipher}')))
        itemLine("self.getsymval('{tls_version}')", str(self.getsymval('{tls_version}')))
        
        allmarco(self)
        footLine("helo/ehlo")    
        return Milter.CONTINUE

    def envfrom(self, mailfrom, *parameter):
        headLine("envfrom")
        itemLine("mailfrom", mailfrom)
        itemLine(" - parameter", str(parameter))

        lineLine()
        itemLine("self.getsymval('{auth_authen}')", str(self.getsymval('{auth_authen}')))
        itemLine("self.getsymval('{auth_author} ')", str(self.getsymval('{auth_author}')))
        itemLine("self.getsymval('{auth_type} ')", str(self.getsymval('{auth_type}')))
        itemLine("self.getsymval('{cert_issuer} ')", str(self.getsymval('{cert_issuer} ')))
        itemLine("self.getsymval('{cert_subject}')", str(self.getsymval('{cert_subject}')))
        itemLine("self.getsymval('{cipher_bits}')", str(self.getsymval('{cipher_bits}')))
        itemLine("self.getsymval('{cipher}')", str(self.getsymval('{cipher}')))        
        itemLine("self.getsymval('{tls_version}')", str(self.getsymval('{tls_version}')))
        itemLine("self.getsymval('{mail_addr}')", str(self.getsymval('{mail_addr}')))
        itemLine("self.getsymval('{mail_host}')", str(self.getsymval('{mail_host}')))
        itemLine("self.getsymval('{mail_mailer}')", str(self.getsymval('{mail_mailer}')))         

        allmarco(self)
        footLine("envfrom")    
        return Milter.CONTINUE
    
    def envrcpt(self, mailto, *parameter):
        headLine("envrcpt")
        itemLine("mailto", mailto)
        itemLine(" - parameter", str(parameter))
        
        lineLine()
        itemLine("self.getsymval('{rcpt_addr}')", str(self.getsymval('{rcpt_addr}')))
        itemLine("self.getsymval('{rcpt_host}')", str(self.getsymval('{rcpt_host}')))
        itemLine("self.getsymval('{rcpt_mailer}')", str(self.getsymval('{rcpt_mailer}')))
        
        allmarco(self)
        footLine("envrcpt")
        headLine("header")    
        return Milter.CONTINUE        

    def header(self, field, value):
        itemLine("field => value", field + ": " + value)
        return Milter.CONTINUE  
        
    def eoh(self):
        lineLine()
        itemLine("self.getsymval('{i}')", str(self.getsymval('{i}')))
        itemLine("self.getsymval('{client_ptr}')", str(self.getsymval('{client_ptr}')))
        itemLine("self.getsymval('{auth_authen}')", str(self.getsymval('{auth_authen}')))
        itemLine("self.getsymval('{auth_author} ')", str(self.getsymval('{auth_author}')))
        itemLine("self.getsymval('{auth_type} ')", str(self.getsymval('{auth_type}')))
        itemLine("self.getsymval('{cert_issuer} ')", str(self.getsymval('{cert_issuer} ')))
        itemLine("self.getsymval('{cert_subject}')", str(self.getsymval('{cert_subject}')))
        itemLine("self.getsymval('{cipher_bits}')", str(self.getsymval('{cipher_bits}')))
        itemLine("self.getsymval('{cipher}')", str(self.getsymval('{cipher}')))
        itemLine("self.getsymval('{tls_version}')", str(self.getsymval('{tls_version}')))
        
        allmarco(self)
        footLine("header")
        
        headLine("eoh")
        itemLine("self.getsymval('{i}')", str(self.getsymval('{i}')))
        
        allmarco(self)
        footLine("eoh")
        return Milter.CONTINUE   

    def body(self, chunk):
        headLine("body")
        itemLine("body", str(chunk))
        itemLine(" - decoded (UTF-8)", str(chunk.decode('UTF-8')))
        
        allmarco(self)
        footLine("body")
        return Milter.CONTINUE

    def eom(self):
        headLine("eom")
        
        itemLine("self.getsymval('{i}')", str(self.getsymval('{i}')))
        itemLine("self.getsymval('{auth_authen}')", str(self.getsymval('{auth_authen}')))
        itemLine("self.getsymval('{auth_author} ')", str(self.getsymval('{auth_author}')))
        itemLine("self.getsymval('{auth_type} ')", str(self.getsymval('{auth_type}')))
        itemLine("self.getsymval('{cert_issuer} ')", str(self.getsymval('{cert_issuer} ')))
        itemLine("self.getsymval('{cert_subject}')", str(self.getsymval('{cert_subject}')))
        itemLine("self.getsymval('{cipher_bits}')", str(self.getsymval('{cipher_bits}')))
        itemLine("self.getsymval('{cipher}')", str(self.getsymval('{cipher}')))
        itemLine("self.getsymval('{tls_version}')", str(self.getsymval('{tls_version}')))
        
        allmarco(self)
        footLine("eom")
        return Milter.CONTINUE   

    def abort(self):
        headLine("abort")
        allmarco(self)
        footLine("abort")
        return Milter.CONTINUE

    def close(self):
        headLine("close")
        allmarco(self)
        footLine("close")        
        return Milter.CONTINUE


def allmarco(self):
    lineLine()
    itemLine("self.getsymval('{j}')", str(self.getsymval('{j}')))
    itemLine("self.getsymval('{_}')", str(self.getsymval('{_}')))
    itemLine("self.getsymval('{client_addr}')", str(self.getsymval('{client_addr}')))
    itemLine("self.getsymval('{client_name}')", str(self.getsymval('{client_name}')))
    itemLine("self.getsymval('{client_port}')", str(self.getsymval('{client_port}')))
    itemLine("self.getsymval('{daemon_addr}')", str(self.getsymval('{daemon_addr}'))) 
    itemLine("self.getsymval('{daemon_name}')", str(self.getsymval('{daemon_name}')))
    itemLine("self.getsymval('{daemon_port}')", str(self.getsymval('{daemon_port}')))
    itemLine("self.getsymval('{v}')", str(self.getsymval('{v}'))) 


def headLine(function):
    clipLine()
    listLine(function, "ENTRY")
    lineLine()

    
def footLine(function):
    lineLine()
    listLine(function, "LEAVE")
    clipLine()


def listLine(function, position):
    __log__.info(__listFormat__.format("sendmail-pymilter - " + position + ": " + function))


def clipLine():
    __log__.info(__clipChar__ * __lineCharCount__)

    
def lineLine():
    __log__.info(__lineChar__ * __lineCharCount__)    


def itemLine(itemKey, itemValue):
    __log__.info(__lineFormat__.format(itemKey, itemValue))


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def CLIParser(argv=None): 
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = '''v %s
  Copyright (c) Klaus Tachtler. All Rights Reserved.
  Klaus Tachtler. <klaus@tachtler.net>
  http://www.tachtler.net''' % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s (%s) %s' % (program_build_date, program_version,)
    program_shortdesc = '''%s\n
  Milter for Sendmail or Postfix to log all possible parts of the e-Mail
  communication, written in Python.

  pymilter is an Open Source implementation of the Sendmail milter protocol,
  for implementing milters in Python that can interface with the Sendmail or
  Postfix MTA.
  
  Python implementation of the Sendmail Milter protocol based on the project
  of pymilter from Stuart D. Gathman (stuart@gathman.org).    
''' % (__import__('__main__').__doc__.split("\n")[1])
    program_license = '''%s

  Created by %s on %s.
  Copyright (c) %s. All rights reserved.

  Licensed under the Apache License, Version 2.0 (the "License"); you
  may not use this file except in compliance with the License. You may
  obtain a copy of the License at
         
  http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
  implied. See the License for the specific language governing
  permissions and limitations under the License.

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, __author__, str(__date__), __organisation__)

    def outError(textKey, textValue):
        parser.print_help()
        sys.stderr.write("\nERROR:  " + str(textKey) % str(textValue))
        sys.exit(0)

    try:
        # Setup argument parser        
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        optional = parser._action_groups.pop()
        required = parser.add_argument_group('required arguments')
        required.add_argument('-l', '--listener', action='store', nargs=1, default='127.0.0.1', type=str, required=True, help='IPv4-Address where the milter is listening', metavar='<IPv4>', dest='ip')
        required.add_argument('-p', '--port', action='store', nargs=1, default='10099', type=int, required=True, help='Port where the milter is listening', metavar='<1..65535>')                    
        parser._action_groups.append(optional)
        optional.add_argument('-v', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        # Check argument -l, --listener if it is a VALID IP address. 
        try:
            global __listener__; __listener__ = str(ipaddress.ip_address(str(args.ip[0])))
        except ValueError:
            outError('Required argument -l,--listener <IPv4> is invalid: %s', str(args.ip[0]))         
        
        # Check argument -p, --port if it is a VALID port number, between 1 and 65535.
        if int(args.port[0]) < 1 or int(args.port[0]) > 65535:
            outError('Required argument -p,--port <port> was NOT a valid port number, between 1 and 65535: %s', str(int(args.port[0])))
        else:
            global __port__; __port__ = int(args.port[0])

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


def main():
    if CLIParser() != 0:
        sys.stderr.write("\nERROR:  An error has occurred and the program has been terminated!")
        sys.exit(0)
        
    __log__.info("%s milter startup" % os.path.basename(sys.argv[0]))
    clipLine() 
    __log__.info(__lineFormat__.format("milter version", str(Milter.getversion()[0]) + "." + str(Milter.getversion()[1]) + "." + str(Milter.getversion()[2])))
    __log__.info(__lineFormat__.format("milter listener", __listener__))
    __log__.info(__lineFormat__.format("milter port", __port__)) 
    clipLine()
    # inet:10099@127.0.0.1
    __socketName__ = "inet:" + str(__port__) + "@" + str(__listener__)
    Milter.factory = InfoMilter
    # Tell the milter, which feature we want to use.
    Milter.set_flags(__flags__)
    Milter.runmilter("pythonfilter", __socketName__, __timeout__)
    clipLine()  
    __log__.info("%s milter shutdown" % sys.argv[0])


if __name__ == '__main__':
    main()
