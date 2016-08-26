var BaseCtrl = require('./_base.controller');

ScheduleViewAndSelectCtrl.prototype = Object.create(BaseCtrl.prototype);
function ScheduleViewAndSelectCtrl($state, $window, $stateParams, scheduleFactory, $analytics) {
  $analytics.pageTrack('/schedule/{}'.replace('{}', $stateParams.scheduleId));

  BaseCtrl.call(this, $state, $window);

  var vm = this;

  var scheduleId = $stateParams.scheduleId;

  vm.selectedSchedule = null;

  if (scheduleId) {
    vm.selectedSchedule = scheduleFactory.setCurrentScheduleById($stateParams.scheduleId);
  }

  if (vm.selectedSchedule === null) {
    vm.goToState('schedule.generatingSchedules', {startScheduleId: scheduleId});
  }
}
angular.module('berkeleyScheduler').controller('ScheduleViewAndSelectCtrl', [
  '$state',
  '$window',
  '$stateParams',
  'scheduleFactory',
  '$analytics',
  ScheduleViewAndSelectCtrl
]);