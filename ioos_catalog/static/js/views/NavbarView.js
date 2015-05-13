"use strict";
/*
 * ioos_catalog/static/js/views/NavbarView.js
 */

var NavbarView = Backbone.View.extend({
  links: {},
  providers: {},
  template: JST['ioos_catalog/static/js/partials/Navbar.html'],
  render: function() {
    var self = this;
    var getLinks = $.ajax({
      url: "/api/resolver/config.json",
      type: "GET",
      dataType: "json",
      success: function(response) {
        console.log("got config");
        _.extend(self.links, response);
      }
    });
    // This needs to be put in a model, but in the interest of time...
    // SORRY!!!!!!
    var getPartners = $.ajax({
      url: "/api/providers",
      type: "GET",
      dataType: "json",
      success: function(response) {
        console.log("got providers");
        self.links.ra_providers = response.ra_providers;
        self.links.national_partners = response.national_partners;
      }
    });

    $.when(getLinks, getPartners).done(function() {
      console.log(self.links);
      self.$el.html(self.template(self.links));
    });
    return this;
  }

});
