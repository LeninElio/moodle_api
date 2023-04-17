# global_params = {
#     "wstoken": 'api_key',
#     "moodlewsrestformat": "json"
# }

resultados = [
    ('01', 'I', 921, '2020-5')
]

list_params = [
    { 
        "wstoken": 'api_key',
        "moodlewsrestformat": "json",
        "wsfunction": "core_course_create_categories", 
        "categories[0][name]": resultado[1], 
        "categories[0][idnumber]": resultado[3], 
        "categories[0][description]": resultado[1], 
        "categories[0][parent]": resultado[2] 
    } for resultado in resultados
]

# params_list = [{**global_params, **params} for params in list_params]

# print(params_list)
print(list_params)


[
    {
        'wstoken': 'api_key', 
        'moodlewsrestformat': 'json', 
        'wsfunction': 'core_course_create_categories', 
        'categories[0][name]': 'I', 
        'categories[0][idnumber]': '2020-5', 
        'categories[0][description]': 'I', 
        'categories[0][parent]': 921
    }
]