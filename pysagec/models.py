from collections import OrderedDict as odict


class Field:
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.value = None

        # These values will be set by metaclass
        self.name = None
        self.default = None

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        else:
            return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        self.value = value
        obj.__dict__[self.name] = value

    def __repr__(self):
        return '<Field name={!r}>'.format(self.name)


class ModelMeta(type):
    def __new__(mcs, clsname, bases, clsdict):
        fields = []
        for name, value in clsdict.items():
            if isinstance(value, Field):
                value.name = name  # Init `Field.name`
                fields.append(value)
        clsdict['fields'] = fields
        return type.__new__(mcs, clsname, bases, clsdict)

    @classmethod
    def __prepare__(mcs, clsname, bases):
        return odict()


class Model(metaclass=ModelMeta):
    root_tag = 'root'

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def as_dict(self):
        tags = [{k.tag_name: k.value} for k in self.fields]
        return {self.root_tag: tags}


class AuthInfo(Model):
    root_tag = 'mrw:AuthInfo'

    franchise_code = Field('mrw:CodigoFranquicia')
    subscriber_code = Field('mrw:CodigoAbonado')
    departament_code = Field('mrw:CodigoDepartamento')
    username = Field('mrw:UserName')
    password = Field('mrw:Password')
