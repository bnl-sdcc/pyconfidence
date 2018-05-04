#!/usr/bin/env python

__author__ = "Jose Caballero"
__email__ = "jcaballero@bnl.gov"


import ConfigParser

class PyConfig(ConfigParser.SafeConfigParser, object):

    def get(self, *k, **kw):
        """
        extension of the original method get()
        :param *k: section, option1, [option2], ..., [optionN]
        :param **kw: original dictionary parameters, plus optional "default"
        :rtype :
        """
        try:
            default = kw.pop('default')
            is_default = True
        except Exception, ex:
            is_default = False

        try:
            value = self.rget(*k, **kw)
        except ConfigParser.NoOptionError, ex:
            if is_default:
                value = default
            else:
                raise ex
        except Exception, ex:
            raise ex
        return value

    def rget(self, *k, **kw):
        if len(k) > 2:
            newsec = value = super(PyConfig, self).get(*k[:2], **kw)
            k = [newsec] + list(k[2:])
            return self.rget(*k, **kw)
        else:
            value = super(PyConfig, self).get(*k, **kw)
            if value == "None":
                value = None
            return value


    def getint(self, *k, **kw):
        """
        extension of the original method getint()
        """
        value = self.get(*k, **kw)
        return int(value)


    def getfloat(self, *k, **kw):
        """
        extension of the original method getfloat()
        """
        value = self.get(*k, **kw)
        return float(value)


    def getboolean(self, *k, **kw):
        """
        extension of the original method getboolean()
        """
        value = self.get(*k, **kw)
        value = value.lower()
        if value not in self._boolean_states:
            raise ValueError, 'Not a boolean: %s' % value
        return self._boolean_states[value]


    def getlist(self, *k, **kw):
        """
        """
        splitter = kw.pop('splitter', ',')
        value = self.get(*k, **kw)
        value_l = [token.strip() for token in value.split(splitter)]
        return value_l


    def getlistint(self, *k, **kw):
        """
        """
        splitter = kw.pop('splitter', ',')
        value = self.get(*k, **kw)
        value_l = [int(token.strip()) for token in value.split(splitter)]
        return value_l


    def getlistfloat(self, *k, **kw):
        """
        """
        splitter = kw.pop('splitter', ',')
        value = self.get(*k, **kw)
        value_l = [float(token.strip()) for token in value.split(splitter)]
        return value_l


    def getlistboolean(self, *k, **kw):
        """
        """
        splitter = kw.pop('splitter', ',')
        value = self.get(*k, **kw)
        value_l = []
        for token in value.split(splitter):
            token = token.strip()
            if token not in self._boolean_states:
                raise ValueError, 'Not a boolean: %s' %token
            value_l.append(self._boolean_states[token])
        return value_l

