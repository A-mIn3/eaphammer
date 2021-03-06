#!/usr/bin/env python
# This file is part of Responder
# Original work by Laurent Gaffie - Trustwave Holdings
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import binascii
import configparser
from . import utils

from core.responder.utils import *

from settings import settings

__version__ = 'Responder 2.3'

class Settings:

    def __init__(self):
        self.ResponderPATH = settings.dict['paths']['directories']['root']
        self.Bind_To = '10.0.0.1'

    def __str__(self):
        ret = 'Settings class:\n'
        for attr in dir(self):
            value = str(getattr(self, attr)).strip()
            ret += "    Settings.%s = %s\n" % (attr, value)
        return ret

    def toBool(self, str):
        return str.upper() == 'ON'

    def ExpandIPRanges(self):
        def expand_ranges(lst):
            ret = []
            for l in lst:
                tab = l.split('.')
                x = {}
                i = 0
                for byte in tab:
                    if '-' not in byte:
                        x[i] = x[i+1] = int(byte)
                    else:
                        b = byte.split('-')
                        x[i] = int(b[0])
                        x[i+1] = int(b[1])
                    i += 2
                for a in range(x[0], x[1]+1):
                    for b in range(x[2], x[3]+1):
                        for c in range(x[4], x[5]+1):
                            for d in range(x[6], x[7]+1):
                                ret.append('%d.%d.%d.%d' % (a, b, c, d))
            return ret

        self.RespondTo = expand_ranges(self.RespondTo)
        self.DontRespondTo = expand_ranges(self.DontRespondTo)

    def populate(self, options):

        config = settings.dict['core']['responder']

        if options['interface'] is None and utils.IsOsX() is False:
            print(utils.color("Error: -I <if> mandatory option is missing", 1))
            sys.exit(-1)

        # Servers
        self.HTTP_On_Off     = self.toBool(config['Responder Core']['http'])
        self.SSL_On_Off      = self.toBool(config['Responder Core']['https'])
        self.SMB_On_Off      = self.toBool(config['Responder Core']['smb'])
        self.SQL_On_Off      = self.toBool(config['Responder Core']['sql'])
        self.FTP_On_Off      = self.toBool(config['Responder Core']['ftp'])
        self.POP_On_Off      = self.toBool(config['Responder Core']['pop'])
        self.IMAP_On_Off     = self.toBool(config['Responder Core']['imap'])
        self.SMTP_On_Off     = self.toBool(config['Responder Core']['smtp'])
        self.LDAP_On_Off     = self.toBool(config['Responder Core']['ldap'])
        self.DNS_On_Off      = self.toBool(config['Responder Core']['dns'])
        self.Krb_On_Off      = self.toBool(config['Responder Core']['kerberos'])

        #self.HTTP_On_Off     = self.toBool(config.get('Responder Core', 'HTTP'))
        #self.SSL_On_Off      = self.toBool(config.get('Responder Core', 'HTTPS'))
        #self.SMB_On_Off      = self.toBool(config.get('Responder Core', 'SMB'))
        #self.SQL_On_Off      = self.toBool(config.get('Responder Core', 'SQL'))
        #self.FTP_On_Off      = self.toBool(config.get('Responder Core', 'FTP'))
        #self.POP_On_Off      = self.toBool(config.get('Responder Core', 'POP'))
        #self.IMAP_On_Off     = self.toBool(config.get('Responder Core', 'IMAP'))
        #self.SMTP_On_Off     = self.toBool(config.get('Responder Core', 'SMTP'))
        #self.LDAP_On_Off     = self.toBool(config.get('Responder Core', 'LDAP'))
        #self.DNS_On_Off      = self.toBool(config.get('Responder Core', 'DNS'))
        #self.Krb_On_Off      = self.toBool(config.get('Responder Core', 'Kerberos'))
        # Db File
        #self.DatabaseFile    = os.path.join(self.ResponderPATH, config.get('Responder Core', 'Database'))
        self.DatabaseFile    = os.path.join(self.ResponderPATH, config['Responder Core']['database'])

        # Log Files
        self.LogDir = os.path.join(self.ResponderPATH, 'logs')

        if not os.path.exists(self.LogDir):
            os.mkdir(self.LogDir)

        self.SessionLogFile      = os.path.join(self.LogDir, config['Responder Core']['sessionlog'])
        self.PoisonersLogFile    = os.path.join(self.LogDir, config['Responder Core']['poisonerslog'])
        self.AnalyzeLogFile      = os.path.join(self.LogDir, config['Responder Core']['analyzelog'])

        self.FTPLog          = os.path.join(self.LogDir, 'FTP-Clear-Text-Password-%s.txt')
        self.IMAPLog         = os.path.join(self.LogDir, 'IMAP-Clear-Text-Password-%s.txt')
        self.POP3Log         = os.path.join(self.LogDir, 'POP3-Clear-Text-Password-%s.txt')
        self.HTTPBasicLog    = os.path.join(self.LogDir, 'HTTP-Clear-Text-Password-%s.txt')
        self.LDAPClearLog    = os.path.join(self.LogDir, 'LDAP-Clear-Text-Password-%s.txt')
        self.SMBClearLog     = os.path.join(self.LogDir, 'SMB-Clear-Text-Password-%s.txt')
        self.SMTPClearLog    = os.path.join(self.LogDir, 'SMTP-Clear-Text-Password-%s.txt')
        self.MSSQLClearLog   = os.path.join(self.LogDir, 'MSSQL-Clear-Text-Password-%s.txt')

        self.LDAPNTLMv1Log   = os.path.join(self.LogDir, 'LDAP-NTLMv1-Client-%s.txt')
        self.HTTPNTLMv1Log   = os.path.join(self.LogDir, 'HTTP-NTLMv1-Client-%s.txt')
        self.HTTPNTLMv2Log   = os.path.join(self.LogDir, 'HTTP-NTLMv2-Client-%s.txt')
        self.KerberosLog     = os.path.join(self.LogDir, 'MSKerberos-Client-%s.txt')
        self.MSSQLNTLMv1Log  = os.path.join(self.LogDir, 'MSSQL-NTLMv1-Client-%s.txt')
        self.MSSQLNTLMv2Log  = os.path.join(self.LogDir, 'MSSQL-NTLMv2-Client-%s.txt')
        self.SMBNTLMv1Log    = os.path.join(self.LogDir, 'SMB-NTLMv1-Client-%s.txt')
        self.SMBNTLMv2Log    = os.path.join(self.LogDir, 'SMB-NTLMv2-Client-%s.txt')
        self.SMBNTLMSSPv1Log = os.path.join(self.LogDir, 'SMB-NTLMSSPv1-Client-%s.txt')
        self.SMBNTLMSSPv2Log = os.path.join(self.LogDir, 'SMB-NTLMSSPv2-Client-%s.txt')

        # HTTP Options
        self.Serve_Exe        = self.toBool(config['HTTP Server']['serve-exe'])
        self.Serve_Always     = self.toBool(config['HTTP Server']['serve-always'])
        self.Serve_Html       = self.toBool(config['HTTP Server']['serve-html'])
        self.Html_Filename    = config['HTTP Server']['htmlfilename']
        self.Exe_Filename     = config['HTTP Server']['exefilename']
        self.Exe_DlName       = config['HTTP Server']['exedownloadname']
        self.WPAD_Script      = config['HTTP Server']['wpadscript']
        self.HtmlToInject     = config['HTTP Server']['htmltoinject']

        if not os.path.exists(self.Html_Filename):
            print(utils.color("/!\ Warning: %s: file not found" % self.Html_Filename, 3, 1))

        if not os.path.exists(self.Exe_Filename):
            print(utils.color("/!\ Warning: %s: file not found" % self.Exe_Filename, 3, 1))

        # SSL Options
        self.SSLKey  = config['HTTPS Server']['sslkey']
        self.SSLCert = config['HTTPS Server']['sslcert']

        # Respond to hosts
        self.RespondTo         = [_f for _f in [x.upper().strip() for x in config['Responder Core']['respondto'].strip().split(',')] if _f]
        self.RespondToName     = [_f for _f in [x.upper().strip() for x in config['Responder Core']['respondtoname'].strip().split(',')] if _f]
        self.DontRespondTo     = [_f for _f in [x.upper().strip() for x in config['Responder Core']['dontrespondto'].strip().split(',')] if _f]
        self.DontRespondToName = [_f for _f in [x.upper().strip() for x in config['Responder Core']['dontrespondtoname'].strip().split(',')] if _f]

        # Auto Ignore List
        self.AutoIgnore                 = self.toBool(config['Responder Core']['autoignoreaftersuccess'])
        self.CaptureMultipleCredentials = self.toBool(config['Responder Core']['capturemultiplecredentials'])
        self.AutoIgnoreList             = []

        # CLI options
        self.LM_On_Off       = options['responder']['lm_downgrade']
        self.WPAD_On_Off     = options['responder']['wpad']
        self.Wredirect       = options['responder']['w_redirect']
        self.NBTNSDomain     = options['responder']['nbtns_domain']
        self.Basic           = options['responder']['basic_auth']
        self.Finger_On_Off   = options['responder']['fingerprint']
        self.Interface       = options['interface']
        self.OURIP           = options['responder']['ourip']
        self.Force_WPAD_Auth = options['responder']['force_wpad_auth']
        self.Upstream_Proxy  = options['responder']['upstream_proxy']
        self.AnalyzeMode     = options['responder']['analyze']
        self.Verbose         = options['responder']['verbose']
        self.CommandLine     = str(sys.argv)

        if self.HtmlToInject is None:
            self.HtmlToInject = ''

        self.Bind_To = utils.FindLocalIP(self.Interface, self.OURIP)

        self.IP_aton         = socket.inet_aton(self.Bind_To)
        self.Os_version      = sys.platform

        # Set up Challenge
        self.NumChal = config['Responder Core']['challenge']

        if len(self.NumChal) is not 16:
            print(utils.color("[!] The challenge must be exactly 16 chars long.\nExample: 1122334455667788", 1))
            sys.exit(-1)

        self.Challenge = ""
        for i in range(0, len(self.NumChal),2):
            self.Challenge += self.NumChal[i:i+2]

        # Set up logging
        logging.basicConfig(filename=self.SessionLogFile, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning('Responder Started: %s' % self.CommandLine)
        logging.warning('Responder Config: %s' % str(self))

        Formatter = logging.Formatter('%(asctime)s - %(message)s')
        PLog_Handler = logging.FileHandler(self.PoisonersLogFile, 'w')
        ALog_Handler = logging.FileHandler(self.AnalyzeLogFile, 'a')
        PLog_Handler.setLevel(logging.INFO)
        ALog_Handler.setLevel(logging.INFO)
        PLog_Handler.setFormatter(Formatter)
        ALog_Handler.setFormatter(Formatter)

        self.PoisonersLogger = logging.getLogger('Poisoners Log')
        self.PoisonersLogger.addHandler(PLog_Handler)

        self.AnalyzeLogger = logging.getLogger('Analyze Log')
        self.AnalyzeLogger.addHandler(ALog_Handler)

def init():
    global Config
    Config = Settings()
