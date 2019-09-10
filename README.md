# pymilter-InfoMilter
Milter for Sendmail or Postfix to log all possible parts of the e-Mail  communication, written in Python.

The project was based on the great work of Stuart D. Gathman (stuart@gathman.org) [sdgathman/pymilter](https://github.com/sdgathman/pymilter)

## Python-File description
The **exection of the Python file with the option ```-h``` or ```--help```** with following command, will show you all **options** you can set, to start the **InfoMilter.py**:
```bash
# python3 InfoMilter.py -h
usage: InfoMilter.py [-h] -l <IPv4> -p <1..65535> [-v]

Copyright (c) 2019 Klaus Tachtler. All Rights Reserved.

  Milter for Sendmail or Postfix to log all possible parts of the e-Mail
  communication, written in Python.

  pymilter is an Open Source implementation of the Sendmail milter protocol,
  for implementing milters in Python that can interface with the Sendmail or
  Postfix MTA.
  
  Python implementation of the Sendmail Milter protocol based on the project
  of pymilter from Stuart D. Gathman (stuart@gathman.org).    

  Created by Klaus Tachtler <klaus@tachtler.net> on 2019-09-10.
  Copyright (c) Klaus Tachtler. All rights reserved.

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

required arguments:
  -l <IPv4>, --listener <IPv4>
                        IPv4-Address where the milter is listening
  -p <1..65535>, --port <1..65535>
                        Port where the milter is listening

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

## Python-File execution
The **execution of the Python file** could be done, for example on a Linux ```shell``` with following command:
```bash
# python3 InfoMilter.py -l 127.0.0.1 -p 10099
2019-09-09 20:39:43,293 - __main__ - INFO - InfoMilter.py milter startup
2019-09-09 20:39:43,294 - __main__ - INFO - ========================================
2019-09-09 20:39:43,294 - __main__ - INFO - milter version                         : 1.0.1
2019-09-09 20:39:43,294 - __main__ - INFO - milter listener                        : 127.0.0.1
2019-09-09 20:39:43,294 - __main__ - INFO - milter port                            : 10099
2019-09-09 20:39:43,294 - __main__ - INFO - ========================================
^C
2019-09-09 20:39:48,297 - __main__ - INFO - ========================================
2019-09-09 20:39:48,297 - __main__ - INFO - InfoMilter.py milter shutdown
```
and could be **stopped** with **[CTRL-c]** key combination.

Under **Linux**, you can see with following command, on which **ipv4-address and port** the **InfoMilter.py** was bind to:
```bash
# netstat -tulpen | grep python3
tcp        0      0 127.0.0.1:10099       0.0.0.0:*          LISTEN     0         1077235    10641/python3
```

## Postfix Milter integration
In order to include InforMilter.jar with ![Postfix](http://www.postfix.org/), minimal adjustments are required in the two following configuration files of Postfix.
  - ```/etc/postfix/main.cf```
  - ```/etc/postfix/master.cf```

#### ```/etc/postfix/main.cf``` 
(Only relevant part of the configuration file!)
```
# --------------------------------------------------------------------------------
# New - http://www.postfix.org/MILTER_README.html
# MILTER CONFIGURATIONS
# --------------------------------------------------------------------------------

# JMilter (info_milter)
info_milter = inet:127.0.0.1:10099
```

#### ```/etc/postfix/master.cf```

(Only relevant part of the configuration file!)
```
#
# Postfix master process configuration file.  For details on the format
# of the file, see the master(5) manual page (command: "man 5 master").
#
# Do not forget to execute "postfix reload" after editing this file.
#
# ==========================================================================
# service type  private unpriv  chroot  wakeup  maxproc command + args
#               (yes)   (yes)   (yes)   (never) (100)
# ==========================================================================
smtp      inet  n       -       n       -       -       smtpd
# InfoMilter
   -o smtpd_milters=${info_milter}
```

:exclamation: **After the changes in the configuration files, you have to restart the Postfix Daemon!**

## Telnet e-Mail-Test
The following **telnet session** will show you the usage of the InfoMilter.py in combination with ```telnet```.
```bash
# telnet 127.0.0.1 25
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
220 pml125.home.tachtler.net ESMTP Postfix
ehlo localhost
250-pml125.home.tachtler.net
250-PIPELINING
250-SIZE 10240000
250-VRFY
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING
mail from: <root@localhost>
250 2.1.0 Ok
rcpt to: <klaus@localhost>
250 2.1.5 Ok
data
354 End data with <CR><LF>.<CR><LF>
Subject: Test e-Mail.
From: sender@example.com
To: receiver@example.com

Hello,

test e-Mail.

Greetings
.
250 2.0.0 Ok: queued as 40B391109F84
quit
221 2.0.0 Bye
Connection closed by foreign host.
```

## LOG-File output
While using the InfoMilter.jar the following output will be written to the **standard command output (```screen / shell```) and a folder named logs will be created, which includes the ```InfoMilter-debug.log``` file and ```InfoMilter-errors.log```.**

An **example output file** could be look like this. (It's based on the **Telnet e-Mail-Test** - **telnet-session** shown above):
```
# python3 InfoMilter.py -l 127.0.0.1 -p 10099
2019-09-10 15:43:59,454 - __main__ - INFO - InfoMilter.py milter startup
2019-09-10 15:43:59,454 - __main__ - INFO - ========================================
2019-09-10 15:43:59,454 - __main__ - INFO - milter version                         : 1.0.1
2019-09-10 15:43:59,454 - __main__ - INFO - milter listener                        : 127.0.0.1
2019-09-10 15:43:59,454 - __main__ - INFO - milter port                            : 10099
2019-09-10 15:43:59,454 - __main__ - INFO - ========================================
2019-09-10 15:47:08,541 - __main__ - INFO - ========================================
2019-09-10 15:47:08,542 - __main__ - INFO - sendmail-pymilter - ENTRY: connect     :
2019-09-10 15:47:08,542 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:08,542 - __main__ - INFO - hostname                               : localhost
2019-09-10 15:47:08,542 - __main__ - INFO - family                                 : 2
2019-09-10 15:47:08,542 - __main__ - INFO -  - family                              : IPv4 (socket.AF_INET)
2019-09-10 15:47:08,542 - __main__ - INFO - hostaddr                               : ('127.0.0.1', 44750)
2019-09-10 15:47:08,542 - __main__ - INFO -  - address                             : 127.0.0.1
2019-09-10 15:47:08,543 - __main__ - INFO -  - port                                : 44750
2019-09-10 15:47:08,543 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:08,543 - __main__ - INFO - self.getsymval('{client_connections}') : None
2019-09-10 15:47:08,543 - __main__ - INFO - self.getsymval('{client_ptr}')         : None
2019-09-10 15:47:08,543 - __main__ - INFO - self.getsymval('{if_addr}')            : None
2019-09-10 15:47:08,543 - __main__ - INFO - self.getsymval('{if_name}')            : None
2019-09-10 15:47:08,543 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:08,543 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:47:08,544 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:47:08,544 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:47:08,544 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:47:08,544 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:47:08,544 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:47:08,544 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:47:08,544 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:47:08,545 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:47:08,545 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:08,545 - __main__ - INFO - sendmail-pymilter - LEAVE: connect     :
2019-09-10 15:47:08,545 - __main__ - INFO - ========================================
2019-09-10 15:47:48,435 - __main__ - INFO - ========================================
2019-09-10 15:47:48,436 - __main__ - INFO - sendmail-pymilter - ENTRY: helo/ehlo   :
2019-09-10 15:47:48,436 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:48,436 - __main__ - INFO - heloname                               : localhost
2019-09-10 15:47:48,436 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:48,436 - __main__ - INFO - self.getsymval('{client_ptr}')         : None
2019-09-10 15:47:48,436 - __main__ - INFO - self.getsymval('{cert_issuer} ')       : None
2019-09-10 15:47:48,436 - __main__ - INFO - self.getsymval('{cert_subject}')       : None
2019-09-10 15:47:48,437 - __main__ - INFO - self.getsymval('{cipher_bits}')        : None
2019-09-10 15:47:48,437 - __main__ - INFO - self.getsymval('{cipher}')             : None
2019-09-10 15:47:48,437 - __main__ - INFO - self.getsymval('{tls_version}')        : None
2019-09-10 15:47:48,437 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:48,437 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:47:48,437 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:47:48,437 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:47:48,437 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:47:48,437 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:47:48,438 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:47:48,438 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:47:48,438 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:47:48,438 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:47:48,438 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:48,438 - __main__ - INFO - sendmail-pymilter - LEAVE: helo/ehlo   :
2019-09-10 15:47:48,438 - __main__ - INFO - ========================================
2019-09-10 15:47:58,748 - __main__ - INFO - ========================================
2019-09-10 15:47:58,748 - __main__ - INFO - sendmail-pymilter - ENTRY: envfrom     :
2019-09-10 15:47:58,748 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:58,748 - __main__ - INFO - mailfrom                               : <root@localhost>
2019-09-10 15:47:58,748 - __main__ - INFO -  - parameter                           : ()
2019-09-10 15:47:58,748 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:58,748 - __main__ - INFO - self.getsymval('{auth_authen}')        : None
2019-09-10 15:47:58,748 - __main__ - INFO - self.getsymval('{auth_author} ')       : None
2019-09-10 15:47:58,749 - __main__ - INFO - self.getsymval('{auth_type} ')         : None
2019-09-10 15:47:58,749 - __main__ - INFO - self.getsymval('{cert_issuer} ')       : None
2019-09-10 15:47:58,749 - __main__ - INFO - self.getsymval('{cert_subject}')       : None
2019-09-10 15:47:58,749 - __main__ - INFO - self.getsymval('{cipher_bits}')        : None
2019-09-10 15:47:58,749 - __main__ - INFO - self.getsymval('{cipher}')             : None
2019-09-10 15:47:58,749 - __main__ - INFO - self.getsymval('{tls_version}')        : None
2019-09-10 15:47:58,749 - __main__ - INFO - self.getsymval('{mail_addr}')          : root@localhost
2019-09-10 15:47:58,749 - __main__ - INFO - self.getsymval('{mail_host}')          : pml125.home.tachtler.net
2019-09-10 15:47:58,750 - __main__ - INFO - self.getsymval('{mail_mailer}')        : local
2019-09-10 15:47:58,750 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:58,750 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:47:58,750 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:47:58,750 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:47:58,750 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:47:58,750 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:47:58,750 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:47:58,750 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:47:58,751 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:47:58,751 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:47:58,751 - __main__ - INFO - ----------------------------------------
2019-09-10 15:47:58,751 - __main__ - INFO - sendmail-pymilter - LEAVE: envfrom     :
2019-09-10 15:47:58,751 - __main__ - INFO - ========================================
2019-09-10 15:48:05,246 - __main__ - INFO - ========================================
2019-09-10 15:48:05,247 - __main__ - INFO - sendmail-pymilter - ENTRY: envrcpt     :
2019-09-10 15:48:05,247 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:05,247 - __main__ - INFO - mailto                                 : <klaus@localhost>
2019-09-10 15:48:05,247 - __main__ - INFO -  - parameter                           : ()
2019-09-10 15:48:05,247 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:05,247 - __main__ - INFO - self.getsymval('{rcpt_addr}')          : klaus@localhost
2019-09-10 15:48:05,247 - __main__ - INFO - self.getsymval('{rcpt_host}')          : pml125.home.tachtler.net
2019-09-10 15:48:05,247 - __main__ - INFO - self.getsymval('{rcpt_mailer}')        : local
2019-09-10 15:48:05,247 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:48:05,248 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:48:05,249 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:05,249 - __main__ - INFO - sendmail-pymilter - LEAVE: envrcpt     :
2019-09-10 15:48:05,249 - __main__ - INFO - ========================================
2019-09-10 15:48:05,249 - __main__ - INFO - ========================================
2019-09-10 15:48:05,249 - __main__ - INFO - sendmail-pymilter - ENTRY: header      :
2019-09-10 15:48:05,249 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,413 - __main__ - INFO - field => value                         : Subject: Test e-Mail.
2019-09-10 15:48:37,413 - __main__ - INFO - field => value                         : From: sender@example.com
2019-09-10 15:48:37,414 - __main__ - INFO - field => value                         : To: receiver@example.com
2019-09-10 15:48:37,414 - __main__ - INFO - field => value                         : Message-Id: <20190910134805.40B391109F84@pml125.home.tachtler.net>
2019-09-10 15:48:37,414 - __main__ - INFO - field => value                         : Date: Tue, 10 Sep 2019 15:47:58 +0200 (CEST)
2019-09-10 15:48:37,415 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,415 - __main__ - INFO - self.getsymval('{i}')                  : 40B391109F84
2019-09-10 15:48:37,415 - __main__ - INFO - self.getsymval('{client_ptr}')         : None
2019-09-10 15:48:37,415 - __main__ - INFO - self.getsymval('{auth_authen}')        : None
2019-09-10 15:48:37,415 - __main__ - INFO - self.getsymval('{auth_author} ')       : None
2019-09-10 15:48:37,415 - __main__ - INFO - self.getsymval('{auth_type} ')         : None
2019-09-10 15:48:37,415 - __main__ - INFO - self.getsymval('{cert_issuer} ')       : None
2019-09-10 15:48:37,416 - __main__ - INFO - self.getsymval('{cert_subject}')       : None
2019-09-10 15:48:37,416 - __main__ - INFO - self.getsymval('{cipher_bits}')        : None
2019-09-10 15:48:37,416 - __main__ - INFO - self.getsymval('{cipher}')             : None
2019-09-10 15:48:37,416 - __main__ - INFO - self.getsymval('{tls_version}')        : None
2019-09-10 15:48:37,416 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,416 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:48:37,416 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:48:37,416 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:48:37,416 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:48:37,417 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:48:37,417 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:48:37,417 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:48:37,417 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:48:37,417 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:48:37,417 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,417 - __main__ - INFO - sendmail-pymilter - LEAVE: header      :
2019-09-10 15:48:37,417 - __main__ - INFO - ========================================
2019-09-10 15:48:37,418 - __main__ - INFO - ========================================
2019-09-10 15:48:37,418 - __main__ - INFO - sendmail-pymilter - ENTRY: eoh         :
2019-09-10 15:48:37,418 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,418 - __main__ - INFO - self.getsymval('{i}')                  : 40B391109F84
2019-09-10 15:48:37,418 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,418 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:48:37,418 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:48:37,418 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:48:37,418 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:48:37,419 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:48:37,419 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:48:37,419 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:48:37,419 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:48:37,419 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:48:37,419 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,419 - __main__ - INFO - sendmail-pymilter - LEAVE: eoh         :
2019-09-10 15:48:37,419 - __main__ - INFO - ========================================
2019-09-10 15:48:37,420 - __main__ - INFO - ========================================
2019-09-10 15:48:37,420 - __main__ - INFO - sendmail-pymilter - ENTRY: body        :
2019-09-10 15:48:37,420 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,420 - __main__ - INFO - body                                   : b'Hello,\r\n\r\ntest e-Mail.\r\n\r\nGreetings\r\n'
2019-09-10 15:48:37,420 - __main__ - INFO -  - decoded (UTF-8)                     : Hello,

test e-Mail.

Greetings

2019-09-10 15:48:37,420 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,421 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:48:37,421 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:48:37,421 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:48:37,421 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:48:37,421 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:48:37,421 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:48:37,421 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:48:37,421 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:48:37,422 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:48:37,422 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,422 - __main__ - INFO - sendmail-pymilter - LEAVE: body        :
2019-09-10 15:48:37,422 - __main__ - INFO - ========================================
2019-09-10 15:48:37,422 - __main__ - INFO - ========================================
2019-09-10 15:48:37,422 - __main__ - INFO - sendmail-pymilter - ENTRY: eom         :
2019-09-10 15:48:37,422 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,423 - __main__ - INFO - self.getsymval('{i}')                  : 40B391109F84
2019-09-10 15:48:37,423 - __main__ - INFO - self.getsymval('{auth_authen}')        : None
2019-09-10 15:48:37,423 - __main__ - INFO - self.getsymval('{auth_author} ')       : None
2019-09-10 15:48:37,423 - __main__ - INFO - self.getsymval('{auth_type} ')         : None
2019-09-10 15:48:37,423 - __main__ - INFO - self.getsymval('{cert_issuer} ')       : None
2019-09-10 15:48:37,423 - __main__ - INFO - self.getsymval('{cert_subject}')       : None
2019-09-10 15:48:37,423 - __main__ - INFO - self.getsymval('{cipher_bits}')        : None
2019-09-10 15:48:37,424 - __main__ - INFO - self.getsymval('{cipher}')             : None
2019-09-10 15:48:37,424 - __main__ - INFO - self.getsymval('{tls_version}')        : None
2019-09-10 15:48:37,424 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,424 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:48:37,424 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:48:37,424 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:48:37,424 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:48:37,424 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:48:37,425 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:48:37,425 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:48:37,425 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:48:37,425 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:48:37,425 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:37,425 - __main__ - INFO - sendmail-pymilter - LEAVE: eom         :
2019-09-10 15:48:37,425 - __main__ - INFO - ========================================
2019-09-10 15:48:44,699 - __main__ - INFO - ========================================
2019-09-10 15:48:44,700 - __main__ - INFO - sendmail-pymilter - ENTRY: close       :
2019-09-10 15:48:44,700 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:44,700 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:44,700 - __main__ - INFO - self.getsymval('{j}')                  : pml125.home.tachtler.net
2019-09-10 15:48:44,700 - __main__ - INFO - self.getsymval('{_}')                  : None
2019-09-10 15:48:44,700 - __main__ - INFO - self.getsymval('{client_addr}')        : None
2019-09-10 15:48:44,700 - __main__ - INFO - self.getsymval('{client_name}')        : None
2019-09-10 15:48:44,700 - __main__ - INFO - self.getsymval('{client_port}')        : None
2019-09-10 15:48:44,701 - __main__ - INFO - self.getsymval('{daemon_addr}')        : 127.0.0.1
2019-09-10 15:48:44,701 - __main__ - INFO - self.getsymval('{daemon_name}')        : pml125.home.tachtler.net
2019-09-10 15:48:44,701 - __main__ - INFO - self.getsymval('{daemon_port}')        : None
2019-09-10 15:48:44,701 - __main__ - INFO - self.getsymval('{v}')                  : Postfix 3.4.6
2019-09-10 15:48:44,701 - __main__ - INFO - ----------------------------------------
2019-09-10 15:48:44,701 - __main__ - INFO - sendmail-pymilter - LEAVE: close       :
2019-09-10 15:48:44,701 - __main__ - INFO - ========================================
^C
2019-09-10 15:48:53,637 - __main__ - INFO - ========================================
2019-09-10 15:48:53,638 - __main__ - INFO - InfoMilter.py milter shutdown
```

## TODO:
A list of possible changes for the future:

- Add a setup.py file 
- Add the possibility to use a configuration file.
- Add a systemd script.
- Build a rpm package for CentOS-7.

## Thanks to
Many thanks for the great work, support and help to realize this project:

- Stuart D. Gathman (stuart@gathman.org) [sdgathman/pymilter](https://github.com/sdgathman/pymilter)
