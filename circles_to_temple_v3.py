"""
Project:  Nature Decode / Nature Visualization
Copyright (c) 2026 Ruhani Kashni (MathRize)
License: MIT License (See LICENSE file for details)
YouTube: https://www.youtube.com/@MathRize
"""
from manim import *
import numpy as np

# --- CUSTOM TEMPLE SHAPE FUNCTION ---
def create_temple_structure(pos, scale_val, main_color, accent_color):
    # 1. The Base (Chabootra)
    base = Cube(side_length=0.7 * scale_val, fill_color=main_color, fill_opacity=1, stroke_color=accent_color, stroke_width=1)
    base.stretch(0.4, dim=2) 
    base.move_to(pos + np.array([0,0,0.15*scale_val])) 

    # 2. The Spire (Shikhara)
    spire = Cone(base_radius=0.35 * scale_val, height=0.8 * scale_val, direction=OUT)
    spire.set_fill(main_color, opacity=1)
    spire.set_stroke(accent_color, width=1)
    spire.next_to(base, OUT, buff=0) 

    return VGroup(base, spire)
# ------------------------------------


class CirclesToTempleFinalV3(ThreeDScene):
    def construct(self):
        # 1. SETUP
        self.camera.background_color = "#0a0a0a" 
        self.set_camera_orientation(phi=0*DEGREES, theta=-90*DEGREES)

        # --- COLOR THEME ---
        MAIN_GOLD = "#D4AF37" 
        DEEP_GOLD = "#AA8C2C" 
        GLOW_COLOR = "#FFFFF0" 

        SCALE_FACTOR = 0.8 

        # =========================================
        # PHASE 1: SACRED GEOMETRY (The Circles)
        # =========================================
        R = 2.0 * SCALE_FACTOR

        center_circle = Circle(radius=R, color=MAIN_GOLD, stroke_width=3, stroke_opacity=0.8)
        
        outer_circles = VGroup()
        for i in range(4):
            angle = i * PI / 2
            center_pos = [R * np.cos(angle), R * np.sin(angle), 0]
            outer_circles.add(Circle(radius=R, color=DEEP_GOLD, stroke_width=2, stroke_opacity=0.5).move_to(center_pos))

        geometry_group = VGroup(center_circle, outer_circles)

        # ANIMATION 1
        self.play(
            Create(center_circle),
            Create(outer_circles, lag_ratio=0.1),
            run_time=2.5,
            rate_func=smooth
        )
        self.wait(0.5)


        # =========================================
        # PHASE 2: IDENTIFYING THE POINTS
        # =========================================
        points_group = VGroup()
        center_point_pos = ORIGIN
        points_group.add(Dot3D(center_point_pos, color=GLOW_COLOR, radius=0.1*SCALE_FACTOR))

        corner_dist = R * 0.8 
        corner_positions = []
        for i in range(4):
            angle = i * PI / 2 + PI/4 
            pos = [corner_dist * np.cos(angle), corner_dist * np.sin(angle), 0]
            corner_positions.append(pos)
            points_group.add(Dot3D(pos, color=MAIN_GOLD, radius=0.08*SCALE_FACTOR))

        # ANIMATION 2
        self.play(
            geometry_group.animate.set_stroke(opacity=0.1, width=1),
            GrowFromCenter(points_group),
            run_time=1.5
        )
        self.wait(0.5)


        # =========================================
        # PHASE 3: THE TEMPLE RISE
        # =========================================
        
        main_shrine_3d = create_temple_structure(center_point_pos, 1.2*SCALE_FACTOR, DEEP_GOLD, MAIN_GOLD)
        
        corner_shrines_3d = VGroup()
        for pos in corner_positions:
            shrine = create_temple_structure(pos, 0.7*SCALE_FACTOR, DEEP_GOLD, MAIN_GOLD)
            corner_shrines_3d.add(shrine)

        plan_lines = VGroup()
        for corner in corner_shrines_3d:
            line = Line(start=main_shrine_3d[0].get_center(), end=corner[0].get_center(), color=MAIN_GOLD, stroke_opacity=0.4, stroke_width=1.5)
            plan_lines.add(line)

        # ANIMATION 3: 3D Camera Move & Rising Effect
        self.move_camera(phi=70*DEGREES, theta=-45*DEGREES, run_time=2)
        
        self.play(FadeOut(geometry_group), FadeOut(points_group), run_time=0.5)

        self.play(
            Create(plan_lines),
            # 'smooth' animation use kiya hai jo kabhi error nahi dega
            GrowFromPoint(main_shrine_3d, main_shrine_3d.get_bottom()),
            GrowFromPoint(corner_shrines_3d[0], corner_shrines_3d[0].get_bottom()),
            GrowFromPoint(corner_shrines_3d[1], corner_shrines_3d[1].get_bottom()),
            GrowFromPoint(corner_shrines_3d[2], corner_shrines_3d[2].get_bottom()),
            GrowFromPoint(corner_shrines_3d[3], corner_shrines_3d[3].get_bottom()),
            run_time=2.5,
            rate_func=smooth 
        )

        self.begin_ambient_camera_rotation(rate=0.1)

        self.wait(4)
