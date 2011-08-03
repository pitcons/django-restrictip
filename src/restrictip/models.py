
import struct
import socket
from django.db import models
from django.utils.translation import ugettext_lazy as _
import fields

class IPIntegerField(models.Field):
    empty_strings_allowed = False
    description = _("IP address")

    def get_internal_type(self):
        return "BigIntegerField"

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.IPIntegerField}
        defaults.update(kwargs)
        return super(IPIntegerField, self).formfield(**defaults)

    def to_python(self, value):
        if value is None:
            return value
        try:
            return struct.unpack('!I', socket.inet_aton(value))[0]
        except (TypeError, ValueError):
            raise exceptions.ValidationError(self.error_messages['invalid'])

class Rule(models.Model):
    path = models.CharField(max_length=255)
    policy = models.CharField(max_length=1, choices=(('d', 'Deny by default'), 
                                                     ('a', 'Allow by default')))
    weight = models.IntegerField(db_index=True, default=0)

    def is_allow(self):
        return self.policy == 'a'

    def is_deny(self):
        return self.policy == 'd'

    def __unicode__(self):
        return self.path

class RuleItem(models.Model):

    rule = models.ForeignKey(Rule)
    ip_from = IPIntegerField(db_index=True)
    ip_to =  IPIntegerField(db_index=True)
    comment = models.CharField(max_length=512, null=True, blank=True)
    action = models.CharField(max_length=1, choices=(('a', 'Allow'), 
                                                     ('d', 'Deny')))

    def is_allow(self):
        return self.action == 'a'

    def is_deny(self):
        return self.action == 'd'

    def __unicode__(self):
        ip_from = socket.inet_ntoa(struct.pack('!I', self.ip_from))
        ip_to = socket.inet_ntoa(struct.pack('!I', self.ip_to))
        return u'({0}) {1} - {2}'.format(self.get_action_display(), ip_from, ip_to)

