import unittest
from xmlToCsv import XmlToCsvConverter
import xml.etree.ElementTree as ET
from enum import Enum


class Tag(Enum):
    string = 1
    string_array = 2
    plurals = 3


class XmlToCsvConverterTest(unittest.TestCase):

    """
    Test the functions in xmlToCsv.py
    """
    converter = XmlToCsvConverter()

    def testCheckTranslationNeededWithTranslatableFalse(self):
        """
        Given the attributes of each resource tag, test whether
        the attribute contains a 'translatable' attribute. If so, return the
        information within that attribute.
        If its not present, assume that translatable is set to true
        """
        resourceAttributes = {self.converter.TRANSLATABLE_FLAG: 'false',
                              'name': 'test'}
        self.assertEqual(self.converter._needsTranslation(resourceAttributes),
                         'false')

    def testCheckTranslationNeededWithTranslatableTrue(self):
        """
        Given the attributes of each resource tag, test whether
        the attribute contains a 'translatable' attribute. If so, return the
        information within that attribute.
        If its not present, assume that translatable is set to true
        """
        resourceAttributes = {self.converter.TRANSLATABLE_FLAG: 'true',
                              'name': 'test'}
        self.assertEqual(self.converter._needsTranslation(resourceAttributes),
                         'true')

    def testCheckTranslationNeededWithTranslatableNotProvided(self):
        """
        Given the attributes of each resource tag, test whether
        the attribute contains a 'translatable' attribute. If so, return the
        information within that attribute.
        If its not present, assume that translatable is set to true
        """
        resourceAttributes = {'name': 'test'}
        self.assertEqual(self.converter._needsTranslation(resourceAttributes),
                         'true')

    def testGetStringResourceInfo(self):
        """
        Given a string resource, test whether we grab all the required
        information.
        """
        stringResource = self._createSampleResource(Tag.string)
        stringTagInfo = self.converter._getInfoFromResourceTag(stringResource)
        self.assertTrue(len(stringTagInfo) == 1)
        self.assertEqual(stringTagInfo[0][self.converter.TAG],
                         stringResource.tag)
        self.assertEqual(stringTagInfo[0][self.converter.TEXT],
                         stringResource.text)
        self.assertEqual(stringTagInfo[0][self.converter.NAME_FLAG],
                         stringResource.attrib['name'])
        self.assertEqual(stringTagInfo[0][self.converter.TRANSLATABLE_FLAG],
                         stringResource.attrib['translatable'])

    def testGetStringArrayResourceInfo(self):
        """
        Given a string-array resource, test whether we grab all the required
        information.
        """
        stringArrResource = self._createSampleResource(Tag.string_array)
        stringArrayTagInfo = self.converter._getInfoFromResourceTag(stringArrResource)
        self.assertTrue(len(stringArrResource) == 3)
        self.assertEqual(stringArrayTagInfo[0][self.converter.TAG],
                         stringArrResource.tag)
        self.assertEqual(stringArrayTagInfo[0][self.converter.TEXT], '')
        self.assertEqual(stringArrayTagInfo[0][self.converter.NAME_FLAG],
                         stringArrResource.attrib['name'])
        # first item tag
        self.assertEqual(stringArrayTagInfo[1][self.converter.TAG],
                         'item')
        self.assertEqual(stringArrayTagInfo[1][self.converter.TEXT],
                         'firstItem')
        self.assertEqual(stringArrayTagInfo[1][self.converter.NAME_FLAG],
                         stringArrResource.attrib['name'])
        # second item tag
        self.assertEqual(stringArrayTagInfo[2][self.converter.TAG],
                         'item')
        self.assertEqual(stringArrayTagInfo[2][self.converter.TEXT],
                         'secondItem')
        self.assertEqual(stringArrayTagInfo[2][self.converter.NAME_FLAG],
                         stringArrResource.attrib['name'])

    def testGetPluralsResourceInfo(self):
        """
        Given a plurals resource, test whether we grab all the required
        information.
        """
        pluralsResource = self._createSampleResource(Tag.plurals)
        pluralsTagInfo = self.converter._getInfoFromResourceTag(pluralsResource)
        self.assertTrue(len(pluralsResource) == 2)
        self.assertEqual(pluralsTagInfo[0][self.converter.TAG],
                         pluralsResource.tag)
        self.assertEqual(pluralsTagInfo[0][self.converter.TEXT], '')
        self.assertEqual(pluralsTagInfo[0][self.converter.NAME_FLAG],
                         pluralsResource.attrib['name'])
        # first item tag
        self.assertEqual(pluralsTagInfo[1][self.converter.TAG],
                         'item')
        self.assertEqual(pluralsTagInfo[1][self.converter.TEXT],
                         '1 day')
        self.assertEqual(pluralsTagInfo[1]['quantity'],
                         'one')
        # second item tag
        self.assertEqual(pluralsTagInfo[2][self.converter.TAG],
                         'item')
        self.assertEqual(pluralsTagInfo[2][self.converter.TEXT],
                         'Other days')
        self.assertEqual(pluralsTagInfo[2]['quantity'],
                         'other')

    def _createSampleResource(self, tagType):
        if (tagType == Tag.string):
            strResource = ET.Element('string')
            strResource.text = 'Hello'
            strResource.set('name', 'hello_id')
            strResource.set('translatable', 'true')
            return strResource
        elif (tagType == Tag.string_array):
            strArrResource = ET.Element('string-array')
            strArrResource.set('name', 'array_id')
            item1 = ET.Element('item')
            item1.text = 'firstItem'
            item2 = ET.Element('item')
            item2.text = 'secondItem'
            item3 = ET.Element('item')
            item3.text = 'thirdItem'
            strArrResource.append(item1)
            strArrResource.append(item2)
            strArrResource.append(item3)
            return strArrResource
        elif (tagType == Tag.plurals):
            pluralsResource = ET.Element('plurals')
            pluralsResource.set('name', 'plurals_id')
            item1 = ET.Element('item')
            item1.set('quantity', 'one')
            item1.text = '1 day'
            item2 = ET.Element('item')
            item2.set('quantity', 'other')
            item2.text = 'Other days'
            pluralsResource.append(item1)
            pluralsResource.append(item2)
            return pluralsResource

if __name__ == '__main__':
    unittest.main()
