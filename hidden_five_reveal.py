"""
Project:  Nature Decode / Nature Visualization
Copyright (c) 2026 Ruhani Kashni (MathRize)
License: MIT License (See LICENSE file for details)
YouTube: https://www.youtube.com/@MathRize
"""
from manim import *
import numpy as np

class HiddenFiveReveal(Scene):
    def construct(self):
        # 1. SETUP: Dark Background for Cinematic feel
        self.camera.background_color = "#050505"

        # COLORS
        GOLD_COLOR = "#FFD700"
        GLOW_COLOR = "#FFFFE0"
        STAR_COLOR = "#FF4500" # Thoda orange-red taaki alag dikhe

        # 2. CREATE CIRCLES (The "Drawing" Phase)
        # Hum 5 circles banayenge jo 72 degrees par rotated honge (Perfect 5 symmetry)
        circles = VGroup()
        R = 2.0 
        
        for i in range(5):
            angle = i * (2 * PI / 5) + PI/2 # 72 degrees rotation
            # Center of the new circle
            center = [R * 0.6 * np.cos(angle), R * 0.6 * np.sin(angle), 0]
            circle = Circle(radius=R, color=GOLD_COLOR, stroke_width=2, stroke_opacity=0.6).move_to(center)
            circles.add(circle)

        # 3. CREATE THE HIDDEN STAR (The "Reveal" Phase)
        # Yeh star unn circles ke intersection points par banega
        star_points = []
        inner_radius = R * 0.4 # Adjust to fit inside intersections
        
        # Star ke 5 points nikaalne ka math
        for i in range(5):
            angle = i * (2 * PI / 5) + PI/2
            star_points.append([inner_radius * np.cos(angle), inner_radius * np.sin(angle), 0])
        
        # Star polygon banana (Pentagram)
        # Order: 0 -> 2 -> 4 -> 1 -> 3 -> 0 (Star drawing pattern)
        star_order = [0, 2, 4, 1, 3]
        ordered_points = [star_points[i] for i in star_order]
        
        hidden_star = Polygon(*ordered_points, color=STAR_COLOR, stroke_width=4).set_fill(STAR_COLOR, opacity=0.3)
        
        # Ek glowing effect star ke liye
        star_glow = hidden_star.copy().set_stroke(width=10, opacity=0.3, color=GLOW_COLOR)

        # ==========================================
        # ANIMATION SCRIPT (Sync with Voiceover)
        # ==========================================

        # Dialogue: "Sacred Geometry mein, jab hum circles ko..."
        self.wait(0.5)

        # Dialogue: "...ek specific pattern mein draw karte hain..."
        # Action: Circles ek-ek karke draw honge (Lag_ratio se flow aayega)
        self.play(
            Create(circles, lag_ratio=0.5), # Dheere dheere banenge
            run_time=4,
            rate_func=smooth
        )

        # Dialogue: "...toh unke beech wahi 'Hidden 5'..."
        self.wait(0.5)

        # Action: Star ubhar kar aayega (Draw + FadeIn)
        self.play(
            Create(hidden_star),
            FadeIn(star_glow),
            # Circles thode halkay ho jayenge taaki Star highlight ho
            circles.animate.set_stroke(opacity=0.3),
            run_time=2
        )

        # Dialogue: "...ubhar kar aata hai."
        # Action: Star thoda pulse karega (Dhadkega)
        self.play(
            hidden_star.animate.scale(1.1),
            star_glow.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=1.5
        )


        self.wait(2)
