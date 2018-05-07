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
        similar to get(), but converts the value into a list of strings
        One of the named parameters is the "splitter", to decide how to 
        split the original value
        """
        splitter = kw.pop('splitter', ',')
        value = self.get(*k, **kw)
        value_l = [token.strip() for token in value.split(splitter)]
        return value_l


    def getlistint(self, *k, **kw):
        """
        similar to getint(), but converts the value into a list of integers 
        One of the named parameters is the "splitter", to decide how to 
        split the original value
        """
        splitter = kw.pop('splitter', ',')
        value = self.get(*k, **kw)
        value_l = [int(token.strip()) for token in value.split(splitter)]
        return value_l


    def getlistfloat(self, *k, **kw):
        """
        similar to getfloat(), but converts the value into a list of floats 
        One of the named parameters is the "splitter", to decide how to 
        split the original value
        """
        splitter = kw.pop('splitter', ',')
        value = self.get(*k, **kw)
        value_l = [float(token.strip()) for token in value.split(splitter)]
        return value_l


    def getlistboolean(self, *k, **kw):
        """
        similar to getboolean(), but converts the value into a list of booleans 
        One of the named parameters is the "splitter", to decide how to 
        split the original value
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


    def merge(self, new_config, overridesection=False, overrideoption=False, includemissing=True):
        """
        :param new_config PyConfig: new config object being merged into the current one
        :param overridesection boolean: determines if a common section should be replaced or merged
        :param overrideoption boolean: determines if a common option should be replaced or merged
        :param includemissing boolean: determines if new options should be added or not
        """
        new_section_l = new_config.sections()
        for new_section in new_section_l:
            if new_section not in self.sections():
                self._clonesection(new_section, new_config)
            else:
                if overridesection:
                    self._overridesection(new_section, new_config)
                else:
                    self._mergesection(new_section, new_config, overrideoption, includemissing)


    def _clonesection(self, new_section, new_config):
        """ 
        create a new section, and copy its content 
        :param new_section str: the section being cloned
        :param new_config PyConfig: the PyConfig object source of the new section
        """
        self.add_section(new_section)
        for opt in new_config.options(new_section):
            value = new_config.get(new_section, opt, raw=True)
            self.set(new_section, opt, value)


    def _overridesection(self, new_section, new_config):
        """ 
        replace an existing section with a new one
        :param new_section str: the section being cloned
        :param new_config PyConfig: the PyConfig object source of the new section
        """
        self.remove_section(new_section)
        self._clonesection(new_section, new_config)

    
    def _mergesection(self, new_section, new_config, overrideoption, includemissing):
        """
        merge the content of a current Config object section
        with the content of the same section 
        from a different Config object
        :param new_section str: the section being merged
        :param new_config PyConfig: config object with the new section
        :param overrideoption boolean: determines if a common option should be replaced or merged
        :param includemissing boolean: determines if new options should be added or not
        """
        option_l = self.options(new_section)
        new_option_l = new_config.options(new_section)
        for new_option in new_option_l:
            value = new_config.get(new_section, new_option, raw=True)
            if new_option in option_l:
                if overrideoption:
                    self.set(new_section, new_option, value)
            else:
                if includemissing:
                    self.set(new_section, new_option, value)
            

