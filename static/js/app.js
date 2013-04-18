window.App = Ember.Application.create({
    LOG_TRANSITIONS: true
});

DS.RESTAdapter.reopen({
  namespace: 'api'
});

App.Store = DS.Store.extend({
    revision: 12
});

App.Chore = DS.Model.extend({
    id: DS.attr('number'),
    task: DS.attr('string'),
    description: DS.attr('string'),
    ownerId: DS.attr('number'),
    workerId: DS.attr('number'),
    postedAt: DS.attr('date')
});

App.Router.map(function() {
    this.resource('chores', {path: 'chores'});
    this.route('about');
});

App.ChoresRoute = Ember.Route.extend({
    setupController: function(controller, model) {
        controller.set('content', model);
    },
    model: function() {
        return App.Chore.find();
    }
});



