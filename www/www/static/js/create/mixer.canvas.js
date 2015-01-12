// this is a work in progress

/* docs
http://stackoverflow.com/questions/9880279/how-do-i-add-a-simple-onclick-event-handler-to-a-canvas-element
http://www.w3schools.com/tags/ref_canvas.asp
http://www.w3schools.com/canvas/canvas_clock.asp
http://www.w3schools.com/html/html5_canvas.asp
*/

var canvas = function(options) {
    // Build default settings object
    var settings = {
        width: options.width || 300,
        height: options.height || 400,
        class: options.class || '',
        parent: options.parent || ''
    };

    // Create canvas element
    var c = document.createElement('canvas');
    c.width = settings.width;
    c.height = settings.height;
    c.classList.add(settings.class);
    document.getElementById(settings.parent).appendChild(c);

    // Clean events
    function clean_mouse_event(evt) {
        var offset = evt.target.getBoundingClientRect();
        return {
            target: evt.target,
            x: Math.round(evt.clientX - offset.left) + 1,
            y: Math.round(evt.clientY - offset.top)
        };
    }

    // Add mouse event
    function add_mouse_event(eventName) {
        c.addEventListener(eventName, function(e) {
            var evt = clean_mouse_event(e);
            listeners[eventName].forEach(function(handler) {
                handler(evt);
            });
        }, false);
    }

    // Supported events
    var events = [
        'click', 'mouseenter', 'mouseleave',
        'mousemove', 'mousedown', 'mouseup'
    ];

    // Generate listeners dict
    var listeners = {};
    for (var i = 0; i < events.length; i++) {
        listeners[events[i]] = [];
        add_mouse_event(events[i]);
    }

    // Initialize canvas context
    var ctx = c.getContext("2d");

    // allow binding to events
    ctx.bind = function (eventType, handler) {
        if (!(eventType in listeners)) throw Error('Event not supported');
        listeners[eventType].push(handler);
    };

    // allow unbinding to events
    ctx.unbind = function (eventType, handler) {
        if (!(eventType in listeners)) throw Error('Event not supported');
        var idx = listeners[eventType].indexOf(handler);
        if (idx > -1)
            delete listeners[eventType][idx]
    };

    // Append some settings
    ctx.height = settings.height;
    ctx.width = settings.width;

    return ctx;
};

var mixer = canvas({
    class: 'drink',
    parent: 'mixer'
});

// Debugging methods
mixer.bind('click', function(e) { console.log('click', e); });
mixer.bind('mouseenter', function(e) { console.log('mouseenter', e); });
mixer.bind('mouseleave', function(e) { console.log('mouseleave', e); });
mixer.bind('mousemove', function(e) { console.log('mousemove', e); });
mixer.bind('mousedown', function(e) { console.log('mousedown', e); });
mixer.bind('mouseup', function(e) { console.log('mouseup', e); });

var canvas_shaper = function(canvas) {
    var elements = [];

    canvas.append = function(element) {
        elements.push(element);
    };

    canvas.remove = function(element) {
        var idx = elements.indexOf(element);
        if (idx > -1) delete elements[idx];
    };

    canvas.clear = function() {
        mixer.clearRect(0, 0, canvas.width, canvas.height);
    };

    return canvas;
};

//    ctx.translate(c.width / 2, c.height / 2);
//    function draw_cup() {
//        ctx.fillStyle = "#000000";
//        ctx.fillRect(-130, 190, 260, 5);
//        ctx.fillRect(-100, -195, 5, 385);
//        ctx.fillRect(100, -195, -5, 385);
//    }
//    draw_cup();
//
//    var start = 188, height = -385;
//
//    function draw_portion(begin, percent, color, title) {
//        ctx.font = '10px Helvetica';
//        var total_text = '' + (Math.round(percent * 10000) / 100) + '%';
//        var title_width = ctx.measureText(title).width + 10;
//        var total_width = ctx.measureText(total_text).width + 10;
//        var bot = start + height * begin - 2.5;
//        var hei = percent * height + 5;
//        var txt_bot = Math.floor(bot + hei + 15);
//
//        // draw overall box
//        ctx.fillStyle = color;
//        ctx.fillRect(-90, Math.floor(bot), 180, Math.ceil(hei));
//
//        // draw clearing boxes
//        ctx.fillStyle = '#ffffff';
//        ctx.fillRect(-85, txt_bot + 4, title_width, -14);
//        ctx.fillRect(85 - total_width, txt_bot + 4, total_width, -14);
//
//        // draw box border
//        ctx.fillStyle = '#000000';
//        ctx.strokeRect(-85, txt_bot + 4, title_width, -14);
//        ctx.strokeRect(85 - total_width, txt_bot + 4, total_width, -14);
//
//        // draw text
//        ctx.fillText(title, -80, txt_bot);
//        ctx.fillText(total_text, 90 - total_width, txt_bot);
//    }
//    draw_portion(0.00, 0.20, '#ff0000', 'first');
//    draw_portion(0.20, 0.20, '#00ff00', 'second');
//    draw_portion(0.40, 0.60, '#0000ff', 'third');
