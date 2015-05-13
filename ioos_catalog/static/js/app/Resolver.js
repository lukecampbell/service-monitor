/*
 * ioos_catalog/static/js/app/Resolver.js
 */

var App = function() {
};

_.extend(App.prototype, {
  name: "Resolver",
  views: {
    resolverView: null,
    navbarView: null
  },
  collections: {},
  models: {
    resolverModel: null,
  },
  start: function() {
    var self = this;
    var url = window.location.href;
    var query = url.substring(url.lastIndexOf("/")+1, url.length);
    /* Views */
    this.views.navbarView = new NavbarView({
      el: $('#navbar-view')
    }).render();
    this.views.resolverView = new ResolverView({
      el: $('#resolver-view')
    });
    this.views.resolverView.render();
    /* Models */
    this.models.resolverModel = new ResolverModel();
    this.models.resolverModel.url = "/api/resolver/asset/" + query;
    
    var modelFetch = this.models.resolverModel.fetch({error: function() {
      $('#resolver-view').html("<h1>Not Found</h1>");
    }});
    $.when(modelFetch).done(function() {
      var url = "/datasets/" + self.models.resolverModel.get('_id');
      window.location.href = url;
    });
  }
});

var app = new App();
