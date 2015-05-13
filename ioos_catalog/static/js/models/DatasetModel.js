"use strict";
/*
 * ioos_catalog/static/js/models/DatasetModel.js
 */

var DatasetModel = Backbone.Model.extend({
  urlRoot: "/api/dataset",
  idAttribute: "_id",
  defaults: {
    "updated": null,
    "uid": "",
    "created": null,
    "active": null,
    "services":[],
  },
  parse: function(response) {
    if(response && response.updated) {
      response.updated = new Date(response.updated.$date * 1000);
    }
    if(response && response.created) {
      response.created = new Date(response.created.$date * 1000);
    }

    if(response) {
      response._id = response._id.$oid;
    }
    return response;
  }
});


