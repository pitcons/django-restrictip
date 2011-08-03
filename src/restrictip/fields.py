
import struct
import socket
import django

class IPIntegerInput(django.forms.widgets.TextInput):
    input_type = 'text'
    
    def _format_value(self, value):        
        if isinstance(value, int) or isinstance(value, long):
            return socket.inet_ntoa(struct.pack('!I', value))
        else:
            return value

class IPIntegerField(django.forms.IPAddressField):
    widget = IPIntegerInput
