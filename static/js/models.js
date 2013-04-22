window.Chore = Backbone.Model.extend({
    url: '/api/chores'
});

window.ChoreList = Backbone.Collection.extend({
    model: Chore,

    url: "/api/chores"
});