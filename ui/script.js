var top_plane, bot_plane;

function setup() {
  createCanvas(800, 800);
  top_plane = new Plane(4, 0.25);
  bot_plane = new Plane(19, 4);
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
  top_plane.update(0.001);
  // bot_plane.update(-0.005);

  // TODO: use a doubly linked list to make this interesting + more performant
  top_plane.reset();
  bot_plane.reset();
  for (var i = 0; i < bot_plane.targets.length; i++) {
    var cup = bot_plane.targets[i];
    for (var j = 0; j < top_plane.targets.length; j++) {
      var spout = top_plane.targets[j];
      if (intersects(cup.b + bot_plane.a, spout.b + top_plane.a, bot_plane.dia, top_plane.dia)) {
        cup.toggle(true);
        spout.toggle(true);
        break; // continue on next cup
      }
    }
  }

  bot_plane.show();
  top_plane.show();
}

function intersects(a, b, a_dia, b_dia) {
  // the denominator of 2 was removed as both the diameter -> radius and the scale factor needed it
  var dx = (cos(a) - cos(b)) * 25, // delta x
    dy = (sin(a) - sin(b)) * 25, // delta y
    dr = Math.min(a_dia - b_dia, b_dia - a_dia);

  return dx * dx + dy * dy < dr * dr;
}

function Plane(n, dia) {
  this.targets = [];
  for (var i = 0; i < n; i++) {
    this.targets.push(new Target(i * TAU / n));
  }
  this.a = 0; // angle of rotation
  this.dia = dia;

  this.show = function() {
    for (var i = 0; i < this.targets.length; i++) {
      this.targets[i].show(this.a, this.dia);
    }
  };

  this.update = function(dv) {
    this.a += dv;
  };
  this.reset = function() {
    for (var i = 0; i < this.targets.length; i++) {
      this.targets[i].toggle(false);
    }
  };
}

function Target(b) {
  this.b = b; // my angle relative to parent
  this.state = false;
  this.cap = 0; // max fill
  this.val = 0; // how full

  this.show = function(a, dia) { // a is parent's angle
    push();
    var angle = a + this.b;
    translate(cos(angle) * 25 / 2, sin(angle) * 25 / 2);
    fill(this.state ? color(0, 255, 0, 100) : color(255, 0, 0, 100))
    ellipse(0, 0, dia, dia);

    fill(0);
    textSize(Math.max(dia / 2, 1));
    textAlign(CENTER, CENTER);
    text(this.state ? "on" : "off", 0, 0);
    pop();
  };

  this.toggle = function(state) {
    this.state = state;
  };
}
