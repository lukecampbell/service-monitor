"use strict";
/*
 * ioos_catalog/static/js/views/ResolverView.js
 */


var ResolverView = Backbone.View.extend({
  template: JST['ioos_catalog/static/js/partials/Resolver.html'],
  render: function() {
    this.$el.html(this.template());
    return this;
  }
});
