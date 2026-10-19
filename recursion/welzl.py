import numpy as np
import matplotlib.pyplot as plt

def run_welzl(P):
    """Wrapper function to handle setup."""
    P_copy = np.copy(P)
    np.random.shuffle(P_copy) # Shuffle exactly once before starting
    welzl.ncalls = 0
    final_circle = welzl(P_copy, [])
    print(f"Finished! Total recursive calls: {welzl.ncalls}")
    return final_circle

def welzl(P, R):
    welzl.ncalls += 1
    # 1. Base cases: array is empty or boundary has 3 points
    if len(P) == 0 or len(R) == 3:
        c = calc_circle(R)
        visualize(P_original, c, R)  # Show calculation
        return c

    # 2. Slice off the last point (Python's equivalent to pSize - 1)
    p = P[-1]
    c = welzl(P[:-1], R)

    # 3. If point is in the circle, keep the circle
    if c is not None and np.linalg.norm(c[0] - p) <= c[1] + 1e-9:
        return c

    # 4. Otherwise, p must be on the boundary
    visualize(P_original, c, R + [p])  # Show point being added to boundary
    return welzl(P[:-1], R + [p])


def calc_circle(R):
    if len(R) == 0: return None
    if len(R) == 1: return (R[0], 0)
    if len(R) == 2:
        return ((R[0] + R[1]) / 2, np.linalg.norm(R[0] - R[1]) / 2)

    # For 3 points, solve the linear system for the center using NumPy
    A = 2 * (np.array(R[1:]) - R[0])
    B = np.sum(np.array(R[1:]) ** 2 - R[0] ** 2, axis=1)
    center = np.linalg.solve(A, B)
    return (center, np.linalg.norm(center - R[0]))


def visualize(all_points, current_circle, boundary):
    plt.clf()  # Clear the previous frame

    # Draw all points
    plt.scatter(all_points[:, 0], all_points[:, 1], c='black', s=20)

    # Draw boundary points in red
    if boundary:
        b_pts = np.array(boundary)
        plt.scatter(b_pts[:, 0], b_pts[:, 1], c='red', s=80)

    # Draw the current circle
    if current_circle is not None:
        center, radius = current_circle
        circle = plt.Circle(center, radius, color='blue', fill=True, alpha=0.2)
        plt.gca().add_patch(circle)
        plt.gca().add_patch(plt.Circle(center, radius, color='blue', fill=False, lw=2))

    plt.xlim(0, 1000)
    plt.ylim(0, 800)
    plt.gca().set_aspect('equal')
    plt.pause(0.3)  # Update screen and pause for animation


# Setup and run
if __name__ == "__main__":
    plt.figure(figsize=(8, 6))

    # Generate 20 random points using NumPy
    P_original = np.random.rand(20, 2) * [600, 400] + 200

    final_circle = run_welzl(np.copy(P_original))

    print(f"Finished! Center: {final_circle[0]}, Radius: {final_circle[1]:.2f}")
    plt.show()  # Keep window open at the end