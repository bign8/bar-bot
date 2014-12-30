//
//  target.h
//  barBotPLC_GUI
//
//  Created by Nate Woods on 12/28/14.
//
//

#ifndef __barBotPLC_GUI__target__
#define __barBotPLC_GUI__target__

#include "ofApp.h"

class Target {
public:
    Target(float start, float stop);
    
    void update();
    void draw(float c_x, float c_y, float radius);
    void setReference(float &reference);
    
    // actual angles
    float getStart();
    float getStop();
    void setStart(float start);
    void setStop(float stop);
    
    bool active;
    
    // volume measurements
    float capacity;
    float amount;
    float percent();
    
private:
    float start;
    float stop;
    float *reference;
};

#endif /* defined(__barBotPLC_GUI__target__) */
