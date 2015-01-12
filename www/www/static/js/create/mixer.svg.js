// Create canvas element
var element = document.createElementNS("http://www.w3.org/2000/svg", "svg");
element.classList.add('drink');
document.getElementById('mixer').appendChild(element);

// Create snap element
var mixer = Snap(element);

var height = 400,
    width = 300,
    inset = 50,
    pad = 5;

// draw cup
var cup = mixer.g(
    mixer.rect(0, height - pad, width, pad), // bot
    mixer.rect(inset - pad, 0, pad, height), // left
    mixer.rect(width - inset, 0, pad, height) // right
);

var left = inset + pad,
    right = width - inset * 2 - pad * 2,
    span = height - pad * 2; // also the bottom

function draw_portion(begin, percent, color, title) {
    var bot = span - span * begin;
    var hei = span * percent;

    var back = mixer.rect(left, bot - hei, right, hei).attr({
        fill: color
    });

    var label = mixer.text(left + pad, bot - hei + pad * 2.5, title);

    var ingredient = mixer.group(back, label);

//    return mixer.g(back);
    return ingredient;
}
var x = draw_portion(0.00, 0.20, '#ff0000', 'first');
draw_portion(0.20, 0.20, '#00ff00', 'second');
draw_portion(0.40, 0.60, '#5959ff', 'third');
