'use strict';

function Schedule(userId, sections) {
  this.courses = {};
  this.meetingsByDay = {
    'Monday': [],
    'Tuesday': [],
    'Wednesday': [],
    'Thursday': [],
    'Friday': []
  };

  var sectionIdList = [];
  sections.forEach(function (section) {
    sectionIdList.push(section.id);
    var courseId = section.course.id;
    if (!this.courses.hasOwnProperty(courseId)) {
      this.courses[courseId] = [];
    }
    this.courses[courseId].push(section);

    for (var day in section.meeting.days) {
      if (section.meeting.days[day]) {
        this.meetingsByDay[day].push(section);
      }
    }
  }, this);
  for (var day in this.meetingsByDay) {
    this.meetingsByDay[day].sort(function(a, b) {
      return a.meeting.startTime.compareTo(b.meeting.startTime);
    });
  }

  this.id = Schedule.generateId([userId].concat(sectionIdList));

  this.selected = true;
}

Schedule.generateId = function(idComponentList) {
  var userId = idComponentList.shift();
  idComponentList = idComponentList.map(function (id) {
    return parseInt(id);
  });
  idComponentList.sort(function(a, b) {
    return a - b;
  });
  idComponentList.unshift(userId);
  return idComponentList.join('.');
};

Schedule.normalizeId = function(id) {
  if (id === null) {
    return null;
  }
  return Schedule.generateId(id.split('.'));
};

Schedule.getUserIdFromId = function(id) {
  return id.split('.')[0];
};

Schedule.getSectionIdsFromId = function(id) {
  return id.split('.').slice(1).map(function(id) {
    return parseInt(id);
  });
};

module.exports = Schedule;