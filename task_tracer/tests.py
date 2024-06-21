# -*- coding: utf-8 -*-

import random
import math
from datetime import datetime, timedelta
from django.test import TestCase
from crud.models import Project, Task
from user.models import User, Token
from user.choices import ROLE_CHOICES, GENDER_CHOICES
from crud.choices import STATUS_CHOICES
from.testdata import users, projects, tasks

def convertToNumbers(name):
    name = name.lower()
    letter_to_number = {
        'a': 0, 'á': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'é': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'í': 8, 'j': 9,
        'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'ó': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18,
        't': 19, 'u': 20, 'ú': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, ' ': None,
    }
    numbers = [str(letter_to_number[char]) for char in name if char in letter_to_number]
    return ''.join(numbers)

def randomIN(index):
    identification_number = f"{convertToNumbers(users[index]['username'])}"
    if len(identification_number) < 15:
        missing_digits = 15 - len(identification_number)
        identification_number += ''.join(str(random.randint(0, 9)) for _ in range(missing_digits))
    elif len(identification_number) > 15:
        identification_number = identification_number[:15]
    return identification_number

def randomCN(index):
    name = convertToNumbers(users[index]['username'])
    contact_number = f"+{random.randint(1, 99)}({random.randint(1, 99)}){name[:2]}-{name[2:6]}"
    if len(contact_number) < 15:
        missing_digits = 15 - len(contact_number)
        contact_number += ''.join(str(random.randint(0, 9)) for _ in range(missing_digits))
    elif len(contact_number) > 15:
        contact_number = contact_number[:15]
    return contact_number

def getGender(index):
    name = users[index]['full_name']
    first_name = name.split()[0]
    if first_name[-1] in ['a', 'i']:
        return GENDER_CHOICES[1][0]
    return GENDER_CHOICES[0][0]

def convertFullNameToUsername(full_name):
    names = full_name.split()
    return names[0].join(names[1])

def convertFullNameToEmail(full_name):
    names = full_name.split()
    first_name = names[0].lower()
    last_name = ' '.join(names[1:]).lower()
    username = first_name + '-' + last_name
    username = ''.join(e for e in username if e.isalnum() or e in '-._@')
    if not username:
        username = 'user'
    return f"{username}@example.com"


for index, user in enumerate(users):
    users[index]['username'] = convertFullNameToUsername(users[index]['full_name'])
    users[index]['password'] = f"{users[index]['username']}v{random.randint(2000,8000)}"
    users[index]['email'] = convertFullNameToEmail(users[index]['full_name'])
    users[index]['identification_number'] = randomIN(index)
    users[index]['contact_number'] = randomCN(index)
    users[index]['gender'] = getGender(index)
    users[index]['role'] = ROLE_CHOICES[random.randint(0, len(ROLE_CHOICES) - 1)][0]
    if random.randint(0, 9) > 3:
        project = random.randint(0, len(projects) - 1)
    else:
        project = None
    users[index]['project'] = project


for index, project in enumerate(projects):
    start_date = datetime.now() + timedelta(days=random.randint(4, 80))
    days = random.randint(11, 40)
    end_date = (start_date + timedelta(days=days)).strftime('%Y-%m-%d')
    num = random.randint(0, 11)
    if num < 4:
        updated_at = start_date.strftime('%Y-%m-%d %H:%M')
    elif num < 8:
        updated_at = (start_date + timedelta(days=days-num)).strftime('%Y-%m-%d %H:%M')
    else:
        updated_at = None

    created_by = None
    num = random.randint(0, 9)
    if num > 1:
        created_by = random.randint(0, len(users)-1)

    updated_by = None
    if updated_at and random.randint(0, 9) > 1:
        updated_by = random.randint(0, len(users)-1)
        if random.randint(0, 9) > 4:
            users[updated_by]['project'] = index

    projects[index]['start_date'] = start_date.strftime('%Y-%m-%d %H:%M')
    projects[index]['created_by'] = created_by
    projects[index]['created_at'] = projects[index]['start_date']
    projects[index]['updated_at'] = updated_at
    projects[index]['updated_by'] = updated_by
    projects[index]['end_date'] = end_date


for index, task in enumerate(tasks):
    start_date = datetime.now() + timedelta(days=random.randint(4, 80))
    days = random.randint(11, 40)
    end_date = (start_date + timedelta(days=days)).strftime('%Y-%m-%d')
    num = random.randint(0, 11)
    if num < 4:
        updated_at = start_date.strftime('%Y-%m-%d %H:%M')
    elif num < 8:
        updated_at = (start_date + timedelta(days=days-num)).strftime('%Y-%m-%d %H:%M')
    else:
        updated_at = None

    created_by = None
    num = random.randint(0, 9)
    if num > 0:
        created_by = random.randint(0, len(users)-1)

    updated_by = None
    if updated_at and random.randint(0, 9) > 1:
        updated_by = random.randint(0, len(users)-1)
        if random.randint(0, 9) > 4:
            users[updated_by]['task'] = index

    assigned_to = None
    num = random.randint(0, 9)
    if num > 5:
        assigned_to = random.randint(0, len(users)-1)
    elif num == 5:
        assigned_to = created_by
    
    if assigned_to:
        project = users[assigned_to]['project']
    elif created_by:
        project = users[created_by]['project']
    else:
        project = random.randint(0, len(users)-1)
    
    state = STATUS_CHOICES[0][0]
    if assigned_to:
        state = STATUS_CHOICES[random.randint(1, len(STATUS_CHOICES) - 1)][0]

    tasks[index]['assigned_to'] = assigned_to
    tasks[index]['state'] = state
    tasks[index]['project'] = project
    tasks[index]['start_date'] = start_date.strftime('%Y-%m-%d %H:%M')
    tasks[index]['created_by'] = created_by
    tasks[index]['created_at'] = tasks[index]['start_date']
    tasks[index]['updated_at'] = updated_at
    tasks[index]['updated_by'] = updated_by
    tasks[index]['end_date'] = end_date

class DataLoadingTest(TestCase):
    def test_load_data(self):
        for index, _user in enumerate(users):
            user = _user.copy()
            del user['project']
            del user['password']
            User.objects.create(**user)
            usero = User.objects.get(username=user['username'])
            usero.set_password(_user['password'])
            usero.save()

        for _project in projects:
            project = _project.copy()
            if project['created_by']:
                created_by = User.objects.get(username=users[project['created_by']]['username'])
                project['created_by'] = created_by
                
            if project['updated_by']:
                updated_by = User.objects.get(username=users[project['updated_by']]['username'])
                project['updated_by'] = updated_by

            User.objects.create(**project)
        
        for _user in users:
            if _user['project']:
                user = User.objects.get(username=_user['username'])
                project = Project.objects.get(name=projects[_user['project']].name)
                user['project'] = project
                user.save()

        for task in tasks:
            Task.objects.create(**project)
        
        for _task in tasks:
            task = _task.copy()
            if task['project']:
                project = User.objects.get(username=projects[task['project']]['name'])
                task['created_by'] = project

            if task['assigned_to']:
                assigned_to = User.objects.get(username=users[task['assigned_to']]['username'])
                task['assigned_to'] = assigned_to

            if task['created_by']:
                created_by = User.objects.get(username=users[task['created_by']]['username'])
                task['created_by'] = created_by
                
            if task['updated_by']:
                updated_by = User.objects.get(username=users[task['updated_by']]['username'])
                task['updated_by'] = updated_by

            User.objects.create(**task)
        

        self.assertEqual(User.objects.count(), len(users))
        self.assertEqual(Project.objects.count(), len(projects))
        self.assertEqual(Task.objects.count(), len(tasks))

        print("Proces ended True")
