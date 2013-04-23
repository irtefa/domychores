window.Chores = new ChoreList();

window.ChoreView = Backbone.View.extend({
    tagName: "p",

    template: _.template($("#chore-template").html()),

    events: {
        "click .accept":    "accept",
        "click .complete": "payUser"
    },

    payUser: function() {
        $.ajax({
            url: '/api/pay/' + this.model.get('id'),
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    window.location.replace("/");
                }
                else {
                    console.log("could not pay worker");
                }
            }
        });    },

    accept: function() {
        $.ajax({
            url: '/api/chore/' + this.model.get('id'),
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    window.location.replace("/");
                }
            }
        });

        $.ajax({
            url: '/api/credit/' + this.model.get('id'),
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({"owner_id": this.model.get('owner_id')}),
            success: function(data) {
                if (data.success) {
                    window.location.replace("/");
                }
                else {
                    console.log("could not credit owner");
                }
            }
        });
    },

    initialize: function() {
        _.bindAll(this, "render");
        this.model.bind('change', this.render);
    },

    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.find('.timeago').timeago();
        return this;
    }
});

window.AppView = Backbone.View.extend({
    el: $("#main"),

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
