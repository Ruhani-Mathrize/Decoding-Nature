"""
Project:  Nature Decode / Nature Visualization
Copyright (c) 2026 Ruhani Kashni (MathRize)
License: MIT License (See LICENSE file for details)
YouTube: https://www.youtube.com/@MathRize
"""
from manim import *
import numpy as np

class OddNumberSymmetry(Scene):
    def construct(self):
        # 1. SETUP: Cinematic Dark Theme
        self.camera.background_color = "#101010" # Dark Grey/Black

        # 2. THE STAGE: Faint Polar Grid (Scientific Look)
        plane = PolarPlane(
            radius_max=3.5,
            size=7,
            azimuth_units="degrees",
            azimuth_label_font_size=24,
            radius_step=1,
            stroke_opacity=0.2, # Very subtle
            background_line_style={"stroke_color": TEAL}
        ).add_coordinates()
        
        # 3. THE VARIABLE (ValueTracker)
        # Yeh 'n' ki value hold karega jo change hoti rahegi
        n_tracker = ValueTracker(1) 

        # 4. THE GLOWING GRAPH (The Hero)
        # always_redraw ka matlab hai jab 'n' change hoga, graph update hoga
        def get_curve():
            n = n_tracker.get_value()
            return ParametricFunction(
                lambda t: plane.polar_to_point(2.5 * np.cos(n * t), t),
                t_range = [0, 2*PI], # 0 to 2PI for full rotation
                color = YELLOW,
                stroke_width = 6
            ).set_stroke(opacity=1).set_sheen(0.5, direction=UR)

        # Glow Effect: Ek moti (thick) transparent line peeche
        def get_glow():
            n = n_tracker.get_value()
            return ParametricFunction(
                lambda t: plane.polar_to_point(2.5 * np.cos(n * t), t),
                t_range = [0, 2*PI],
                color = YELLOW,
                stroke_width = 15, # Motai zyada
                stroke_opacity = 0.3 # Transparency kam
            )

        graph = always_redraw(get_curve)
        glow = always_redraw(get_glow)

        # 5. THE DYNAMIC EQUATION
        # Isme hum 'n' ko alag color denge
        equation_text = MathTex(r"r = \cos(", "n", r"\theta)").scale(1.5).to_corner(UL)
        equation_text[1].set_color(ORANGE) # 'n' ko highlight kiya
        
        # Number indicator jo change hoga
        number_label = always_redraw(lambda: 
            MathTex(f"n = {n_tracker.get_value():.0f}", color=ORANGE)
            .scale(1.5)
            .next_to(equation_text, DOWN)
        )

        # --- ANIMATION SEQUENCE ---

        # Scene Start
        self.play(Create(plane), run_time=1.5)
        self.play(Write(equation_text))
        self.play(FadeIn(number_label))
        
        # Initial Circle (n=1)
        self.play(Create(glow), Create(graph), run_time=1.5)
        self.wait(0.5)

        # MORPH: 1 -> 3 (Triangle/3 Petals)
        # Script: "Jab hum equation mein odd numbers — jaise 3..."
        self.play(
            n_tracker.animate.set_value(3),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)

        # MORPH: 3 -> 5 (Champa/5 Petals)
        # Script: "...5..."
        self.play(
            n_tracker.animate.set_value(5), # 5 Petals
            graph.animate.set_color(GOLD),  # Color change for impact
            glow.animate.set_color(GOLD),
            run_time=2,
            rate_func=smooth
        )
        # Yahan Champa ka reference aayega script mein
        self.wait(1)

        # MORPH: 5 -> 7 (7 Petals)
        # Script: "...7 use karte hain..."
        self.play(
            n_tracker.animate.set_value(7),
            graph.animate.set_color(PINK), # Another color change
            glow.animate.set_color(PINK),
            run_time=2,
            rate_func=smooth
        )
        self.wait(2)
        
        # Final Polish: Rotate the whole thing slowly (Cinematic finish)
        self.play(
            Rotate(VGroup(graph, glow), angle=PI/4),
            run_time=3

        )
