window.Chores = new ChoreList();

window.ChoreView = Backbone.View.extend({
    tagName: "p",
    // the template in our index where we are going to render our chores
    template: _.template($("#chore-template").html()),
    // events that will interact with the backend server
    events: {
        "click .accept":    "accept",
        "click .complete": "payUser"
    },
    // event to pay a user once he completed a chore
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
        });
   },
   // event to accept a task and credit the owner of the task
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
        // upon this ajax post request the chore and the owner gets credited
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
        var id = $('#user-id').html();
        this.$el.html(this.template(this.model.toJSON()));
        this.$el.find('.timeago').timeago();
        var owner_id = this.$el.find('#owner_id').html();
        // hides accept button if this is your chore
        if(id === owner_id) {
            this.$el.find('.accept').addClass("hidden");
        }
        // hides completed button if you are not the owner of that chore
        if(id != owner_id) {
            this.$el.find('.complete').addClass("hidden");
        }
        return this;
    }
});

window.AppView = Backbone.View.extend({
    el: $("#main"),
    // binds all events to the render action of the view
    initialize: function() {
        _.bindAll(this, "render");
        Chores.bind("all", this.render);
        Chores.fetch();
    },
    render: function() {
        Chores.each(this.addOne);
    },
    // adds each chore to the chores view
    addOne: function(chore) {
        var view = new ChoreView({model: chore});
        this.$("#chore-list").append(view.render().el);
    }
});

window.App = new AppView();
