#!/usr/bin/env python
# coding: utf-8
# In[45]:
import pytest

input_data = "10FA0E00"

assert_pattern = {'field1': 'Low',
                     'field2': '00',
                     'field3': '01',
                     'field4': '00',
                     'field5': '00',
                     'field6': '01',
                     'field7': '00',
                     'field8': 'Very High',
                     'field9': '00',
                     'field10': '00', }


def get_data_from_payload(payload):

    # проверка на корректность ввода
    if type(payload) != str or len(payload) != 8:
        return 'Faulty Payload'
    
    # переформатирование байтов в биты 
    binary = "" 
    for char in payload:
        binary += "{:04b}".format(int(char, 16))
    binary = [binary[0:8], binary[8:16], binary[16:24], binary[24:32]]
        
    # запись результатов     
    result = {  'field1' : binary[0][0:3],
                'field2' : '0'+binary[0][2],
                'field3' : '0'+binary[0][3],
                'field4' : binary[0][5:8],
                'field5' : '0'+binary[1][7],
                'field6' : '0'+binary[1][1],
                'field7' : '0'+binary[1][7],
                'field8' : binary[2][4:7],
                'field9' : '0'+binary[2][0],
                'field10' : '0'+binary[2][1] }

    # парсинг особых полей
    match int(result['field1'], 2):
        case 0:
            result['field1'] = 'Low'
        case 1 | 2 | 3 | 5 | 6:
            result['field1'] = 'reserved'
        case 4:
            result['field1'] = 'Medium'
        case 7:
            result['field1'] = 'High'
        case _:
            result['field1'] = 'Something went wrong during parsing'
    match int(result['field4'], 2):
        case 0:
            result['field4'] = '00'
        case 1:
            result['field4'] = '10'
        case 2:
            result['field4'] = '20'
        case 3:
            result['field4'] = '30'
        case 4:
            result['field4'] = '40'
        case 5:
            result['field4'] = '50'
        case 6:
            result['field4'] = '60'
        case 7:
            result['field4'] = '70'
        case _:
            result['field4'] = 'Something went wrong during parsing'
    match int(result['field8'], 2):
        case 0:
            result['field8'] = 'Very Low'
        case 1|3|6:
            result['field8'] = 'reserved'
        case 2:
            result['field8'] = 'Low'
        case 4:
            result['field8'] = 'Medium'
        case 5:
            result['field8'] = 'High'
        case 7:
            result['field8'] = 'Very High'
        case _:
            result['field8'] = 'Something went wrong during parsing'
            
    return result


class TestClass:

    def test_1(self):
        test_1_result = get_data_from_payload(input_data)
        assert test_1_result == assert_pattern, f"the result does not match the validation pattern, got: {test_1_result}"

    def test_2(self):
        test_2_result = get_data_from_payload(input_data)
        assert test_2_result != 'Faulty Payload', f"the result does not require type or length"
        
    def test_3(self):
        test_3_result = get_data_from_payload(input_data)
        assert len(test_3_result) == 10, f"the length of response does not equal to 10, got: {len(test_3_result)}"



