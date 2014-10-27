var width = 800,
    height = 800,
    radius = Math.min(width, height)*.4,
    color = d3.scale.category20c();

var partition = d3.layout.partition()
    .sort(null)
    .size([2 * Math.PI, radius * radius])
    .value(function(d) { return d.size; });

var arc = d3.svg.arc()
    .startAngle(function(d) { return d.x; })
    .endAngle(function(d) { return d.x + d.dx; })
    .innerRadius(function(d) { return Math.sqrt(d.y); })
    .outerRadius(function(d) { return Math.sqrt(d.y + d.dy); });


function collect_children() {
  var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height * .5 + ")");

  d3.select(self.frameElement).style("height", height + "px");

  var file = "demo_emissions.json";

  d3.json(file, function(error, root) {
    var tooltip = d3.select("body")
      .append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden");
    
    var g = svg.datum(root).selectAll("path")
      .data(partition.nodes)
      .enter().append("g");
    
    var path = g.append("path")
      .attr("display", function(d) { return d.depth ? null : "none"; }) // hide inner ring
      .attr("d", arc)
      .style("stroke", "#fff")
      .style("fill", function(d) {
	var name = d.parent ? d.parent.name : "";
	if (name != ""){
	  name = d.parent.parent ? "" : d.name;
	  if (name == "") {
	    name = d.parent.parent.parent ? d.parent.parent.name : d.parent.name;
	  }
	}
	return color(name); })
      .style("fill-rule", "evenodd")
      .each(stash);

    var text = g.append("text")
      .attr("transform", function(d) { return "translate(" + arc.centroid(d)  + ")" + "rotate(" + rotateText(d) + ")" ; })
      .attr("text-anchor", "middle")
      .style("font-size", function(d) { return (12/d.depth+6)+"px"; })
      .style("fill", "#444")
      .text(function(d) { return d.size>300 ? d.name: ""; });
    
    d3.selectAll("button").on("click", function change() {
      d3.selectAll("text").remove();
      var newdata = modPartition(path.data());

      path.data(newdata)
	.transition()
	.duration(1500)
	.attrTween("d", arcTween);
    });
    
  });
}

// how to rotate text
function rotateText(d) {
  // Offset the angle by 90 deg since the '0' degree axis for arc is Y axis, while
  // for text it is the X axis.
  var thetaDeg = (180 / Math.PI * (arc.startAngle()(d) + arc.endAngle()(d)) / 2 - 90);
  // If we are rotating the text by more than 90 deg, then "flip" it.
  // This is why "text-anchor", "middle" is important, otherwise, this "flip" would
  // a little harder.
  return (thetaDeg > 90) ? thetaDeg - 180 : thetaDeg;
}

// Stash the old values for transition.
function stash(d) {
  d.x0 = d.x;
  d.dx0 = d.dx;
}

// Interpolate the arcs in data space.
function arcTween(a) {
  var i = d3.interpolate({x: a.x0, dx: a.dx0}, a);
  return function(t) {
    var b = i(t);
    a.x0 = b.x;
    a.dx0 = b.dx;
    return arc(b);
  };
}

function modPartition(p) {
  p.forEach(function(d){
    d.x = d.x + 1;
  });
  return p;
}

