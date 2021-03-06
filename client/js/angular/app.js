(function() {
  'use strict';

  angular.module('berkeleyScheduler', [
      'ui.router',
      // 'ngAnimate',
      'ngSanitize',
      'ngCookies',
      'ngMaterial',
      'angulartics',
      'angulartics.google.analytics',
      'contenteditable',
      'LocalStorageModule'
  ]);

  // Configuration
  require('./config');

  // Factories
  require('./courseDiscovery.service');
  require('./finals.service');
  require('./reverseLookup.service');
  require('./schedule.factory');

  // Services
  require('./user.service');
  require('./course.service');
  require('./event.service');
  require('./savedSchedule.service');
  require('./schedulingOptions.service');
  require('./timeSpent.service');

  // Filters
  require('./reverse.filter');

  // Controllers
  require('./_base.controller');
  require('./confirmEventDeleteDialog.controller');
  require('./courseFind.controller');
  require('./exportToCalendarDialog.controller');
  require('./generatingSchedules.controller');
  require('./mobileUnoptimizedDialog.controller');
  require('./shareDialog.controller');
  require('./viewCourse.controller');
  require('./viewEvent.controller');
  require('./viewSchedule.controller');

  // Directives
  require('./termSelector.directive');
  require('./courseDisplay.directive');
  require('./eventDisplay.directive');
  require('./meetingEditor.directive');
  require('./timePicker.directive');
  require('./preferences.directive.js');
  require('./generateSchedules.directive');
  require('./scheduleDisplay.directive');

  // Run
  require('./run');
})();
