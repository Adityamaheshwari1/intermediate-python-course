# This is the main file for the tailoring application.
# It will contain the GUI and pattern generation logic.
import tkinter as tk

class TailoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tailoring App")

        # Create the main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # Left frame for measurements
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        # Right frame for the pattern
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, padx=10)

        # --- Measurement Inputs ---
        tk.Label(left_frame, text="Measurements (in cm)").pack()

        self.measurements = {}
        measurements_list = [
            "Waist Circumference",
            "Hip Circumference",
            "Waist to Hip Length",
            "Crotch Depth",
            "Waist to Knee Length",
            "Waist to Ankle Length",
            "Ankle Circumference",
        ]
        for measurement in measurements_list:
            frame = tk.Frame(left_frame)
            frame.pack(pady=2)
            label = tk.Label(frame, text=f"{measurement}:", width=15, anchor='w')
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            self.measurements[measurement] = entry

        # --- Generate Button ---
        generate_button = tk.Button(left_frame, text="Generate Pattern", command=self.generate_pattern)
        generate_button.pack(pady=10)

        # --- Pattern Canvas ---
        self.canvas = tk.Canvas(right_frame, width=400, height=600, bg="white")
        self.canvas.pack()

    def generate_pattern(self):
        self.canvas.delete("all")

        try:
            # --- Get measurements and convert to float ---
            waist_circ = float(self.measurements["Waist Circumference"].get())
            hip_circ = float(self.measurements["Hip Circumference"].get())
            waist_to_hip = float(self.measurements["Waist to Hip Length"].get())
            crotch_depth = float(self.measurements["Crotch Depth"].get())
            waist_to_knee = float(self.measurements["Waist to Knee Length"].get())
            waist_to_ankle = float(self.measurements["Waist to Ankle Length"].get())
            ankle_circ = float(self.measurements["Ankle Circumference"].get())

            # --- Calculations from the tutorial ---
            # Using a scale factor to fit the pattern on the canvas
            scale = 4

            # The article uses 1/2 hip and 1/2 waist measurements for the draft
            half_hip = hip_circ / 2
            half_waist = waist_circ / 2

            # 1. Draw a right-angle using your ½ hip measurement + 2cm of ease for the width, and waist to ankle measurement for the height.
            width = (half_hip + 2) / scale
            height = waist_to_ankle / scale

            x_offset = 20
            y_offset = 20

            # Draw the main block
            self.canvas.create_rectangle(x_offset, y_offset, x_offset + width, y_offset + height, outline="grey", tags="pattern")

            # Add the other 3 measurements: waist to hip, crotch depth + 1.5cm of ease, and waist to knee.
            hip_line_y = y_offset + (waist_to_hip / scale)
            crotch_line_y = y_offset + ((crotch_depth + 1.5) / scale)
            knee_line_y = y_offset + (waist_to_knee / scale)

            self.canvas.create_line(x_offset, hip_line_y, x_offset + width, hip_line_y, fill="lightgrey", tags="pattern")
            self.canvas.create_line(x_offset, crotch_line_y, x_offset + width, crotch_line_y, fill="lightgrey", tags="pattern")
            self.canvas.create_line(x_offset, knee_line_y, x_offset + width, knee_line_y, fill="lightgrey", tags="pattern")

            # 2. Separate the front and the back pieces
            center_line_x = x_offset + width / 2
            self.canvas.create_line(center_line_x, y_offset, center_line_x, y_offset + height, fill="grey", tags="pattern")

            # 3. To find out where the crotch points will be
            front_crotch_ext = (half_hip / 8) / scale
            back_crotch_ext = (front_crotch_ext * scale + 3) / scale

            front_crotch_point_x = center_line_x - front_crotch_ext
            back_crotch_point_x = center_line_x + back_crotch_ext

            self.canvas.create_line(center_line_x, crotch_line_y, front_crotch_point_x, crotch_line_y, fill="blue", tags="pattern")
            self.canvas.create_line(center_line_x, crotch_line_y, back_crotch_point_x, crotch_line_y, fill="red", tags="pattern")

            # This is a simplified version of the remaining steps, as drawing complex curves is tricky.
            # I will represent the pattern pieces with polygons for now.

            # Front Piece
            front_waist = ((half_waist / 2) + 1.5) / scale
            front_top_left_x = center_line_x - front_waist

            front_points = [
                front_top_left_x, y_offset,
                center_line_x, y_offset,
                center_line_x, hip_line_y,
                front_crotch_point_x, crotch_line_y,
                front_top_left_x, y_offset + height, # Simplified bottom point
                front_top_left_x, y_offset
            ]
            self.canvas.create_polygon(front_points, outline='blue', fill='', width=2, tags="pattern")

            # Back Piece
            back_waist = ((half_waist / 2) + 0.5) / scale
            back_top_right_x = center_line_x + back_waist

            back_points = [
                center_line_x, y_offset,
                back_top_right_x, y_offset,
                back_top_right_x, y_offset + height, # Simplified bottom point
                back_crotch_point_x, crotch_line_y,
                center_line_x, hip_line_y,
                center_line_x, y_offset,
            ]
            self.canvas.create_polygon(back_points, outline='red', fill='', width=2, tags="pattern")

        except (ValueError, ZeroDivisionError):
            # Handle cases where the input is not a valid number or is zero
            error_label = tk.Label(self.canvas, text="Please enter valid, non-zero numbers for all measurements.", fg="red")
            self.canvas.create_window(200, 20, window=error_label)


if __name__ == "__main__":
    root = tk.Tk()
    app = TailoringApp(root)
    root.mainloop()
