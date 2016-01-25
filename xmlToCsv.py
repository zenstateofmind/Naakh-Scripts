import xml.etree.ElementTree as ET
import csv

"""
Takes in a strings.xml file from android res directory
and converts it into a CSV file that contains all the words/phrases
that need to be translated
Something that we need to be sure about:
https://docs.python.org/3.4/library/xml.html#xml-vulnerabilities
"""


class XmlToCsvConverter():

    STRING_TAG = 'string'
    STRING_ARRAY_TAG = 'string-array'
    ITEM_TAG = 'item'
    PLURALS_TAG = 'plurals'

    TRANSLATABLE_FLAG = 'translatable'
    NAME_FLAG = 'name'
    QUANTITY_FLAG = 'quantity'

    TAG = 'Tag'
    ATTRIBUTES = 'Attributes'
    TEXT = 'Text'

    def convertToCsv(self, xmlFileName):
        """
        Checks whether the xml file name passed in as the parameter is a
        'xml'. If not, it throws an error. If valid, scrapes through the
        xml file and spits out a csv file. The CSV file gets created in the
        same directory as the python file
        """
        if (xmlFileName.endswith(".xml")):
            # scrape the data
            # create csv file -> ID, String, Comment, Translated String
            resourcesInfo = self._scrapeXmlFile(xmlFileName)
            self._createCsv(resourcesInfo)
        else:
            raise NameError('The filename should end with .xml')

    def _scrapeXmlFile(self, xmlFileName):
        """
        Takes in an xml file and returns a list of dictionary objects
        containing information of the xml file
        """
        tree = ET.parse(xmlFileName)
        root = tree.getroot()
        # Child here can be of type 'string' or 'string-array' or maybe more
        resourcesInfo = []
        for resource in root:
            listOfDicts = self._getInfoFromResourceTag(resource)
            for resourceDict in listOfDicts:
                resourcesInfo.append(resourceDict)
        return resourcesInfo

    def _getInfoFromResourceTag(self, child):
        """
        Scrapes through each individual [string, string-array, plurals] tag
        and returns data in the following format:
        string tag:
        [
            {
                'Tag': 'string'
                'Name': _tag_id_
                'Translatable': true/false
                'Quantity': '' (only applies to plurals->item tag)
                'Text': phrase/word that needs to be translated
            }
        ]
        string-array tag:
        [
            {
                'Tag': 'string-array'
                'Name': _tag_id_
                'Translatable': true/false
                'Quantity': '' (only applies to plurals->item tag)
                'Text': '' (the phrases are in item tags that follow)
            },
            {
                'Tag': 'item'
                'Name': _same_tag_id_as_string_array
                'Translatable': _same_as_string_array
                'Quantity': '' (only applies to plurals->item tag)
                'Text': phrase/word that needs to be translated
            }, ...
        ]
        plurals tag:
        [
            {
                'Tag': 'plurals'
                'Name': _tag_id_
                'Translatable': true/false
                'Quantity': '' (only applies to plurals->item tag)
                'Text': '' (the phrases are in item tags that follow)
            },
            {
                'Tag': 'item'
                'Name': _same_tag_id_as_plurals_tag
                'Translatable': same_as_plurals_tag
                'Quantity': _quantity_id_
                'Text': phrase/word that needs to be translated
            }, ...
        ]
        """
        listOfDicts = []

        dict = {}
        dict[self.TAG] = child.tag
        dict[self.NAME_FLAG] = child.attrib[self.NAME_FLAG]
        dict[self.TRANSLATABLE_FLAG] = self._needsTranslation(child.attrib)
        if child.tag == self.STRING_TAG:
            # gather data
            dict[self.TEXT] = child.text
            dict[self.QUANTITY_FLAG] = ''
            listOfDicts.append(dict)
        elif child.tag == self.STRING_ARRAY_TAG:
            dict[self.TEXT] = ''
            dict[self.QUANTITY_FLAG] = ''
            listOfDicts.append(dict)
            for item in self._getItems(child):
                listOfDicts.append(item)
        elif child.tag == self.PLURALS_TAG:
            dict[self.TEXT] = ''
            dict[self.QUANTITY_FLAG] = ''
            listOfDicts.append(dict)
            for item in self._getItems(child):
                listOfDicts.append(item)
        return listOfDicts

    def _needsTranslation(self, resourceAttributes):
        """
        Takes an attribute resource tag (dict object) and returns:
            true if the phrase in this tag needs translation
            false if the phrase in this tag doesnt need translation
        """
        if self.TRANSLATABLE_FLAG in resourceAttributes:
            return resourceAttributes[self.TRANSLATABLE_FLAG]
        else:
            return 'true'

    def _getItems(self, resource):
        """
        Get all the children of string-array/plurals tags
        """

        if (resource.tag == self.STRING_TAG):
            raise TypeError('You cannot pass in a string array')

        items = []

        for item in resource.findall(self.ITEM_TAG):
            dict = {}
            dict[self.TAG] = self.ITEM_TAG
            dict[self.NAME_FLAG] = resource.attrib[self.NAME_FLAG]
            dict[self.TRANSLATABLE_FLAG] = self._needsTranslation(resource.attrib)
            dict[self.TEXT] = item.text
            if (resource.tag == self.STRING_ARRAY_TAG):
                dict[self.QUANTITY_FLAG] = ''
            else:
                dict[self.QUANTITY_FLAG] = item.attrib[self.QUANTITY_FLAG]
            items.append(dict)
        return items

    def _createCsv(self, resourcesInfo):
        """
        resourcesInfo: a list of dictionary objects each of which contains
        information from a resource tag (string, string-array, plurals)

        This method creates a csv file with all the information given the
        resourcesInfo data structure,
        """
        csvFile = open("test.csv", 'w')
        csvWriter = csv.writer(csvFile, dialect='excel')
        csvWriter.writerow(["Tag", "Id", "Translatable", "Text", "Quantity"])
        for dictResource in resourcesInfo:
            csvWriter.writerow(self._convertDictionaryToList(dictResource))

    def _convertDictionaryToList(self, dictResource):
        """
        Given a dictionary (each dictionary contains information
        within one string/string-array/plurals/item tag), converts it
        into a list containing information in the following order:
            Tag, Name_id, Translatable, Text, Quantity
        """
        row = []

        if (not dictResource):
            return row

        row.append(dictResource[self.TAG])
        row.append(dictResource[self.NAME_FLAG])
        row.append(dictResource[self.TRANSLATABLE_FLAG])
        row.append(dictResource[self.TEXT])
        row.append(dictResource[self.QUANTITY_FLAG])
        return row

if __name__ == '__main__':
    converter = XmlToCsvConverter()
    # Add the xml file right here
    converter.convertToCsv('/Users/nikhiljoshi/Documents/Naakh/strings_sample.xml')
