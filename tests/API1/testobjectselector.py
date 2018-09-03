"""
Unit test for object selector parameters.

Originally implemented as doctests in Topographica in the file
testEnumerationParameter.txt
"""

import param
from . import API1TestCase
from collections import OrderedDict

class TestObjectSelectorParameters(API1TestCase):

    def setUp(self):
        super(TestObjectSelectorParameters, self).setUp()
        class P(param.Parameterized):
            e = param.ObjectSelector(default=5,objects=[5,6,7])
            f = param.ObjectSelector(default=10)
            h = param.ObjectSelector(default=None)
            g = param.ObjectSelector(default=None,objects=[7,8])
            i = param.ObjectSelector(default=7,objects=[9],check_on_set=False)
            s = param.ObjectSelector(default=3,objects=OrderedDict(one=1,two=2,three=3))

        self.P = P

    def test_set_object_constructor(self):
        p = self.P(e=6)
        self.assertEqual(p.e, 6)

    def test_get_range_list(self):
        r = self.P.param.params("g").get_range()
        self.assertEqual(r['7'],7)
        self.assertEqual(r['8'],8)

    def test_get_range_dict(self):
        r = self.P.param.params("s").get_range()
        self.assertEqual(r['one'],1)
        self.assertEqual(r['two'],2)

    def test_set_object_outside_bounds(self):
        p = self.P(e=6)
        try:
            p.e = 9
        except ValueError:
            pass
        else:
            raise AssertionError("Object set outside range.")

    def test_set_object_setattr(self):
        p = self.P(e=6)
        p.f = 9
        self.assertEqual(p.f, 9)
        p.g = 7
        self.assertEqual(p.g, 7)
        p.i = 12
        self.assertEqual(p.i, 12)


    def test_set_object_not_None(self):
        p = self.P(e=6)
        p.g = 7
        try:
            p.g = None
        except ValueError:
            pass
        else:
            raise AssertionError("Object set outside range.")

    def test_set_object_setattr_post_error(self):
        p = self.P(e=6)
        p.f = 9
        self.assertEqual(p.f, 9)
        p.g = 7
        try:
            p.g = None
        except ValueError:
            pass
        else:
            raise AssertionError("Object set outside range.")

        self.assertEqual(p.g, 7)
        p.i = 12
        self.assertEqual(p.i, 12)

    def test_initialization_out_of_bounds(self):
        try:
            class Q(param.Parameterized):
                q = param.ObjectSelector(5,objects=[4])
        except ValueError:
            pass
        else:
            raise AssertionError("ObjectSelector created outside range.")


    def test_initialization_no_bounds(self):
        try:
            class Q(param.Parameterized):
                q = param.ObjectSelector(5,objects=10)
        except TypeError:
            pass
        else:
            raise AssertionError("ObjectSelector created without range.")


if __name__ == "__main__":
    import nose
    nose.runmodule()
