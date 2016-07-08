#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests for cloudshell.core.networking.networking_utils
"""

from unittest import TestCase

from cloudshell.networking import networking_utils as nu


class TestNetworkingUtils(TestCase):

    def setUp(self):
        """  """
        pass

    def tearDown(self):
        """  """
        pass

    def test_01_isInteger(self):
        """ Test suite for isInteger method """
        self.assertTrue(nu.isInteger(123))
        self.assertTrue(nu.isInteger("123"))
        self.assertTrue(nu.isInteger(u"123"))
        self.assertFalse(nu.isInteger("abc"))
        # self.assertFalse(nu.isInteger(123.4)) ???
        self.assertFalse(nu.isInteger("123.4"))

    def test_02_normalizeStr(self):
        """ Test suite for normalizeStr method """
        text = """
                Here is some multiline
                 Future     test textN/A,
               """
        self.assertEqual(nu.normalizeStr(text), "Hereissomemultilinetesttext.")

    def test_03_getNewIP(self):
        """ Test suite for getNewIP method """
        pass

    def test_04_validateIP(self):
        """ Test suite for validateIP method """
        self.assertTrue(nu.validateIP("127.0.0.1"))

        self.assertFalse(nu.validateIP("localhost"))
        self.assertFalse(nu.validateIP("127.0.0"))
        self.assertFalse(nu.validateIP("127.0.0.0.0"))
        self.assertFalse(nu.validateIP("127.0.0."))
        self.assertFalse(nu.validateIP("127.0.0.256"))
        self.assertFalse(nu.validateIP("127.0.0.-1"))

    def test_05_validateVlanNumber(self):
        """ Test suite for validateVlanNumber method """
        self.assertTrue(nu.validateVlanNumber(5))
        self.assertTrue(nu.validateVlanNumber("5"))
        self.assertTrue(nu.validateVlanNumber(1))
        self.assertTrue(nu.validateVlanNumber(4000))

        self.assertFalse(nu.validateVlanNumber(0))
        self.assertFalse(nu.validateVlanNumber(4001))

    def test_06_validateVlanRange(self):
        """ Test suite for validateVlanRange method """
        self.assertTrue(nu.validateVlanRange("1, 3000-4000"))
        self.assertFalse(nu.validateVlanRange("0"))

    def test_07_verifyIpInRange(self):
        """ Test suite for verifyIpInRange method """
        self.assertTrue(nu.validateVlanRange("1, 3000-4000"))
        self.assertFalse(nu.validateVlanRange("0"))
