from xml.dom.minidom import Document, parse


class InfoBatch:
    def __init__(self, title, pre_node_titles):
        self.title = title
        self.pre_node_titles = pre_node_titles


def save_data_xml(course_list, file_path):
    doc = Document()
    courses = doc.createElement('course_list')
    doc.appendChild(courses)

    for course in course_list:
        single_course = doc.createElement('course')
        courses.appendChild(single_course)

        single_course_name = doc.createElement('course_name')
        course_name = doc.createTextNode(course.name)
        single_course.appendChild(single_course_name)
        single_course_name.appendChild(course_name)

        pre_course = doc.createElement('pre_course')
        pre_course_name = ','.join(course.pre_course)
        course_name = doc.createTextNode(pre_course_name)
        single_course.appendChild(pre_course)
        pre_course.appendChild(course_name)

        after_course = doc.createElement('after_course')
        after_course_name = ','.join(course.after_course)
        course_name = doc.createTextNode(after_course_name)
        single_course.appendChild(after_course)
        after_course.appendChild(course_name)

    with open(file_path, 'wb+') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))


def load_data_xml(file_path):
    info_list = []
    doc = parse(file_path)

    courses = doc.getElementsByTagName("course")
    for course in courses:
        title = course.getElementsByTagName("course_name")[0].childNodes[0].data
        try:
            pre_node_titles = course.getElementsByTagName("pre_node_titles")[0].childNodes[0].data
            pre_node_titles = pre_node_titles.split(',')
            info_list.append(InfoBatch(title, pre_node_titles))
        except IndexError:
            info_list.append(InfoBatch(title, []))

    return info_list


'''
course_list = []
course_list.append(Course('Advance Math'))
course_list.append(Course('Linear Algebra'))
course_list.append(Course('Procedure Oriented Programming'))
course_list.append(Course('Object Oriented Programming'))
course_list[-1].add_pre_course(course_list, ['Procedure Oriented Programming'])
course_list.append(Course('College Physics'))
course_list[-1].add_pre_course(course_list, ['Advance Math'])
course_list.append(Course('Digital Logic'))
course_list[-1].add_pre_course(course_list, ['Procedure Oriented Programming'])
course_list.append(Course('Computer Organization'))
course_list[-1].add_pre_course(course_list, ['Advance Math', 'Procedure Oriented Programming', 'Digital Logic'])
course_list.append(Course('Computer Architecture'))
course_list[-1].add_pre_course(course_list,
                               ['Advance Math', 'Procedure Oriented Programming', 'Digital Logic', 'Computer Organization'])

save_data_xml(course_list, 'resource/data/data.xml')
'''
