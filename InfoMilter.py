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
    # yum install python36 python36-libs python36-devel python36-pip
    # yum install python36-pymilter
    # pip3 install log4p
    # pip3 install ipaddress
    For pymilter 1.0.4 (latest
    # yum install gcc
    # yum install sendmail-devel
    # systemctl stop sendmail.service
    # systemctl disable sendmail.service
    # systemctl enable postfix.service
    # systemctl start postfix.sevice
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
__updated__ = '2019-09-13'
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


class OutputFormater():
    '''Formatter for the log output'''
    
    def __init__(self, clipChar, lineChar, lineCharCount, listFormat, lineFormat, errorLineFormat):
        self.clipChar = clipChar
        self.lineChar = lineChar
        self.lineCharCount = lineCharCount
        self.listFormat = listFormat
        self.lineFormat = lineFormat
        self.errorLineFormat = errorLineFormat
    
    # Line with frame character.
    def clipLine(self):
        __log__.info(self.clipChar * self.lineCharCount)
        
    # Line with separator character.
    def lineLine(self):
        __log__.info(self.lineChar * self.lineCharCount)  

    # Line with key value pair output.    
    def itemLine(self, itemKey, itemValue):
        __log__.info(self.lineFormat.format(itemKey, itemValue))
        
    # Line with key value pair error output.    
    def errorLine(self, itemKey, itemValue):
        __log__.error(self.lineFormat.format(itemKey, itemValue))
        
    # Line with start end character with counter for the part.
    def listLine(self, function, position):
        __log__.info(self.listFormat.format("sendmail-pymilter - " + position + ": " + function))

    def headLine(self, function):
        self.clipLine()
        self.listLine(function, "ENTRY")
        self.lineLine()
        
    def footLine(self, function):
        self.lineLine()
        self.listLine(function, "LEAVE")
        self.clipLine()


# Initialize output formatter for the log output.
__logOutput__ = OutputFormater("=", "-", 40, "{:39}:", "{:39}: {:1}", "{:38}: {:1}")


class InfoMilter(Milter.Milter):
    
    # Create a new instance with each new connection.
    def __init__(self):
        # Integer incremented with each call.
        self.id = Milter.uniqueID() 

    def connect(self, hostname, family, hostaddr):
        __logOutput__.headLine("connect")
        __logOutput__.itemLine("hostname", hostname)
        __logOutput__.itemLine("family", family)
        
        if family == AF_INET:
            __logOutput__.itemLine(" - family", "IPv4 (socket.AF_INET)")
        elif family == AF_INET6:
            __logOutput__.itemLine(" - family", "IPv6 (socket.AF_INET6)")
        elif family == AF_UNIX:
            __logOutput__.itemLine(" - family", "UNIX (socket.AF_UNIX)")
        else:
            __logOutput__.itemLine(" - family", "unknown")
        
        __logOutput__.itemLine("hostaddr", str(hostaddr))
        
        if family == AF_INET:
            __logOutput__.itemLine(" - address", str(hostaddr[0]))
            __logOutput__.itemLine(" - port", str(hostaddr[1]))
        elif family == AF_INET6:
            __logOutput__.itemLine(" - address", str(hostaddr[2]))
            __logOutput__.itemLine(" - port", str(hostaddr[3]))
        elif family == AF_UNIX:   
            __logOutput__.temLine(" - socket", "UNIX")
        else:
            __logOutput__.itemLine(" - result", "unknown")                        
        
        __logOutput__.lineLine()
        __logOutput__.itemLine("self.getsymval('{client_connections}')", str(self.getsymval('{client_connections}')))
        __logOutput__.itemLine("self.getsymval('{client_ptr}')", str(self.getsymval('{client_ptr}')))
        __logOutput__.itemLine("self.getsymval('{if_addr}')", str(self.getsymval('{if_addr}')))
        __logOutput__.itemLine("self.getsymval('{if_name}')", str(self.getsymval('{if_name}')))
        
        allmacro(self)
        __logOutput__.footLine("connect")
        return Milter.CONTINUE
    
    def hello(self, heloname):
        __logOutput__.headLine("helo/ehlo")
        __logOutput__.itemLine("heloname", heloname)
        
        __logOutput__.lineLine()  
        __logOutput__.itemLine("self.getsymval('{client_ptr}')", str(self.getsymval('{client_ptr}')))
        __logOutput__.itemLine("self.getsymval('{cert_issuer} ')", str(self.getsymval('{cert_issuer} ')))
        __logOutput__.itemLine("self.getsymval('{cert_subject}')", str(self.getsymval('{cert_subject}')))
        __logOutput__.itemLine("self.getsymval('{cipher_bits}')", str(self.getsymval('{cipher_bits}')))
        __logOutput__.itemLine("self.getsymval('{cipher}')", str(self.getsymval('{cipher}')))
        __logOutput__.itemLine("self.getsymval('{tls_version}')", str(self.getsymval('{tls_version}')))
        
        allmacro(self)
        __logOutput__.footLine("helo/ehlo")    
        return Milter.CONTINUE

    def envfrom(self, mailfrom, *parameter):
        __logOutput__.headLine("envfrom")
        __logOutput__.itemLine("mailfrom", mailfrom)
        __logOutput__.itemLine(" - parameter", str(parameter))

        __logOutput__.lineLine()
        __logOutput__.itemLine("self.getsymval('{auth_authen}')", str(self.getsymval('{auth_authen}')))
        __logOutput__.itemLine("self.getsymval('{auth_author} ')", str(self.getsymval('{auth_author}')))
        __logOutput__.itemLine("self.getsymval('{auth_type} ')", str(self.getsymval('{auth_type}')))
        __logOutput__.itemLine("self.getsymval('{cert_issuer} ')", str(self.getsymval('{cert_issuer} ')))
        __logOutput__.itemLine("self.getsymval('{cert_subject}')", str(self.getsymval('{cert_subject}')))
        __logOutput__.itemLine("self.getsymval('{cipher_bits}')", str(self.getsymval('{cipher_bits}')))
        __logOutput__.itemLine("self.getsymval('{cipher}')", str(self.getsymval('{cipher}')))        
        __logOutput__.itemLine("self.getsymval('{tls_version}')", str(self.getsymval('{tls_version}')))
        __logOutput__.itemLine("self.getsymval('{mail_addr}')", str(self.getsymval('{mail_addr}')))
        __logOutput__.itemLine("self.getsymval('{mail_host}')", str(self.getsymval('{mail_host}')))
        __logOutput__.itemLine("self.getsymval('{mail_mailer}')", str(self.getsymval('{mail_mailer}')))         

        allmacro(self)
        __logOutput__.footLine("envfrom")    
        return Milter.CONTINUE
    
    def envrcpt(self, mailto, *parameter):
        __logOutput__.headLine("envrcpt")
        __logOutput__.itemLine("mailto", mailto)
        __logOutput__.itemLine(" - parameter", str(parameter))
        
        __logOutput__.lineLine()
        __logOutput__.itemLine("self.getsymval('{rcpt_addr}')", str(self.getsymval('{rcpt_addr}')))
        __logOutput__.itemLine("self.getsymval('{rcpt_host}')", str(self.getsymval('{rcpt_host}')))
        __logOutput__.itemLine("self.getsymval('{rcpt_mailer}')", str(self.getsymval('{rcpt_mailer}')))
        
        allmacro(self)
        __logOutput__.footLine("envrcpt")
        __logOutput__.headLine("header")    
        return Milter.CONTINUE        

    def header(self, field, value):
        __logOutput__.itemLine("field => value", field + ": " + value)
        return Milter.CONTINUE  
        
    def eoh(self):
        __logOutput__.lineLine()
        __logOutput__.itemLine("self.getsymval('{i}')", str(self.getsymval('{i}')))
        __logOutput__.itemLine("self.getsymval('{client_ptr}')", str(self.getsymval('{client_ptr}')))
        __logOutput__.itemLine("self.getsymval('{auth_authen}')", str(self.getsymval('{auth_authen}')))
        __logOutput__.itemLine("self.getsymval('{auth_author} ')", str(self.getsymval('{auth_author}')))
        __logOutput__.itemLine("self.getsymval('{auth_type} ')", str(self.getsymval('{auth_type}')))
        __logOutput__.itemLine("self.getsymval('{cert_issuer} ')", str(self.getsymval('{cert_issuer} ')))
        __logOutput__.itemLine("self.getsymval('{cert_subject}')", str(self.getsymval('{cert_subject}')))
        __logOutput__.itemLine("self.getsymval('{cipher_bits}')", str(self.getsymval('{cipher_bits}')))
        __logOutput__.itemLine("self.getsymval('{cipher}')", str(self.getsymval('{cipher}')))
        __logOutput__.itemLine("self.getsymval('{tls_version}')", str(self.getsymval('{tls_version}')))
        
        allmacro(self)
        __logOutput__.footLine("header")
        
        __logOutput__.headLine("eoh")
        __logOutput__.itemLine("self.getsymval('{i}')", str(self.getsymval('{i}')))
        
        allmacro(self)
        __logOutput__.footLine("eoh")
        return Milter.CONTINUE   

    def body(self, chunk):
        __logOutput__.headLine("body")
        __logOutput__.itemLine("body", str(chunk))
        __logOutput__.itemLine(" - decoded (UTF-8)", str(chunk.decode('UTF-8')))
        
        allmacro(self)
        __logOutput__.footLine("body")
        return Milter.CONTINUE

    def eom(self):
        __logOutput__.headLine("eom")
        
        __logOutput__.itemLine("self.getsymval('{i}')", str(self.getsymval('{i}')))
        __logOutput__.itemLine("self.getsymval('{auth_authen}')", str(self.getsymval('{auth_authen}')))
        __logOutput__.itemLine("self.getsymval('{auth_author} ')", str(self.getsymval('{auth_author}')))
        __logOutput__.itemLine("self.getsymval('{auth_type} ')", str(self.getsymval('{auth_type}')))
        __logOutput__.itemLine("self.getsymval('{cert_issuer} ')", str(self.getsymval('{cert_issuer} ')))
        __logOutput__.itemLine("self.getsymval('{cert_subject}')", str(self.getsymval('{cert_subject}')))
        __logOutput__.itemLine("self.getsymval('{cipher_bits}')", str(self.getsymval('{cipher_bits}')))
        __logOutput__.itemLine("self.getsymval('{cipher}')", str(self.getsymval('{cipher}')))
        __logOutput__.itemLine("self.getsymval('{tls_version}')", str(self.getsymval('{tls_version}')))
        
        allmacro(self)
        __logOutput__.footLine("eom")
        return Milter.CONTINUE   

    def abort(self):
        __logOutput__.headLine("abort")
        allmacro(self)
        __logOutput__.footLine("abort")
        return Milter.CONTINUE

    def close(self):
        __logOutput__.headLine("close")
        allmacro(self)
        __logOutput__.footLine("close")        
        return Milter.CONTINUE


def allmacro(self):
    __logOutput__.lineLine()
    __logOutput__.itemLine("self.getsymval('{j}')", str(self.getsymval('{j}')))
    __logOutput__.itemLine("self.getsymval('{_}')", str(self.getsymval('{_}')))
    __logOutput__.itemLine("self.getsymval('{client_addr}')", str(self.getsymval('{client_addr}')))
    __logOutput__.itemLine("self.getsymval('{client_name}')", str(self.getsymval('{client_name}')))
    __logOutput__.itemLine("self.getsymval('{client_port}')", str(self.getsymval('{client_port}')))
    __logOutput__.itemLine("self.getsymval('{daemon_addr}')", str(self.getsymval('{daemon_addr}'))) 
    __logOutput__.itemLine("self.getsymval('{daemon_name}')", str(self.getsymval('{daemon_name}')))
    __logOutput__.itemLine("self.getsymval('{daemon_port}')", str(self.getsymval('{daemon_port}')))
    __logOutput__.itemLine("self.getsymval('{v}')", str(self.getsymval('{v}')))


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
        required.add_argument('-l', '--listener',
                              action='store',
                              nargs=1,
                              default='127.0.0.1',
                              type=str,
                              required=True,
                              help='IPv4-Address where the milter is listening',
                              metavar='<IPv4>',
                              dest='ip')
        required.add_argument('-p', '--port',
                              action='store',
                              nargs=1,
                              default='10099',
                              type=int,
                              required=True,
                              help='Port where the milter is listening',
                              metavar='<1..65535>')                    
        parser._action_groups.append(optional)
        optional.add_argument('-v', '--version',
                              action='version',
                              version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        # Check argument -l, --listener if it is a VALID IP address. 
        try:
            global __listener__; __listener__ = str(ipaddress.ip_address(str(args.ip[0])))
        except ValueError:
            outError('Required argument -l,--listener <IPv4> is invalid: %s', str(args.ip[0]))         
        
        # Check argument -p, --port if it is a VALID port number, between 1 and 65535.
        if int(args.port[0]) < 1 or int(args.port[0]) > 65535:
            outError('Required argument -p,--port <port> was NOT a valid port number, between 1 and 65535: %s',
                     str(int(args.port[0])))
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
    __logOutput__.clipLine() 
    __logOutput__.itemLine("milter version",
                           str(Milter.getversion()[0]) 
                           +"." + str(Milter.getversion()[1]) 
                           +"." + str(Milter.getversion()[2]))
    __logOutput__.itemLine("milter listener", __listener__)
    __logOutput__.itemLine("milter port", __port__)
    __logOutput__.clipLine()
    # inet:10099@127.0.0.1
    __socketName__ = "inet:" + str(__port__) + "@" + str(__listener__)
    Milter.factory = InfoMilter
    # Tell the milter, which feature we want to use.
    Milter.set_flags(__flags__)
    Milter.runmilter("pythonfilter", __socketName__, __timeout__)
    __logOutput__.clipLine()  
    __log__.info("%s milter shutdown" % sys.argv[0])


if __name__ == '__main__':
    main()
