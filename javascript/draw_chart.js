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

var ghgs;
var path;
var svg;
function draw_chart(order) {
  svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height * .5 + ")");

  var file = "demo_emissions.json";

  d3.select(self.frameElement).style("height", height + "px");

  d3.json(file, function(error, root) { 
    if (error) return console.warn(error);
    ghgs = root;
    var tooltip = d3.select("body").append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden");
    
    var p = svg.datum(ghgs).selectAll("path")
      .data(partition.nodes);
    
    p.enter().append("path")
      .attr("display", function(d) { 
	return d.depth ? null : "none"; }) // hide inner ring
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
      .on("mouseover", function(d){return tooltip.style("visibility", "visible").text(d.size + " MtCO2e");})
      .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX + 20)+"px");})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
      .each(stash);

    p = addLabels(p);
  });
}

function addLabels(p){
  p.enter().append("text")
    .attr("transform", function(d) { return "translate(" + arc.centroid(d)  + ")" + "rotate(" + rotateText(d) + ")" ; })
    .attr("text-anchor", "middle")
    .style("font-size", function(d) { return (12/d.depth+6)+"px"; })
    .style("fill", "#444")
      .style("z-index", "2")
    .text(function(d) { return d.size>300 ? d.name: ""; });
  return p;
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
