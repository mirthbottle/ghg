var ghgs;
var newdata;
var olddata;
function invertibleSunburst(root) {
  ghgs = root;

  var width = 800,
  height = 800,
  radius = Math.min(width, height)*.4,
  color = d3.scale.category20c(),
  minsize = 300,
  animated = false;
  
  var partition = d3.layout.partition()
    .sort(null)
    .size([2 * Math.PI, radius * radius])
    .value(function(d) { return d.size; });

  /* draw arc functions */
  var arc = d3.svg.arc()
    .startAngle(function(d) { return d.x; })
    .endAngle(function(d) { return d.x + d.dx; })
    .innerRadius(function(d) { return Math.sqrt(d.y); })
    .outerRadius(function(d) { return Math.sqrt(d.y + d.dy); });

  colorArc = function(d) {
    var name = d.parent ? d.parent.name : "";
    if (name != ""){
      name = d.parent.parent ? "" : d.name;
      if (name == "") {
	name = d.parent.parent.parent ? d.parent.parent.name : d.parent.name;
      }
    }
    return color(name); 
  }

  /* tooltip functions */
  var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden");

  function addTooltip(selection){
    selection
      .on("mouseover", function(d){return tooltip.style("visibility", "visible").text(d.size + " MtCO2e " + d.name);})
      .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX + 20)+"px");})
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");});
  }

  /* text functions */
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


  function textCentroid(d){
    var label_d = jQuery.extend({}, d);
    if (d.depth == 2){
      label_d.x = d.x + d.dx/10;
    }
    return arc.centroid(label_d);
  }
  transformText = function(d) { 
    return "translate(" + textCentroid(d)  + ")" + "rotate(" + rotateText(d) + ")" ; 
  }
  function drawText(selection){
    selection
      .attr("text-anchor", "middle")
      .style("font-size", function(d) { return (12/d.depth+6)+"px"; })
      .style("fill", "#444")
      .text(function(d) { return d.size>300 ? d.name: ""; });
  }  

  /* draw chart */
  var svg = d3.select("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height * .5 + ")");

  var g = svg.datum(root).selectAll("path")
    .data(partition.nodes);

  var path = g.enter().append("path")
    .attr("display", function(d) { return d.depth ? null : "none"; }) // hide inner ring
    .attr("d", arc)
    .style("stroke", "#fff")
    .style("fill", colorArc)
    .style("fill-rule", "evenodd")
    .call(addTooltip)
    .each(stash);

  var text = g.enter().append("text")
    .attr("transform", transformText)
    .call(drawText);

  olddata = path.data();
  d3.selectAll("#animate1, #animate2").on("click", function change() {
    if (animated == false) {
      animated = true;
      newdata = invertPartition(path.data());
    }
    else {
      newdata = revertPartition(path.data());
    }
      
    path.data(newdata).enter().append("path").attr("opacity", 0)
      .call(addTooltip)
      .transition()
      .duration(5000)
      .attrTween("d", arcTween)
      .style("stroke", "#fff")
      .style("fill", function(d) {
	var name = d.name.charAt(0).toUpperCase() + d.name.slice(1);
	return color(name); })
      .attr("opacity", 1);
    
    path
      .transition()
      .duration(5000)
      .attrTween("d", arcTween)
      .style("fill", function(d) {
	var name = d.name.charAt(0).toUpperCase() + d.name.slice(1);
	return color(name); });
    
    text.data(newdata).enter().append("text").attr("opacity", 0.1)
      .transition()
      .duration(5000)
      .attr("opacity", 1)
      .attrTween("transform",textTween)
      .call(drawText);

    text
      .transition()
      .duration(5000)
      .attrTween("transform",textTween);
  });
  
  // Stash the old values for transition.
  function stash(d) {
    d.x1 = d.x;
    d.dx1 = d.dx;
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

  // Interpolate the text so it matches the arcs
  // attribute to edit is transform
  // compute intermediate arc.centroid(d) and rotateText(d)
  function textTween(a){
    var j = d3.interpolate({x: a.x0, dx: a.dx0}, a);
    // .attr("transform", function(d) { return "translate(" + arc.centroid(d)  + ")" + "rotate(" + rotateText(d) + ")" ; })
    return function(t) {
      var b = j(t);
      a.x0 = b.x;
      a.dx0 = b.dx;
      return "translate(" + textCentroid(b)  + ")" + "rotate(" + rotateText(b) + ")" ;
    }
  }

}


function invertPartition(p) {
  var new_parents = [];
  var names = [];
  var maxxs = [];
  var offsets = [];
  p.forEach(function(d){
    if (d.depth == 2){
      var i = names.indexOf(d.name);
      if (i == -1) {
	names.push(d.name);
	maxxs.push(d.dx);  // the end of the first one
	d.x = 0;
      }
      else {
	d.x = maxxs[i];  // where the next one should be set to
	maxxs[i] += d.dx; // increment maxx
      }
    }
  });
  
  var c = 0;    
  for(var j=0; j<maxxs.length; j++){
    offsets[j] = c;
      c += maxxs[j];
  }
  
  p.forEach(function(d){
    if (d.depth == 2){
      var i = names.indexOf(d.name);
      d.x += offsets[i];
      if (i == 0) {
	// change the parent to be the same as the child
	d.parent.x = d.x;
	d.parent.dx = d.dx;
	d.parent.size = d.size;
      }
      else {
	// make new parent nodes
	var parent = jQuery.extend({}, d.parent);
	parent.x0 = d.parent.x + d.parent.dx;
	parent.dx0 = 0;
	parent.x = d.x;
	parent.dx = d.dx;
	parent.size = d.size;
	parent.children = [d];
	new_parents.push(parent);
      }
    }
    else if (d.depth == 3){
      // child of energy category
      var change = d.parent.x0 - d.parent.x;
      d.x = d.x - change;
    }
  });
  p = p.concat(new_parents);
  return p;
}
function select_file(view){
  
  if (view == "source"){
    var file = "demo_emissions.json";
    var minsize = 300;
  }
  else{
    var file = "demo_enduse.json";
    var minsize = 70;
  }
  return [file, minsize];
}

// switch contents of x1 and x
// x0 = x
function revertPartition(p){
  p.forEach(function(d){
    d.x = d.x1;
    d.dx = d.dx1;
    d.x1 = d.x0;
    d.dx1 = d.dx0;
  });
  return p; 
}
