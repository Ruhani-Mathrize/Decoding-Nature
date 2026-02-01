"""
Project:  Nature Decode / Nature Visualization
Copyright (c) 2026 Ruhani Kashni (MathRize)
License: MIT License (See LICENSE file for details)
YouTube: https://www.youtube.com/@MathRize
"""
from manim import *
import numpy as np

class PatternOfFive(ThreeDScene):
    def construct(self):
        # 1. SETUP: Cinematic Dark Mode & 3D Camera
        self.camera.background_color = "#050505"
        self.set_camera_orientation(phi=75*DEGREES, theta=-30*DEGREES)

        # 2. DEFINE THE MATHEMATICAL FLOWER
        def get_math_flower(color_theme):
            return ParametricFunction(
                lambda t: np.array([
                    1.5 * np.cos(5*t) * np.cos(t), 
                    1.5 * np.cos(5*t) * np.sin(t),
                    0 
                ]),
                t_range=[0, 2*PI],
                fill_opacity=0.4, 
                fill_color=color_theme, 
                stroke_color=color_theme, 
                stroke_width=2
            )

        # 3. INITIAL STATE
        center_flower = get_math_flower(GOLD)
        self.play(GrowFromCenter(center_flower), run_time=1.5)
        self.wait(0.5)

        # 4. THE REPETITION
        flowers_group = VGroup()
        
        # FIX 1: 'CREAM' ki jagah Hex code
        colors = [RED_D, PINK, YELLOW_D, ORANGE, "#FFFDD0"] 
        
        radius_of_spread = 4.0 

        for i in range(5):
            angle = i * (2*PI / 5) + PI/2 
            
            target_pos = np.array([
                radius_of_spread * np.cos(angle),
                radius_of_spread * np.sin(angle),
                0
            ])
            
            new_flower = get_math_flower(colors[i]).move_to(ORIGIN)
            flowers_group.add(new_flower)
            
            # FIX 2: 'ease_out_cubic' ki jagah standard 'smooth' use kiya hai
            self.play(
                center_flower.animate.scale(0.1).set_opacity(0), 
                new_flower.animate.move_to(target_pos).scale(0.8), 
                run_time=1.5,
                rate_func=smooth 
            )
        
        self.remove(center_flower)

        # 5. THE STABILITY (Pentagon)
        pentagon_points = [f.get_center() for f in flowers_group]
        pentagon = Polygon(*pentagon_points, color=BLUE_E, stroke_width=3, stroke_opacity=0.5)
        
        pentagon_glow = pentagon.copy().set_stroke(width=8, opacity=0.2, color=BLUE)

        self.play(
            Create(pentagon),
            FadeIn(pentagon_glow),
            run_time=2
        )

        # 6. CINEMATIC FINISH
        self.begin_ambient_camera_rotation(rate=0.08) 
        
        self.play(
            flowers_group.animate.scale(1.05),
            run_time=2,
            rate_func=there_and_back,
            lag_ratio=0.1
        )
        

        self.wait(4)
