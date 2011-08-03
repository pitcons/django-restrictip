"""
middlware to restrict IP addresses
"""
import re
import struct
import socket
from django import http
from django.template.loader import get_template
from django.template import TemplateDoesNotExist, Context

from models import Rule, RuleItem


class RescrictIpMiddleware(object):

    def get_ip(self, request):
        ip = request.META.get('REMOTE_ADDR', False)
        if (not ip or ip == '127.0.0.1') and request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
            
        int_ip = struct.unpack('!I', socket.inet_aton(ip))[0]
        return int_ip 

    def process_request(self, request):
        ip = self.get_ip(request)
        for rule in Rule.objects.order_by('weight'):
            if re.match(rule.path, request.path_info):
                items = RuleItem.objects.filter(ip_from__lte=ip,
                                                ip_to__gte=ip,
                                                rule=rule)[:1]
                if items:
                    return None if items[0].is_allow() else self.forbidden()

                return None if rule.is_allow() else self.forbidden()
        return None

    def forbidden(self):
        try:            
            template = get_template('403.html')
            html = template.render(Context({}))
        except TemplateDoesNotExist:
            html = '<h1>Forbidden</h1>'
        return http.HttpResponseForbidden(html)
