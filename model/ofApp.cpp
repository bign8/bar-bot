#define TOP_COUNT 20
#define BOT_COUNT 10

#include "ofApp.h"
#include "plane.h"
#include "target.h"

//--------------------------------------------------------------
void ofApp::setup(){
    
    // Variable Defaults
    mouseX = -1;
    mouseY = -1;
    bSmooth = true;
    
    // Settings
    ofSetFrameRate(60); // caps the framerate at 60fps.
    ofSetCircleResolution(50);
    ofBackground(255,255,255);
    ofSetWindowTitle("Bar Bot PLC GUI");
    ofShowCursor();
    ofEnableAntiAliasing();
    
    // Build top
    Target *temp;
    float arc_length = PI / TOP_COUNT, start, stop;
    top = new Plane(0.0);
    top->color = ofColor::blue;
    
    // TODO: load targets from file + change with UI
    for (int i = 0; i < TOP_COUNT; i++) {
        start = i * arc_length * 2;
        stop = start + arc_length / 2;
        
        temp = new Target(start, stop);
        temp->setReference(top->angle);
        temp->capacity = 200;
        temp->amount = 200;
        top->targets->push_back(*temp);
    }
    
    // Build bottom
    arc_length = PI / BOT_COUNT;
    bot = new Plane(0.0);
    bot->color = ofColor::red;
    
    // TODO: load targets from file + change with UI
    for (int i = 0; i < BOT_COUNT; i++) {
        start = i * arc_length * 2;
        stop = start + arc_length;
        
        temp = new Target(start, stop);
        temp->setReference(bot->angle);
        temp->capacity = 100;
        temp->amount = 0;
        bot->targets->push_back(*temp);
    }
}

//--------------------------------------------------------------
void ofApp::update(){
    float delta_x = mouseX - oldMouseX;
    delta_x /= ofGetWidth();
    delta_x *= 360;
    oldMouseX = mouseX;
    
    float delta_y = mouseY - oldMouseY;
    delta_y /= ofGetHeight();
    delta_y *= 360;
    oldMouseY = mouseY;
    
    bool is_active = ofInRange(mouseX, 0, ofGetWidth());
    is_active &= ofInRange(mouseY, 0, ofGetHeight());
    
    top->angle += ofDegToRad(is_active ? delta_x : .5);
    bot->angle -= ofDegToRad(is_active ? delta_y : .5);
    top->update();
    bot->update();
    
    // determine active targets
    activeTargets();
}

void ofApp::activeTargets() {
    bool is_active;
    float start_diff, stop_diff, amount = 0.033;
    for (std::vector<Target>::iterator t = top->targets->begin(); t != top->targets->end(); ++t) {
        for (std::vector<Target>::iterator b = bot->targets->begin(); b != bot->targets->end(); ++b) {
            start_diff = ofAngleDifferenceRadians(t->getStart(), b->getStart());
            stop_diff = ofAngleDifferenceRadians(t->getStop(), b->getStop());
            is_active = ofSign(start_diff) != ofSign(stop_diff);
            is_active &= b->amount < b->capacity;
            is_active &= t->amount > 0;
            
            if (is_active) {
                t->amount -= amount;
                b->amount += amount;
                
                t->active |= is_active;
                b->active |= is_active;
            }
        }
    }
}

//--------------------------------------------------------------
void ofApp::draw(){
    ofDrawBitmapStringHighlight("Black = Pouring", 20, 20);
//    ofDrawBitmapStringHighlight(ofToString(ofGetFrameRate()) + " fps", 20, 20);
//    ofDrawBitmapStringHighlight(ofToString(top->angle) + " angle", 20, 40);
    
    float c_x = ofGetWidth(), c_y = ofGetHeight();
    
    // Combined
    ofEnableAlphaBlending();
    top->draw(c_x / 2, c_y * 2 / 3, 200);
    bot->draw(c_x / 2, c_y * 2 / 3, 200);
    ofDisableAlphaBlending();
    
    // Individual
    top->draw(c_x * 1 / 4, c_y / 4, 100);
    bot->draw(c_x * 3 / 4, c_y / 4, 100);
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    switch (key) {
        
        // Toggle smothing
        case 's':
            bSmooth = !bSmooth;
            (bSmooth ? ofEnableAntiAliasing : ofDisableAntiAliasing)();
            break;
        
        // Reset fill levels
        case 'r':
            for (std::vector<Target>::iterator b = bot->targets->begin(); b != bot->targets->end(); ++b) {
                b->amount = 0;
            }
            break;
            
        default:
            break;
    }
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){

}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y){
    mouseX = x;
    mouseY = y;
}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){
    cout << msg.message << endl;
}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){ 

}