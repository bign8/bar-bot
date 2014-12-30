//
//  plane.cpp
//  barBotPLC_GUI
//
//  Created by Nate Woods on 12/28/14.
//
//

#include "ofApp.h"
#include "plane.h"

//int items;

Plane::Plane(float angle) {
    this->angle = angle;
    this->targets = new std::vector<Target>();
};

void Plane::draw(float c_x, float c_y, float radius) {
    ofNoFill();
    ofSetColor(color);
    ofCircle(c_x, c_y, radius);
    
    float x = cos(this->angle);
    float y = sin(this->angle);
    ofLine(c_x, c_y, c_x + x * radius / 3, c_y + y * radius / 3);
    
    for (std::vector<Target>::iterator it = targets->begin(); it != targets->end(); ++it) {
        it->draw(c_x, c_y, radius * .75);
    }
};

void Plane::update() {
    this->angle = ofWrapRadians(this->angle);
    for (std::vector<Target>::iterator it = targets->begin(); it != targets->end(); ++it) {
        it->update();
    }
};
