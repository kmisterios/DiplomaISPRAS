import ruptures as rpt
import numpy as np
from datetime import datetime, time
import matplotlib.pyplot as plt
import seaborn


def date_str_to_sec(date_str):
    return (datetime.fromisoformat(date_str) - datetime(1970, 1, 1)).total_seconds()


def time_str_to_sec(time_str):
    t = time.fromisoformat(time_str)
    return t.hour*60*60 + t.minute*60 + t.second + t.microsecond/1000000


def to_subtraction(samples):
    new_samples = []
    m = 0
    odd = 0
    #print(len(str(samples[0] - samples[1])))
    for i in range(1, len(samples)):
        d = samples[i] // 100000 -samples[i-1] // 100000
        if np.abs(d) > 170:
            if odd == 0:
                m = d
                odd = 1
            else:
                m = 0
        new_samples.append(d + m)
    return new_samples


def to_subtraction_from_first(samples):
    new_samples = [0]
    for i in range(len(samples)):
        m = np.sum(new_samples) / len(new_samples)
        print(m)
        new_samples.append(samples[i] - m)
    return new_samples


def from_format_to_timestamp(sample, date_format):
    return np.abs((datetime.strptime(sample, date_format) - datetime(1970, 1, 1)).total_seconds())


def cpd_count(samples, schema, name):
    result = []
    if name == "item":
        numbers = []
        for sample in samples:
            numbers.append(len(sample.keys()))
        numbers = np.array(numbers)
        model = "l1"
        algo = rpt.Pelt(model=model, min_size=1, jump=1).fit(numbers)
        result = algo.predict(pen=5) + ['item']
        return result
    keys = []
    for key in schema["properties"].keys():
        if schema["properties"][key]["type"] == name:
            keys.append(key)
    for key in keys:
        subtraction = 1
        numbers = []
        for sample in samples:
            if key in sample.keys():
                if name == "number" or name == "integer":
                    numbers.append(sample[key])
                else:
                    try:
                        formatt = schema["properties"][key]["format"]
                        if formatt == "date" or formatt == "date-time":
                            numbers.append(date_str_to_sec(sample[key]))
                            if subtraction:
                                subtraction = 2
                        elif formatt == "time":
                            numbers.append(date_str_to_sec(sample[key]))
                            if subtraction:
                                subtraction = 2
                        elif formatt == "timestamp":
                            numbers.append(int(sample[key]))
                            if subtraction:
                                subtraction = 2
                        else:
                            try:
                                numbers.append(from_format_to_timestamp(sample[key], formatt))
                                if subtraction:
                                    subtraction = 2
                            except:
                                raise
                    except KeyError:
                        numbers.append(len(sample[key]))
            else:
                return result

        numbers = np.array(numbers)
        if subtraction == 2:
            print('я тут ', key)
            numbers = np.array(to_subtraction(numbers))
            #print(numbers)
        numbers = np.array(numbers)
        if (numbers.min() == numbers.max()) or key == 'phone number':
            model = "l1"
            algo = rpt.Pelt(model=model, min_size=1, jump=1).fit(numbers)
            predict = algo.predict(pen=5)
            if subtraction == 2:
                predict = list(np.array(predict) + 1)
            result.append(predict + [key])
        else:
            model = "rbf"
            #algo = rpt.Pelt(model=model, min_size=1, jump=1).fit(numbers)
            algo = rpt.Binseg(model=model, jump=1).fit(numbers)
            #algo = rpt.BottomUp(model=model, jump=1, min_size=1).fit(numbers)
            #algo = rpt.Window(width=5, model=model, jump=1, min_size=1).fit(numbers)
            try:
                predict = algo.predict(pen=5)
            except ValueError:
                model = "l1"
                algo = rpt.Pelt(model=model, min_size=1, jump=1).fit(numbers)
                predict = algo.predict(pen=5)
            if subtraction == 2:
                predict = list(np.array(predict) + 1)
            result.append(predict + [key])
    return result

