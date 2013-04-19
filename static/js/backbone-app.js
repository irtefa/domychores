$(function() {
    window.Chore = Backbone.Model.extend({
        defaults: {
            "test": "this is a test"
        }
    });

    window.ChoreList = Backbone.Collection.extend({
        model: Chore,

        url: "/api/chores"
    });

    window.Chores = new ChoreList();

    window.ChoreView = Backbone.View.extend({
        tagName: "li",

        template: _.template($("#chore-template").html()),

        initialize: function() {
            this.listenTo(this.model, "change", this.render);
            this.model.view = this;
        },

        render: function() {
            $(this.el).html(this.template(this.model.toJSON()));
            var task = this.model.get('task');
            this.$('.chore-task').text(task);
            return this;
        }
    });

    window.AppView = Backbone.View.extend({
        el: $("#app"),

        initialize: function() {
            _.bindAll(this, "render");
            Chores.bind("all", this.render);
            Chores.fetch();
        },

        render: function() {
            Chores.each(this.addOne);
        },

        addOne: function(chore) {
            var view = new ChoreView({model: chore});
            this.$("#chore-list").append(view.render().el);
        }
    });

    window.App = new AppView();
});
