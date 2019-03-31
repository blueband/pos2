"""A modular API for interacting
with the RouteSMS HTTP API
"""
import requests
from RouteSMS.error import RouteSMSException


class RouteSMS(object):
    """Interact with the RouteSMS HTTP API"""

    def __init__(self, username, password):
        """
        Class constructor
        :param username:
        :param password:
        :return:
        """
        self.username = username
        self.password = password

    def send_message(self, recipient, sender, message):
        """
        Accepts the message details and sends SMS
        :param recipient:
        :param sender:
        :param message:
        :return:
        """
        recipient = str(recipient)
        #http://www.estoresms.com/smsapi.php?username=user&password=1234&sender=@@sender@@&recipient=@@recipient@@&message=@@message@@&

        #url = "http://smsplus3.routesms.com:8080/bulksms/bulksms?"
        url = "http://www.estoresms.com:80/smsapi.php?"
        credentials = "username=" + self.username + "&password=" + self.password
        msg_type = "&type=0&dlr=1"

        # msg_format = "&destination=" + recipient + "&source=" + \
        #              sender + "&message=" + message

        msg_format = "&sender=@@" + sender +  "&recipient=@@" + recipient + "@@&message=@@" + message + "@@&"

        #final = url + credentials + msg_type + msg_format
        final = url + credentials + msg_format

        try:
            result = requests.get(final)
            status = result.text.split("|")
            if status[0] == "1701" and status[1] == recipient:
                return True
            else:
                print(status)
                return False
        except requests.ConnectionError:
            raise RouteSMSException("Internet connection error", "00")

