import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Physics constants
G = 9.81
RIM_HEIGHT = 3.05  # in meters

def get_sample_data():
    t = np.linspace(0, 1.25, 45)
    v0 = 8.1
    angle = np.radians(53)
    # projectile motion formula
    x = v0 * np.cos(angle) * t
    y = 2.05 + (v0 * np.sin(angle) * t - 0.5 * G * t**2)
    # Add random wiggle so it acts like real video footage
    np.random.seed(42)
    x_noisy = x + np.random.normal(0, 0.035, len(t))
    y_noisy = y + np.random.normal(0, 0.035, len(t))
    return x_noisy, y_noisy

def parabola(x, a, b, c):
    return a * x**2 + b * x + c

def analyze_shot(x_data, y_data):
    # Fit points to y = ax^2 + bx + c
    popt, _ = curve_fit(parabola, x_data, y_data)
    a, b, c = popt

    # Calculate entry angle
    # Find x where y = RIM_HEIGHT
    # a * x**2 + b * x + c = RIM_HEIGHT
    # a * x**2 + b * x + (c - RIM_HEIGHT) = 0
    c_prime = c - RIM_HEIGHT
    discriminant = b**2 - 4 * a * c_prime

    if discriminant < 0:
        # No real roots, the ball doesn't reach rim height
        entry_angle = np.nan  # Or handle error appropriately
    else:
        x_rim1 = (-b + np.sqrt(discriminant)) / (2 * a)
        x_rim2 = (-b - np.sqrt(discriminant)) / (2 * a)

        # Choose the x_rim that makes sense for entering the hoop (usually the one further along x-axis for a shot)
        # For typical projectile motion, 'a' should be negative (parabola opens downwards).
        # The larger x-root typically corresponds to the descending part of the trajectory for a shot.
        if a < 0:
            x_at_rim = max(x_rim1, x_rim2)
        else:
            # This case is unlikely for projectile motion of a basketball, but handle it defensively.
            x_at_rim = min(x_rim1, x_rim2)

        # Calculate the slope at x_at_rim: dy/dx = 2ax + b
        slope_at_rim = 2 * a * x_at_rim + b
        entry_angle = np.degrees(np.arctan(slope_at_rim))

    return a, b, c, entry_angle

def plot_results(x_data, y_data, a, b, c, entry_angle):
    x_fit = np.linspace(min(x_data), max(x_data), 100)
    y_fit = parabola(x_fit, a, b, c)
    plt.figure(figsize=(9, 5))
    plt.scatter(x_data, y_data, color='red', s=20, label='Tracked Points')
    plt.plot(x_fit, y_fit, 'b-', label=f'Fitted Arc (Entry Angle: {entry_angle:.1f}deg)')
    plt.axhline(y=RIM_HEIGHT, color='g', linestyle='--', label='Rim (3.05m)')
    plt.title('Basketball Trajectory')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('shot_plot.png')
    plt.show()

if __name__ == '__main__':
    x_pts, y_pts = get_sample_data()
    a, b, c, angle = analyze_shot(x_pts, y_pts)

    print(f'Entry Angle: {angle:.2f} degrees')
    plot_results(x_pts, y_pts, a, b, c, angle)
