/*
 * Some other header comment which is not a license
 * More text here
 */

/**
  * @ngdoc controller
  * @name invenioSearchCtrl
  * @namespace invenioSearchCtrl
  * @description
  *    Invenio search controller.
  */
function invenioSearchCtrl($scope, invenioSearchHandler,
  invenioSearchAPI) {

  // Assign controller to `vm`
  var vm = this;

/*
 * More stuff was here
 */

angular.module('invenioSearch.controllers')
  .controller('invenioSearchCtrl', invenioSearchCtrl);
