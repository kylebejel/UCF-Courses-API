from os import name
from app import Course

class CourseHelper():
    def __init__(self, class_type, number, semesters):
        self.class_type = class_type
        self.number = number
        self.semesters = semesters

class_type_codes = ['CS Required','IT Required', 'CS & IT Elective', 'IT Elective', 'IT Required (ONLY ONE can be used for CS Elective)', 'CS & IT Required', 'CS Required & IT Elective', 'Not Approved', 'CS Elective']
courses = []
helpers = []
not_found = []

out = open('C:\\Users\\Test Bench\\Desktop\\Coding\\UCF CS Courses API\\helper\\out2.txt','r', encoding='utf8')
pdf = open('C:\\Users\\Test Bench\\Desktop\\Coding\\UCF CS Courses API\\helper\\pdf2.txt','r', encoding='utf8')

# infiles
pdflines = pdf.readlines()
outlines = out.readlines()

# outfiles
coursesupdatedfp = open('courses_updated.txt', 'w', encoding='utf8')
notfoundfp = open('not_found.txt', 'w', encoding='utf8')

for l in range(0,len(pdflines),4):
    # temp = pdflines[l+2]
    print(pdflines)
    print(f'type: {pdflines[l]}\nnumber: {pdflines[l+1]}\nsemesters: {pdflines[l+2]}\n')
    t = class_type_codes[int(pdflines[l].replace("\n", "").replace(" ",""))-1]
    num = pdflines[l+1].replace(" ","").replace("\n","")
    sem = pdflines[l+2].replace(" ","")
    # helper = CourseHelper(class_type_codes[int(pdflines[l].replace('\n',''))-1],pdflines[l+1].replace(" ", "").replace('\n',''),pdflines[l+2].replace('\n',''))
    helper = CourseHelper(t, num, sem)
    helpers.append(helper)
    # l = l+4

for l in range(0, len(outlines),8):
    course = Course(outlines[l].replace("\n",""),outlines[l+1].replace("\n",""),outlines[l+2].replace("\n",""),outlines[l+3].replace("\n",""),outlines[l+4].replace("\n",""))
    courses.append(course)
    # l+=8

for helper in helpers:
    isFound = False
    for course in courses:
        if helper.number == course.number:
            course.semesters = helper.semesters
            course.class_type = helper.class_type
            isFound = True
    if not isFound:
        not_found.append(helper)

courseout = []
for course in courses:
    lines = f'{course.number}\n{course.name}\n{course.credit_hours}\n{course.lab_field_hours}\n{course.prerequisites}\n{course.description}\n{course.class_type}\n{course.semesters}\n'
    courseout.append(lines)
    # number
    # name
    # self.credit_hours = credit_hours
    # self.lab_field_hours = lab_field_hours
    # self.prerequisites = prerequisites
    # self.description = description
    # self.class_type = None
    # self.semesters = None

nfout = []
for nf in not_found:
    lines = f'{nf.class_type}\n{nf.number}\n{nf.semesters}\n'
    nfout.append(lines)

coursesupdatedfp.writelines(courseout)
notfoundfp.writelines(nfout)

coursesupdatedfp.close()
notfoundfp.close()

out.close()
pdf.close()