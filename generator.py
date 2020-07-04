import json
import random
import string
import exrex
from datetime import datetime, time
from datetime import timedelta
import numpy as np


def generate_float(sch, field):
    if sch["properties"][field]["type"] == "array":
        try:
            return random.randrange(sch["properties"][field]["items"]["minimum"],
                                    sch["properties"][field]["items"]["maximum"]) + round(random.random(), 3)
        except KeyError:
            return random.randrange(1, 20) + round(random.random(), 3)
    else:
        try:
            return random.randrange(sch["properties"][field]["minimum"],
                                    sch["properties"][field]["maximum"]) + round(random.random(), 3)
        except KeyError:
            return random.randrange(1, 20) + round(random.random(), 3)


def generate_string(sch, field):
    if sch["properties"][field]["type"] == "array":
        try:
            pat = sch["properties"][field]["items"]["pattern"]
            return exrex.getone(pat)
        except KeyError:
            letters = string.ascii_lowercase
            try:
                length = random.randint(sch["properties"][field]["items"]["minlength"],
                                        sch["properties"][field]["items"]["maxlength"])
            except KeyError:
                length = random.randint(3, 10)
            return ''.join(random.choice(letters) for i in range(length))
    else:
        try:
            pat = sch["properties"][field]["pattern"]
            return exrex.getone(pat)
        except KeyError:
            letters = string.ascii_lowercase
            try:
                length = random.randint(sch["properties"][field]["minlength"],
                                        sch["properties"][field]["maxlength"])
            except KeyError:
                length = random.randint(3, 10)
            return ''.join(random.choice(letters) for i in range(length))


def generate_int(sch, field):
    if sch["properties"][field]["type"] == "array":
        try:
            return random.randint(sch["properties"][field]['items']["minimum"],
                                  sch["properties"][field]['items']["maximum"])
        except KeyError:
            return random.randint(0, 15)
    else:
        try:
            return random.randint(sch["properties"][field]["minimum"], sch["properties"][field]["maximum"])
        except KeyError:
            return random.randint(0, 15)


def generate_phone_number(sch, err):
    if err == 0:
        return "+79" + str(random.randint(111111111, 999999999))
    else:
        return "8(9" + str(random.randint(11, 99)) + ')' + str(random.randint(1111111, 9999999))


def generate_array(sch, field, length):
    try:
        type_of_item = sch["properties"][field]["items"]["type"]
        if type_of_item == "number":
            return [generate_float(sch, field) for i in range(length)]
        if type_of_item == "integer":
            return [generate_int(sch, field) for i in range(length)]
        if type_of_item == "string":
            try:
                Format = sch["properties"][field]["items"]["format"]
                return [generate_datetime(Format, 0) for i in range(length)]
            except KeyError:
                return [generate_string(sch, field) for i in range(length)]
        if type_of_item == "array":
            try:
                type_of_item = sch["properties"][field]["items"]["items"]["type"]
                if type_of_item == "number":
                    return [[generate_float(sch, field) for i in range(length)]
                            for j in range(random.randint(np.abs(length - 3), length + 3))]
                if type_of_item == "integer":
                    return [[generate_int(sch, field) for i in range(length)]
                            for j in range(random.randint(np.abs(length - 3), length + 3))]
                if type_of_item == "string":
                    try:
                        Format = sch["properties"][field]["items"]["items"]["format"]
                        return [[generate_datetime(Format, 0) for i in range(length)]
                                for j in range(random.randint(np.abs(length - 3), length + 3))]
                    except KeyError:
                        return [[generate_string(sch, field) for i in range(length)]
                                for j in range(random.randint(np.abs(length - 3), length + 3))]
            except KeyError:
                return [[generate_int(sch, field) for i in range(length)]
                        for j in range(random.randint(np.abs(length - 3), length + 3))]
    except KeyError:
        return [generate_int(sch, field) for i in range(length)]


 # -------------------------------------------------------------------------------------------------------------------
 # for date and time
def add_re_for_formats(schema, field):
    if schema["properties"][field]["format"] == "date" or schema["properties"][field]["format"] == "date-time":
        schema["properties"][field]["pattern"] = "^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"

    if schema["properties"][field]["format"] == "time":
        schema["properties"][field]["pattern"] = "([0-9]{2}:){2}[0-9]{2}"


def get_random_date():
    while 1:
        try:
            date1 = exrex.getone('(0[1-9]|1[0-9]|2[0-9]|3[0-1])-(0[1-9]|1[0-2])-20(1[0-9]|0[1-9])')
            d = datetime.strptime(date1, '%d-%m-%Y').isoformat()
            return d[:-9]
        except ValueError:
            continue


def get_random_time():
    time1 = exrex.getone('(0[1-9]|1[0-9]|2[0-3]):(0[1-9]|[1-5][0-9]):(0[1-9]|[1-5][0-9])')
    return time.fromisoformat(time1)


def get_random_datetime():
    while 1:
        try:
            date1 = exrex.getone('(0[1-9]|1[0-9]|2[0-3]):(0[1-9]|[1-5][0-9]):(0[1-9]|[1-5][0-9]) (0[1-9]|1[0-9]|2[0-9]|3[0-1])-(0[1-9]|1[0-2])-20(1[0-9]|0[1-9])')
            d = datetime.strptime(date1, '%H:%M:%S %d-%m-%Y')
            return d.isoformat()
        except ValueError:
            continue


def get_random_close_date(start, delta):
    end = start + timedelta(days=delta)
    before_start = start - timedelta(days=delta)
    deltta = end - before_start
    int_delta = (deltta.days * 24 * 60 * 60) + deltta.seconds
    random_second = random.randrange(int_delta)
    return before_start + timedelta(seconds=random_second)


def generate_datetime(f, delta, start=''):
    if f == "date":
        if delta == 0:
            return get_random_date()
        else:
            if start != '':
                start = datetime.fromisoformat(start)
                return get_random_close_date(start, delta).isoformat()[:-9]
            else:
                return get_random_date()

    if f == "time":
        return get_random_time().isoformat()

    if f == "date-time":
        if delta == 0:
            return get_random_datetime()
        else:
            if start != '':
                start = datetime.fromisoformat(start)
                return get_random_close_date(start, delta).isoformat()
            else:
                return get_random_datetime()

#--------------------------------------------------------------------------------------------------------------


def error1(n, schema):
    try:
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    p = round((random.random()*0.2+0.4)*n)
    is_sample_strange = []
    for i in range(p):
        is_sample_strange.append(0)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)
    for i in range(p,n):
        is_sample_strange.append(1)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        str_keys = []
        for key in schema["properties"].keys():
            if schema["properties"][key]["type"] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    str_keys.append(key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        if len(str_keys) > 0:
            for j in range(1, len(str_keys)):
                try:
                    Format = schema["properties"][str_keys[j]]['format']
                    key = str_keys[j]
                    schema1 = schema
                    add_re_for_formats(schema1, key)
                    try:
                        data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                    except IndexError:
                        data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                except KeyError:
                    data[str_keys[j]] = generate_string(schema, str_keys[j])
            data[str_keys[0]] = ''
        else:
            return 0,  is_sample_strange
        data_arr.append(data)
    with open('data/anomaly1_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return str_keys[0], is_sample_strange


# Текст с вероятнстью P = 58,9% есть, а потом его нет
def error2(n, schema):
    try:
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    p = round((random.random() * 0.2 + 0.4) * n)
    is_sample_strange = []
    error_key = 0
    for i in range(p):
        is_sample_strange.append(0)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        str_keys = []
        for key in schema["properties"].keys():
            if schema["properties"][key]["type"] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    str_keys.append(key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        if len(str_keys) > 0:
            if len(str_keys) > 1:
                for j in range(2, len(str_keys)):
                    try:
                        Format = schema["properties"][str_keys[j]]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, str_keys[j])
                        try:
                            data[str_keys[j]] = generate_datetime(Format, 1, data_arr[-1][str_keys[j]])
                        except IndexError:
                            data[str_keys[j]] = generate_datetime(Format, 1, samples_collection[-1][str_keys[j]])
                    except KeyError:
                        data[str_keys[j]] = generate_string(schema, str_keys[j])

                try:
                    Format = schema["properties"][str_keys[0]]['format']
                    schema1 = schema
                    add_re_for_formats(schema1, str_keys[0])
                    try:
                        data[str_keys[0]] = generate_datetime(Format, 1, data_arr[-1][str_keys[0]])
                    except IndexError:
                        data[str_keys[0]] = generate_datetime(Format, 1, samples_collection[-1][str_keys[0]])
                except KeyError:
                    data[str_keys[0]] = generate_string(schema, str_keys[0])

                if random.random() <= 0.58:
                    try:
                        Format = schema["properties"][str_keys[1]]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, str_keys[1])
                        try:
                            data[str_keys[1]] = generate_datetime(Format, 1, data_arr[-1][str_keys[1]])
                        except IndexError:
                            data[str_keys[1]] = generate_datetime(Format, 1, samples_collection[-1][str_keys[1]])
                    except KeyError:
                        data[str_keys[1]] = generate_string(schema, str_keys[1])
                else:
                    data[str_keys[1]] = ''
                error_key = str_keys[1]
            else:
                if random.random() <= 0.58:
                    try:
                        Format = schema["properties"][str_keys[0]]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, str_keys[0])
                        try:
                            data[str_keys[0]] = generate_datetime(Format, 1, data_arr[-1][str_keys[0]])
                        except IndexError:
                            data[str_keys[0]] = generate_datetime(Format, 1, samples_collection[-1][str_keys[0]])
                    except KeyError:
                        data[str_keys[0]] = generate_string(schema, str_keys[0])
                else:
                    data[str_keys[0]] = ''
                error_key = str_keys[0]
        else:
            return 0, is_sample_strange
        data_arr.append(data)
    for i in range(p,n):
        data = {}
        is_sample_strange.append(1)
        data["idOfCrawler"] = schema["idOfCrawler"]
        str_keys = []
        for key in schema["properties"].keys():
            if schema["properties"][key]["type"] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    str_keys.append(key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        if len(str_keys) > 0:
            if len(str_keys) > 1:
                for j in range(2, len(str_keys)):
                    try:
                        Format = schema["properties"][str_keys[j]]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, str_keys[j])
                        try:
                            data[str_keys[j]] = generate_datetime(Format, 1, data_arr[-1][str_keys[j]])
                        except IndexError:
                            data[str_keys[j]] = generate_datetime(Format, 1, samples_collection[-1][str_keys[j]])
                    except KeyError:
                        data[str_keys[j]] = generate_string(schema, str_keys[j])

                try:
                    Format = schema["properties"][str_keys[0]]['format']
                    schema1 = schema
                    add_re_for_formats(schema1, str_keys[0])
                    try:
                        data[str_keys[0]] = generate_datetime(Format, 1, data_arr[-1][str_keys[0]])
                    except IndexError:
                        data[str_keys[0]] = generate_datetime(Format, 1, samples_collection[-1][str_keys[0]])
                except KeyError:
                    data[str_keys[0]] = generate_string(schema, str_keys[0])
                data[str_keys[1]] = ''
                error_key = str_keys[1]
            else:
                data[str_keys[0]] = ''
                error_key = str_keys[0]
        else:
            return 0,  is_sample_strange
        data_arr.append(data)

    if error_key != 0:
        k = p - 1
        while data_arr[k][error_key] == '':
            is_sample_strange[k] = 1
            k = k - 1
        with open('data/anomaly2_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(data_arr, json_file)
    return error_key, is_sample_strange


# Число n раз [8,9], а c n + 1 раза [50,70]
def error3(n, schema):
    try:
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    p = round((random.random() * 0.2 + 0.4) * n)
    is_sample_strange = []
    count = sum([schema["properties"][key]['type'] == "number" for key in schema["properties"].keys()])
    if count == 0:
        return 0,  is_sample_strange
    for i in range(p):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)
    for i in range(p,n):
        data = {}
        is_sample_strange.append(1)
        data["idOfCrawler"] = schema["idOfCrawler"]
        j = 0
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format= schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                if j == 0:
                    data[key] = generate_float(schema, key) * 10
                    j += 1
                    err_field = key
                else:
                    data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)
    with open('data/anomaly3_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return err_field, is_sample_strange


# Токены поменялись с +7915... на 8(9...
def error4(n, schema):
    try:
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    p = round((random.random() * 0.2 + 0.4) * n)
    is_sample_strange = []
    count = sum([key == "phone number" for key in schema["properties"].keys()])
    if count == 0:
        return 0,  is_sample_strange
    for i in range(p):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)
    for i in range(p,n):
        is_sample_strange.append(1)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 1)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)

    with open('data/anomaly4_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return 'phone number', is_sample_strange


# Изменение числа item-ов для страницы
def error5(n, schema):
    try:
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    p = round((random.random() * 0.2 + 0.4) * n)
    is_sample_strange = []
    for i in range(p):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)
    for i in range(p,n):
        is_sample_strange.append(1)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        keys_count = len(schema["properties"].keys())
        k = 1
        for key in schema["properties"].keys():
            if k > round(keys_count * 0.5):
                break
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
            k += 1
        data_arr.append(data)

    with open('data/anomaly5_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return is_sample_strange


def error6(n, schema):
    try:
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    p = round((random.random() * 0.2 + 0.4) * n)
    is_sample_strange = []
    error_key = 0
    for i in range(p):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)
    for i in range(p,n):
        data = {}
        is_sample_strange.append(1)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        if Format == "time":
                            is_sample_strange[-1] = 0
                        error_key = key
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        d = generate_datetime(Format, 0)
                        data[key] = d
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)

    if error_key != 0:
        with open('data/anomaly6_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(data_arr, json_file)
    return error_key, is_sample_strange


def error7(n, schema, num_of_err):
    try:
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        sampi = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)
    data_arr = []
    n = int(n)
    p = round((random.random() * 0.2 + 0.4) * n)
    is_sample_strange = []
    error_key = 0
    for i in range(p):
        data = {}
        is_sample_strange.append(0)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)
    for i in range(p,n):
        data = {}
        is_sample_strange.append(1)
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                error_key = key
                if num_of_err == 7:
                    data[key] = []
                else:
                    data[key] = generate_array(schema, key, random.randint(20, 25))
        data_arr.append(data)
    if error_key != 0:
        if num_of_err == 7:
            with open('data/anomaly7_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
                json.dump(data_arr, json_file)
        if num_of_err == 8:
            with open('data/anomaly8_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
                json.dump(data_arr, json_file)

    return error_key, is_sample_strange


def noErrors(n, schema):
    no_collection = False
    try:
        with open('data/collection' + str(schema["idOfCrawler"]) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except FileNotFoundError:
        no_collection = True
    data_arr = []
    n = 10
    is_sample_strange = []
    for i in range(2 * n):
        is_sample_strange.append(0)
        data = {}
        data["idOfCrawler"] = schema["idOfCrawler"]
        for key in schema["properties"].keys():
            if schema["properties"][key]['type'] == "string":
                if key == "phone number":
                    data[key] = generate_phone_number(schema, 0)
                else:
                    try:
                        Format = schema["properties"][key]['format']
                        schema1 = schema
                        add_re_for_formats(schema1, key)
                        try:
                            data[key] = generate_datetime(Format, 1, data_arr[-1][key])
                        except IndexError:
                            if no_collection:
                                data[key] = generate_datetime(Format, 0)
                            else:
                                data[key] = generate_datetime(Format, 1, samples_collection[-1][key])
                    except KeyError:
                        data[key] = generate_string(schema, key)
            if schema["properties"][key]['type'] == "integer":
                data[key] = generate_int(schema, key)
            if schema["properties"][key]['type'] == "number":
                data[key] = generate_float(schema, key)
            if schema["properties"][key]['type'] == "array":
                data[key] = generate_array(schema, key, random.randint(4, 8))
        data_arr.append(data)
    with open('data/noAnomalies_id_' + str(schema["idOfCrawler"]) + '.json', 'w') as json_file:
        json.dump(data_arr, json_file)
    return is_sample_strange
