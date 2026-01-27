from manim import *
import numpy as np

# --- Custom Colors for Premium Look ---
RICH_GOLD = "#FFD700" # Gehra Sona
AMBER_GLOW = "#FF4500" # Aag jaisa Narangi
DEEP_BRONZE = "#CD7F32"

class SacredGeometryCinematic(Scene):
    def construct(self):
        # 1. ATMOSPHERE: Not just black, but dark vignette
        self.camera.background_color = "#050505" # Almost black

        RADIUS = 2.5

        # --- HELPER FUNCTION FOR TRUE GLOW ---
        # Yeh function ek object ke peeche multiple dhundhli layers banata hai
        def make_glowing_stroke(mobject, glow_color, layers=4, max_width=20, base_opacity=0.4):
            glow_group = VGroup()
            for i in range(layers):
                # Har layer pichli se thodi moti aur zyada transparent hogi
                width = max_width * (i + 1) / layers
                opacity = base_opacity * (1 - (i / layers))
                glow_layer = mobject.copy()
                glow_layer.set_stroke(width=width, color=glow_color, opacity=opacity)
                glow_layer.set_fill(opacity=0)
                glow_group.add(glow_layer)
            # Asli object ko sabse upar rakho
            glow_group.add(mobject)
            return glow_group


        # --- OBJECTS CREATION ---

        # 1. The Central Circle (Molten Gold Look)
        center_circle_base = Circle(radius=RADIUS, color=RICH_GOLD, stroke_width=5)
        center_circle_base.set_sheen(0.8, direction=UR) # Metallic Shine
        # Isko thoda sa glow dete hain
        center_circle = make_glowing_stroke(center_circle_base, RICH_GOLD, layers=3, max_width=12, base_opacity=0.2)

        # 2. The 5 Surrounding Circles (Bronze/Gold Mix)
        surrounding_circles_group = VGroup()
        for i in range(5):
            angle_rad = (i * 72 + 90) * DEGREES
            new_center = np.array([RADIUS * np.cos(angle_rad), RADIUS * np.sin(angle_rad), 0])
            
            # Base circle
            circle_base = Circle(radius=RADIUS, color=DEEP_BRONZE, stroke_width=3)
            # Ispe kam glow rakhenge taaki focus beech mein rahe
            glowing_circle = make_glowing_stroke(circle_base, DEEP_BRONZE, layers=2, max_width=8, base_opacity=0.15)
            glowing_circle.move_to(new_center)
            surrounding_circles_group.add(glowing_circle)


        # 3. The Resulting Symmetry (The Fiery Reveal)
        # Calculation for perfect fit
        pentagon_base = RegularPolygon(n=5, color=AMBER_GLOW, stroke_width=6)
        pentagon_scale_factor = RADIUS * np.sqrt((3 - np.sqrt(5))/2) * 1.236
        pentagon_base.scale(pentagon_scale_factor)
        pentagon_base.rotate(180*DEGREES + 36*DEGREES) 
        
        # Star inside
        pentagram_base = Star(n=5, outer_radius=pentagon_base.width/2, color=AMBER_GLOW, stroke_width=4)
        pentagram_base.rotate(180*DEGREES + 36*DEGREES)
        
        symmetry_base = VGroup(pentagon_base, pentagram_base)
        
        # ISKO SABSE ZYADA GLOW DENGE (Intense Fire Effect)
        final_symmetry = make_glowing_stroke(symmetry_base, AMBER_GLOW, layers=6, max_width=40, base_opacity=0.5)


        # --- ANIMATION SEQUENCE (Slow & Majestic) ---

        # Voiceover: "Sacred Geometry mein bhi..."
        # Central circle 'ubhar' kar aata hai
        self.play(
            DrawBorderThenFill(center_circle_base),
            FadeIn(center_circle[0:-1]), # Glow layers fade in
            run_time=2.5, 
            rate_func=smooth
        )
        self.wait(0.5)

        # Voiceover: "...circles ko ek specific pattern mein draw karein,"
        # Surrounding circles draw hote hain
        self.play(
            LaggedStart(
                *[Create(c[-1]) for c in surrounding_circles_group], # Draw base layer
                lag_ratio=0.3
            ),
            LaggedStart(
                *[FadeIn(c[0:-1]) for c in surrounding_circles_group], # Fade in glow layers
                lag_ratio=0.3
            ),
            run_time=5,
            rate_func=linear
        )
        
        # Voiceover: "...toh unke beech ek Pentagonal..."
        # Baaki circles ko dim karte hain
        self.play(
            center_circle.animate.set_opacity(0.2),
            surrounding_circles_group.animate.set_opacity(0.2),
            run_time=1.5
        )

        # Voiceover: "...symmetry ubhar kar aati hai."
        # THE BIG REVEAL: Aag ki tarah jalta hua Pentagon aata hai
        self.play(
            Create(final_symmetry[-1]), # Draw the main lines
            FadeIn(final_symmetry[0:-1]), # Ignite the glow
            run_time=3,
            rate_func=there_and_back_with_pause # Thoda pulse karega
        )
        
        # Final slow, hypnotic rotation
        self.play(
            Rotate(VGroup(center_circle, surrounding_circles_group, final_symmetry), angle=PI/5),
            run_time=7,
            rate_func=smooth
        )