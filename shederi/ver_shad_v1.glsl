#version 330

uniform float time;

in vec2 in_pos;

in vec2 in_vel;

in vec3 in_color;

in float in_fade_rate;

out vec4 color;

void main() {
    float alpha = 1 - (in_fade_rate * time);
    if(alpha < 0) alpha = 0;
    color = vec4(in_color[0], in_color[1], in_color[2], alpha);
    vec2 new_vel = in_vel;
    new_vel[1] -= time * 0.2;
    vec2 new_pos = in_pos + (time * new_vel);
    gl_Position = vec4(new_pos, 0.0, 1);
}