from typing_extensions import Required
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'POSTGRES URI'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Course():
    def __init__(self, number_name, credit_hours, lab_field_hours, prerequisites, description):
        temp = number_name.split(' - ')
        self.number = temp[0]
        self.name = temp[1]
        # self.number = number
        # self.name = name
        self.credit_hours = credit_hours
        self.lab_field_hours = lab_field_hours
        self.prerequisites = prerequisites
        self.description = description
        self.class_type = None
        self.semesters = None

    def __init__(self, number, name, credit_hours, lab_field_hours, prerequisites, description, class_type, semesters):
        self.number = number
        self.name = name
        self.credit_hours = credit_hours
        self.lab_field_hours = lab_field_hours
        self.prerequisites = prerequisites
        self.description = description
        self.class_type =  class_type
        self.semesters = semesters

class Courses(db.Model):
    __tablename__ = 'courses'
    number = db.Column(db.String(8), primary_key = True)
    name = db.Column(db.String(100), unique = True)
    credit_hours = db.Column(db.Integer)
    lab_field_hours = db.Column(db.Integer)
    prerequisites = db.Column(db.String(300))
    description = db.Column(db.Text())
    class_type = db.Column(db.String(100))
    semesters = db.Column(db.String(15))

    def __init__(self, course):
        self.number = course.number
        self.name = course.name
        self.credit_hours = course.credit_hours
        self.lab_field_hours = course.lab_field_hours
        self.prerequisites = course.prerequisites
        self.description = course.description
        self.class_type = course.class_type
        self.semesters = course.semesters

# course_list = []
# coursefp = open('C:\\Users\\Test Bench\\Desktop\\Coding\\UCF CS Courses API\\courses_updated.txt', 'r', encoding='utf8')
# coursefp2 = open('C:\\Users\\Test Bench\\Desktop\\Coding\\UCF CS Courses API\\not_found.txt', 'r', encoding='utf8')

# for x in range(0,50):
#     number = coursefp.readline().replace('\n','')
#     name = coursefp.readline().replace('\n','')
#     credit_hours = coursefp.readline().replace('\n','')
#     lab_field_hours = coursefp.readline().replace('\n','')
#     prerequisites = coursefp.readline().replace('\n','')
#     description = coursefp.readline().replace('\n','')
#     class_type = coursefp.readline().replace('\n','')
#     semesters = coursefp.readline().replace('\n','')
#     throw_away = coursefp.readline().replace('\n','')

#     c = Course(number, name, credit_hours, lab_field_hours, prerequisites, description, class_type, semesters)
#     course_list.append(c)

# for x in range(0,35):
#     number = coursefp2.readline().replace('\n','')
#     name = coursefp2.readline().replace('\n','')
#     credit_hours = coursefp2.readline().replace('\n','')
#     lab_field_hours = coursefp2.readline().replace('\n','')
#     prerequisites = coursefp2.readline().replace('\n','')
#     description = coursefp2.readline().replace('\n','')
#     class_type = coursefp2.readline().replace('\n','')
#     semesters = coursefp2.readline().replace('\n','')
#     throw_away = coursefp2.readline().replace('\n','')

#     c = Course(number, name, credit_hours, lab_field_hours, prerequisites, description, class_type, semesters)
#     course_list.append(c)

# for c in course_list:
#     # print(c.number)
#     if c.number == 'CNT4932':
#         continue
#     data = Courses(c)
#     db.session.add(data)
#     db.session.commit()

# print("BEBEBEBEBE" + course_list[2].number)
# fp = open('C:\\Users\\Test Bench\\Desktop\\Coding\\UCF CS Courses API\\helper\\out.txt','r', encoding='utf8')

# lines = fp.readlines()
# for l in range(0,len(lines)):
#     temp = lines[l].split(' - ')
#     number = temp[0]
#     name = temp[1]
#     data = Courses(number, name, lines[l+1], lines[l+2],lines[l+3],lines[l+4])
#     db.session.add(data)
#     db.session.commit()
#     # change increment of iterator
#     l+=6
#     # return

# # populate(db)
@app.route('/', methods=['GET'])
def home():
    retjson = []
    data = db.session.query(Courses).all()
    for d in data:
        c = {
            'number':d.number,
            'name':d.name,
            'credit_hours':d.credit_hours,
            'lab_field_hours':d.lab_field_hours,
            'prerequisites':d.prerequisites,
            'description':d.description,
            'class_type':d.class_type,
            'semesters':d.semesters
        }
        retjson.append(c)
    return jsonify(retjson)

@app.route('/class_type/<string:ctype>')
def search_by_class_type(ctype):
    retjson = []
    # data =[]
    # data2 = []
    # data3 = []
    ctype = ctype.lower()

    if ctype == 'cs_required':
        # 1 - CS Required
        # 6 - CS & IT Required
        # 7 - CS Required IT 
        data = db.session.query(Courses).filter_by(class_type='CS Required').all()
        data2 = db.session.query(Courses).filter_by(class_type='CS & IT Required').all()
        data3 = db.session.query(Courses).filter_by(class_type='CS Required & IT Elective').all()
    
    if ctype == 'it_required':
        # 2 - IT Required
        # 6 - CS & IT Required
        # 5 - IT Required (one can be used for CS Elective)
        data = db.session.query(Courses).filter_by(class_type='IT Required').all()
        data2 = db.session.query(Courses).filter_by(class_type='CS & IT Required').all()
        data3 = db.session.query(Courses).filter_by(class_type='IT Required (one can be used for CS Elective)').all()
    
    if ctype == 'cs_elective':
        # 3 - CS & IT Elective
        # 5 - IT Required (one can be used for CS Elective)
        # 9 - CS Elective
        data = db.session.query(Courses).filter_by(class_type='CS & IT Elective').all()
        data2 = db.session.query(Courses).filter_by(class_type='IT Required (one can be used for CS Elective)').all()
        data3 = db.session.query(Courses).filter_by(class_type='CS Elective').all()

    if ctype == 'it_elective':
        # 3 - CS & IT Elective
        # 4 - IT Elective
        # 7 - CS Required IT Elective
        data = db.session.query(Courses).filter_by(class_type='CS & IT Elective').all()
        data2 = db.session.query(Courses).filter_by(class_type='IT Elective').all()
        data3 = db.session.query(Courses).filter_by(class_type='CS Required & IT Elective').all()

    for d in data:
        c = {
            'number':d.number,
            'name':d.name,
            'credit_hours':d.credit_hours,
            'lab_field_hours':d.lab_field_hours,
            'prerequisites':d.prerequisites,
            'description':d.description,
            'class_type':d.class_type,
            'semesters':d.semesters
        }
        retjson.append(c)
    
    for d in data2:
        c = {
            'number':d.number,
            'name':d.name,
            'credit_hours':d.credit_hours,
            'lab_field_hours':d.lab_field_hours,
            'prerequisites':d.prerequisites,
            'description':d.description,
            'class_type':d.class_type,
            'semesters':d.semesters
        }
        retjson.append(c)

    for d in data3:
        c = {
            'number':d.number,
            'name':d.name,
            'credit_hours':d.credit_hours,
            'lab_field_hours':d.lab_field_hours,
            'prerequisites':d.prerequisites,
            'description':d.description,
            'class_type':d.class_type,
            'semesters':d.semesters
        }
        retjson.append(c)

    if len(retjson)<1:
        return jsonify({
            'error':'course not found or input error; check parameters.'
        })
    return jsonify(retjson)

@app.route('/number/<string:cnum>')
def search_by_number(cnum):
    retjson = []
    data = db.session.query(Courses).filter_by(number=cnum).all()
    if len(data) < 1:
        r = {
            'error':'course not found or input error; check parameters.'
        }
        return jsonify(r)
        
    for d in data:
        c = {
            'number':d.number,
            'name':d.name,
            'credit_hours':d.credit_hours,
            'lab_field_hours':d.lab_field_hours,
            'prerequisites':d.prerequisites,
            'description':d.description,
            'class_type':d.class_type,
            'semesters':d.semesters
        }
        retjson.append(c)
    return jsonify(retjson)

@app.route('/semester/<string:sem>')
def search_by_semester(sem):
    retjson = []
    # or sem.upper == 'SPRING'
    sem = sem.capitalize()
    if sem != 'Occasional':
        data = db.session.query(Courses).filter_by(semesters='Fall,Spring').all()
        for d in data:
            c = {
                'number':d.number,
                'name':d.name,
                'credit_hours':d.credit_hours,
                'lab_field_hours':d.lab_field_hours,
                'prerequisites':d.prerequisites,
                'description':d.description,
                'class_type':d.class_type,
                'semesters':d.semesters
            }
            retjson.append(c)
    if sem == 'Both':
        return jsonify(retjson)
    else:
        data = db.session.query(Courses).filter_by(semesters=sem)
        for d in data:
            c = {
                'number':d.number,
                'name':d.name,
                'credit_hours':d.credit_hours,
                'lab_field_hours':d.lab_field_hours,
                'prerequisites':d.prerequisites,
                'description':d.description,
                'class_type':d.class_type,
                'semesters':d.semesters
            }
            retjson.append(c)
    if len(retjson)<1 or (sem != 'Fall' and sem != 'Spring' and sem != 'Both' and sem != 'Occasional'):
        return jsonify({
            'error':'course not found or input error; check parameters.'
        })
    return jsonify(retjson)

if __name__ == '__main__':
    app.run()

# 1 - CS Required
# 2 - IT Required
# 3 - CS & IT Elective
# 4 - IT Elective
# 5 - IT Required (one can be used for CS Elective)
# 6 - CS & IT Required
# 7 - CS Required IT Elective
# 8 - Not Approved
# 9 - CS Elective
