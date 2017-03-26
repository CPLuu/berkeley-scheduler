#!/usr/bin/env python3

from collections import defaultdict
import json
import sys

from utils import *


def extract_instructor_info_from_json(instructor_json):
    return {
        'name': instructor_json['instructor']['names'][0]['formattedName'],
        'role': instructor_json['role'].get('description', None),
    }


def extract_meeting_info_from_json(meeting_json):
    extracted_instructors = []
    for instructor_json in meeting_json.get('assignedInstructors', []):
        if 'names' in instructor_json['instructor'] and instructor_json['instructor']['names']:
            extracted_instructors.append(
                extract_instructor_info_from_json(instructor_json)
            )
    return {
        'startTime': meeting_json.get('startTime', None),
        'endTime': meeting_json.get('endTime', None),
        'days': {
            'Sunday': meeting_json.get('meetsSunday', None),
            'Monday': meeting_json.get('meetsMonday', None),
            'Tuesday': meeting_json.get('meetsTuesday', None),
            'Wednesday': meeting_json.get('meetsWednesday', None),
            'Thursday': meeting_json.get('meetsThursday', None),
            'Friday': meeting_json.get('meetsFriday', None),
            'Saturday': meeting_json.get('meetsSaturday', None),
        },
        'dayAbbrvs': meeting_json.get('meetsDays', None),
        'location': meeting_json.get('location', {}),
        'instructors': extracted_instructors,
    }


def extract_enrollment_info_from_json(enrollment_json):
    return {
        'eCurr': enrollment_json['enrolledCount'],
        'eMin': enrollment_json['minEnroll'],
        'eMax': enrollment_json['maxEnroll'],
        'wCurr': enrollment_json['waitlistedCount'],
        'wMax': enrollment_json['maxWaitlist']
    }


def extract_section_info_from_json(section_json):
    extracted_meetings = [extract_meeting_info_from_json(meeting_json)
                          for meeting_json in section_json.get('meetings', [])]

    return {
        'number': section_json.get('number', ''),
        'isPrimary': section_json['association']['primary'],
        'associatedPrimarySectionId': section_json['association']['primaryAssociatedSectionId'],
        'type': section_json['component']['code'],
        'id': section_json['id'],
        'meetings': extracted_meetings,
        'graded': section_json['graded'],
        'status': section_json['enrollmentStatus']['status'],
        'enrollment': extract_enrollment_info_from_json(section_json['enrollmentStatus']),
        'print': section_json['printInScheduleOfClasses']
    }


def extract_units_info_from_json(units_json):
    return {
        'minimum': units_json['minimum'],
        'maximum': units_json['maximum']
    }


def extract_class_info_from_json(sections_json, class_json, course_json):
    extracted_sections = {}
    for section_json in sections_json:
        section = extract_section_info_from_json(section_json)
        extracted_sections[section['id']] = section

    primary_section_id = sections_json[0]['association']['primaryAssociatedSectionId']

    return {
        # Course info
        'displayName': course_json['displayName'],
        'title': course_json['title'],
        "description": course_json['description'],
        "crossListed": course_json['crossListedCourses'],

        # Class info
        'id': primary_section_id,
        'primaryComponent': class_json['primaryComponent']['code'],
        'status': class_json['status']['code'],
        'instructionMode': class_json['instructionMode']['code'],
        'finalExam': class_json['finalExam'],
        'print': class_json['anyPrintInScheduleOfClasses'],
        'units': extract_units_info_from_json(class_json['allowedUnits']),
        'grading': class_json['gradingBasis']['code'],
        'enrollment': extract_enrollment_info_from_json(class_json['aggregateEnrollmentStatus']),
        'sections': list(extracted_sections.values())
    }


def extract_course_info_from_class_json(class_json):
    course_json = class_json['course']

    return {
        'displayName': course_json['displayName'],
        'title': course_json['title'],
        "description": course_json.get('description'),
        "crossListedCourses": course_json.get('crossListedCourses'),
    }


def main():
    with open(departments(), 'r') as f:
        subject_areas = sorted(json.load(f)['subjectAreas'].keys())

    completed = set()
    num_total = len(subject_areas)

    for subject_area in subject_areas:
        if subject_area in completed:
            continue

        # Courses
        with open(course_listing_by_subject_area(subject_area)) as f:
            courses_json = json.load(f)

        # Classes
        classes_json = defaultdict(dict)
        try:
            chunk_number = 0
            while True:
                with open(fetched_classes_by_subject_area_new(subject_area, chunk_number)) as f:
                    for class_ in json.load(f)['apiResponse']['response']['classes']:
                        catalog_number, section_number = extract_number_from_class(class_)
                        classes_json[catalog_number][section_number] = class_

                chunk_number += 1
        except IOError:
            pass

        # Sections
        with open(fetched_class_sections_by_subject_area(subject_area)) as f:
            sections_json = json.load(f)

        # Extraction
        classes = defaultdict(dict)
        for catalog_number, class_sections in sections_json.items():
            for section_number, section in class_sections.items():
                sections_json = section['apiResponse']['response']['classSections']
                class_json = classes_json[catalog_number][section_number]
                try:
                    course_json = courses_json[catalog_number]
                except KeyError:
                    print('{} {}-{}'.format(subject_area, catalog_number, section_number))
                    course_json = extract_course_info_from_class_json(class_json)

                classes[catalog_number][section_number] = \
                    extract_class_info_from_json(sections_json, class_json, course_json)

        with open(class_listing_by_subject_area(subject_area), 'w') as f:
            json.dump(classes, f)
        completed.add(subject_area)
        print('completed {}/{}'.format(len(completed), num_total))


if __name__ == '__main__':
    sys.exit(main())