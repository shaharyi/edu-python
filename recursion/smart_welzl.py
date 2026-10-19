import numpy as np
import matplotlib.pyplot as plt


def run_welzl(P, animate=False):
    """
    Smart Welzl wrapper.
    Maintains O(N) expected time but bounds max stack depth to 3.
    """
    P_copy = np.copy(P)
    np.random.shuffle(P_copy)  # Critical: Shuffle exactly once at the start

    calls = 0
    P_original = np.copy(P)

    if animate:
        plt.figure(figsize=(8, 6))

    def welzl_recursive(P_slice, R):
        nonlocal calls
        calls += 1

        # 1. Base case: 3 boundary points strictly define a circle
        if len(R) == 3:
            c = calc_circle(R)
            if animate: visualize(P_original, c, R)
            return c

        # 2. Start with the circle defined strictly by the current boundary points
        current_circle = calc_circle(R)

        # 3. Iterative Forward Sweep (Avoids deep initial recursion)
        for i, p in enumerate(P_slice):

            # If the point is outside the current circle...
            if current_circle is None or np.linalg.norm(current_circle[0] - p) > current_circle[1] + 1e-9:

                # Recurse ONLY on the points seen so far, adding 'p' to the boundary
                current_circle = welzl_recursive(P_slice[:i], R + [p])

                if animate: visualize(P_original, current_circle, R + [p])

        return current_circle

    # Run algorithm
    final_circle = welzl_recursive(P_copy, [])

    print(f"Total recursive calls: {calls}")

    if animate:
        visualize(P_original, final_circle, [])
        plt.title("Final Minimum Enclosing Circle")
        plt.show()

    return final_circle


def calc_circle(R):
    """Calculates the exact circumcircle for 0, 1, 2, or 3 points."""
    if len(R) == 0: return None
    if len(R) == 1: return (R[0], 0.0)
    if len(R) == 2:
        return ((R[0] + R[1]) / 2.0, np.linalg.norm(R[0] - R[1]) / 2.0)

    # 3 points: solve linear system
    A = 2 * (np.array(R[1:]) - R[0])
    B = np.sum(np.array(R[1:]) ** 2 - R[0] ** 2, axis=1)
    center = np.linalg.solve(A, B)
    return (center, np.linalg.norm(center - R[0]))


def visualize(all_points, current_circle, boundary):
    plt.clf()
    plt.scatter(all_points[:, 0], all_points[:, 1], c='black', s=20)

    if boundary:
        b_pts = np.array(boundary)
        plt.scatter(b_pts[:, 0], b_pts[:, 1], c='red', s=80)

    if current_circle is not None:
        center, radius = current_circle
        circle = plt.Circle(center, radius, color='blue', fill=True, alpha=0.2)
        plt.gca().add_patch(circle)
        plt.gca().add_patch(plt.Circle(center, radius, color='blue', fill=False, lw=2))

    plt.xlim(0, 800)
    plt.ylim(0, 600)
    plt.gca().set_aspect('equal')
    plt.pause(0.1)


# Example Usage:
if __name__ == "__main__":
    # You can safely test this with 50,000+ points now without RecursionError
    P_test = np.random.rand(500, 2) * [600, 400] + 100

    print("Running smart calculation...")
    result = run_welzl(P_test, animate=False)
    print(f"Center: {result[0]}, Radius: {result[1]:.2f}")