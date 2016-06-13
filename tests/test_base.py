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
