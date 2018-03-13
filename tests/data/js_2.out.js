/*
 * This file is part of Invenio.
 * Copyright (C) 2015-2018 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */
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
