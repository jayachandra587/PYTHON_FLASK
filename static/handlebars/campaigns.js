(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['campaigns'] = template({"1":function(container,depth0,helpers,partials,data) {
    var alias1=container.lambda, alias2=container.escapeExpression;

  return "        <tr>\n            <td>"
    + alias2(alias1((depth0 != null ? depth0.name : depth0), depth0))
    + "</td>\n            <td>"
    + alias2(alias1((depth0 != null ? depth0.today_spend : depth0), depth0))
    + "</td>\n            <td>"
    + alias2(alias1((depth0 != null ? depth0.wins : depth0), depth0))
    + "</td>\n            <td>"
    + alias2(alias1((depth0 != null ? depth0.inbounds : depth0), depth0))
    + "</td>\n            <td>"
    + alias2(alias1((depth0 != null ? depth0.ad_ctr : depth0), depth0))
    + "</td>\n            <td>"
    + alias2(alias1((depth0 != null ? depth0.conversions : depth0), depth0))
    + "</td>\n            <td>"
    + alias2(alias1((depth0 != null ? depth0.conversion_rate : depth0), depth0))
    + "</td>\n            <td>"
    + alias2(alias1((depth0 != null ? depth0.cpa : depth0), depth0))
    + "</td>\n        </tr>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, helper, alias1=depth0 != null ? depth0 : (container.nullContext || {});

  return "<h4> "
    + container.escapeExpression(((helper = (helper = helpers.region || (depth0 != null ? depth0.region : depth0)) != null ? helper : helpers.helperMissing),(typeof helper === "function" ? helper.call(alias1,{"name":"region","hash":{},"data":data}) : helper)))
    + " </h4>\n<table class=\"table\">\n<thead>\n  <tr>\n      <th>Campaign Name</th>\n      <th> Spend </th>\n      <th> Wins </th>\n      <th> Inbounds </th>\n      <th> AdCTR </th>\n      <th> Conversions </th>\n      <th> Conversion Rate </th>\n      <th> CPA </th>\n  </tr>\n</thead>\n\n<tbody>\n"
    + ((stack1 = helpers.each.call(alias1,(depth0 != null ? depth0.campaigns : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "</tbody>\n</table>";
},"useData":true});
})();