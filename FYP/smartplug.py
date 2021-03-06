##
# The MIT License (MIT)
#
# Copyright (c) 2014 Stefan Wendler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
##

__author__ = 'Stefan Wendler, sw@kaltpost.de'

import requests as req
import optparse as par
import logging as log

from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parseString


class SmartPlug(object):

    """
    Simple class to access a "EDIMAX Smart Plug Switch SP-1101W"

    Usage example when used as library:
    
    p = SmartPlug("192.168.2.143", ('admin', 'password'))

    p.state = "OFF"
    p.state = "ON"
    print(p.state)
    
    Usage example when used as command line utility:

    turn plug on:

    python smartplug.py -H 172.16.100.75 -l admin -p 1234 -s ON

    turn plug off:

    python smartplug.py -H 172.16.100.75-l admin -p 1234 -s OFF

    get plug state:

    python smartplug.py -H 172.16.100.75-l admin -p 1234 -g

    """

    def __init__(self, host, auth):

        """
        Create a new SmartPlug instance identified by the given URL.

        :rtype : object
        :param host: The IP/hostname of the SmartPlug. E.g. '172.16.100.75'
        :param auth: User and password to authenticate with the plug. E.g. ('admin', '1234')
        """

        self.url = "http://%s:10000/smartplug.cgi" % host
        self.auth = auth
        self.domi = getDOMImplementation()

    def __xml_cmd(self, cmdId, cmdStr):

        """
        Create XML representation of a command.

        :param cmdId: Use 'get' to request plug state, use 'setup' change plug state.
        :param cmdStr: Empty string for 'get', 'ON' or 'OFF' for 'setup'
        :return: XML representation of command
        """

        doc = self.domi.createDocument(None, "SMARTPLUG", None)
        doc.documentElement.setAttribute("id", "edimax")

        cmd = doc.createElement("CMD")
        cmd.setAttribute("id", cmdId)
        state = doc.createElement("Device.System.Power.State")
        cmd.appendChild(state)
        state.appendChild(doc.createTextNode(cmdStr))

        doc.documentElement.appendChild(cmd)

        return doc.toxml()

    def __post_xml(self, xml):

        """
        Post XML command  as multipart file to SmartPlug, parse XML response.

        :param xml: XML representation of command (as generated by __xml_cmd)
        :return: 'OK' on success, 'FAILED' otherwise
        """

        files = {'file': xml}

        res = req.post(self.url, auth=self.auth, files=files)

        if res.status_code == req.codes.ok:
            dom = parseString(res.text)

            try:
                val = dom.getElementsByTagName("CMD")[0].firstChild.nodeValue

                if val is None:
                    val = dom.getElementsByTagName("CMD")[0].getElementsByTagName("Device.System.Power.State")[0].\
                        firstChild.nodeValue

                return val

            except Exception as e:

                print(e.__str__())

        return None

    @property
    def state(self):

        """
        Get the current state of the SmartPlug.

        :return: 'ON' or 'OFF'
        """

        res = self.__post_xml(self.__xml_cmd("get", ""))

        if res != "ON" and res != "OFF":
            raise Exception("Failed to communicate with SmartPlug")

        return res

    @state.setter
    def state(self, value):

        """
        Set the state of the SmartPlug

        :param value: 'ON', 'on', 'OFF' or 'off'
        """

        if value == "ON" or value == "on":
            res = self.__post_xml(self.__xml_cmd("setup", "ON"))
        else:
            res = self.__post_xml(self.__xml_cmd("setup", "OFF"))

        if res != "OK":
            raise Exception("Failed to communicate with SmartPlug")

if __name__ == "__main__":

    # this turns on debugging from requests library
    log.basicConfig(level=log.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    usage = "%prog [options]"

    parser = par.OptionParser(usage)

    parser.add_option("-H", "--host",  default="172.16.100.75", help="Base URL of the SmartPlug")
    parser.add_option("-l", "--login",  default="admin", help="Login user to authenticate with SmartPlug")
    parser.add_option("-p", "--password",  default="1234", help="Password to authenticate with SmartPlug")

    parser.add_option("-g", "--get",  action="store_true", help="Get state of plug")
    parser.add_option("-s", "--set",  help="Set state of plug: ON or OFF")

    (options, args) = parser.parse_args()

    try:

        p = SmartPlug(options.host, (options.login, options.password))

        if options.get:
            print(p.state)
        elif options.set:
            p.state = options.set

    except Exception as e:
        print(e.__str__())