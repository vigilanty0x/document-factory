import unittest
from document_factory import render,probe
class Tests(unittest.TestCase):
 def test_render(self): self.assertEqual(render("Hi {{name}}",{"name":"Ada"})["markdown"],"Hi Ada")
 def test_missing(self): self.assertFalse(render("{{x}}",{})["ok"])
 def test_extra(self): self.assertFalse(render("plain",{"x":1})["ok"])
 def test_probe(self): self.assertTrue(probe()["ok"])
if __name__=="__main__":unittest.main()
