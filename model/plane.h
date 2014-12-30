//
//  plane.h
//  barBotPLC_GUI
//
//  Created by Nate Woods on 12/28/14.
//
//

#ifndef barBotPLC_GUI_plane_h
#define barBotPLC_GUI_plane_h

#include "target.h"

class Plane {
public:
    Plane(float angle);
    
    void update();
    void draw(float c_x, float c_y, float radius);
    
    float angle;
    std::vector<Target> *targets;
    
    // Drawing variables
    ofColor color;
};

#endif
