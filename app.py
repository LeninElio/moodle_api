from functions import moodle

# moodle.matricular_usuario('thisis', 'curso alimania')

# cursos = moodle.cursos_por_categoria(15)

# print(cursos_mat)
# for curso in cursos:
#     moodle.matricular_usuario('thisis', curso)

cursos_mat = moodle.cursos_por_username('thisis')
print(cursos_mat)


# ['Curso de ejemplo N° 1, Primero Secundaria, 1', 'Curso de ejemplo N° 2, Primero Secundaria, 1']