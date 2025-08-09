from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm

def generate_pattern(length, waist, hip_height, round_hip, thigh, ankle, customer_name):
    """Generates a PDF sewing pattern for a customer."""
    filename = f"{customer_name.replace(' ', '_')}_pattern.pdf"
    page_width = 29.7 * inch
    page_height = 42 * inch

    c = canvas.Canvas(filename, pagesize=(page_width, page_height))

    # --- Define Points ---
    Ax, Ay = inch + 1*inch, page_height - inch
    Bx, By = Ax - 1*inch + (waist / 4)*inch + 2.5*inch, Ay - 1*inch
    Cx, Cy = Ax - 1*inch, Ay - hip_height*inch
    Dx, Dy = Bx, By - hip_height*inch + 1*inch
    Ex, Ey = Cx, Ay - ((round_hip*inch) / 4) + 1.5*inch
    Fx, Fy = Ex + ((thigh*inch) / 2) + 1.5*inch, Ey
    Gx, Gy = Ax, Ay - length*inch
    Hx, Hy = Gx + (ankle*inch) / 2, Gy
    Ix, Iy = Gx - 0.25*inch, Gy - 2*inch
    Jx, Jy = Hx +  0.25*inch, Iy

    # --- Draw Points ---
    c.setFillColorRGB(0, 0, 1)
    for x, y in [(Ax, Ay), (Bx, By), (Cx, Cy), (Dx, Dy), (Ex, Ey),
                 (Fx, Fy), (Gx, Gy), (Hx, Hy), (Ix, Iy), (Jx, Jy)]:
        c.circle(x, y, 3, fill=1)

    # --- Draw Lines ---
    c.setStrokeColorRGB(1, 0, 0)
    c.line(Ax, Ay, Bx, By)
    c.line(Bx, By, Dx, Dy)
    c.line(Cx, Cy, Ex, Ey)
    c.line(Ex, Ey, Gx, Gy)
    c.line(Gx, Gy, Ix, Iy)
    c.line(Hx, Hy, Jx, Jy)
    c.line(Ix, Iy, Jx, Jy)
    c.line(Fx, Fy, Hx, Hy)

    # --- Crotch Curve (D to F) ---
    c.setStrokeColorRGB(0, 0.5, 0)
    c.bezier(Dx, Dy,
             Dx - 0.2 * inch, Dy - 2.5 * inch,
             Fx - 2.25 * inch, Fy + 0.55 * inch,
             Fx, Fy)

    # Curve between A and C
    c.setStrokeColorRGB(0, 0.5, 0)
    c.bezier(Ax, Ay,
             Ax - 0.4 * inch, Ay + 0.25 * inch,
             Cx - 0.3 * inch, Cy - 0.25 * inch,
             Cx, Cy)

    # --- Labels ---
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0)
    points = {
        "A": (Ax, Ay), "B": (Bx, By), "C": (Cx, Cy),
        "D": (Dx, Dy), "E": (Ex, Ey), "F": (Fx, Fy),
        "G": (Gx, Gy), "H": (Hx, Hy), "I": (Ix, Iy), "J": (Jx, Jy)
    }
    for label, (x, y) in points.items():
        c.drawString(x + 0.2 * cm, y + 0.3 * cm, label)

    # --- Coordinate Labels ---
    c.setFont("Helvetica", 9)
    for label, (x, y) in points.items():
        c.drawString(x - 1.5 * cm, y - 0.6 * cm, f"{label} = ({round(x)}, {round(y)})")

    c.drawString(Ax, Ay + 1.5 * cm, f"Pattern for: {customer_name}")
    c.save()
    print(f"✅ Successfully generated pattern for {customer_name} at {filename}")
