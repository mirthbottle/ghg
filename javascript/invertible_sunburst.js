// invertibleSunburst
function inSun(root, width, minsize) {
  var height = 800,
  width = width,
  minsize = minsize,
  radius = Math.min(width, height)*.4,
  color = d3.scale.category20c();
  
  var partition = d3.layout.partition()
      .sort(null)
      .size([2 * Math.PI, radius * radius])
      .value(function(d) { return d.size; });

  /* draw general arc */
  var arc = d3.svg.arc()
    .startAngle(function(d) { return d.x; })
    .endAngle(function(d) { return d.x + d.dx; })
    .innerRadius(function(d) { return Math.sqrt(d.y); })
    .outerRadius(function(d) { return Math.sqrt(d.y + d.dy); });
  
  var arc_copyxs = function(d1, d2){
    d1.x0 = d2.x0;
    d1.dx0 = d2.dx0;
    d1.x = d2.x;
    d1.dx = d2.dx;
    d1.size = d2.size;
    return d1;
  }

  /* tooltip functions */
  var tooltip = d3.select("body").append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden");

  var addTooltip = function(selection){
    selection
      .on("mouseover", function(d){
	return tooltip.style("visibility", "visible")
	  .text(d.size + " MtCO2e " + d.name);})
      .on("mousemove", function(){
	return tooltip.style("top", (event.pageY-10)+"px")
	  .style("left",(event.pageX + 20)+"px");})
      .on("mouseout", function(){
	return tooltip.style("visibility", "hidden");});
  }

  /* text functions */
  // how to rotate text
  var textrotate = function(d) {
    // Offset the angle by 90 deg since the '0' degree axis for arc is Y axis
    // while for text it is the X axis.
    
    // If we are rotating the text by more than 90 deg, then "flip" it.
    // This is why "text-anchor", "middle" is important, otherwise, this "flip" would
    // a little harder.
    var label_d = jQuery.extend({}, d);
    if (d.depth == 2){
      label_d.x = d.x + d.dx/10;
    }
    var thetaDeg = (180 / Math.PI * (arc.startAngle()(label_d) + arc.endAngle()(label_d)) / 2 - 90);
    return (thetaDeg > 90) ? thetaDeg - 180 : thetaDeg;
  }
  var textcentroid = function(d){
    var label_d = jQuery.extend({}, d);
    if (d.depth == 2){
      label_d.x = d.x + d.dx/10;
    }
    return arc.centroid(label_d);
  }
    
  var texttransform = function(d) { 
    return "translate(" + textcentroid(d)  + ")" + "rotate(" + textrotate(d) + ")" ; 
  }
  
  var textwrite = function(d){
    var text = d.size>minsize ? d.name: "";
    if (d.depth == 2 && that.view == 2){
      text = "";
    }
    return text;
  }
  var textdraw = function(selection){
    selection
      .text(textwrite)
      .attr("text-anchor", "middle")
      .style("font-size", function(d) { return (12/d.depth+6)+"px"; })
      .style("fill", "#444");
  }   // end of text functions

  var style_newsib_paths = function(selection){
    selection
      .transition()
      .delay(5000)
      .attrTween("d", arcTween)
      .style("stroke", "#fff")
      .style("fill", function(d) {
	var name = d.name.charAt(0).toUpperCase() + d.name.slice(1);
	return color(name); });
  }

  var style_newsib_texts = function(selection){
    selection
      .attr("opacity", 0.1)
      .transition()
      .duration(5000)
      .attr("opacity", 1)
      .attrTween("transform",textTween);
  }

  var style_newrent_paths = function(selection){
    selection
      .style("stroke", "#fff")
      .style("fill", function(d) {
	var name = d.name.charAt(0).toUpperCase() + d.name.slice(1);
	return color(name); })
      .transition()
      .duration(5000)
      .attrTween("d", arcTween);
  }
  
  var style_newrent_texts = function(selection){
    selection
      .attr("opacity", 0.1)
      .transition()
      .duration(5000)
      .attr("opacity", 1)
      .attrTween("transform",textTween)
      .call(textdraw);
  }

  var invertPartition = function(p) {
    var new_siblings = [];
    var new_parents = [];
    var names = [];
    var maxxs = [];
    var new_sibling_sizes = [];
    var offsets = [];
    p.forEach(function(d){
      // if node is in the second ring, save the unique names in names
      // add up sizes of the nodes with that name in maxxs
      if (d.depth == 2){
	var i = names.indexOf(d.name);
	if (i == -1) {
	  var sibling = jQuery.extend({}, d);
	  sibling.dx1 = 0;
	  new_siblings.push(sibling);
	  names.push(d.name);
	  maxxs.push(d.dx);  // the end of the first one
	  new_sibling_sizes.push(d.size);
	  d.x = 0;
	}
	// if it's not the first node with that name
	else {
	  d.x = maxxs[i];  // set the start of the node
	  maxxs[i] += d.dx; // increment maxxs[i]
	  new_sibling_sizes[i] += d.size;
	}
      }
    });
    
    // set the offsets (x position) of the first node of each name
    var c = 0;    
    for(var j=0; j<maxxs.length; j++){
      offsets[j] = c;
      new_siblings[j].x = c;
      new_siblings[j].dx = maxxs[j];
      new_siblings[j].size = new_sibling_sizes[j];
      c += maxxs[j];
    }
    
    p.forEach(function(d){
      if (d.depth == 2){
	// put the nodes in the first ring in the right places
	var i = names.indexOf(d.name);
	d.x += offsets[i];
	if (i == 0) {
	  // change the parent to be the same as the child
	  d.parent = arc_copyxs(d.parent, d);
	}
	else {
	  // make new parent nodes
	  // actually x0 and dx0 should be set as the sibling, not the parent
	  var parent = jQuery.extend({}, d.parent);
	  parent.children = [d];
	  parent = arc_copyxs(parent, d);
	  parent.x1 = parent.x0;
	  parent.dx1 = parent.dx0;
	  new_parents.push(parent);
	}
      }
      else if (d.depth == 3){
	// put the nodes in the third ring in the right places
	var change = d.parent.x0 - d.parent.x;
	d.x = d.x - change;
      }
    });
    return [p, new_siblings, new_parents];
  }

  // switch contents of x1 and x
  // x0 = x
  var revertPartition = function(p){
    p.forEach(function(d){
      d.x = d.x1;
      d.dx = d.dx1;
      d.x1 = d.x0;
      d.dx1 = d.dx0;
    });
    return p; 
  }
  // arc colors for view 1
  var colorArc = function(d) {
    var name = d.parent ? d.parent.name : "";
    if (name != ""){
      name = d.parent.parent ? "" : d.name;
      if (name == "") {
	name = d.parent.parent.parent ? d.parent.parent.name : d.parent.name;
      }
    }
    return color(name); 
  }
  
  // Stash the old values for transition.
  var stash = function(d) {
    d.x1 = d.x;
    d.dx1 = d.dx;
    d.x0 = d.x;
    d.dx0 = d.dx;
  }
  
  // Interpolate the arcs in data space.
  var arcTween = function(a) {
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
  var textTween = function(a){
    var j = d3.interpolate({x: a.x0, dx: a.dx0}, a);
    // .attr("transform", function(d) { return "translate(" + arc.centroid(d)  + ")" + "rotate(" + rotateText(d) + ")" ; })
    return function(t) {
      var b = j(t);
      a.x0 = b.x;
      a.dx0 = b.dx;
      return "translate(" + textcentroid(b)  + ")" + "rotate(" + textrotate(b) + ")" ;
    }
  }

  var that = {
    new_siblings: [],
    ghgs: root,
    animated: false,
    view: 1 }

  that.draw = function() {    
    /* draw chart */
    that.view = 1;
    var svg = d3.select("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height * .5 + ")");

    var gpaths = svg.append("g").attr("id", "gpaths");
    var gtexts = svg.append("g").attr("id", "gtext");

    that.path = gpaths.selectAll("path").data(partition.nodes(root));
    that.path.enter().append("path")
      .attr("display", function(d) { return d.depth ? null : "none"; }) // hide inner ring
      .attr("d", arc)
      .style("stroke", "#fff")
      .style("fill", colorArc)
      .style("fill-rule", "evenodd")
      .call(addTooltip)
      .each(stash);

    that.text = gtexts.selectAll("text").data(partition.nodes(root));
    that.text.enter().append("text")
      .attr("transform", texttransform)
      .call(textdraw);

    // make empty group containers for new siblings and new paths for view 2
    that.gnewsib_paths = gpaths.append("g").attr("id", "gnsibpaths");
    that.gnewrent_paths = gpaths.append("g").attr("id", "gnrentpaths");
    that.gnewsib_texts = gtexts.append("g").attr("id", "gnsibtexts");
    that.gnewrent_texts = gtexts.append("g").attr("id", "gnrenttexts");

  } // end of that.draw()
  
  that.change = function() {
    if (that.animated == false) {
      // draw view2 the first time
      that.view = 2;
      that.animated = true;
      var ip = invertPartition(that.path.data());
      that.existing_data = ip[0];
      that.new_siblings = ip[1];
      that.new_parents = ip[2];
      // handle the existing data, new siblings, and new parents separately

      that.path.data(that.existing_data)
	.call(addTooltip)
	.transition()
	.duration(5000)
	.attrTween("d", arcTween)
	.style("fill", function(d) { 
	  // new colors for depth 2 arcs
	  var name = d.name.charAt(0).toUpperCase() + d.name.slice(1);
	  return color(name); });

      that.text.data(that.existing_data)
	.transition()
	.duration(5000)
	.attrTween("transform",textTween)
	.text(textwrite);
      
      // new parent paths
      that.gnewrent_paths.selectAll("path").data(that.new_parents).enter().append("path")
	.call(addTooltip)
      	.call(style_newrent_paths);

      // new parent texts
      that.gnewrent_texts.selectAll("text").data(that.new_parents).enter().append("text")
	.call(style_newrent_texts);

      // new sibling paths
      that.gnewsib_paths.selectAll("path").data(that.new_siblings).enter().append("path")
	.call(addTooltip)
	.call(style_newsib_paths);
	
      // new sibling texts
      that.gnewsib_texts.selectAll("text").data(that.new_siblings).enter().append("text")
	.call(style_newsib_texts)
	.call(textdraw)
	.text(function(d){ return d.size>minsize ? d.name: ""; });
    }
    else {
      that.existing_data = revertPartition(that.existing_data);
      that.new_siblings = revertPartition(that.new_siblings);
      that.new_parents = revertPartition(that.new_parents);
      
      that.path.data(that.existing_data)
	.call(addTooltip)
	.transition()
	.duration(5000)
	.attrTween("d", arcTween);

      if (that.view == 2) {
	// transition back to view 1
	that.view = 1;

	// new parent paths should move back
	that.gnewrent_paths.selectAll("path").data(that.new_parents)
	  .transition()
	  .duration(5000)
	  .attrTween("d", arcTween)
	  .remove();
	
	// new parent texts should move back and then disappear
	that.gnewrent_texts.selectAll("text")
	  .transition()
	  .duration(5000)
	  .attrTween("transform",textTween)
	  .remove();

	that.gnewsib_paths.selectAll("path")
	  .remove();
	
	that.gnewsib_texts.selectAll("text")
	  .remove();
      }
      else {
	// transition to view 2
	that.view = 2; 
	that.gnewsib_paths.selectAll("path").data(that.new_siblings).enter().append("path")
	  .call(addTooltip)
	  .call(style_newsib_paths);
	
	that.gnewsib_texts.selectAll("text").data(that.new_siblings).enter().append("text")
	  .call(style_newsib_texts)
	  .call(textdraw)
	  .text(function(d){ return d.size>minsize ? d.name: ""; });
	
	// add new parent paths again
	that.gnewrent_paths.selectAll("path").data(that.new_parents).enter().append("path")
	  .call(addTooltip)
      	  .call(style_newrent_paths);
	
	// add new parent text again
	that.gnewrent_texts.selectAll("text").data(that.new_parents).enter().append("text")
	  .call(style_newrent_texts);
	
      }
      // redraw text
      that.text.data(that.existing_data)
	.transition()
	.duration(5000)
	.attrTween("transform",textTween)
	.call(textdraw);
    }     
  } // end of change function

  return that;
}


function selectFile(dataset){
  
  if (dataset == "source"){
    var file = "demo_emissions.json";
    var minsize = 300;
  }
  else{
    var file = "demo_enduse.json";
    var minsize = 70;
  }
  return [file, minsize];
}
