from collections import OrderedDict as odict


class Field:
    def __init__(self, tag_name, *, default=None, **kwargs):
        self.tag_name = tag_name
        self.value = None
        self.default = default

        # This value will be set by metaclass
        self.name = None

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        else:
            return obj.__dict__.get(self.name, self.default)

    def __set__(self, obj, value):
        self.value = value
        obj.__dict__[self.name] = value

    def as_dict(self, obj):
        return {self.tag_name: self.__get__(obj)}


class String(Field):
    def __repr__(self):
        return '<String name={!r}>'.format(self.name)


class Nested(Field):
    def __init__(self, tag_name, model, default=None,
                 unwrap=False, many=False, **kwargs):
        super().__init__(tag_name, default=default)

        assert not (many and unwrap), ('If `many` is `True `unwrap` must be '
                                       'set to `False`')

        self.model = model
        self.unwrap = unwrap
        self.many = many
        self.default = [model()] if many else model()

    def as_dict(self, obj):
        data = self.__get__(obj)
        if self.many:
            return {self.tag_name: [item.as_dict() for item in data]}
        elif self.unwrap:
            return {self.tag_name: data.as_dict()[self.model.root_tag]}
        else:
            return {self.tag_name: data.as_dict()}

    def __repr__(self):
        return '<Nested name={!r} model={!r}>'.format(self.name, self.model)


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
        # By returning an OrderedDict instead of a normal dictionary,
        # the resulting definition order is easily captured.
        # See Python Cookbook, Third Edition. Chapter 9
        return odict()


class Model(metaclass=ModelMeta):
    root_tag = 'root'

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def as_dict(self):
        return {self.root_tag: [f.as_dict(self) for f in self.fields]}
