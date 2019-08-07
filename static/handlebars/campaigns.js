(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['campaigns'] = template({"1":function(container,depth0,helpers,partials,data) {
    var alias1=container.lambda, alias2=container.escapeExpression;

  return "            <tr>\n                <td>"
    + alias2(alias1((depth0 != null ? depth0.name : depth0), depth0))
    + "</td>\n                <td>"
    + alias2(alias1((depth0 != null ? depth0.wins : depth0), depth0))
    + "</td>\n                <td>"
    + alias2(alias1((depth0 != null ? depth0.spend : depth0), depth0))
    + "</td>\n            </tr>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return "<div class=\"container\">\n  <h2> RTB Portal </h2>\n  <p> Realtime performance monitoring for RTB </p>\n  <table class=\"table\">\n    <thead>\n      <tr>\n        <th>Campaign Name</th>\n        <th> Wins </th>\n        <th> Spend </th>\n      </tr>\n    </thead>\n\n    <tbody>\n"
    + ((stack1 = helpers.each.call(depth0 != null ? depth0 : (container.nullContext || {}),(depth0 != null ? depth0.campaigns : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "    </tbody>\n  </table>\n</div>";
},"useData":true});
})();