#!/usr/bin/env python
# encoding: utf-8

import os
import StringIO
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pfp

class TestBasic(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def _test_parse_build(self, data, template):
		dom = pfp.parse(StringIO.StringIO(data), template)
		self.assertEqual(dom._pfp__build(), data)
		return dom
	
	def test_single_decl_parse(self):
		dom = self._test_parse_build(
			"\x41",
			"""
				char a;
			"""
		)

	def test_basic_parse(self):
		dom = self._test_parse_build(
			"\x00\x01\x02\x03",
			"""
				struct DATA {
					char a;
					char b;
					char c;
					char d;
				} data;
			"""
		)
	
	def test_nested_basic_parse(self):
		dom = self._test_parse_build(
			"\x00\x01\x02\x03",
			"""
				struct DATA {
					char a;
					char b;

					struct {
						char a;
						char b;
					} nested;
				} data;
			"""
		)
	
	def test_typedef_basic_parse(self):
		dom = self._test_parse_build(
			"\xff\x00\x00\xff",
			"""
				typedef unsigned short BLAH;
				BLAH a;
				short b;
			"""
		)
		import pdb ; pdb.set_trace()
		self.assertTrue(dom.a, 0xff00)
		self.assertEqual(dom.b, 0xff)

if __name__ == "__main__":
	unittest.main()
