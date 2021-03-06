import pandas as pd
from flask import Flask, render_template, send_file
from flask import request
import hashlib
import json

 
app = Flask(__name__, static_url_path='')
data = pd.read_json('text.json')

def first_option(A):
    df = pd.DataFrame(data[A])
    excel_writer = pd.ExcelWriter('output_1.xlsx')
    df.to_excel(excel_writer, sheet_name="sheet1")
    df.to_csv('csv_1.csv', encoding='utf-8', index=False)
    excel_writer.save()
    return data[A]

def second_option(A):
    df = data.iloc[A]
    result = pd.DataFrame()
    for i in range(1, 45):
        current = df[i].apply(lambda x: 1 if x != 0 and x != 'EMPTY' else 0)
        result = pd.concat([result, current], axis = 1)
    excel_writer = pd.ExcelWriter('output_2.xlsx')
    result.to_excel(excel_writer, sheet_name="sheet1")
    result.to_csv('csv_2.csv', encoding='utf-8', index=False)
    excel_writer.save()
    return result
  
def third_option(A):
    df = data.iloc[A]
    result = df.apply(lambda x: ','.join(tuple(x)), axis = 1)
    result = pd.DataFrame(result, index =A)
    excel_writer = pd.ExcelWriter('output_3.xlsx')
    df.to_excel(excel_writer, sheet_name="sheet1")
    df.to_csv('csv_3.csv', encoding='utf-8', index=False)
    excel_writer.save()
    return result

def fourth_option(A):
    df = data.iloc[A]
    result = df.apply(lambda x: hashlib.md5(json.dumps(list(x), sort_keys=True).encode('utf-8')).hexdigest(), axis = 1)
    result = pd.DataFrame(result, index = A)
    excel_writer = pd.ExcelWriter('output_4.xlsx')
    result.to_excel(excel_writer, sheet_name="sheet1")
    result.to_csv('csv_4.csv', encoding='utf-8', index=False)
    excel_writer.save()
    return result

@app.route('/getfile/<name>')
def get_output_file(name):
    return send_file(name, as_attachment=True)

@app.route('/f', methods=['POST'])
def f():   
    b = request.form['dzen']
    if b == '1':
        if request.form['A'].upper() == 'ALL':
            A = [i for i in range(1, 45)]
        else:
            A = list(map(int, request.form['A'].split(',')))
        return first_option(A).to_html() +  """
                                                <html>
                                                 <head>
                                                 <meta charset="utf-8">
                                                      <title>Result for the first option</title>
                                                        </head>
                                                         <body>
                                                          <p><a href=/getfile/output_1.xlsx>Скачать файл в xlsx формате</a>
                                                                  <a href=/getfile/csv_1.csv>Скачать файл в csv формате</a>
                                                           </body>
                                                    </html>
                                                    """
    elif b == '2':
        A = list(map(int, request.form['A'].split(',')))
        return second_option(A).to_html() + """
                                            <html>
                                            <head>
                                             <meta charset="utf-8">
                                                <title>Results for the second option</title>
                                                </head>
                                                <body>
                                               <p><a href=/getfile/output_2.xlsx>Скачать файл в xlsx формате</a>
                                                 <a href=/getfile/csv_2.csv>Скачать файл в csv формате</a>
                                                  </body>
                                                  </html>
                                                """
    elif b == '3':
        A = list(map(int, request.form['A'].split(',')))
        return third_option(A).to_html(pd.set_option('display.max_colwidth', -1)) + """
                                                                                      <html>
                                                                                       <head>
                                                                                      <meta charset="utf-8">
                                                                                        <title>Results for the second option</title>
                                                                                     </head>
                                                                                      <body>
                                                                                       <p><a href=/getfile/output_2.xlsx>Скачать файл в xlsx формате</a>
                                                                                       <a href=/getfile/csv_2.csv>Скачать файл в csv формате</a>
                                                                                     </body>
                                                                                   </html>
                                                                                 """
    else:
        if request.form['A'].upper() == 'ALL':
            A = [i for i in range(452)]
        else:
            A = list(map(int, request.form['A'].split(',')))
        return fourth_option(A).to_html() + """
                                             <html>
                                             <head>
                                               <meta charset="utf-8">
                                            <title>Results for the fourth option</title>
                                               </head>
                                                 <body>
                                                <p><a href=/getfile/output_4.xlsx>Скачать файл в xlsx формате</a>
                                                  <a href=/getfile/csv_4.csv>Скачать файл в csv формате</a>
                                                 </body>
                                                  </html>
                                               """

@app.route('/')
def f0():
    return render_template('index.html')
 
if __name__ == '__main__':
    app.run(debug=True)
