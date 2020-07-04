# -*- coding: utf-8 -*-
import os
from Service import app
from flask import render_template, flash, redirect, request, url_for
from werkzeug.utils import secure_filename
from Service.forms import LinkForm, GetSchemasForm
import json
from jsonschema import validate
import numpy as np
from cpd import cpd_count
from generator import error1, error2, error3, error4, error5, error6, noErrors, error7
import random
import os
import traceback

ALLOWED_EXTENSIONS = {'json'}
TP, FN, FP = 0, 0, 0
error = 'no'


def allowed_file(filename):
    global ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def route():
    return redirect('/home')


# for rendering
@app.route('/schemas', methods=['GET', 'POST'])
def schemas():
    form = GetSchemasForm()
    if request.method == 'POST':
        if request.form['action'] == 'Read':
            return redirect('/schemas/schemas')
        elif request.form['action'] == 'Get':
            ids = form.id.data
            if len(ids) == 0:
                flash('YOU\'VE FORGOTTEN TO WRITE THE  ID OF THE SCHEMA')
                return redirect('/schemas')
            else:
                try:
                    int(ids)
                except:
                    flash('WRONG DATA')
                    return redirect('/schemas')
                return redirect('/schemas/schemas/' + ids)
        elif request.form['action'] == 'Upload':
            schema = form.newSchema.data
            if len(schema) == 0:
                flash('YOU\'VE FORGOTTEN TO WRITE THE SCHEMA')
                return redirect('/schemas')
            else:
                try:
                    schema = json.loads(schema)
                except:
                    flash('WRONG DATA')
                    return redirect('/schemas')
                path = 'Service/schemas.json'
                with open(path, 'r') as f:
                    schemas = json.loads(f.read())
                last_id = schemas[-1]["idOfCrawler"]
                schema["idOfCrawler"] = last_id + 1
                schemas = schemas + [schema]
                with open(path, 'w') as f:
                    json.dump(schemas, f)
                flash('YOUR SCHEMA IS SUCCESSFULLY WRITTEN')
                return redirect('/schemas')
        elif request.form['action'] == 'Delete':
            ids = form.idDelete.data
            if len(ids) == 0:
                flash('YOU\'VE FORGOTTEN TO WRITE THE  ID OF THE SCHEMA')
                return redirect('/schemas')
            else:
                try:
                    int(ids)
                except:
                    flash('WRONG DATA')
                    return redirect('/schemas')
                return redirect('/schemas/delete/' + ids)
    return render_template('schemas_base.html', title="Schemas_base", form=form)


@app.route('/requests/schemas', methods=['POST'])
def upload_schema():
    schema = request.data
    #print(schema)
    if len(schema) == 0:
        return 'YOU\'VE FORGOTTEN TO WRITE THE SCHEMA'
    else:
        try:
            schema = json.loads(schema)
        except:
            return 'WRONG DATA'
        path = 'Service/schemas.json'
        with open(path, 'r') as f:
            schemas = json.loads(f.read())

        for i, x in enumerate(schemas):
            del x["idOfCrawler"]
            if x == schema:
                return 'THIS SCHEMA ALREADY EXISTS WITH ID = '+str(i+1)

        with open(path, 'r') as f:
            schemas = json.loads(f.read())
        last_id = schemas[-1]["idOfCrawler"]
        schema["idOfCrawler"] = last_id + 1
        schemas = schemas + [schema]
        with open(path, 'w') as f:
            json.dump(schemas, f)
        return 'YOUR SCHEMA IS SUCCESSFULLY WRITTEN'


# for rendering
@app.route('/schemas/schemas', methods=['GET'])
def get_schemas():
    path = 'Service/schemas.json'
    with open(path, 'r') as f:
        schemas = json.loads(f.read())
    for schema in schemas:
        flash(schema)
    return render_template('schemas.html', title="Schemas")


# for testing
@app.route('/requests/schemas', methods=['GET'])
def get_schemas_req():
    path = 'Service/schemas.json'
    with open(path, 'r') as f:
        schemas = f.read()
    return schemas


# for rendering
@app.route('/schemas/schemas/<int:schema_id>', methods=['GET'])
def get_schema(schema_id):
    path = 'Service/schemas.json'
    with open(path, 'r') as f:
        schemas = json.loads(f.read())
    schema = filter(lambda t: t["idOfCrawler"] == schema_id, schemas)
    schema = list(schema)
    if len(schema) == 0:
        flash("There is no schema with id = " + str(schema_id))
    else:
        flash(schema[0])
    return render_template('schema.html', title="Schema")


# for testing
@app.route('/requests/schemas/<int:schema_id>', methods=['GET'])
def get_schema_req(schema_id):
    path = 'Service/schemas.json'
    with open(path, 'r') as f:
        schemas = json.loads(f.read())
    schema = filter(lambda t: t["idOfCrawler"] == schema_id, schemas)
    schema = list(schema)
    if len(schema) == 0:
        return "There is no schema with id = " + str(schema_id)
    else:
        return str(schema[0])


# for rendering
@app.route('/schemas/delete/<int:schema_id>', methods=['GET'])
def delete_schema(schema_id):
    path = 'Service/schemas.json'
    with open(path, 'r') as f:
        schemas = json.loads(f.read())
    schema = filter(lambda t: t["idOfCrawler"] == schema_id, schemas)
    schema = list(schema)
    if len(schema) == 0:
        flash("There is no schema with id = " + str(schema_id))
    else:
        schemas.remove(schema[0])
        for i in range(len(schemas)):
            schemas[i]["idOfCrawler"] = i + 1
        with open(path, 'w') as f:
            json.dump(schemas, f)
        flash("Schema has been deleted!")
    return render_template('schema.html', title="Schema")


# for testing
@app.route('/requests/delete/<int:schema_id>', methods=['GET'])
def delete_schema_req(schema_id):
    path = 'Service/schemas.json'
    with open(path, 'r') as f:
        schemas = json.loads(f.read())
    schema = filter(lambda t: t["idOfCrawler"] == schema_id, schemas)
    schema = list(schema)
    if len(schema) == 0:
        return "There is no schema with id = " + str(schema_id)
    else:
        schemas.remove(schema[0])
        try:
            os.remove("data/collection" + str(schema_id) + ".json")
        except FileNotFoundError:
            print('no collection to delete')
        for i in range(len(schemas)):
            schemas[i]["idOfCrawler"] = i + 1
        with open(path, 'w') as f:
            json.dump(schemas, f)
    return "Schema has been deleted!"


# for rendering
@app.route('/home', methods=['GET', 'POST'])
def home():
    global error
    form = LinkForm()
    n = random.randint(10, 20)
    path = 'Service/schemas.json'
    with open(path, 'r') as f:
        schemass = json.loads(f.read())
    idCrawl = 1
    schema = schemass[idCrawl]
    if request.method == 'POST':
        type_of_error = int(form.link.data)
        if type_of_error == 1:
            error, samp = error1(n, schema)
            if error == 0:
                flash("CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA")
                return redirect('/home')
        if type_of_error == 2:
            error, samp = error2(n, schema)
            if error == 0:
                flash("CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA")
                return redirect('/home')
        if type_of_error == 3:
            error, samp = error3(n, schema)
            print(error)
            if error == 0:
                flash("CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA")
                return redirect('/home')
        if type_of_error == 4:
            error = 'phone number'
            mes, samp = error4(n, schema)
            if mes == 0:
                flash("CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA")
                return redirect('/home')
        if type_of_error == 5:
            error = 'item'
            samp = error5(n, schema)
        if type_of_error == 0:
            error = 'no'
            samp = noErrors(n, schema)
        return redirect('/verify')
    return render_template('home.html', title='Home', form=form)


# for testing
@app.route('/requests/<int:schema_id>/generate', methods=['POST'])
def generate(schema_id):
    global error
    n = 15
    path = 'Service/schemas.json'
    with open(path, 'r') as f:
        schemass = json.loads(f.read())
    schema = schemass[schema_id - 1]
    type_of_error = int(request.data)
    if type_of_error == 1:
        error, samp = error1(n, schema)
        if error == 0:
            return "CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA"
    if type_of_error == 2:
        error, samp = error2(n, schema)
        if error == 0:
            return "CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA"
    if type_of_error == 3:
        error, samp = error3(n, schema)
        if error == 0:
            return "CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA"
    if type_of_error == 4:
        error = 'phone number'
        mes, samp = error4(n, schema)
        if mes == 0:
            return "CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA"
    if type_of_error == 5:
        error = 'item'
        samp = error5(n, schema)
    if type_of_error == 6:
        error, samp = error6(n, schema)
        print(error)
        if error == 0:
            return "CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA"
    if type_of_error == 7:
        error, samp = error7(n, schema, 7)
        print(error)
        if error == 0:
            return "CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA"
    if type_of_error == 8:
        error, samp = error7(n, schema, 8)
        print(error)
        if error == 0:
            return "CAN'T GENERATE THIS TYPE OF MISTAKE WITH CHOSEN SCHEMA"
    if type_of_error == 0:
        error = 'no'
        samp = noErrors(n, schema)
    return {"samples": samp, "message": "samples for error " + str(type_of_error) + " are generated"}


@app.route('/go')
def go():
    return redirect('/verify')


# for rendering
@app.route('/verify', methods=['GET', 'POST'])
def link():
    global error, FN, FP, TP
    path = 'Service/schemas.json'
    n = random.randint(10, 20)
    with open(path, 'r') as f:
        schemass = json.loads(f.read())
    idCrawl = 1
    schema = schemass[idCrawl]
    try:
        with open('data/collection' + str(idCrawl + 1) + '.json', 'r') as f:
            samples = json.loads(f.read())
    except:
        samp = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(idCrawl + 1) + '.json', 'r') as f:
            collection_init = json.loads(f.read())
        with open('data/collection' + str(idCrawl + 1) + '.json', 'w') as json_file:
            json.dump(collection_init, json_file)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            redirect('/verify')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/verify')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        new_samples = json.loads(file.read())
        print('Collection length: ', len(samples))
        samples = samples + new_samples
        num_err = 0
        for sample in new_samples:
            try:
                validate(instance=sample, schema=schema)
            except:
                num_err += 1
                flash('Error in schema\n')
        # if there are errors in schemas, it's no reason to continue tests
        if num_err > 0:
            return redirect('/index')
        else:
            flash('No errors in schemas\n')
        # let's try change point detection
        result_num = cpd_count(samples, schema, "number")
        result_len_str = cpd_count(samples, schema, "string")
        result_len_arr = cpd_count(samples, schema, "array")
        result_item_count = cpd_count(samples, schema, "item")
        num_err = 0
        for result in result_num:
            if len(result) == 2:
                print(result[-1])
                if result[-1] == error:
                    FP += 1
                else:
                    TP += 1
                flash(result[-1] + ': No anomaly \n')
            else:
                print(result[-1])
                if result[-1] != error:
                    FN += 1
                    print(result[-1])
                num_err += 1
                flash(result[-1] + ': Anomaly \n')
        for result in result_len_str:
            if len(result) == 2:
                if result[-1] == error:
                    FP += 1
                else:
                    TP += 1
                flash(result[-1] + ': No anomaly \n')
            else:
                if result[-1] != error:
                    FN += 1
                # print(result[-1])
                num_err += 1
                flash(result[-1] + ': Anomaly \n')
        for result in result_len_arr:
            if len(result) == 2:
                if result[-1] == error:
                    FP += 1
                else:
                    TP += 1
                flash(result[-1] + ': No anomaly \n')
            else:
                if result[-1] != error:
                    FN += 1
                    print(result[-1])
                num_err += 1
                flash(result[-1] + ': Anomaly \n')
        if len(result_item_count) == 2:
            if result_item_count[-1] == error:
                FP += 1
            else:
                TP += 1
            flash(result_item_count[-1] + ': No anomaly \n')
        else:
            if result_item_count[-1] != error:
                FN += 1
                print(result_item_count[-1])
            num_err += 1
            flash(result_item_count[-1] + ': Anomaly \n')
        if num_err == 0:
            with open('data/collection' + str(idCrawl + 1) + '.json', 'w') as f:
                json.dump(samples, f)
        print('True positives: ', TP)
        print('False positives', FP)
        print('False negatives: ', FN)
        if (TP + FP > 0) or (TP + FN > 0):
            precision = TP / (TP + FP)
            recall = TP / (TP + FN)
            f1_score = 2 * precision * recall / (precision + recall)
            flash('f1-score: ' + str(f1_score * 100) + '%')
        return redirect('/index')
    return render_template('verify.html', title='Enter your json:')


# for testing
@app.route('/requests/<int:schema_id>/verify', methods=['POST'])
def verify_test(schema_id):
    path = 'Service/schemas.json'
    n = random.randint(10, 20)
    with open(path, 'r') as f:
        schemass = json.loads(f.read())
    schema = schemass[schema_id - 1]
    try:
        with open('data/collection' + str(schema_id) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
    except:
        sampi = noErrors(n, schema)
        with open('data/noAnomalies_id_' + str(schema_id) + '.json', 'r') as f:
            samples_collection = json.loads(f.read())
        with open('data/collection' + str(schema_id) + '.json', 'w') as json_file:
            json.dump(samples_collection, json_file)

    type_of_error = str(int(request.data))
    if type_of_error == '0':
        with open('data/noAnomalies_id_' + str(schema_id) + '.json', 'r') as f:
            new_samples = json.loads(f.read())
    else:
        with open('data/anomaly' + type_of_error + '_id_' + str(schema_id) + '.json', 'r') as f:
            new_samples = json.loads(f.read())
    print('Collection length: ', len(samples_collection))
    samples = samples_collection + new_samples
    num_err = 0
    for sample in new_samples:
        try:
            validate(instance=sample, schema=schema)
        except:
            num_err += 1
            return {"sample": sample, "message": 'Error in schema', "details": str(traceback.format_exc())}
    # if there are errors in schemas, it's no reason to continue tests
    if num_err == 0:
        message = 'No errors in schemas'
    # let's try change point detection
    result_num = cpd_count(samples, schema, "number")
    result_len_str = cpd_count(samples, schema, "string")
    result_len_arr = cpd_count(samples, schema, "array")
    result_item_count = cpd_count(samples, schema, "item")
    samp = []
    for result in result_num:
        print(result)
        if len(result) > 2:
            samp = []
            if result[0] < len(samples_collection):  # пока не знаю, как исправить
                result = result[1:]
            length = result[0] - len(samples_collection) # if j == 0 else result[j] - result[j - 1]
            for k in range(len(new_samples)):
                if k < length:
                    samp.append(0)
                else:
                    samp.append(1)
            print(len(samp), len(new_samples))
            assert len(samp) == len(new_samples)
            return {"prediction": samp, "message": message, "field": result[-1]}  # позже нужно будет добавлять в массив и возвращать в конце,
                                                             # ошибка может быть в нескольких полях

    for result in result_len_arr:
        print(result)
        if len(result) > 2:
            samp = []
            length = result[0] - len(samples_collection)  # if j == 0 else result[j] - result[j - 1]
            for k in range(len(new_samples)):
                if k < length:
                    samp.append(0)
                else:
                    samp.append(1)
            assert len(samp) == len(new_samples)
            return {"prediction": samp, "message": message, "field": result[-1]}

    print(result_item_count)
    if len(result_item_count) > 2:
        samp = []
        length = result_item_count[0] - len(samples_collection)  # if j == 0 else result[j] - result[j - 1]
        for k in range(len(new_samples)):
            if k < length:
                samp.append(0)
            else:
                samp.append(1)
        print(len(samp), len(new_samples))
        assert len(samp) == len(new_samples)
        return {"prediction": samp, "message": message, "field": result_item_count[-1]}

    for result in result_len_str:
        print(result)
        if len(result) > 2:
            samp = []
            if result[0] < len(samples_collection):  # пока не знаю, как исправить
                result = result[1:]
            length = result[0] - len(samples_collection)  # if j == 0 else result[j] - result[j - 1]
            for k in range(len(new_samples)):
                if k < length:
                    samp.append(0)
                else:
                    samp.append(1)
            print(samp)
            assert len(samp) == len(new_samples)
            return {"prediction": samp, "message": message, "field": result[-1]}

    for i in range(len(new_samples)):
        samp.append(0)
    with open('data/collection' + str(schema_id) + '.json', 'w') as f:
        json.dump(samples, f)
    return {"prediction": samp, "message": message}


# for rendering
@app.route('/index')
def index():
    return render_template('index.html', title='Results')
