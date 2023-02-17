import datetime

from django.test import TestCase

from .serializers import RefbookSerializer, ElementSerializer
from .models import Refbook, Version, Element, ElementVersion


class RefbookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Refbook.objects.create(code='1',
                               name='Специальности медработников',
                               description='Специальности по классификатору')

    def test_code_value(self):
        refbook = Refbook.objects.get(id=1)
        code_value = refbook.code
        self.assertEquals(code_value, '1')

    def test_name_value(self):
        refbook = Refbook.objects.get(id=1)
        name_value = refbook.name
        self.assertEquals(name_value, 'Специальности медработников')

    def test_code_max_length(self):
        refbook = Refbook.objects.get(id=1)
        max_length = refbook._meta.get_field('code').max_length
        self.assertEquals(max_length, 100)

    def test_name_max_length(self):
        refbook = Refbook.objects.get(id=1)
        max_length = refbook._meta.get_field('name').max_length
        self.assertEquals(max_length, 300)

    def test_object_str_name_is_field_name(self):
        refbook = Refbook.objects.get(id=1)
        expected_object_name = '%s' % (refbook.name)
        self.assertEquals(expected_object_name, str(refbook))


class VersionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        refbook1 = Refbook.objects.create(code='1',
                               name='Специальности медработников',
                               description='Специальности по классификатору')
        refbook2 = Refbook.objects.create(code='2',
                               name='Болезни',
                               description='Список болезней по классификатору')
        Version.objects.create(refbook_id=refbook1,
                               version='0.1',
                               date='2022-06-15')
        Version.objects.create(refbook_id=refbook1,
                               version='0.2',
                               date='2023-01-30')
        Version.objects.create(refbook_id=refbook2,
                               version='1.0',
                               date='2022-09-10')

    def test_version_value(self):
        version1 = Version.objects.get(id=1)
        version2 = Version.objects.get(id=3)
        version1_value = version1.version
        version2_value = version2.version
        self.assertEquals(version1_value,'0.1')
        self.assertEquals(version2_value,'1.0')

    def test_date_value(self):
        version1 = Version.objects.get(id=1)
        version2 = Version.objects.get(id=3)
        date1_value = version1.date
        date2_value = version2.date
        self.assertEquals(date1_value.strftime('%Y-%m-%d'), '2022-06-15')
        self.assertEquals(date2_value.strftime('%Y-%m-%d'), '2022-09-10')

    def test_refbook_id_value(self):
        version1 = Version.objects.get(id=1)
        version2 = Version.objects.get(id=3)
        refbook1_id_value = version1.refbook_id.id
        refbook2_id_value = version2.refbook_id.id
        self.assertEquals(refbook1_id_value, 1)
        self.assertEquals(refbook2_id_value, 2)

    def test_version_max_length(self):
        version = Version.objects.get(id=1)
        max_length = version._meta.get_field('version').max_length
        self.assertEquals(max_length, 50)

    def test_object_str_name_is_version(self):
        version = Version.objects.get(id=1)
        expected_object_name = '%s' % (version.version)
        self.assertEquals(expected_object_name, str(version))


class ElementModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        refbook = Refbook.objects.create(code='1',
                                         name='Специальности медработников',
                                         description='Специальности по классификатору')
        version1 = Version.objects.create(refbook_id=refbook,
                                          version='0.1',
                                          date='2022-06-15')
        version2 = Version.objects.create(refbook_id=refbook,
                                          version='0.2',
                                          date='2023-01-30')
        element1 = Element.objects.create(code='A23',
                                          value='Травматолог')
        element2 = Element.objects.create(code='A99',
                                          value='Хирург')
        ElementVersion.objects.create(version=version1,
                                      element=element1)
        ElementVersion.objects.create(version=version1,
                                      element=element2)
        ElementVersion.objects.create(version=version2,
                                      element=element1)
        ElementVersion.objects.create(version=version2,
                                      element=element2)


    def test_code_value(self):
        element1 = Element.objects.get(id=1)
        element2 = Element.objects.get(id=2)
        element1_value = element1.code
        element2_value = element2.code
        self.assertEquals(element1_value,'A23')
        self.assertEquals(element2_value,'A99')

    def test_value_value(self):
        element1 = Element.objects.get(id=1)
        element2 = Element.objects.get(id=2)
        element1_value = element1.value
        element2_value = element2.value
        self.assertEquals(element1_value,'Травматолог')
        self.assertEquals(element2_value,'Хирург')

    def test_code_max_length(self):
        element = Element.objects.get(id=1)
        max_length = element._meta.get_field('code').max_length
        self.assertEquals(max_length, 100)

    def test_value_max_length(self):
        element = Element.objects.get(id=1)
        max_length = element._meta.get_field('value').max_length
        self.assertEquals(max_length, 300)

    def test_object_str_name_is_value(self):
        element = Element.objects.get(id=1)
        expected_object_name = '%s' % (element.value)
        self.assertEquals(expected_object_name, str(element))

    def test_equal_element_id_version_id(self):
        element_version1 = ElementVersion.objects.get(id=1)
        element1_id = element_version1.element.id
        version1_id = element_version1.version.id

        element_version2 = ElementVersion.objects.get(id=2)
        element2_id = element_version2.element.id
        version2_id = element_version2.version.id

        element_version3 = ElementVersion.objects.get(id=3)
        element3_id = element_version3.element.id
        version3_id = element_version3.version.id

        element_version4 = ElementVersion.objects.get(id=4)
        element4_id = element_version4.element.id
        version4_id = element_version4.version.id

        self.assertEquals(element1_id, 1)
        self.assertEquals(version1_id, 1)

        self.assertEquals(element2_id, 2)
        self.assertEquals(version2_id, 1)

        self.assertEquals(element3_id, 1)
        self.assertEquals(version3_id, 2)

        self.assertEquals(element4_id, 2)
        self.assertEquals(version4_id, 2)


class RefbookAPICase(TestCase):
    @classmethod
    def setUpTestData(cls):
        refbook1 = Refbook.objects.create(code='1',
                                          name='Специальности медработников',
                                          description='Специальности по классификатору')
        refbook2 = Refbook.objects.create(code='2',
                                          name='Болезни',
                                          description='Список болезней по классификатору')
        Version.objects.create(refbook_id=refbook1,
                               version='0.1',
                               date='2022-06-15')
        Version.objects.create(refbook_id=refbook1,
                               version='0.2',
                               date='2022-11-15')
        Version.objects.create(refbook_id=refbook2,
                               version='1.0',
                               date='2023-01-10')
        Version.objects.create(refbook_id=refbook2,
                               version='2.0',
                               date='2023-01-30')

    def test_get_refbooks_without_date(self):
        refbook1 = Refbook.objects.get(id=1)
        refbook2 = Refbook.objects.get(id=2)
        url = 'http://127.0.0.1:8000/api/refbooks/'
        response = self.client.get(url)
        serializer_data = {'refbooks': RefbookSerializer([refbook1, refbook2], many=True).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_refbooks_with_date(self):
        date1 = '2022-12-01'
        queryset1 = Refbook.objects.filter(versions__date__lte=date1).distinct()
        url1 = 'http://127.0.0.1:8000/api/refbooks/?date={}'.format(date1)
        response1 = self.client.get(url1)
        serializer_data1 = {'refbooks': RefbookSerializer(queryset1, many=True).data}
        self.assertEqual(serializer_data1, response1.data)

        date2 = '2023-02-15'
        queryset2 = Refbook.objects.filter(versions__date__lte=date2).distinct()
        url2 = 'http://127.0.0.1:8000/api/refbooks/?date={}'.format(date2)
        response2 = self.client.get(url2)
        serializer_data2 = {'refbooks': RefbookSerializer(queryset2, many=True).data}
        self.assertEqual(serializer_data2, response2.data)


class ElementsAPICase(TestCase):
    @classmethod
    def setUpTestData(cls):
        refbook = Refbook.objects.create(code='1',
                                         name='Специальности медработников',
                                         description='Специальности по классификатору')
        version1 = Version.objects.create(refbook_id=refbook,
                                          version='0.1',
                                          date='2022-06-15')
        version2 = Version.objects.create(refbook_id=refbook,
                                          version='0.2',
                                          date='2022-11-11')
        version3 = Version.objects.create(refbook_id=refbook,
                                          version='0.3',
                                          date='2023-01-30')
        element1 = Element.objects.create(code='A23',
                                          value='Травматолог')
        element2 = Element.objects.create(code='A99',
                                          value='Хирург')
        ElementVersion.objects.create(version=version1,
                                      element=element1)
        ElementVersion.objects.create(version=version1,
                                      element=element2)
        ElementVersion.objects.create(version=version2,
                                      element=element1)
        ElementVersion.objects.create(version=version2,
                                      element=element2)
        ElementVersion.objects.create(version=version3,
                                      element=element2)

    def test_get_elements_with_version(self):
        refbook_id = 1
        version = '0.1'
        version_id = 1
        url = 'http://127.0.0.1:8000/api/refbooks/{}/elements/?version={}'.format(refbook_id, version)
        response = self.client.get(url)
        queryset = Element.objects.filter(version_id=version_id)
        serializer_data = {'elements': ElementSerializer(queryset, many=True).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_elements_without_version(self):
        refbook_id = 1
        url = 'http://127.0.0.1:8000/api/refbooks/{}/elements/'.format(refbook_id)
        response = self.client.get(url)
        date_today = datetime.datetime.now()
        version = Version.objects.filter(refbook_id=refbook_id,
                                         date__lte=date_today).order_by('date').last()
        queryset = Element.objects.filter(version_id=version.id)
        serializer_data = {'elements': ElementSerializer(queryset, many=True).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_valid_element_with_version(self):
        code = 'A99'.replace('"', '')
        value = 'Хирург'.replace('"', '')
        refbook_id = 1
        version = '0.3'
        version_id = 3

        url = 'http://127.0.0.1:8000/api/refbooks/{}/check_element/?code={}&value={}&version={}'.\
            format(refbook_id, code, value, version)
        response = self.client.get(url)

        queryset = Element.objects.filter(code=code,
                                          value=value,
                                          version_id=version_id)

        serializer_data = {'element': ElementSerializer(queryset, many=True).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_valid_element_without_version(self):
        code = 'A99'.replace('"', '')
        value = 'Хирург'.replace('"', '')
        refbook_id = 1

        url = 'http://127.0.0.1:8000/api/refbooks/{}/check_element/?code={}&value={}'. \
            format(refbook_id, code, value)
        response = self.client.get(url)

        date_today = datetime.datetime.now()
        version = Version.objects.filter(refbook_id=refbook_id,
                                         date__lte=date_today).order_by('date').last()

        queryset = Element.objects.filter(code=code,
                                          value=value,
                                          version_id=version.id)

        serializer_data = {'element': ElementSerializer(queryset, many=True).data}
        self.assertEqual(serializer_data, response.data)

    def test_get_valid_element_result_is_null(self):
        code = 'A23'.replace('"', '')
        value = 'Травматолог'.replace('"', '')
        refbook_id = 1

        url = 'http://127.0.0.1:8000/api/refbooks/{}/check_element/?code={}&value={}'. \
            format(refbook_id, code, value)

        date_today = datetime.datetime.now()
        version = Version.objects.filter(refbook_id=refbook_id,
                                         date__lte=date_today).order_by('date').last()

        queryset = Element.objects.filter(code=code,
                                          value=value,
                                          version_id=version.id)

        serializer_data = {'element': ElementSerializer(queryset, many=True).data}
        self.assertEqual(serializer_data, {'element': []})
