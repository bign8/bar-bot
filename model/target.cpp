//
//  target.cpp
//  barBotPLC_GUI
//
//  Created by Nate Woods on 12/28/14.
//
//

#include "ofApp.h"
#include "target.h"

Target::Target(float start, float stop) {
    this->start = ofWrapRadians(start);
    this->stop = ofWrapRadians(stop);
};

void Target::update() {
    active = false;
};

void Target::draw(float c_x, float c_y, float radius) {
    float arc_length = radius * abs(this->start - this->stop);
    float middle = abs(this->start - this->stop) / 2 + *this->reference + this->start;
    float x = c_x + cos(middle) * radius;
    float y = c_y + sin(middle) * radius;
    float rad = arc_length / 2;
    
    
    ofStyle temp = ofGetStyle();
    if (active) ofSetColor(ofColor::black);
    
    // Fill progress
    ofPath progress;
    progress.moveTo(x + rad + 1, y);
    progress.arc(x, y, rad + 1, rad + 1, 0, percent() * 359);
    progress.setStrokeColor(ofGetStyle().color);
    progress.setStrokeWidth(2);
    progress.setFilled(false);
    progress.draw();
    
    // Draw regular circle outline
    ofNoFill();
    ofCircle(x, y, rad);
    
    ofSetColor(temp.color);
};

void Target::setReference(float &reference) {
    this->reference = &reference;
};

float Target::getStart() {
    return ofWrapRadians(this->start + *this->reference);
};

float Target::getStop() {
    return ofWrapRadians(this->stop + *this->reference);
};

void Target::setStart(float start) {
    this->start = ofWrapRadians(start);
};

void Target::setStop(float stop) {
    this->stop = ofWrapRadians(stop);
};

float Target::percent() {
    return this->amount / this->capacity;
};