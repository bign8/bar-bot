var top_plane, bot_plane, out = document.getElementById('state');

function setup() {
  createCanvas(800, 800);
  top_plane = new Plane("t", 9, 0.25);
  bot_plane = new Plane("b", 19, 4);
}

function draw() {
  clear();
  noFill();
  translate(width / 2, height / 2);
  scale(20);
  strokeWeight(0.1);

  // ellipse(0, 0, 25, 25);
  ellipse(0, 0, 20, 20);
  ellipse(0, 0, 30, 30);
  top_plane.a += 0.001; // update rotation angle
  // bot_plane.a -= 0.0005;

  // TODO: use a doubly linked list to make this interesting + more performant
  // TODO: convert to discrete events for distrete event simulation planning
  reset(top_plane.targets); reset(bot_plane.targets);
  for (var i = 0; i < bot_plane.targets.length; i++) {
    var cup = bot_plane.targets[i];
    for (var j = 0; j < top_plane.targets.length; j++) {
      var spout = top_plane.targets[j];
      if (intersects(cup.b + bot_plane.a, spout.b + top_plane.a, bot_plane.dia, top_plane.dia)) {
        cup.state = true;
        spout.state = true;
        break; // continue on next cup
      }
    }
  }

  out.innerHTML = bot_plane.show() + "\n" + top_plane.show();
}

function intersects(a, b, a_dia, b_dia) {
  // the denominator of 2 was removed as both the diameter -> radius and the scale factor needed it
  var dx = (cos(a) - cos(b)) * 25, // delta x
    dy = (sin(a) - sin(b)) * 25, // delta y
    dr = Math.min(a_dia - b_dia, b_dia - a_dia);

  return dx * dx + dy * dy < dr * dr;
}

function reset(list) {
  for (var i = 0; i < list.length; i++) {
    list[i].old = list[i].state;
    list[i].state = false;
  }
}

function Plane(name, n, dia) {
  this.targets = [];
  for (var i = 0; i < n; i++) {
    this.targets.push(new Target(name + i, i * TAU / n));
  }
  this.a = 0; // angle of rotation
  this.dia = dia;
}

function Target(id, b) {
  this.id = id; // node identifier
  this.b = b; // my angle relative to parent
  this.state = false; // is it possible to be poured into
  this.old = false; // what the previous state of this object is
  this.cap = 0; // max fill
  this.val = 0; // how full
}

// ------------------- render -------------------

Plane.prototype.show = function() {
  var out = "";
  for (var i = 0; i < this.targets.length; i++) {
    this.targets[i].show(this.a, this.dia);
    out += (this.targets[i].state ? "1" : "0") + " ";
  }
  return out;
};

Target.prototype.show = function(a, dia) { // a is parent's angle
  push();
  var angle = a + this.b;
  translate(cos(angle) * 25 / 2, sin(angle) * 25 / 2);
  fill(this.state ? color(0, 255, 0, 100) : color(255, 0, 0, 100))
  ellipse(0, 0, dia, dia);

  fill(0);
  textSize(1);
  textAlign(CENTER, CENTER);
  text(this.id + "\n" + (this.state ? "on" : "off"), 0, 0);
  pop();

  // if (this.state != this.old) console.log(this.id, "changing from", this.old, "to", this.state);
};
