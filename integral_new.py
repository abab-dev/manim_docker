import numpy as np
from manim import *

# To run this:
# 1. Save it as a Python file (e.g., integral_area_centered.py)
# 2. Open your terminal or command prompt
# 3. Navigate to the directory where you saved the file
# 4. Run the command: manim -pql integral_area_centered.py IntegralAreaInterpretationCentered
#    (-pql means preview, quality low - use -pqm for medium, -pqh for high)


class IntegralAreaInterpretationCentered(Scene):  # Renamed class for clarity
    def construct(self):
        # --- CONFIGURATION ---
        axes_y_shift = DOWN * 0.5  # How much to shift axes down from center
        top_label_buff = 0.5  # Buffer from top edge for main labels
        label_scale = 0.9  # Scale factor for top labels

        # 1. Setup Axes and Function
        axes = Axes(
            x_range=[0, 7.1, 1],  # Extend x_range slightly for label room
            y_range=[0, 8.1, 1],  # Extend y_range slightly
            x_length=7,
            y_length=5,
            axis_config={"include_numbers": True},
            x_axis_config={"numbers_to_include": np.arange(1, 7.1, 1)},
            y_axis_config={"numbers_to_include": np.arange(1, 8.1, 1)},
            tips=False,  # Optionally remove arrow tips if crowded
        ).add_coordinates()
        # Center the axes and shift down
        axes.center().shift(axes_y_shift)

        # Define the function: f(x) = x^2/5 + 1
        def func(x):
            return x**2 / 5 + 1

        # Define the integration interval [a, b]
        a = 1
        b = 6

        # Create the graph
        graph = axes.plot(func, x_range=[0, 7], color=BLUE)
        graph_label = axes.get_graph_label(
            graph,
            label=MathTex("f(x) = \\frac{x^2}{5} + 1").scale(
                0.8
            ),  # Slightly smaller label
            x_val=4.5,
            direction=UP * 1.0,  # Adjust direction/distance if needed
        )

        # Create axes labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("f(x)").shift(LEFT * 0.5)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph), Write(graph_label))
        self.wait(1)

        # 2. Introduce Riemann Sums (Approximation)
        num_rects_tracker = ValueTracker(5)

        riemann_rects = always_redraw(
            lambda: axes.get_riemann_rectangles(
                graph=graph,
                x_range=[a, b],
                dx=(b - a) / num_rects_tracker.get_value(),
                input_sample_type="left",
                stroke_width=0.5,
                stroke_color=BLACK,
                fill_opacity=0.6,
                color=[YELLOW, ORANGE],
            )
        )

        # Position Riemann sum label near the top edge
        rects_label = MathTex("Area \\approx \\sum_{i=1}^{n} f(x_i^*) \\Delta x")
        rects_label.scale(label_scale).to_edge(UP, buff=top_label_buff)

        # Position n value text below the rects_label
        n_value_text = always_redraw(
            lambda: MathTex(f"n = {int(num_rects_tracker.get_value())}")
            .scale(label_scale)  # Scale consistently
            .next_to(rects_label, DOWN, buff=0.2)
        )

        self.play(Write(rects_label))
        self.play(Create(riemann_rects), Write(n_value_text))
        self.wait(1)

        # Animate increasing the number of rectangles
        self.play(num_rects_tracker.animate.set_value(10), run_time=1.5)
        self.wait(0.5)
        self.play(num_rects_tracker.animate.set_value(20), run_time=1.5)
        self.wait(0.5)
        self.play(num_rects_tracker.animate.set_value(50), run_time=2)
        self.wait(1)
        self.play(num_rects_tracker.animate.set_value(100), run_time=2)
        self.wait(1)

        # 3. Transition to the Definite Integral (Exact Area)
        self.play(FadeOut(n_value_text), FadeOut(rects_label))  # Fade out old labels

        integral_area = axes.get_area(
            graph=graph,
            x_range=[a, b],
            color=[BLUE, TEAL],
            opacity=0.7,
        )

        # Create integral sign using the corrected structure
        integral_sign = MathTex(
            "Area = \\int",  # Part 0
            "_{" + str(a) + "}",  # Part 1: _{a}
            "^{" + str(b) + "}",  # Part 2: ^{b}
            " f(x) \\, dx",  # Part 3
        )
        integral_sign[1].set_color(YELLOW)
        integral_sign[2].set_color(ORANGE)

        # Position integral sign near the top edge
        integral_sign.scale(label_scale).to_edge(UP, buff=top_label_buff)

        # Calculate and create the exact area text
        exact_area_val = 58 / 3
        area_text = MathTex(f"= \\frac{{58}}{{3}} \\approx {exact_area_val:.2f}")
        # Position area text BELOW the integral sign
        area_text.scale(label_scale).next_to(integral_sign, DOWN, buff=0.25)

        # Animation: Fade out rectangles, fade in smooth area and NEW labels
        self.play(
            ReplacementTransform(riemann_rects, integral_area),
            Write(integral_sign),  # Write the integral sign first
            run_time=2,
        )
        self.play(Write(area_text))  # Then write the area value below it
        self.wait(3)

        # Fade out everything at the end (optional)
        # self.play(FadeOut(axes), FadeOut(graph), FadeOut(graph_label),
        #           FadeOut(integral_area), FadeOut(integral_sign), FadeOut(area_text))
