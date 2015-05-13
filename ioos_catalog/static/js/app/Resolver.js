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
  models: {},
  start: function() {

    var url = window.location.href;
    var query = url.substring(url.lastIndexOf("/")+1, url.length);
    console.log(query);
    /* Views */
    this.views.navbarView = new NavbarView({
      el: $('#navbar-view')
    }).render();
    this.views.resolverView = new ResolverView({
      el: $('#resolver-view')
    });
    this.views.resolverView.render();
    console.log("Resolver started");
  }
});

var app = new App();
