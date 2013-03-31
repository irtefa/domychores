$(document).ready(function($) {
    var TestView = Backbone.View.extend({
        el: $('#remove'),

        render: function() {
            console.log("Rendering now...");
            $(this.el).html("<span>Can you see me? That means Backbone works!</span>");
        }
    });

    var view = new TestView();
    view.render();
});