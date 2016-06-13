from collections import OrderedDict as odict


class BaseField:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        else:
            return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        self.value = value
        obj.__dict__[self.name] = value


class Field(BaseField):
    def __init__(self, tag_name, default=None):
        self.tag_name = tag_name
        self.value = None
        self.default = default

        # This value will be set by metaclass
        self.name = None

    def as_dict(self, obj):
        return {self.tag_name: self.__get__(obj)}

    def __repr__(self):
        return '<Field name={!r}>'.format(self.name)


class Nested(BaseField):
    def __init__(self, tag_name, model, unwrap=False, many=False):
        assert (
            not (many and unwrap),
            'If `many` is `True `unwrap` must be set to `False`'
        )
        self.tag_name = tag_name
        self.model = model
        self.unwrap = unwrap
        self.many = many

        self.value = None
        self.default = [model()] if many else model()

        # This value will be set by metaclass
        self.name = None

    def as_dict(self, obj):
        data = self.__get__(obj)
        if not self.many and self.unwrap:
            return {self.tag_name: data.as_dict()[self.model.root_tag]}
        elif not self.many and not self.unwrap:
            return {self.tag_name: data.as_dict()}
        elif self.many:
            return {self.tag_name: [item.as_dict() for item in data]}

    def __repr__(self):
        return '<Nested name={!r} type={!r}>'.format(self.name, self.model)


class ModelMeta(type):
    def __new__(mcs, clsname, bases, clsdict):
        fields = []
        for name, value in clsdict.items():
            if isinstance(value, (Field, Nested)):
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
        tags = []
        for k in self.fields:
            value = k.as_dict(self)
            tags.append(value)

        return {self.root_tag: tags}
