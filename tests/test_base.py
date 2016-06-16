from pysagec import base


def test_field():
    f = base.Field('tag')
    assert f.__get__(None, None) is f


def test_string():
    f = base.String('tag')
    assert 'String' in repr(f)


def test_nested():
    f = base.Nested('tag', base.Model)
    assert 'Nested' in repr(f)


def test_model_as_dict():
    class MyModel(base.Model):
        root_tag = 'root'
        prop1 = base.String('tag1')
        prop2 = base.String('tag2')

    model = MyModel(prop1=42)
    model.prop2 = 'foo'

    assert model.prop1 == 42
    assert {'root': [{'tag1': 42}, {'tag2': 'foo'}]} == model.as_dict()


def test_model_default():
    class MyModel(base.Model):
        root_tag = 'root'
        prop = base.String('tag', default='x')

    model = MyModel()
    assert model.prop == 'x'


def test_field_ignore_if_none_do_not_show_field():
    class MyModel(base.Model):
        root_tag = 'root'
        prop1 = base.Field('tag1', default=None, ignore_if_none=False)
        prop2 = base.Field('tag2', default=None, ignore_if_none=True)

    model = MyModel()
    assert {'root': [{'tag1': None}]} == model.as_dict()


def test_nested_ignore_if_none_do_not_show_field():
    class ChildModel(base.Model):
        root_tag = None
        leaf1 = base.String('leaf1')
        leaf2 = base.String('leaf2')

    class ParentModel(base.Model):
        root_tag = 'root'
        prop = base.Nested('tag', ChildModel, unwrap=True, ignore_if_none=True)

    model = ParentModel(prop=None)
    expected = {'root': []}
    assert expected == model.as_dict()


def test_nested_single_unwrap():
    class ChildModel(base.Model):
        root_tag = None
        leaf1 = base.String('leaf1')
        leaf2 = base.String('leaf2')

    class ParentModel(base.Model):
        root_tag = 'root'
        prop = base.Nested('tag', ChildModel, unwrap=True)

    model = ParentModel()
    expected = {'root': [{'tag': [{'leaf1': None}, {'leaf2': None}]}]}
    assert expected == model.as_dict()


def test_nested_single_wrap():
    class ChildModel(base.Model):
        root_tag = 'child'
        leaf1 = base.String('leaf1')
        leaf2 = base.String('leaf2')

    class ParentModel(base.Model):
        root_tag = 'root'
        prop = base.Nested('tag', ChildModel, unwrap=False)

    model = ParentModel()
    expected_nested = {'child': [{'leaf1': None}, {'leaf2': None}]}
    expected = {'root': [{'tag': expected_nested}]}
    assert expected == model.as_dict()


def test_nested_many():
    class ChildModel(base.Model):
        root_tag = 'child'
        leaf1 = base.String('leaf1')
        leaf2 = base.String('leaf2')

    class ParentModel(base.Model):
        root_tag = 'root'
        prop = base.Nested('tag', ChildModel, many=True)

    model = ParentModel()
    expected_nested = [{'child': [{'leaf1': None}, {'leaf2': None}]}]
    expected = {'root': [{'tag': expected_nested}]}
    assert expected == model.as_dict()


def test_model_eq():
    class MyModel(base.Model):
        root_tag = 'root'
        prop = base.String('tag')

    m1 = MyModel(prop='42')
    m2 = MyModel(prop='42')
    m3 = MyModel(prop='2')
    assert m1 is not m2
    assert m1 == m2
    assert m1 != m3


def test_model_from_dict():
    class MyModel(base.Model):
        root_tag = 'root'
        prop = base.String('tag')

    data = {'root': [{'prop': '42'}]}
    model = MyModel.from_dict(data)

    expected_model = MyModel(prop='42')
    assert expected_model.prop == model.prop
    assert expected_model == model


def test_model_nested_from_dict():
    class ChildModel(base.Model):
        root_tag = 'child'
        leaf1 = base.String('leaf1')
        leaf2 = base.String('leaf2')

    class ParentModel(base.Model):
        root_tag = 'root'
        prop = base.Nested('tag', ChildModel, unwrap=False)

    nested = {'child': [{'leaf1': '42'}, {'leaf2': '3'}]}
    data = {'root': [{'tag': nested}]}
    model = ParentModel.from_dict(data)

    expected_model = ParentModel(tag=[ChildModel(leaf1='42', leaf2='3')])
    assert expected_model == model


def test_model_with_root_tag_none():
    class MyModel(base.Model):
        root_tag = None
        prop1 = base.String('tag1')
        prop2 = base.String('tag2')

    model = MyModel(prop1='1', prop2='two')
    assert {None: [{'tag1': '1'}, {'tag2': 'two'}]} == model.as_dict()
